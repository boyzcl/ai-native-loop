from __future__ import annotations

import argparse
import json

from repo_candidate_review_lib import (
    format_candidate_summary,
    list_repo_candidates,
    update_repo_candidate_status,
)
from runtime_memory_lib import resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List or review ai-native-loop runtime repo candidates without publishing repo assets."
    )
    parser.add_argument(
        "--only-status",
        default=None,
        choices=["pending", "accepted", "rejected"],
        help="Filter listed candidates by current review status.",
    )
    parser.add_argument("--slug", default=None, help="Candidate slug to update.")
    parser.add_argument(
        "--status",
        default=None,
        choices=["pending", "accepted", "rejected"],
        help="Apply one explicit review status to --slug.",
    )
    parser.add_argument("--reason", default="", help="Review reason for the applied status.")
    parser.add_argument("--summary", default="", help="Short review summary for the candidate.")
    parser.add_argument(
        "--reviewer",
        default="manual-review",
        help="Reviewer label written into the review history.",
    )
    parser.add_argument(
        "--target-kind",
        default=None,
        choices=["pattern", "failure-mode", "benchmark", "release-note", "none"],
        help="Optional gated repo target for accepted candidates.",
    )
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument("--root", default=None, help="Runtime root directory.")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    runtime_root = resolution.runtime_root.expanduser()

    if args.slug and args.status:
        snapshot = update_repo_candidate_status(
            runtime_root,
            slug=args.slug,
            status=args.status,
            reason=args.reason,
            reviewer=args.reviewer,
            target_kind=None if args.target_kind == "none" else args.target_kind,
            summary=args.summary or None,
        )
        payload = format_candidate_summary(snapshot) | {
            "applied_status": args.status,
            "reviewed_at": snapshot["reviewed_at"],
            "reviewer": args.reviewer,
            "summary": args.summary or None,
        }
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 0

    snapshots = list_repo_candidates(runtime_root)
    if args.only_status:
        snapshots = [
            snapshot
            for snapshot in snapshots
            if snapshot["evidence"]["repo_candidate_status"] == args.only_status
        ]
    print(
        json.dumps(
            [format_candidate_summary(snapshot) for snapshot in snapshots],
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
