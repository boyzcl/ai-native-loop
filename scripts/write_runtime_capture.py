from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from promotion_trigger_lib import run_script, should_attempt_invocation_promotion
from runtime_memory_lib import append_capture, enrich_capture_record, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one ai-native-loop runtime capture record.")
    parser.add_argument(
        "--record-file",
        required=True,
        help="Path to a JSON file containing one capture record.",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host id used to resolve the runtime root. Examples: codex, claude-code, openclaw.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    parser.add_argument(
        "--skip-promotion-trigger",
        action="store_true",
        help="Write the capture only and skip the bounded invocation-time promotion cycle.",
    )
    parser.add_argument(
        "--promotion-limit",
        type=int,
        default=2,
        help="Hard cap for the bounded invocation-time promotion cycle. Default: 2.",
    )
    parser.add_argument(
        "--strict-promotion-trigger",
        action="store_true",
        help="Fail the command if the bounded invocation-time promotion cycle fails.",
    )
    args = parser.parse_args()

    record_path = Path(args.record_file).expanduser()
    record = json.loads(record_path.read_text(encoding="utf-8"))
    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    record = enrich_capture_record(record, resolution)
    capture_path = append_capture(resolution.runtime_root, record)

    if not args.skip_promotion_trigger and should_attempt_invocation_promotion(record):
        cycle_args = ["--trigger-source", "invocation", "--limit", str(args.promotion_limit)]
        if args.host:
            cycle_args.extend(["--host", args.host])
        if args.root:
            cycle_args.extend(["--root", args.root])
        try:
            summary, _ = run_script(
                Path(__file__).with_name("run_promotion_cycle.py"),
                cycle_args,
                cwd=Path(__file__).resolve().parents[1],
            )
            print(
                json.dumps(
                    {
                        "capture_path": str(capture_path),
                        "promotion_trigger_status": summary.get("status"),
                        "promotion_run_id": summary.get("worker_summary", {}).get("run_id"),
                        "pending_before": summary.get("before", {}).get("pending_backlog_size"),
                        "pending_after": summary.get("after", {}).get("pending_backlog_size"),
                    },
                    ensure_ascii=True,
                ),
                file=sys.stderr,
            )
        except Exception as exc:
            message = f"warning: invocation-time promotion trigger failed after capture write: {exc}"
            if args.strict_promotion_trigger:
                raise SystemExit(message)
            print(message, file=sys.stderr)

    print(capture_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
