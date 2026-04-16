from __future__ import annotations

import argparse
from pathlib import Path

from runtime_memory_lib import ensure_runtime_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize ai-native-loop runtime memory directories.")
    parser.add_argument(
        "--root",
        default="~/.codex/skills/ai-native-loop/runtime",
        help="Runtime root directory. Default: ~/.codex/skills/ai-native-loop/runtime",
    )
    args = parser.parse_args()

    result = ensure_runtime_root(Path(args.root))
    print(f"initialized runtime root: {result['runtime_root']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
