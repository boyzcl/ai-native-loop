from __future__ import annotations

import argparse
import json

from runtime_memory_lib import read_recent_captures, resolve_runtime_resolution


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
        "--host",
        default=None,
        help="Host id used to resolve the runtime root. Examples: codex, claude-code, openclaw.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Runtime root directory. Overrides host defaults and environment-based resolution.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    records = read_recent_captures(resolution.runtime_root, scene=args.scene, limit=args.limit)
    print(json.dumps(records, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
