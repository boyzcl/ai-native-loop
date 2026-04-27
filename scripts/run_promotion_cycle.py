from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from time import perf_counter

from promotion_trigger_lib import (
    ActiveRunLockError,
    append_trigger_history,
    maybe_write_trigger_capture,
    promotion_run_lock,
    run_script,
    snapshot_runtime,
)
from runtime_memory_lib import ensure_runtime_root, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one bounded ai-native-loop promotion cycle.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional hard cap on how many pending items to process in this cycle.",
    )
    parser.add_argument(
        "--stale-lock-seconds",
        type=int,
        default=21600,
        help="Treat an existing trigger lock as stale after this many seconds.",
    )
    parser.add_argument(
        "--capture-mode",
        choices=("none", "raw_only"),
        default="none",
        help="Optionally append a raw-only runtime capture describing this trigger run.",
    )
    parser.add_argument(
        "--trigger-source",
        choices=("manual", "invocation", "automation"),
        default="manual",
        help="Label the source that initiated this cycle.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    ensure_runtime_root(resolution.runtime_root, resolution)
    runtime_root = resolution.runtime_root.expanduser()
    before = snapshot_runtime(runtime_root)
    started_at = datetime.now().astimezone().isoformat()
    started = perf_counter()

    worker_args: list[str] = []
    if args.host:
        worker_args.extend(["--host", args.host])
    if args.root:
        worker_args.extend(["--root", args.root])
    worker_args.extend(["--trigger-source", args.trigger_source])
    if args.limit is not None:
        worker_args.extend(["--limit", str(args.limit)])

    try:
        with promotion_run_lock(
            runtime_root,
            "promotion-cycle",
            stale_seconds=args.stale_lock_seconds,
        ) as lock_path:
            worker_summary, worker_stderr = run_script(
                Path(__file__).with_name("promotion_worker.py"),
                worker_args,
                cwd=Path(__file__).resolve().parents[1],
            )
            after = snapshot_runtime(runtime_root)
            capture_path = maybe_write_trigger_capture(
                runtime_root,
                resolution,
                capture_mode=args.capture_mode,
                run_kind="cycle",
                run_id=f"{worker_summary['run_id']}-cycle-capture",
                objective="consume pending runtime promotion backlog on a bounded local cadence",
                what_worked=(
                    f"promotion cycle processed {worker_summary['processed_count']} items and "
                    f"moved pending backlog from {before.pending_backlog_size} to {after.pending_backlog_size}"
                ),
                remaining_risk=(
                    "trigger automation is now connected locally, but long-horizon cadence stability "
                    "still needs continued observation"
                ),
                next_input=(
                    "watch whether pending backlog stays near zero across repeated real runs and keep repo "
                    "candidate growth bounded to runtime-only candidates"
                ),
            )
            finished_at = datetime.now().astimezone().isoformat()
            summary = {
                "run_kind": "cycle",
                "status": "completed",
                "started_at": started_at,
                "finished_at": finished_at,
                "duration_ms": round((perf_counter() - started) * 1000, 2),
                "runtime_root": str(runtime_root),
                "host": resolution.host_id,
                "trigger_source": args.trigger_source,
                "requested_limit": args.limit,
                "lock_path": str(lock_path),
                "before": before.__dict__,
                "after": after.__dict__,
                "worker_summary": worker_summary,
                "worker_stderr": worker_stderr or None,
                "trigger_capture_path": capture_path,
            }
    except ActiveRunLockError as exc:
        finished_at = datetime.now().astimezone().isoformat()
        summary = {
            "run_kind": "cycle",
            "status": "skipped_locked",
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_ms": round((perf_counter() - started) * 1000, 2),
            "runtime_root": str(runtime_root),
            "host": resolution.host_id,
            "trigger_source": args.trigger_source,
            "requested_limit": args.limit,
            "before": before.__dict__,
            "after": before.__dict__,
            "reason": str(exc),
        }
    except Exception as exc:
        finished_at = datetime.now().astimezone().isoformat()
        summary = {
            "run_kind": "cycle",
            "status": "failed",
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_ms": round((perf_counter() - started) * 1000, 2),
            "runtime_root": str(runtime_root),
            "host": resolution.host_id,
            "trigger_source": args.trigger_source,
            "requested_limit": args.limit,
            "before": before.__dict__,
            "reason": str(exc),
        }
        append_trigger_history(runtime_root, summary)
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        return 1

    append_trigger_history(runtime_root, summary)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
