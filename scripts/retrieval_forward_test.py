from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_memory_lib import rank_promoted_field_notes, resolve_runtime_resolution


def load_cases(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def legacy_rank_promoted_field_notes(runtime_root: Path, scene: str | None = None, limit: int = 5) -> list[dict]:
    runtime_root = runtime_root.expanduser()
    note_files = sorted((runtime_root / "promoted" / "field-notes").glob("*.md"), reverse=True)
    promotion_ledger = json.loads((runtime_root / "state" / "promotion-ledger.json").read_text(encoding="utf-8"))
    note_stats = promotion_ledger.get("note_stats", {})
    query_tokens = _tokenize(scene or "")
    ranked = []
    for note_file in note_files:
        text = note_file.read_text(encoding="utf-8")
        note_tokens = _tokenize(f"{note_file.stem} {text}")
        overlap = legacy_token_overlap(query_tokens, note_tokens) if query_tokens else 0.0
        ranked.append(
            {
                "path": str(note_file),
                "slug": note_file.stem,
                "title": note_file.stem.replace("-", " "),
                "matched_tokens": sorted(query_tokens & note_tokens),
                "weighted_overlap": round(overlap, 4),
                "reuse_count": int(note_stats.get(note_file.stem, {}).get("reuse_count", 0)),
                "recency": note_file.stat().st_mtime,
                "has_overlap": overlap > 0,
            }
        )
    ranked.sort(
        key=lambda item: (
            item["has_overlap"],
            item["weighted_overlap"],
            item["reuse_count"],
            item["recency"],
        ),
        reverse=True,
    )
    if query_tokens and any(item["has_overlap"] for item in ranked):
        ranked = [item for item in ranked if item["has_overlap"]]
    return ranked[:limit]


def _tokenize(text: str) -> set[str]:
    tokens = set()
    for raw in text.lower().split():
        token = "".join(char for char in raw if char.isalnum() or char in {"-", "_"})
        if len(token) < 3:
            continue
        tokens.add(token)
        for subtoken in token.replace("_", "-").split("-"):
            if len(subtoken) >= 3:
                tokens.add(subtoken)
    return tokens


def legacy_token_overlap(query_tokens: set[str], note_tokens: set[str]) -> float:
    if not query_tokens or not note_tokens:
        return 0.0
    return len(query_tokens & note_tokens) / max(1, min(len(query_tokens), len(note_tokens)))


def evaluate_cases(cases: list[dict], results_by_case: dict[str, list[dict]]) -> dict:
    summaries = []
    top1_hits = 0
    top3_hits = 0
    false_positive_cases = 0
    false_negative_cases = 0

    for case in cases:
        results = results_by_case[case["id"]]
        top_slugs = [item["slug"] for item in results[:3]]
        expected_any = set(case.get("expected_any", []))
        must_not = set(case.get("must_not_contain", []))
        top1 = top_slugs[0] if top_slugs else None
        if case.get("expected_top"):
            top1_hit = top1 == case["expected_top"]
        else:
            top1_hit = bool(top1 and top1 in expected_any)
        top3_hit = bool(expected_any & set(top_slugs))
        false_positives = [slug for slug in top_slugs if slug in must_not]
        false_negative = not top3_hit

        top1_hits += int(top1_hit)
        top3_hits += int(top3_hit)
        false_positive_cases += int(bool(false_positives))
        false_negative_cases += int(false_negative)
        summaries.append(
            {
                "id": case["id"],
                "query": case["query"],
                "top_3": top_slugs,
                "expected_any": case.get("expected_any", []),
                "expected_top": case.get("expected_top"),
                "top1_hit": top1_hit,
                "top3_hit": top3_hit,
                "false_positive_slugs": false_positives,
                "false_negative": false_negative,
            }
        )

    total = max(1, len(cases))
    return {
        "summary": {
            "case_count": len(cases),
            "top1_hit_rate": round(top1_hits / total, 4),
            "top3_hit_rate": round(top3_hits / total, 4),
            "false_positive_case_rate": round(false_positive_cases / total, 4),
            "false_negative_case_rate": round(false_negative_cases / total, 4),
        },
        "cases": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run retrieval forward tests against promoted runtime notes.")
    parser.add_argument("--host", default=None, help="Host id used to resolve the runtime root.")
    parser.add_argument("--root", default=None, help="Runtime root directory.")
    parser.add_argument(
        "--cases-file",
        default=str(
            Path(__file__).resolve().parents[1]
            / "docs"
            / "benchmarks"
            / "runtime-retrieval-forward-test-cases.json"
        ),
        help="JSON file describing forward-test cases.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of ranked notes to inspect per case.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    runtime_root = resolution.runtime_root.expanduser()
    cases = load_cases(Path(args.cases_file).expanduser())

    legacy_results = {
        case["id"]: legacy_rank_promoted_field_notes(runtime_root, scene=case["query"], limit=args.limit)
        for case in cases
    }
    current_results = {
        case["id"]: rank_promoted_field_notes(runtime_root, scene=case["query"], limit=args.limit)
        for case in cases
    }

    payload = {
        "runtime_root": str(runtime_root),
        "cases_file": str(Path(args.cases_file).expanduser()),
        "legacy": evaluate_cases(cases, legacy_results),
        "current": evaluate_cases(cases, current_results),
        "case_details": {
            case["id"]: {
                "legacy_top_5": [
                    {
                        "slug": item["slug"],
                        "matched_tokens": item["matched_tokens"],
                        "weighted_overlap": item["weighted_overlap"],
                    }
                    for item in legacy_results[case["id"]][:5]
                ],
                "current_top_5": [
                    {
                        "slug": item["slug"],
                        "matched_tokens": item["matched_tokens"],
                        "weighted_overlap": item["weighted_overlap"],
                        "title_overlap": item.get("title_overlap"),
                    }
                    for item in current_results[case["id"]][:5]
                ],
            }
            for case in cases
        },
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
