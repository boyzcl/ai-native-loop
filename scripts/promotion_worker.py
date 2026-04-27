from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from runtime_memory_lib import ensure_runtime_root, parse_runtime_timestamp, resolve_runtime_resolution


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]+")
SECTION_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
BENCHMARK_WORD_RE = re.compile(r"\bbenchmark\b")
STOP_TOKENS = {
    "a",
    "after",
    "ai",
    "all",
    "and",
    "before",
    "bounded",
    "card",
    "checkpoint",
    "current",
    "decision",
    "for",
    "from",
    "guide",
    "input",
    "into",
    "loop",
    "next",
    "note",
    "packet",
    "phase",
    "photo",
    "project",
    "runtime",
    "skill",
    "stage",
    "system",
    "task",
    "that",
    "the",
    "this",
    "with",
}


@dataclass
class PendingItem:
    capture_file: Path
    session_id: str
    scene: str
    promotion_hint: str
    timestamp: str


@dataclass
class PromotedNote:
    path: Path
    slug: str
    title: str
    text: str
    tokens: set[str]
    source_session_ids: list[str]
    repo_candidate_paths: list[str]
    archived: bool = False


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def slugify(text: str, limit: int = 72) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return (slug or "note")[:limit].strip("-") or "note"


def titleize(text: str) -> str:
    parts = [part for part in re.split(r"[\s_-]+", text.strip()) if part]
    return " ".join(word.capitalize() for word in parts) or "Untitled"


def normalize_tokens(*parts: str) -> set[str]:
    tokens: set[str] = set()
    for part in parts:
        for token in TOKEN_RE.findall(part.lower()):
            if token in STOP_TOKENS or len(token) < 3:
                continue
            tokens.add(token)
            for subtoken in token.replace("_", "-").split("-"):
                if subtoken not in STOP_TOKENS and len(subtoken) >= 3:
                    tokens.add(subtoken)
    return tokens


def textify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(textify(item) for item in value if textify(item))
    return str(value)


def string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [textify(item) for item in value if textify(item)]
    rendered = textify(value)
    return [rendered] if rendered else []


def combined_record_text(record: dict[str, Any]) -> str:
    return "\n".join(
        [
            textify(record.get("scene", "")),
            textify(record.get("objective", "")),
            textify(record.get("initial_block", "")),
            textify(record.get("what_worked", "")),
            textify(record.get("remaining_risk", "")),
            textify(record.get("next_input", "")),
            " ".join(string_list(record.get("candidate_pattern_tags", []))),
            " ".join(string_list(record.get("candidate_failure_tags", []))),
        ]
    )


def read_capture_record(capture_file: Path, session_id: str) -> dict[str, Any]:
    for line in capture_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("session_id") == session_id:
            return record
    raise ValueError(f"capture {session_id} not found in {capture_file}")


def parse_pending(queue: dict[str, Any]) -> list[PendingItem]:
    items = []
    for raw in queue.get("pending", []):
        items.append(
            PendingItem(
                capture_file=Path(raw["capture_file"]).expanduser(),
                session_id=raw["session_id"],
                scene=raw["scene"],
                promotion_hint=raw["promotion_hint"],
                timestamp=raw["timestamp"],
            )
        )
    return items


def load_all_captures(runtime_root: Path) -> list[dict[str, Any]]:
    captures: list[dict[str, Any]] = []
    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line in capture_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            captures.append(json.loads(line))
    return captures


def load_promoted_notes(runtime_root: Path, ledger: dict[str, Any]) -> list[PromotedNote]:
    note_stats = ledger.get("note_stats", {})
    notes: list[PromotedNote] = []
    for path in sorted((runtime_root / "promoted" / "field-notes").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        stat = note_stats.get(path.stem, {})
        title = extract_heading(text) or titleize(path.stem)
        notes.append(
            PromotedNote(
                path=path,
                slug=path.stem,
                title=title,
                text=text,
                tokens=normalize_tokens(path.stem, text),
                source_session_ids=list(stat.get("source_session_ids", [])),
                repo_candidate_paths=list(stat.get("repo_candidate_paths", [])),
            )
        )
    return notes


def extract_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def token_overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    return intersection / max(1, min(len(left), len(right)))


def shared_tag_overlap(record: dict[str, Any], note: PromotedNote) -> float:
    tags = set(string_list(record.get("candidate_pattern_tags", [])) + string_list(record.get("candidate_failure_tags", [])))
    note_tags = set(TOKEN_RE.findall(note.text.lower()))
    if not tags:
        return 0.0
    shared = len({tag.lower() for tag in tags} & note_tags)
    return shared / max(1, len(tags))


def similarity(record_tokens: set[str], record: dict[str, Any], note: PromotedNote) -> float:
    return max(token_overlap(record_tokens, note.tokens), shared_tag_overlap(record, note))


def score_record(
    record: dict[str, Any],
    policy: dict[str, Any],
    scene_counts: Counter[str],
    tag_counts: Counter[str],
    recent_scene_counts: Counter[str],
    recent_tag_counts: Counter[str],
) -> tuple[int, dict[str, bool], int]:
    pattern_tags = string_list(record.get("candidate_pattern_tags", []))
    failure_tags = string_list(record.get("candidate_failure_tags", []))
    combined = combined_record_text(record).lower()
    repeat_signal = scene_counts[record.get("scene", "")] > 1 or any(
        tag_counts[tag] > 1 for tag in pattern_tags + failure_tags
    )
    transfer_signal = len(set(pattern_tags + failure_tags)) >= 2
    specificity_signal = min(
        len(textify(record.get("what_worked", ""))),
        len(textify(record.get("remaining_risk", ""))),
        len(textify(record.get("next_input", ""))),
    ) >= 80
    future_judgment_signal = len(textify(record.get("next_input", ""))) >= 100 and any(
        keyword in combined
        for keyword in ["freeze", "scope", "checkpoint", "gate", "threshold", "review", "archive", "merge", "promote", "evidence"]
    )
    benchmark_signal = any(
        keyword in combined
        for keyword in ["benchmark", "validation", "acceptance", "go/no-go", "go no go", "stage", "phase"]
    )
    signals = {
        "repeat_signal": repeat_signal,
        "transfer_signal": transfer_signal,
        "specificity_signal": specificity_signal,
        "future_judgment_signal": future_judgment_signal,
        "benchmark_signal": benchmark_signal,
    }
    score = 0
    for key, enabled in signals.items():
        if enabled:
            score += int(policy.get("scoring", {}).get(key, 0))
    recent_repeat_count = recent_scene_counts[record.get("scene", "")]
    recent_repeat_count += sum(recent_tag_counts[tag] for tag in pattern_tags + failure_tags)
    return score, signals, recent_repeat_count


def should_archive_low_value(record: dict[str, Any], policy: dict[str, Any]) -> tuple[bool, str | None]:
    combined = combined_record_text(record).lower()
    for keyword in policy.get("archive_keywords", []):
        if keyword in combined:
            return True, f"matched archive keyword: {keyword}"
    if record.get("promotion_hint") == "raw_only":
        return True, "promotion_hint requested raw_only"
    return False, None


def note_matches_low_value(text: str, policy: dict[str, Any]) -> tuple[bool, str | None]:
    lowered = text.lower()
    for keyword in policy.get("archive_keywords", []):
        if keyword in lowered:
            return True, keyword
    return False, None


def find_best_note_match(record: dict[str, Any], record_tokens: set[str], notes: list[PromotedNote]) -> tuple[PromotedNote | None, float]:
    best_note = None
    best_score = 0.0
    for note in notes:
        score = similarity(record_tokens, record, note)
        if score > best_score:
            best_score = score
            best_note = note
    return best_note, best_score


def render_field_note(record: dict[str, Any], score: int, signals: dict[str, bool], source_capture: Path) -> str:
    title = titleize(record.get("scene", "field note"))
    pattern_tags = string_list(record.get("candidate_pattern_tags", []))
    failure_tags = string_list(record.get("candidate_failure_tags", []))
    signal_lines = [f"- `{name}`: {'yes' if enabled else 'no'}" for name, enabled in signals.items()]
    pattern_lines = [f"- `{tag}`" for tag in pattern_tags] or ["- none"]
    failure_lines = [f"- `{tag}`" for tag in failure_tags] or ["- none"]
    return "\n".join(
        [
            f"# Field Note: {title}",
            "",
            "## Scene",
            "",
            f"- `{record.get('scene', '')}`",
            "",
            "## Objective",
            "",
            f"- {textify(record.get('objective', ''))}",
            "",
            "## Initial Block",
            "",
            f"- {textify(record.get('initial_block', ''))}",
            "",
            "## Intervention Level",
            "",
            f"- `{textify(record.get('intervention_level', ''))}`",
            "",
            "## Core Artifacts Produced",
            "",
            *[f"- `{artifact}`" for artifact in string_list(record.get("artifacts_produced", []))],
            "",
            "## What Worked",
            "",
            f"- {textify(record.get('what_worked', ''))}",
            "",
            "## What Failed Or Remained Risky",
            "",
            f"- {textify(record.get('remaining_risk', ''))}",
            "",
            "## Re-input",
            "",
            f"- {textify(record.get('next_input', ''))}",
            "",
            "## Candidate Pattern Tags",
            "",
            *pattern_lines,
            "",
            "## Candidate Failure Tags",
            "",
            *failure_lines,
            "",
            "## Promotion Signals",
            "",
            f"- `score`: {score}",
            *signal_lines,
            "",
            "## Source Runtime Captures",
            "",
            f"- `{source_capture}#{record.get('session_id', '')}`",
            "",
            "## Merge History",
            "",
            f"- `{record.get('timestamp', '')}` created from `{record.get('session_id', '')}`",
            "",
        ]
    ).rstrip() + "\n"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]
    return path.with_name(f"{path.stem}-{digest}{path.suffix}")


def create_field_note(
    runtime_root: Path,
    record: dict[str, Any],
    score: int,
    signals: dict[str, bool],
    ledger: dict[str, Any],
    touched_slugs: set[str],
) -> PromotedNote:
    note_dir = runtime_root / "promoted" / "field-notes"
    slug = slugify(record.get("scene", "field-note"))
    path = ensure_unique_path(note_dir / f"{slug}.md")
    slug = path.stem
    text = render_field_note(record, score, signals, Path(record["capture_file"]))
    path.write_text(text, encoding="utf-8")
    note = PromotedNote(
        path=path,
        slug=slug,
        title=extract_heading(text) or titleize(record.get("scene", "")),
        text=text,
        tokens=normalize_tokens(slug, text),
        source_session_ids=[record["session_id"]],
        repo_candidate_paths=[],
    )
    update_note_stats(
        ledger,
        note,
        record["session_id"],
        action="promote_to_field_note",
    )
    touched_slugs.add(slug)
    return note


def append_merge(note: PromotedNote, record: dict[str, Any], ledger: dict[str, Any], touched_slugs: set[str]) -> PromotedNote:
    addition = "\n".join(
        [
            "## Merge History",
            "",
            f"- `{record.get('timestamp', '')}` merged `{record.get('session_id', '')}`",
            f"  - scene: `{record.get('scene', '')}`",
            f"  - what_worked: {textify(record.get('what_worked', ''))}",
            f"  - next_input: {textify(record.get('next_input', ''))}",
            "",
            "## Source Runtime Captures",
            "",
            f"- `{record.get('capture_file', '')}#{record.get('session_id', '')}`",
            "",
        ]
    )
    note.path.write_text(note.text.rstrip() + "\n\n" + addition, encoding="utf-8")
    updated_text = note.path.read_text(encoding="utf-8")
    updated_note = PromotedNote(
        path=note.path,
        slug=note.slug,
        title=note.title,
        text=updated_text,
        tokens=normalize_tokens(note.slug, updated_text),
        source_session_ids=note.source_session_ids + [record["session_id"]],
        repo_candidate_paths=note.repo_candidate_paths,
    )
    update_note_stats(
        ledger,
        updated_note,
        record["session_id"],
        action="merge_into_existing_note",
    )
    touched_slugs.add(note.slug)
    return updated_note


def write_archive_record(runtime_root: Path, record: dict[str, Any], reason: str) -> Path:
    archive_dir = runtime_root / "promoted" / "archive"
    slug = slugify(record.get("scene", "archive"))
    path = ensure_unique_path(archive_dir / f"{slug}.md")
    body = "\n".join(
        [
            f"# Archived Runtime Note: {titleize(record.get('scene', 'archive'))}",
            "",
            "## Decision",
            "",
            "- `archive`",
            "",
            "## Reason",
            "",
            f"- {reason}",
            "",
            "## Source Runtime Capture",
            "",
            f"- `{record.get('capture_file', '')}#{record.get('session_id', '')}`",
            "",
            "## Next Input",
            "",
            f"- {textify(record.get('next_input', ''))}",
            "",
        ]
    )
    path.write_text(body + "\n", encoding="utf-8")
    return path


def update_note_stats(ledger: dict[str, Any], note: PromotedNote, session_id: str, action: str) -> None:
    note_stats = ledger.setdefault("note_stats", {})
    entry = note_stats.setdefault(
        note.slug,
        {
            "note_path": str(note.path),
            "title": note.title,
            "created_at": datetime.now().astimezone().isoformat(),
            "last_updated_at": None,
            "last_reused_at": None,
            "source_session_ids": [],
            "repeat_evidence_count": 0,
            "merge_count": 0,
            "repo_candidate_paths": [],
            "repo_candidate_status": "pending",
            "repo_candidate_status_reason": None,
            "archived": False,
            "archive_reason": None,
            "reuse_count": 0,
            "last_action": None,
        },
    )
    entry["note_path"] = str(note.path)
    entry["title"] = note.title
    entry["last_updated_at"] = datetime.now().astimezone().isoformat()
    entry["last_action"] = action
    if session_id not in entry["source_session_ids"]:
        entry["source_session_ids"].append(session_id)
    if action == "merge_into_existing_note":
        entry["merge_count"] += 1
    if action == "archive":
        entry["archived"] = True


def record_repeat_evidence(ledger: dict[str, Any], note_slug: str, repeat_evidence_count: int) -> None:
    note_stats = ledger.setdefault("note_stats", {})
    entry = note_stats.setdefault(note_slug, {})
    entry["repeat_evidence_count"] = max(int(entry.get("repeat_evidence_count", 0)), int(repeat_evidence_count))


def maybe_create_repo_candidate(
    runtime_root: Path,
    note: PromotedNote,
    record: dict[str, Any],
    score: int,
    signals: dict[str, bool],
    recent_repeat_count: int,
    ledger: dict[str, Any],
    policy: dict[str, Any],
) -> tuple[bool, Path | None, dict[str, bool]]:
    note_stats = ledger.get("note_stats", {}).get(note.slug, {})
    low_value, low_value_keyword = note_matches_low_value(note.text, policy)
    min_reuse_count = int(policy.get("repo_candidate_min_reuse_count", 2))
    min_source_sessions = int(policy.get("repo_candidate_min_source_sessions", 2))
    reuse_count = int(note_stats.get("reuse_count", 0))
    source_session_count = len(note_stats.get("source_session_ids", []))
    merge_count = int(note_stats.get("merge_count", 0))
    repeat_evidence_count = max(int(note_stats.get("repeat_evidence_count", 0)), int(recent_repeat_count))
    gate_checks = {
        "repeated_recently": repeat_evidence_count > 1,
        "source_session_ready": source_session_count >= min_source_sessions or merge_count >= 1,
        "reuse_recorded": reuse_count >= min_reuse_count,
        "pattern_intake_ready": signals["transfer_signal"] and signals["specificity_signal"] and signals["future_judgment_signal"],
        "benchmark_or_release_ready": bool(BENCHMARK_WORD_RE.search(note.text.lower())) or "release narrative" in note.text.lower(),
        "blocked_as_low_value": low_value,
    }
    gate_count = sum(
        1
        for key, enabled in gate_checks.items()
        if key != "blocked_as_low_value" and enabled
    )
    if gate_checks["blocked_as_low_value"]:
        return False, None, gate_checks
    if score < int(policy.get("repo_candidate_min_score", 4)):
        return False, None, gate_checks
    if not gate_checks["pattern_intake_ready"]:
        return False, None, gate_checks
    if policy.get("repo_candidate_require_repeat_or_reuse", True) and not (
        gate_checks["reuse_recorded"]
        or (gate_checks["source_session_ready"] and gate_checks["benchmark_or_release_ready"])
    ):
        return False, None, gate_checks
    if gate_count < int(policy.get("repo_candidate_gate_min", 2)):
        return False, None, gate_checks

    candidate_dir = runtime_root / "promoted" / "repo-candidates"
    path = candidate_dir / f"{note.slug}.md"
    checks = [f"- `{name}`: {'yes' if enabled else 'no'}" for name, enabled in gate_checks.items()]
    body = "\n".join(
        [
            f"# Repo Candidate: {note.title}",
            "",
            "## Why This Stayed Gated",
            "",
            "- This file is a repo candidate only.",
            "- It does not publish pattern, failure mode, benchmark, or release assets automatically.",
            "",
            "## Evidence",
            "",
            f"- `promotion_score`: {score}",
            f"- `note_path`: `{note.path}`",
            f"- `source_session`: `{record.get('session_id', '')}`",
            f"- `reuse_count`: {reuse_count}",
            f"- `last_reused_at`: `{note_stats.get('last_reused_at')}`",
            *checks,
            "",
            "## Candidate Tags",
            "",
            *[f"- `{tag}`" for tag in string_list(record.get("candidate_pattern_tags", [])) + string_list(record.get("candidate_failure_tags", []))],
            "",
            "## Next Review",
            "",
            "- Confirm repeated reuse or benchmark relevance before promoting anything into repo public assets.",
            "",
        ]
    )
    path.write_text(body + "\n", encoding="utf-8")
    note_stats = ledger.setdefault("note_stats", {}).setdefault(note.slug, {})
    repo_candidate_paths = note_stats.setdefault("repo_candidate_paths", [])
    if str(path) not in repo_candidate_paths:
        repo_candidate_paths.append(str(path))
    note_stats.setdefault("repo_candidate_status", "pending")
    return True, path, gate_checks


def reconcile_repo_candidates(
    runtime_root: Path,
    note_by_slug: dict[str, PromotedNote],
    ledger: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    created: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []
    min_score = int(policy.get("repo_candidate_min_score", 4))
    gate_min = int(policy.get("repo_candidate_gate_min", 2))
    min_reuse_count = int(policy.get("repo_candidate_min_reuse_count", 2))
    min_source_sessions = int(policy.get("repo_candidate_min_source_sessions", 2))
    note_stats = ledger.get("note_stats", {})

    for slug, note in note_by_slug.items():
        entry = note_stats.get(slug, {})
        if entry.get("archived"):
            continue
        expected_path = runtime_root / "promoted" / "repo-candidates" / f"{slug}.md"

        source_count = len(entry.get("source_session_ids", []))
        merge_count = int(entry.get("merge_count", 0))
        low_value, low_value_keyword = note_matches_low_value(note.text, policy)
        score = min_score
        reuse_count = int(entry.get("reuse_count", 0))
        repeat_evidence_count = int(entry.get("repeat_evidence_count", 0))
        if source_count > 1:
            score += 1
        if "## Candidate Pattern Tags" in note.text and "## Candidate Failure Tags" in note.text:
            score += 1

        gate_checks = {
            "repeated_recently": source_count > 1 or merge_count > 0 or repeat_evidence_count > 1,
            "source_session_ready": source_count >= min_source_sessions or merge_count > 0,
            "reuse_recorded": reuse_count >= min_reuse_count,
            "pattern_intake_ready": all(
                marker in note.text
                for marker in ["## What Worked", "## What Failed Or Remained Risky", "## Re-input"]
            ),
            "benchmark_or_release_ready": bool(BENCHMARK_WORD_RE.search(note.text.lower())) or "release narrative" in note.text.lower(),
            "blocked_as_low_value": low_value,
        }
        gate_count = sum(
            1
            for key, enabled in gate_checks.items()
            if key != "blocked_as_low_value" and enabled
        )
        qualifies = score >= min_score and gate_count >= gate_min and not gate_checks["blocked_as_low_value"]
        if policy.get("repo_candidate_require_repeat_or_reuse", True):
            qualifies = qualifies and (
                gate_checks["reuse_recorded"]
                or (gate_checks["source_session_ready"] and gate_checks["benchmark_or_release_ready"])
            )
        if not qualifies:
            if expected_path.exists():
                expected_path.unlink()
                entry["repo_candidate_paths"] = [
                    path for path in entry.get("repo_candidate_paths", []) if path != str(expected_path)
                ]
                entry["repo_candidate_status"] = "rejected"
                entry["repo_candidate_status_reason"] = "did not meet tightened gate"
                removed.append(
                    {
                        "repo_candidate_path": str(expected_path),
                        "reason": (
                            f"did not meet tightened gate"
                            + (f" (low value keyword: {low_value_keyword})" if low_value_keyword else "")
                        ),
                    }
                )
            continue

        existing_candidates = set(entry.get("repo_candidate_paths", []))
        if str(expected_path) in existing_candidates or expected_path.exists():
            entry.setdefault("repo_candidate_status", "pending")
            continue

        body = "\n".join(
            [
                f"# Repo Candidate: {note.title}",
                "",
                "## Why This Stayed Gated",
                "",
                "- This asset remains a repo candidate only.",
                "- It still needs an explicit repo-layer review before becoming any public pattern, failure mode, benchmark, or release narrative.",
                "",
                "## Evidence Snapshot",
                "",
                f"- `note_path`: `{note.path}`",
                f"- `source_session_count`: {source_count}",
                f"- `merge_count`: {merge_count}",
                f"- `reuse_count`: {reuse_count}",
                f"- `last_reused_at`: `{entry.get('last_reused_at')}`",
                f"- `promotion_score_floor`: {score}",
                *[f"- `{name}`: {'yes' if enabled else 'no'}" for name, enabled in gate_checks.items()],
                "",
                "## Review Prompt",
                "",
                "- Check whether this note has repeated real reuse or benchmark evidence strong enough for repo-level abstraction.",
                "",
            ]
        )
        expected_path.write_text(body + "\n", encoding="utf-8")
        entry.setdefault("repo_candidate_paths", []).append(str(expected_path))
        entry.setdefault("repo_candidate_status", "pending")
        created.append({"note_path": str(note.path), "repo_candidate_path": str(expected_path), "gate_checks": gate_checks})

    return {"created": created, "removed": removed}


def apply_working_set_ceiling(
    runtime_root: Path,
    ledger: dict[str, Any],
    touched_slugs: set[str],
    ceiling: int,
) -> list[dict[str, Any]]:
    note_dir = runtime_root / "promoted" / "field-notes"
    notes = sorted(note_dir.glob("*.md"))
    if len(notes) <= ceiling:
        return []

    stats = ledger.get("note_stats", {})
    candidates = []
    for path in notes:
        entry = stats.get(path.stem, {})
        rank = (
            int(entry.get("reuse_count", 0)),
            int(entry.get("merge_count", 0)),
            len(entry.get("source_session_ids", [])),
        )
        candidates.append((path, rank, path.stem in touched_slugs))

    # Keep the hottest notes; archive untouched, low-signal overflow first.
    candidates.sort(key=lambda item: (item[2], item[1][0], item[1][1], item[1][2], item[0].stat().st_mtime))
    overflow = len(notes) - ceiling
    archived: list[dict[str, Any]] = []
    for path, _, _ in candidates[:overflow]:
        target = runtime_root / "promoted" / "archive" / path.name
        target = ensure_unique_path(target)
        path.rename(target)
        entry = stats.setdefault(path.stem, {})
        entry["archived"] = True
        entry["archive_reason"] = "working_set_ceiling"
        entry["last_action"] = "archive"
        entry["last_updated_at"] = datetime.now().astimezone().isoformat()
        archived.append({"note": str(path), "archived_to": str(target), "reason": "working_set_ceiling"})
    return archived


def trim_reviewed_history(queue: dict[str, Any], max_items: int) -> None:
    reviewed = queue.setdefault("reviewed", [])
    if len(reviewed) > max_items:
        queue["reviewed"] = reviewed[-max_items:]


def process_pending(
    runtime_root: Path,
    queue: dict[str, Any],
    ledger: dict[str, Any],
    policy: dict[str, Any],
    limit: int | None = None,
    trigger_source: str | None = None,
) -> dict[str, Any]:
    pending_items = parse_pending(queue)
    pending_before = len(pending_items)
    backlog_threshold = int(policy.get("backlog_threshold", 10))
    default_batch_size = int(policy.get("default_batch_size", 5))
    backlog_triggered = pending_before >= backlog_threshold
    batch_size = pending_before if backlog_triggered else min(default_batch_size, pending_before)
    if limit is not None:
        batch_size = min(batch_size, limit)

    captures = load_all_captures(runtime_root)
    scene_counts = Counter(record.get("scene", "") for record in captures)
    tag_counts = Counter(
        tag
        for record in captures
        for tag in string_list(record.get("candidate_pattern_tags", [])) + string_list(record.get("candidate_failure_tags", []))
    )
    now = datetime.now().astimezone()
    recent_cutoff = now - timedelta(days=7)
    recent_records = [
        record
        for record in captures
        if parse_runtime_timestamp(record["timestamp"]) >= recent_cutoff
    ]
    recent_scene_counts = Counter(record.get("scene", "") for record in recent_records)
    recent_tag_counts = Counter(
        tag
        for record in recent_records
        for tag in string_list(record.get("candidate_pattern_tags", [])) + string_list(record.get("candidate_failure_tags", []))
    )

    notes = load_promoted_notes(runtime_root, ledger)
    note_by_slug = {note.slug: note for note in notes}
    touched_slugs: set[str] = set()
    run_actions = Counter()
    reviewed_items = []
    processed_items: list[PendingItem] = []

    for item in pending_items[:batch_size]:
        record = read_capture_record(item.capture_file, item.session_id)
        record["capture_file"] = str(item.capture_file)
        record_tokens = normalize_tokens(combined_record_text(record))
        score, signals, recent_repeat_count = score_record(
            record,
            policy,
            scene_counts,
            tag_counts,
            recent_scene_counts,
            recent_tag_counts,
        )
        low_value, archive_reason = should_archive_low_value(record, policy)
        best_note, best_similarity = find_best_note_match(record, record_tokens, list(note_by_slug.values()))

        action = "keep_raw"
        target_path: str | None = None
        repo_candidate_path: str | None = None
        gate_checks: dict[str, bool] | None = None
        reason = None

        if low_value:
            action = "archive"
            reason = archive_reason
            archive_path = write_archive_record(runtime_root, record, archive_reason or "policy archive")
            target_path = str(archive_path)
        elif best_note and best_similarity >= float(policy.get("dedup_similarity_threshold", 0.52)):
            action = "merge_into_existing_note"
            reason = f"matched existing note `{best_note.slug}` with similarity {best_similarity:.2f}"
            merged_note = append_merge(best_note, record, ledger, touched_slugs)
            note_by_slug[merged_note.slug] = merged_note
            record_repeat_evidence(ledger, merged_note.slug, recent_repeat_count)
            target_path = str(merged_note.path)
            created_candidate, candidate_path, gate_checks = maybe_create_repo_candidate(
                runtime_root,
                merged_note,
                record,
                score,
                signals,
                recent_repeat_count,
                ledger,
                policy,
            )
            if created_candidate and candidate_path is not None:
                repo_candidate_path = str(candidate_path)
        elif best_note and best_similarity >= float(policy.get("merge_similarity_threshold", 0.36)) and score < int(policy.get("repo_candidate_min_score", 4)):
            action = "merge_into_existing_note"
            reason = f"soft-matched existing note `{best_note.slug}` with similarity {best_similarity:.2f}"
            merged_note = append_merge(best_note, record, ledger, touched_slugs)
            note_by_slug[merged_note.slug] = merged_note
            record_repeat_evidence(ledger, merged_note.slug, recent_repeat_count)
            target_path = str(merged_note.path)
            created_candidate, candidate_path, gate_checks = maybe_create_repo_candidate(
                runtime_root,
                merged_note,
                record,
                score,
                signals,
                recent_repeat_count,
                ledger,
                policy,
            )
            if created_candidate and candidate_path is not None:
                repo_candidate_path = str(candidate_path)
        elif score < int(policy.get("promote_min_score", 3)):
            action = "keep_raw"
            reason = f"score {score} stayed below promote threshold"
        else:
            current_promoted_count = len(list((runtime_root / "promoted" / "field-notes").glob("*.md")))
            ceiling = int(policy.get("promoted_working_set_ceiling", 20))
            if current_promoted_count >= ceiling and score < int(policy.get("repo_candidate_min_score", 4)):
                action = "archive"
                reason = "working set ceiling reached and sample was not strong enough to create a new note"
                archive_path = write_archive_record(runtime_root, record, reason)
                target_path = str(archive_path)
            else:
                action = "promote_to_field_note"
                created_note = create_field_note(runtime_root, record, score, signals, ledger, touched_slugs)
                note_by_slug[created_note.slug] = created_note
                record_repeat_evidence(ledger, created_note.slug, recent_repeat_count)
                target_path = str(created_note.path)
                created_candidate, candidate_path, gate_checks = maybe_create_repo_candidate(
                    runtime_root,
                    created_note,
                    record,
                    score,
                    signals,
                    recent_repeat_count,
                    ledger,
                    policy,
                )
                if created_candidate and candidate_path is not None:
                    repo_candidate_path = str(candidate_path)

        run_actions[action] += 1
        processed_items.append(item)
        reviewed_items.append(
            {
                "timestamp": datetime.now().astimezone().isoformat(),
                "session_id": item.session_id,
                "scene": item.scene,
                "promotion_hint": item.promotion_hint,
                "score": score,
                "signals": signals,
                "action": action,
                "reason": reason,
                "target_path": target_path,
                "repo_candidate_path": repo_candidate_path,
                "repo_gate_checks": gate_checks,
            }
        )

    remaining = pending_items[batch_size:]
    queue["pending"] = [
        {
            "capture_file": str(item.capture_file),
            "session_id": item.session_id,
            "scene": item.scene,
            "promotion_hint": item.promotion_hint,
            "timestamp": item.timestamp,
        }
        for item in remaining
    ]
    queue.setdefault("reviewed", []).extend(reviewed_items)
    trim_reviewed_history(queue, int(policy.get("max_reviewed_history", 200)))

    overflow_archives = apply_working_set_ceiling(
        runtime_root,
        ledger,
        touched_slugs,
        int(policy.get("promoted_working_set_ceiling", 20)),
    )
    if overflow_archives:
        run_actions["archive"] += len(overflow_archives)

    reconciled_candidates = reconcile_repo_candidates(runtime_root, note_by_slug, ledger, policy)
    if reconciled_candidates["created"]:
        run_actions["create_repo_candidate"] += len(reconciled_candidates["created"])
    if reconciled_candidates["removed"]:
        run_actions["drop_repo_candidate"] += len(reconciled_candidates["removed"])

    pending_after = len(queue.get("pending", []))
    run_id = f"promotion-run-{datetime.now().astimezone().strftime('%Y%m%dT%H%M%S')}"
    summary = {
        "run_id": run_id,
        "timestamp": datetime.now().astimezone().isoformat(),
        "trigger_source": trigger_source,
        "requested_limit": limit,
        "reconcile_only": limit == 0,
        "processed_count": len(reviewed_items),
        "pending_before": pending_before,
        "pending_after": pending_after,
        "batch_size": batch_size,
        "backlog_threshold": backlog_threshold,
        "backlog_triggered": backlog_triggered,
        "actions": dict(run_actions),
        "overflow_archives": overflow_archives,
        "reconciled_repo_candidates": reconciled_candidates,
        "reviewed_items": reviewed_items,
    }
    ledger["updated_at"] = summary["timestamp"]
    ledger["last_run_id"] = run_id
    ledger.setdefault("runs", []).append(summary)
    return summary


def update_manifest(runtime_root: Path) -> None:
    manifest_path = runtime_root / "state" / "runtime-memory-manifest.json"
    manifest = load_json(manifest_path)
    manifest["last_review_at"] = datetime.now().astimezone().isoformat()
    write_json(manifest_path, manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description="Consume ai-native-loop review queue and auto-promote bounded runtime knowledge.")
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
        "--limit",
        type=int,
        default=None,
        help="Optional hard cap on how many pending items to process in this run.",
    )
    parser.add_argument(
        "--trigger-source",
        choices=("manual", "invocation", "automation"),
        default=None,
        help="Optional label for the caller that initiated this promotion run.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    ensure_runtime_root(resolution.runtime_root, resolution)
    runtime_root = resolution.runtime_root.expanduser()

    queue_path = runtime_root / "inbox" / "review-queue.json"
    ledger_path = runtime_root / "state" / "promotion-ledger.json"
    policy_path = runtime_root / "state" / "promotion-policy.json"

    queue = load_json(queue_path)
    ledger = load_json(ledger_path)
    policy = load_json(policy_path)

    summary = process_pending(
        runtime_root,
        queue,
        ledger,
        policy,
        limit=args.limit,
        trigger_source=args.trigger_source,
    )

    write_json(queue_path, queue)
    write_json(ledger_path, ledger)
    update_manifest(runtime_root)

    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
