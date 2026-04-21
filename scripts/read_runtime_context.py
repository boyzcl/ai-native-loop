from __future__ import annotations

import argparse
import json

from runtime_memory_lib import (
    read_promoted_field_notes,
    read_recent_captures,
    record_promoted_note_reuse,
    resolve_runtime_resolution,
)


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
    parser.add_argument(
        "--include-promoted",
        action="store_true",
        help="Return up to 3 relevant promoted field notes together with recent captures.",
    )
    parser.add_argument(
        "--record-reuse",
        action="store_true",
        help="When promoted notes are returned, write reuse-hit events into runtime state.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    records = read_recent_captures(resolution.runtime_root, scene=args.scene, limit=args.limit)
    if args.include_promoted:
        promoted = read_promoted_field_notes(resolution.runtime_root, scene=args.scene, limit=3)
        reuse = None
        if args.record_reuse:
            reuse = record_promoted_note_reuse(
                resolution.runtime_root,
                promoted,
                scene=args.scene,
            )
        print(
            json.dumps(
                {
                    "captures": records,
                    "promoted_field_notes": promoted,
                    "reuse_recorded": reuse,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    else:
        print(json.dumps(records, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
