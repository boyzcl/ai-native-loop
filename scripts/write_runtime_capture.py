from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_memory_lib import append_capture


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one ai-native-loop runtime capture record.")
    parser.add_argument(
        "--record-file",
        required=True,
        help="Path to a JSON file containing one capture record.",
    )
    parser.add_argument(
        "--root",
        default="~/.codex/skills/ai-native-loop/runtime",
        help="Runtime root directory. Default: ~/.codex/skills/ai-native-loop/runtime",
    )
    args = parser.parse_args()

    record_path = Path(args.record_file).expanduser()
    record = json.loads(record_path.read_text(encoding="utf-8"))
    capture_path = append_capture(Path(args.root), record)
    print(capture_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
