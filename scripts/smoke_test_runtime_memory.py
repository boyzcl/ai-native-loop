from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path

from runtime_memory_lib import append_capture, ensure_runtime_root, read_recent_captures, validate_runtime_root


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ai-native-loop-runtime-") as temp_dir:
        runtime_root = Path(temp_dir)
        ensure_runtime_root(runtime_root)

        record = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "session_id": "smoke-test-session",
            "skill_name": "ai-native-loop",
            "scene": "research-to-report",
            "objective": "verify runtime capture and retrieval",
            "initial_block": "materials are scattered",
            "intervention_level": "medium",
            "artifacts_produced": [
                "Diagnosis Card",
                "Task Packet",
                "Re-input Packet",
                "Loop Recovery Block",
            ],
            "what_worked": "task packet stabilized the next step",
            "remaining_risk": "sources still need verification",
            "next_input": "re-run with explicit source-check step",
            "candidate_pattern_tags": ["research-to-report"],
            "candidate_failure_tags": ["answer-before-structure"],
            "promotion_hint": "review_for_field_note",
        }

        append_capture(runtime_root, record)
        errors = validate_runtime_root(runtime_root)
        if errors:
            for error in errors:
                print(error)
            return 1

        related = read_recent_captures(runtime_root, scene="research-to-report", limit=1)
        if not related or related[0]["session_id"] != "smoke-test-session":
            print("failed to retrieve smoke test capture by scene")
            return 1

        print(f"smoke test passed: {runtime_root}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
