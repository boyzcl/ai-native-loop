from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


BENCHMARK_OR_RELEASE_RE = re.compile(r"\bbenchmark\b|release narrative|release note|go/no-go|go no go")
LOW_SIGNAL_CONTEXT_RE = re.compile(r"\bbatch\d+\b|photo|guide-api|gpt-pro")
REVIEW_STATUS_SECTION_RE = re.compile(
    r"\n## Review Status\n.*?(?=\n## |\Z)",
    re.DOTALL,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _bool_text(value: bool) -> str:
    return "yes" if value else "no"


def _target_kind_or_none(target_kind: str | None) -> str:
    return target_kind or "none"


def _review_status_block(
    *,
    status: str,
    reviewed_at: str,
    reviewer: str,
    target_kind: str | None,
    reason: str,
    summary: str | None,
) -> str:
    lines = [
        "## Review Status",
        "",
        f"- `status`: `{status}`",
        f"- `reviewed_at`: `{reviewed_at}`",
        f"- `reviewer`: `{reviewer}`",
        f"- `target_kind`: `{_target_kind_or_none(target_kind)}`",
        f"- `reason`: {reason or 'none'}",
        f"- `summary`: {summary or 'none'}",
        "",
    ]
    return "\n".join(lines)


def update_candidate_markdown(
    candidate_path: Path,
    *,
    status: str,
    reviewed_at: str,
    reviewer: str,
    target_kind: str | None,
    reason: str,
    summary: str | None,
) -> None:
    text = candidate_path.read_text(encoding="utf-8")
    block = _review_status_block(
        status=status,
        reviewed_at=reviewed_at,
        reviewer=reviewer,
        target_kind=target_kind,
        reason=reason,
        summary=summary,
    )
    if REVIEW_STATUS_SECTION_RE.search(text):
        updated = REVIEW_STATUS_SECTION_RE.sub("\n" + block.rstrip() + "\n", text, count=1)
    else:
        updated = text.rstrip() + "\n\n" + block
    candidate_path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def _pattern_intake_ready(note_text: str) -> bool:
    return all(
        marker in note_text
        for marker in ["## What Worked", "## What Failed Or Remained Risky", "## Re-input"]
    )


def build_repo_candidate_snapshot(runtime_root: Path, slug: str, ledger: dict[str, Any]) -> dict[str, Any]:
    note_stats = ledger.get("note_stats", {}).get(slug, {})
    candidate_path = runtime_root / "promoted" / "repo-candidates" / f"{slug}.md"
    note_path = Path(note_stats.get("note_path", runtime_root / "promoted" / "field-notes" / f"{slug}.md"))
    note_text = note_path.read_text(encoding="utf-8") if note_path.exists() else ""
    candidate_text = candidate_path.read_text(encoding="utf-8") if candidate_path.exists() else ""
    source_session_ids = list(note_stats.get("source_session_ids", []))
    merge_count = int(note_stats.get("merge_count", 0))
    reuse_count = int(note_stats.get("reuse_count", 0))
    repeat_evidence_count = int(note_stats.get("repeat_evidence_count", 0) or 0)
    benchmark_or_release_ready = bool(BENCHMARK_OR_RELEASE_RE.search(note_text.lower()))
    local_only_risk = bool(LOW_SIGNAL_CONTEXT_RE.search(note_text.lower()))
    pattern_intake_ready = _pattern_intake_ready(note_text)
    evidence = {
        "source_session_count": len(source_session_ids),
        "source_session_ids": source_session_ids,
        "merge_count": merge_count,
        "reuse_count": reuse_count,
        "repeat_evidence_count": repeat_evidence_count,
        "benchmark_or_release_ready": benchmark_or_release_ready,
        "pattern_intake_ready": pattern_intake_ready,
        "local_only_risk": local_only_risk,
        "archived": bool(note_stats.get("archived")),
        "repo_candidate_status": note_stats.get("repo_candidate_status", "pending"),
        "repo_candidate_status_reason": note_stats.get("repo_candidate_status_reason"),
        "repo_candidate_reviewed_at": note_stats.get("repo_candidate_reviewed_at"),
        "repo_candidate_target_kind": note_stats.get("repo_candidate_target_kind"),
        "repo_candidate_review_summary": note_stats.get("repo_candidate_review_summary"),
        "last_reused_at": note_stats.get("last_reused_at"),
    }
    recommendation, recommendation_reason = recommend_repo_candidate_status(evidence)
    return {
        "slug": slug,
        "title": note_stats.get("title", slug.replace("-", " ")),
        "note_path": str(note_path),
        "candidate_path": str(candidate_path),
        "candidate_exists": candidate_path.exists(),
        "candidate_text": candidate_text,
        "note_text": note_text,
        "evidence": evidence,
        "recommendation": recommendation,
        "recommendation_reason": recommendation_reason,
    }


def recommend_repo_candidate_status(evidence: dict[str, Any]) -> tuple[str, str]:
    if evidence["archived"]:
        return "rejected", "note already archived or superseded in runtime"
    if not evidence["pattern_intake_ready"]:
        return "rejected", "field note lacks pattern-intake sections required for repo drafting"
    if evidence["local_only_risk"] and evidence["reuse_count"] == 0 and evidence["source_session_count"] <= 1:
        return "rejected", "candidate still looks project-specific and has no reuse evidence"
    if evidence["reuse_count"] >= 2 and (
        evidence["source_session_count"] >= 2
        or evidence["merge_count"] >= 1
        or evidence["benchmark_or_release_ready"]
    ):
        return "accepted", "reuse evidence is strong enough to justify repo-layer drafting review"
    if evidence["source_session_count"] >= 3 and evidence["benchmark_or_release_ready"]:
        return "accepted", "multi-session consolidation plus benchmark/release relevance clears manual review gate"
    return "pending", "keep gated until reuse, merge, or clearer repo target evidence accumulates"


def list_repo_candidates(runtime_root: Path) -> list[dict[str, Any]]:
    ledger = load_json(runtime_root / "state" / "promotion-ledger.json")
    snapshots = []
    for candidate_path in sorted((runtime_root / "promoted" / "repo-candidates").glob("*.md")):
        snapshots.append(build_repo_candidate_snapshot(runtime_root, candidate_path.stem, ledger))
    return snapshots


def update_repo_candidate_status(
    runtime_root: Path,
    *,
    slug: str,
    status: str,
    reason: str,
    reviewer: str,
    target_kind: str | None,
    summary: str | None,
) -> dict[str, Any]:
    ledger_path = runtime_root / "state" / "promotion-ledger.json"
    candidate_path = runtime_root / "promoted" / "repo-candidates" / f"{slug}.md"

    ledger = load_json(ledger_path)
    note_stats = ledger.setdefault("note_stats", {})
    entry = note_stats.get(slug)
    if entry is None:
        raise SystemExit(f"unknown repo candidate slug: {slug}")
    if not candidate_path.exists():
        raise SystemExit(f"repo candidate file does not exist: {candidate_path}")

    reviewed_at = datetime.now().astimezone().isoformat()
    entry["repo_candidate_status"] = status
    entry["repo_candidate_status_reason"] = reason or None
    entry["repo_candidate_reviewed_at"] = reviewed_at
    entry["repo_candidate_target_kind"] = target_kind or None
    entry["repo_candidate_review_summary"] = summary or None
    entry["last_updated_at"] = reviewed_at
    entry.setdefault("repo_candidate_reviews", []).append(
        {
            "reviewed_at": reviewed_at,
            "status": status,
            "reason": reason or None,
            "reviewer": reviewer,
            "target_kind": target_kind or None,
            "summary": summary or None,
        }
    )
    ledger["updated_at"] = reviewed_at
    write_json(ledger_path, ledger)

    update_candidate_markdown(
        candidate_path,
        status=status,
        reviewed_at=reviewed_at,
        reviewer=reviewer,
        target_kind=target_kind,
        reason=reason,
        summary=summary,
    )

    snapshot = build_repo_candidate_snapshot(runtime_root, slug, ledger)
    snapshot["reviewed_at"] = reviewed_at
    snapshot["reviewer"] = reviewer
    snapshot["applied_status"] = status
    return snapshot


def format_candidate_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    evidence = snapshot["evidence"]
    return {
        "slug": snapshot["slug"],
        "title": snapshot["title"],
        "current_status": evidence["repo_candidate_status"],
        "recommendation": snapshot["recommendation"],
        "recommendation_reason": snapshot["recommendation_reason"],
        "target_kind": evidence.get("repo_candidate_target_kind"),
        "evidence": {
            "source_session_count": evidence["source_session_count"],
            "merge_count": evidence["merge_count"],
            "reuse_count": evidence["reuse_count"],
            "repeat_evidence_count": evidence["repeat_evidence_count"],
            "pattern_intake_ready": _bool_text(evidence["pattern_intake_ready"]),
            "benchmark_or_release_ready": _bool_text(evidence["benchmark_or_release_ready"]),
            "local_only_risk": _bool_text(evidence["local_only_risk"]),
            "archived": _bool_text(evidence["archived"]),
        },
        "candidate_path": snapshot["candidate_path"],
        "note_path": snapshot["note_path"],
    }
