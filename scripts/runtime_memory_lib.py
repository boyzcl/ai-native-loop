from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from typing import Iterable


SKILL_NAME = "ai-native-loop"
GLOBAL_RUNTIME_ROOT_ENV = "AI_NATIVE_LOOP_RUNTIME_ROOT"
GLOBAL_HOST_ENV = "AI_NATIVE_LOOP_HOST"

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


@dataclass(frozen=True)
class HostSpec:
    host_id: str
    display_name: str
    support_tier: str
    default_runtime_root: str
    home_env_var: str | None = None
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeResolution:
    host_id: str
    display_name: str
    support_tier: str
    runtime_root: Path
    source: str
    is_known_host: bool


HOST_SPECS = {
    "codex": HostSpec(
        host_id="codex",
        display_name="Codex",
        support_tier="officially_supported",
        default_runtime_root="~/.codex/skills/ai-native-loop/runtime",
        home_env_var="CODEX_HOME",
        aliases=("openai",),
    ),
    "claude-code": HostSpec(
        host_id="claude-code",
        display_name="Claude Code",
        support_tier="experimental",
        default_runtime_root="~/.claude/skills/ai-native-loop/runtime",
        home_env_var="CLAUDE_CODE_HOME",
        aliases=("claude", "claude_code"),
    ),
    "openclaw": HostSpec(
        host_id="openclaw",
        display_name="OpenClaw",
        support_tier="experimental",
        default_runtime_root="~/.openclaw/skills/ai-native-loop/runtime",
        home_env_var="OPENCLAW_HOME",
        aliases=("open-claw",),
    ),
}


def _host_env_key(host_id: str) -> str:
    return host_id.upper().replace("-", "_")


def known_host_ids() -> list[str]:
    return sorted(HOST_SPECS)


def normalize_host(host: str | None) -> str:
    if not host:
        return "codex"

    normalized = host.strip().lower().replace("_", "-")
    for spec in HOST_SPECS.values():
        if normalized == spec.host_id or normalized in spec.aliases:
            return spec.host_id
    return normalized


def resolve_runtime_resolution(
    host: str | None = None,
    root: str | Path | None = None,
    environ: dict[str, str] | None = None,
) -> RuntimeResolution:
    env = environ or os.environ
    normalized_host = normalize_host(host or env.get(GLOBAL_HOST_ENV))

    if root:
        runtime_root = Path(root).expanduser()
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=runtime_root,
            source="explicit_root",
            is_known_host=spec is not None,
        )

    explicit_root = env.get(GLOBAL_RUNTIME_ROOT_ENV)
    if explicit_root:
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=Path(explicit_root).expanduser(),
            source=f"env:{GLOBAL_RUNTIME_ROOT_ENV}",
            is_known_host=spec is not None,
        )

    spec = HOST_SPECS.get(normalized_host)
    if spec is None:
        raise ValueError(
            "unknown host requires --root or AI_NATIVE_LOOP_RUNTIME_ROOT: "
            f"{normalized_host}"
        )

    host_runtime_env = f"AI_NATIVE_LOOP_{_host_env_key(normalized_host)}_RUNTIME_ROOT"
    if env.get(host_runtime_env):
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=Path(env[host_runtime_env]).expanduser(),
            source=f"env:{host_runtime_env}",
            is_known_host=True,
        )

    if spec.home_env_var and env.get(spec.home_env_var):
        runtime_root = Path(env[spec.home_env_var]).expanduser() / "skills" / SKILL_NAME / "runtime"
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=runtime_root,
            source=f"env:{spec.home_env_var}",
            is_known_host=True,
        )

    return RuntimeResolution(
        host_id=spec.host_id,
        display_name=spec.display_name,
        support_tier=spec.support_tier,
        runtime_root=Path(spec.default_runtime_root).expanduser(),
        source=f"default:{spec.host_id}",
        is_known_host=True,
    )


def enrich_capture_record(record: dict, resolution: RuntimeResolution) -> dict:
    enriched = dict(record)
    enriched.setdefault("runtime_host", resolution.host_id)
    enriched.setdefault("runtime_root", str(resolution.runtime_root))
    enriched.setdefault("runtime_root_source", resolution.source)
    return enriched


def default_manifest(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict:
    manifest = {
        "version": 1,
        "runtime_root": str(runtime_root),
        "created_at": datetime.now().astimezone().isoformat(),
        "capture_policy": "medium_plus_write_local_capture",
        "last_review_at": None,
        "notes": "runtime layer stores local experience; repository remains the public validation layer",
    }
    if resolution is not None:
        manifest.update(
            {
                "runtime_host": resolution.host_id,
                "runtime_host_display_name": resolution.display_name,
                "runtime_host_support_tier": resolution.support_tier,
                "runtime_root_resolution_source": resolution.source,
            }
        )
    return manifest


def ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict:
    return {
        "runtime_root": str(runtime_root.expanduser()),
        "runtime_host": resolution.host_id if resolution else None,
        "runtime_root_source": resolution.source if resolution else None,
        "created": _ensure_runtime_root(runtime_root, resolution),
    }


def _ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution | None) -> list[str]:
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
        runtime_root / "state" / "runtime-memory-manifest.json": default_manifest(runtime_root, resolution),
    }

    for file_path, data in defaults.items():
        if not file_path.exists():
            file_path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    readme_path = runtime_root / "README.md"
    if not readme_path.exists():
        readme_text = (
            "# Runtime Memory\n\n"
            "This directory stores local ai-native-loop runtime captures, light indices, review queue, and promoted notes.\n"
        )
        if resolution is not None:
            readme_text += (
                f"\n- Host: `{resolution.display_name}`\n"
                f"- Support tier: `{resolution.support_tier}`\n"
                f"- Resolution source: `{resolution.source}`\n"
            )
        readme_path.write_text(readme_text, encoding="utf-8")

    return created


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
