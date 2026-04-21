from __future__ import annotations

import argparse
import json

from repo_candidate_review_lib import format_candidate_summary, update_repo_candidate_status
from runtime_memory_lib import resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the review status of one runtime repo candidate.")
    parser.add_argument("--slug", required=True, help="Repo candidate slug / promoted note stem.")
    parser.add_argument(
        "--status",
        required=True,
        choices=["pending", "accepted", "rejected"],
        help="Review decision for the repo candidate.",
    )
    parser.add_argument(
        "--reason",
        default="",
        help="Optional review reason recorded in the promotion ledger.",
    )
    parser.add_argument(
        "--reviewer",
        default="manual-review",
        help="Reviewer label recorded in the review history.",
    )
    parser.add_argument(
        "--target-kind",
        default=None,
        choices=["pattern", "failure-mode", "benchmark", "release-note", "none"],
        help="Optional repo-layer target kind. This remains gated and does not publish assets.",
    )
    parser.add_argument(
        "--summary",
        default="",
        help="Optional short review summary written to the candidate and ledger.",
    )
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument("--root", default=None, help="Runtime root directory.")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    runtime_root = resolution.runtime_root.expanduser()
    snapshot = update_repo_candidate_status(
        runtime_root,
        slug=args.slug,
        status=args.status,
        reason=args.reason,
        reviewer=args.reviewer,
        target_kind=None if args.target_kind == "none" else args.target_kind,
        summary=args.summary or None,
    )
    print(
        json.dumps(
            format_candidate_summary(snapshot)
            | {
                "applied_status": args.status,
                "reason": args.reason or None,
                "reviewed_at": snapshot["reviewed_at"],
                "reviewer": args.reviewer,
                "summary": args.summary or None,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
