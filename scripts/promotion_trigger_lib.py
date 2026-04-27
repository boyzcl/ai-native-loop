from __future__ import annotations

import json
import os
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from runtime_memory_lib import append_capture, enrich_capture_record


TRIGGER_HISTORY_PATH = Path("state/promotion-trigger-history.jsonl")
TRIGGER_LOCK_DIR = Path("state/locks")


class ActiveRunLockError(RuntimeError):
    """Raised when a promotion trigger run is already active."""


@dataclass(frozen=True)
class RuntimeSnapshot:
    pending_backlog_size: int
    reviewed_count: int
    promoted_note_count: int
    archived_note_count: int
    repo_candidate_count: int
    last_promotion_run_id: str | None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot_runtime(runtime_root: Path) -> RuntimeSnapshot:
    queue = load_json(runtime_root / "inbox" / "review-queue.json")
    ledger = load_json(runtime_root / "state" / "promotion-ledger.json")
    note_stats = ledger.get("note_stats", {})

    repo_candidate_files = sorted((runtime_root / "promoted" / "repo-candidates").glob("*.md"))
    active_candidate_count = sum(
        1
        for path in repo_candidate_files
        if note_stats.get(path.stem, {}).get("repo_candidate_status", "pending") != "rejected"
    )

    return RuntimeSnapshot(
        pending_backlog_size=len(queue.get("pending", [])),
        reviewed_count=len(queue.get("reviewed", [])),
        promoted_note_count=len(list((runtime_root / "promoted" / "field-notes").glob("*.md"))),
        archived_note_count=len(list((runtime_root / "promoted" / "archive").glob("*.md"))),
        repo_candidate_count=active_candidate_count,
        last_promotion_run_id=ledger.get("last_run_id"),
    )


def append_trigger_history(runtime_root: Path, event: dict[str, Any]) -> None:
    history_path = runtime_root / TRIGGER_HISTORY_PATH
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=True) + "\n")


@contextmanager
def promotion_run_lock(
    runtime_root: Path,
    lock_name: str,
    *,
    stale_seconds: int = 21600,
) -> Iterator[Path]:
    lock_dir = runtime_root / TRIGGER_LOCK_DIR
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{lock_name}.lock"
    now = datetime.now().astimezone()
    payload = {
        "lock_name": lock_name,
        "created_at": now.isoformat(),
        "pid": os.getpid(),
    }

    if lock_path.exists():
        try:
            existing = json.loads(lock_path.read_text(encoding="utf-8"))
            created_at = datetime.fromisoformat(existing["created_at"])
        except (json.JSONDecodeError, KeyError, ValueError):
            created_at = None
        if created_at is not None and (now - created_at).total_seconds() <= stale_seconds:
            raise ActiveRunLockError(
                f"promotion trigger lock is active for {lock_name}: {lock_path}"
            )
        lock_path.unlink(missing_ok=True)

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    fd = os.open(lock_path, flags, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
        yield lock_path
    finally:
        lock_path.unlink(missing_ok=True)


def run_script(script_path: Path, args: list[str], *, cwd: Path) -> tuple[dict[str, Any], str]:
    command = [sys.executable, str(script_path), *args]
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if completed.returncode != 0:
        error_message = stderr or stdout or f"{script_path.name} exited with {completed.returncode}"
        raise RuntimeError(error_message)
    if not stdout:
        raise RuntimeError(f"{script_path.name} produced empty stdout")
    try:
        return json.loads(stdout), stderr
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{script_path.name} did not emit JSON stdout") from exc


def should_attempt_invocation_promotion(record: dict[str, Any]) -> bool:
    return (
        record.get("intervention_level") in {"medium", "strong"}
        and record.get("promotion_hint") != "raw_only"
    )


def maybe_write_trigger_capture(
    runtime_root: Path,
    resolution: Any,
    *,
    capture_mode: str,
    run_kind: str,
    run_id: str,
    objective: str,
    what_worked: str,
    remaining_risk: str,
    next_input: str,
) -> str | None:
    if capture_mode == "none":
        return None

    record = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "session_id": run_id,
        "skill_name": "ai-native-loop",
        "scene": f"promotion-trigger-{run_kind}",
        "objective": objective,
        "initial_block": "runtime promotion depended on manual worker invocation before this trigger layer ran",
        "intervention_level": "medium",
        "artifacts_produced": [
            f"{run_kind}-summary-json",
        ],
        "what_worked": what_worked,
        "remaining_risk": remaining_risk,
        "next_input": next_input,
        "candidate_pattern_tags": [
            "promotion-trigger-mechanism",
            "runtime-governance",
        ],
        "candidate_failure_tags": [
            "manual-worker-gap",
            "pending-backlog-drift",
        ],
        "promotion_hint": "raw_only",
    }
    record = enrich_capture_record(record, resolution)
    capture_path = append_capture(runtime_root, record)
    return str(capture_path)
