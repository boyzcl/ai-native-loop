from __future__ import annotations

import argparse
import json
import math
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from promotion_worker import load_json, process_pending, update_manifest, write_json
from runtime_memory_lib import append_capture, read_promoted_field_notes, record_promoted_note_reuse, resolve_runtime_resolution


def load_capture_records(runtime_root: Path) -> list[dict]:
    records = []
    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line in capture_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            records.append(json.loads(line))
    return records


def load_case_queries(default_cases_file: Path) -> list[str]:
    cases = json.loads(default_cases_file.read_text(encoding="utf-8"))
    return [case["query"] for case in cases]


def replay_backlog(temp_root: Path, seed_records: list[dict], replay_multiplier: int) -> dict[str, int]:
    base_time = datetime.now().astimezone() - timedelta(days=21)
    appended = 0
    for cycle in range(replay_multiplier):
        for index, record in enumerate(seed_records, start=1):
            replayed = dict(record)
            replayed["session_id"] = f"{record['session_id']}-stress-{cycle + 1:02d}-{index:03d}"
            replayed["timestamp"] = (base_time + timedelta(hours=(cycle * len(seed_records)) + index)).isoformat()
            append_capture(temp_root, replayed)
            appended += 1
    return {"replayed_capture_count": appended}


def drain_review_queue(temp_root: Path) -> list[dict]:
    queue_path = temp_root / "inbox" / "review-queue.json"
    ledger_path = temp_root / "state" / "promotion-ledger.json"
    policy_path = temp_root / "state" / "promotion-policy.json"
    queue = load_json(queue_path)
    ledger = load_json(ledger_path)
    policy = load_json(policy_path)
    runs = []

    while queue.get("pending"):
        summary = process_pending(temp_root, queue, ledger, policy)
        runs.append(summary)
        write_json(queue_path, queue)
        write_json(ledger_path, ledger)
        update_manifest(temp_root)

    summary = process_pending(temp_root, queue, ledger, policy, limit=0)
    runs.append(summary)
    write_json(queue_path, queue)
    write_json(ledger_path, ledger)
    update_manifest(temp_root)
    return runs


def replay_reuse(temp_root: Path, queries: list[str], reuse_passes: int) -> int:
    total = 0
    for pass_index in range(reuse_passes):
        for query in queries:
            promoted = read_promoted_field_notes(temp_root, scene=query, limit=3)
            result = record_promoted_note_reuse(
                temp_root,
                promoted,
                scene=query,
                source=f"stress_reuse_replay_pass_{pass_index + 1}",
            )
            total += int(result.get("recorded", 0))
    return total


def governance_report(runtime_root: Path) -> dict:
    queue = load_json(runtime_root / "inbox" / "review-queue.json")
    promotion_ledger = load_json(runtime_root / "state" / "promotion-ledger.json")
    reuse_ledger = load_json(runtime_root / "state" / "reuse-ledger.json")
    policy = load_json(runtime_root / "state" / "promotion-policy.json")
    field_note_files = sorted((runtime_root / "promoted" / "field-notes").glob("*.md"))
    archive_files = sorted((runtime_root / "promoted" / "archive").glob("*.md"))
    repo_candidate_files = sorted((runtime_root / "promoted" / "repo-candidates").glob("*.md"))
    reviewed = queue.get("reviewed", [])
    note_stats = promotion_ledger.get("note_stats", {})

    promoted = sum(1 for item in reviewed if item.get("action") == "promote_to_field_note")
    merged = sum(1 for item in reviewed if item.get("action") == "merge_into_existing_note")
    archived = sum(1 for item in reviewed if item.get("action") == "archive")
    active_candidates = [
        path
        for path in repo_candidate_files
        if not note_stats.get(path.stem, {}).get("archived")
        and note_stats.get(path.stem, {}).get("repo_candidate_status", "pending") != "rejected"
    ]
    reused_notes = [
        path
        for path in field_note_files
        if int(note_stats.get(path.stem, {}).get("reuse_count", 0)) > 0
    ]

    total_reviewed = max(1, len(reviewed))
    promoted_count = len(field_note_files)
    repo_candidate_count = len(active_candidates)
    archive_rate = archived / total_reviewed
    merge_rate = merged / total_reviewed
    promoted_reuse_rate = len(reused_notes) / max(1, promoted_count)
    return {
        "pending_backlog_size": len(queue.get("pending", [])),
        "reviewed_count": len(reviewed),
        "promoted_note_count": promoted_count,
        "archived_note_count": len(archive_files),
        "repo_candidate_count": repo_candidate_count,
        "reuse_event_count": len(reuse_ledger.get("events", [])),
        "archive_rate": round(archive_rate, 4),
        "merge_rate": round(merge_rate, 4),
        "promoted_note_reuse_rate": round(promoted_reuse_rate, 4),
        "working_set_ceiling": int(policy.get("promoted_working_set_ceiling", 20)),
    }


def evaluate_stability(report: dict) -> dict:
    ceiling = int(report["working_set_ceiling"])
    promoted_count = int(report["promoted_note_count"])
    repo_candidate_count = int(report["repo_candidate_count"])
    archive_rate = float(report["archive_rate"])
    merge_rate = float(report["merge_rate"])
    reuse_rate = float(report["promoted_note_reuse_rate"])
    return {
        "promoted_working_set_controlled": promoted_count <= ceiling,
        "archive_rate_reasonable": 0.05 <= archive_rate <= 0.55,
        "merge_rate_reasonable": 0.05 <= merge_rate <= 0.7,
        "repo_candidate_bounded": repo_candidate_count <= max(4, math.ceil(promoted_count * 0.6)),
        "reuse_evidence_trustworthy_enough": reuse_rate >= 0.3,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay a larger backlog against a temp runtime and judge governance stability.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument("--root", default=None, help="Runtime root directory.")
    parser.add_argument("--replay-multiplier", type=int, default=3, help="How many times to replay the current captures.")
    parser.add_argument("--reuse-passes", type=int, default=3, help="How many retrieval reuse passes to replay.")
    parser.add_argument(
        "--cases-file",
        default=str(
            Path(__file__).resolve().parents[1]
            / "docs"
            / "benchmarks"
            / "runtime-retrieval-forward-test-cases.json"
        ),
        help="Forward-test cases used as reuse replay queries.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    source_root = resolution.runtime_root.expanduser()
    seed_records = load_capture_records(source_root)
    queries = load_case_queries(Path(args.cases_file).expanduser())

    with tempfile.TemporaryDirectory(prefix="ai-native-loop-stress-") as temp_dir:
        temp_root = Path(temp_dir) / "runtime"
        shutil.copytree(source_root, temp_root)

        replay_stats = replay_backlog(temp_root, seed_records, args.replay_multiplier)
        promotion_runs = drain_review_queue(temp_root)
        reuse_event_count = replay_reuse(temp_root, queries, args.reuse_passes)
        promotion_runs.extend(drain_review_queue(temp_root))

        report = governance_report(temp_root)
        payload = {
            "source_runtime_root": str(source_root),
            "temp_runtime_root": str(temp_root),
            "seed_capture_count": len(seed_records),
            "replay_stats": replay_stats,
            "reuse_replay_events": reuse_event_count,
            "promotion_run_count": len(promotion_runs),
            "final_report": report,
            "stability_judgment": evaluate_stability(report),
        }
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
