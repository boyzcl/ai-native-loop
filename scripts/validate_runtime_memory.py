from __future__ import annotations

import argparse
from pathlib import Path

from runtime_memory_lib import validate_runtime_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ai-native-loop runtime memory structure.")
    parser.add_argument(
        "--root",
        default="~/.codex/skills/ai-native-loop/runtime",
        help="Runtime root directory. Default: ~/.codex/skills/ai-native-loop/runtime",
    )
    args = parser.parse_args()

    errors = validate_runtime_root(Path(args.root))
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"runtime memory is valid: {Path(args.root).expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
