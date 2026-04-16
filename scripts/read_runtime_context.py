from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_memory_lib import read_recent_captures


def main() -> int:
    parser = argparse.ArgumentParser(description="Read recent ai-native-loop runtime captures by scene.")
    parser.add_argument(
        "--scene",
        default=None,
        help="Scene tag to filter by. If omitted, returns most recent captures across scenes.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of captures to return. Default: 5",
    )
    parser.add_argument(
        "--root",
        default="~/.codex/skills/ai-native-loop/runtime",
        help="Runtime root directory. Default: ~/.codex/skills/ai-native-loop/runtime",
    )
    args = parser.parse_args()

    records = read_recent_captures(Path(args.root), scene=args.scene, limit=args.limit)
    print(json.dumps(records, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
