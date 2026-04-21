from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from runtime_memory_lib import resolve_runtime_resolution


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report ai-native-loop runtime governance metrics.")
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
    runtime_root = resolution.runtime_root.expanduser()
    queue = load_json(runtime_root / "inbox" / "review-queue.json")
    promotion_ledger = load_json(runtime_root / "state" / "promotion-ledger.json")
    reuse_ledger = load_json(runtime_root / "state" / "reuse-ledger.json")
    field_note_files = sorted((runtime_root / "promoted" / "field-notes").glob("*.md"))
    archive_files = sorted((runtime_root / "promoted" / "archive").glob("*.md"))
    repo_candidate_files = sorted((runtime_root / "promoted" / "repo-candidates").glob("*.md"))

    reviewed = queue.get("reviewed", [])
    promoted = sum(1 for item in reviewed if item.get("action") == "promote_to_field_note")
    merged = sum(1 for item in reviewed if item.get("action") == "merge_into_existing_note")
    archived = sum(1 for item in reviewed if item.get("action") == "archive")
    kept_raw = sum(1 for item in reviewed if item.get("action") == "keep_raw")

    note_stats = promotion_ledger.get("note_stats", {})
    reused_notes = [
        path
        for path in field_note_files
        if int(note_stats.get(path.stem, {}).get("reuse_count", 0)) > 0
    ]
    candidate_notes = [path for path in repo_candidate_files if not note_stats.get(path.stem, {}).get("archived")]
    candidate_statuses = Counter(
        note_stats.get(path.stem, {}).get("repo_candidate_status", "pending")
        for path in candidate_notes
    )
    active_candidates = [
        path
        for path in candidate_notes
        if note_stats.get(path.stem, {}).get("repo_candidate_status", "pending") != "rejected"
    ]
    accepted_candidates = [
        path
        for path in active_candidates
        if note_stats.get(path.stem, {}).get("repo_candidate_status") == "accepted"
    ]

    report = {
        "runtime_root": str(runtime_root),
        "pending_backlog_size": len(queue.get("pending", [])),
        "reviewed_count": len(reviewed),
        "promoted_note_count": len(field_note_files),
        "archived_note_count": len(archive_files),
        "repo_candidate_count": len(active_candidates),
        "repo_candidate_pending_count": candidate_statuses.get("pending", 0),
        "repo_candidate_accepted_count": candidate_statuses.get("accepted", 0),
        "repo_candidate_rejected_count": candidate_statuses.get("rejected", 0),
        "repo_candidate_total_count": len(candidate_notes),
        "reuse_event_count": len(reuse_ledger.get("events", [])),
        "capture_to_reviewed_count": len(reviewed),
        "review_to_promote_rate": safe_rate(promoted, len(reviewed)),
        "dedup_merge_rate": safe_rate(merged, len(reviewed)),
        "archive_rate": safe_rate(archived, len(reviewed)),
        "keep_raw_rate": safe_rate(kept_raw, len(reviewed)),
        "promoted_note_reuse_rate": safe_rate(len(reused_notes), len(field_note_files)),
        "repo_candidate_accept_rate": safe_rate(len(accepted_candidates), len(candidate_notes)),
        "last_promotion_run_id": promotion_ledger.get("last_run_id"),
        "last_reuse_at": reuse_ledger.get("updated_at"),
    }
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
