from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


RUNTIME_SUBDIRS = [
    "captures",
    "index",
    "inbox",
    "promoted/field-notes",
    "promoted/archive",
    "state",
]

REQUIRED_CAPTURE_FIELDS = [
    "timestamp",
    "session_id",
    "skill_name",
    "scene",
    "objective",
    "initial_block",
    "intervention_level",
    "artifacts_produced",
    "what_worked",
    "remaining_risk",
    "next_input",
    "candidate_pattern_tags",
    "candidate_failure_tags",
    "promotion_hint",
]


def default_manifest(runtime_root: Path) -> dict:
    return {
        "version": 1,
        "runtime_root": str(runtime_root),
        "created_at": datetime.now().astimezone().isoformat(),
        "capture_policy": "medium_plus_write_local_capture",
        "last_review_at": None,
        "notes": "runtime layer stores local experience; repository remains the public validation layer",
    }


def ensure_runtime_root(runtime_root: Path) -> dict:
    runtime_root = runtime_root.expanduser()
    created = []
    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    defaults = {
        runtime_root / "index" / "by-scene.json": {},
        runtime_root / "index" / "by-pattern.json": {},
        runtime_root / "index" / "by-failure-mode.json": {},
        runtime_root / "inbox" / "review-queue.json": {"pending": []},
        runtime_root / "state" / "runtime-memory-manifest.json": default_manifest(runtime_root),
    }

    for file_path, data in defaults.items():
        if not file_path.exists():
            file_path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    readme_path = runtime_root / "README.md"
    if not readme_path.exists():
        readme_path.write_text(
            "# Runtime Memory\n\n"
            "This directory stores local ai-native-loop runtime captures, light indices, review queue, and promoted notes.\n",
            encoding="utf-8",
        )

    return {"runtime_root": str(runtime_root), "created": created}


def validate_capture(record: dict) -> None:
    missing = [field for field in REQUIRED_CAPTURE_FIELDS if field not in record]
    if missing:
        raise ValueError(f"capture record missing required fields: {', '.join(missing)}")

    if record["intervention_level"] not in {"light", "medium", "strong"}:
        raise ValueError("intervention_level must be one of: light, medium, strong")

    if not isinstance(record["artifacts_produced"], list):
        raise ValueError("artifacts_produced must be a list")

    if not isinstance(record["candidate_pattern_tags"], list):
        raise ValueError("candidate_pattern_tags must be a list")

    if not isinstance(record["candidate_failure_tags"], list):
        raise ValueError("candidate_failure_tags must be a list")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def append_capture(runtime_root: Path, record: dict) -> Path:
    runtime_root = runtime_root.expanduser()
    validate_capture(record)

    timestamp = datetime.fromisoformat(record["timestamp"])
    capture_file = runtime_root / "captures" / f"{timestamp.date().isoformat()}.jsonl"
    with capture_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")

    _update_index(runtime_root / "index" / "by-scene.json", [record["scene"]], record, "scene")
    _update_index(runtime_root / "index" / "by-pattern.json", record["candidate_pattern_tags"], record, "pattern")
    _update_index(runtime_root / "index" / "by-failure-mode.json", record["candidate_failure_tags"], record, "failure_mode")

    if record["promotion_hint"] != "raw_only":
        queue_path = runtime_root / "inbox" / "review-queue.json"
        queue = _load_json(queue_path)
        queue.setdefault("pending", []).append(
            {
                "capture_file": str(capture_file),
                "session_id": record["session_id"],
                "scene": record["scene"],
                "promotion_hint": record["promotion_hint"],
                "timestamp": record["timestamp"],
            }
        )
        _write_json(queue_path, queue)

    return capture_file


def _update_index(index_path: Path, keys: Iterable[str], record: dict, label: str) -> None:
    index = _load_json(index_path)
    for key in keys:
        if not key:
            continue
        entry = index.setdefault(
            key,
            {"count": 0, "latest_timestamp": None, "latest_session_id": None, "label": label},
        )
        entry["count"] += 1
        entry["latest_timestamp"] = record["timestamp"]
        entry["latest_session_id"] = record["session_id"]
    _write_json(index_path, index)


def read_recent_captures(runtime_root: Path, scene: str | None = None, limit: int = 5) -> list[dict]:
    runtime_root = runtime_root.expanduser()
    capture_files = sorted((runtime_root / "captures").glob("*.jsonl"), reverse=True)
    found: list[dict] = []
    for capture_file in capture_files:
        lines = capture_file.read_text(encoding="utf-8").splitlines()
        for line in reversed(lines):
            if not line.strip():
                continue
            record = json.loads(line)
            if scene and record.get("scene") != scene:
                continue
            found.append(record)
            if len(found) >= limit:
                return found
    return found


def validate_runtime_root(runtime_root: Path) -> list[str]:
    runtime_root = runtime_root.expanduser()
    errors = []
    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        if not path.exists() or not path.is_dir():
            errors.append(f"missing directory: {path}")

    json_files = [
        runtime_root / "index" / "by-scene.json",
        runtime_root / "index" / "by-pattern.json",
        runtime_root / "index" / "by-failure-mode.json",
        runtime_root / "inbox" / "review-queue.json",
        runtime_root / "state" / "runtime-memory-manifest.json",
    ]

    for json_file in json_files:
        if not json_file.exists():
            errors.append(f"missing file: {json_file}")
            continue
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json in {json_file}: {exc}")

    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line_no, line in enumerate(capture_file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                validate_capture(record)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid capture in {capture_file}:{line_no}: {exc}")

    return errors
