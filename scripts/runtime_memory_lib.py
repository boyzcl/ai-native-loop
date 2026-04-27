from __future__ import annotations

from collections import Counter
import json
from dataclasses import dataclass
from datetime import datetime
import math
import os
from pathlib import Path
import re
from typing import Iterable


SKILL_NAME = "ai-native-loop"
GLOBAL_RUNTIME_ROOT_ENV = "AI_NATIVE_LOOP_RUNTIME_ROOT"
GLOBAL_HOST_ENV = "AI_NATIVE_LOOP_HOST"

RUNTIME_SUBDIRS = [
    "captures",
    "index",
    "inbox",
    "promoted/field-notes",
    "promoted/archive",
    "promoted/repo-candidates",
    "state",
]

REQUIRED_CAPTURE_FIELDS = [
    "timestamp",
    "session_id",
    "skill_name",
    "scene",
    "objective",
    "initial_block",
    "intervention_level",
    "artifacts_produced",
    "what_worked",
    "remaining_risk",
    "next_input",
    "candidate_pattern_tags",
    "candidate_failure_tags",
    "promotion_hint",
]

PROMOTED_NOTE_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]+")
PROMOTED_NOTE_STOPWORDS = {
    "after",
    "and",
    "before",
    "current",
    "field",
    "for",
    "from",
    "into",
    "loop",
    "next",
    "note",
    "runtime",
    "task",
    "the",
    "this",
    "with",
}
PROMOTED_RETRIEVAL_WEIGHT_FLOOR = 0.24
RETRIEVAL_EXCLUDED_SECTION_TITLES = {
    "source runtime captures",
    "merge history",
}


@dataclass(frozen=True)
class HostSpec:
    host_id: str
    display_name: str
    support_tier: str
    default_runtime_root: str
    home_env_var: str | None = None
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeResolution:
    host_id: str
    display_name: str
    support_tier: str
    runtime_root: Path
    source: str
    is_known_host: bool


HOST_SPECS = {
    "codex": HostSpec(
        host_id="codex",
        display_name="Codex",
        support_tier="officially_supported",
        default_runtime_root="~/.codex/skills/ai-native-loop/runtime",
        home_env_var="CODEX_HOME",
        aliases=("openai",),
    ),
    "claude-code": HostSpec(
        host_id="claude-code",
        display_name="Claude Code",
        support_tier="experimental",
        default_runtime_root="~/.claude/skills/ai-native-loop/runtime",
        home_env_var="CLAUDE_CODE_HOME",
        aliases=("claude", "claude_code"),
    ),
    "openclaw": HostSpec(
        host_id="openclaw",
        display_name="OpenClaw",
        support_tier="experimental",
        default_runtime_root="~/.openclaw/skills/ai-native-loop/runtime",
        home_env_var="OPENCLAW_HOME",
        aliases=("open-claw",),
    ),
}


def _host_env_key(host_id: str) -> str:
    return host_id.upper().replace("-", "_")


def known_host_ids() -> list[str]:
    return sorted(HOST_SPECS)


def normalize_host(host: str | None) -> str:
    if not host:
        return "codex"

    normalized = host.strip().lower().replace("_", "-")
    for spec in HOST_SPECS.values():
        if normalized == spec.host_id or normalized in spec.aliases:
            return spec.host_id
    return normalized


def resolve_runtime_resolution(
    host: str | None = None,
    root: str | Path | None = None,
    environ: dict[str, str] | None = None,
) -> RuntimeResolution:
    env = environ or os.environ
    normalized_host = normalize_host(host or env.get(GLOBAL_HOST_ENV))

    if root:
        runtime_root = Path(root).expanduser()
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=runtime_root,
            source="explicit_root",
            is_known_host=spec is not None,
        )

    explicit_root = env.get(GLOBAL_RUNTIME_ROOT_ENV)
    if explicit_root:
        spec = HOST_SPECS.get(normalized_host)
        return RuntimeResolution(
            host_id=normalized_host,
            display_name=spec.display_name if spec else normalized_host,
            support_tier=spec.support_tier if spec else "custom",
            runtime_root=Path(explicit_root).expanduser(),
            source=f"env:{GLOBAL_RUNTIME_ROOT_ENV}",
            is_known_host=spec is not None,
        )

    spec = HOST_SPECS.get(normalized_host)
    if spec is None:
        raise ValueError(
            "unknown host requires --root or AI_NATIVE_LOOP_RUNTIME_ROOT: "
            f"{normalized_host}"
        )

    host_runtime_env = f"AI_NATIVE_LOOP_{_host_env_key(normalized_host)}_RUNTIME_ROOT"
    if env.get(host_runtime_env):
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=Path(env[host_runtime_env]).expanduser(),
            source=f"env:{host_runtime_env}",
            is_known_host=True,
        )

    if spec.home_env_var and env.get(spec.home_env_var):
        runtime_root = Path(env[spec.home_env_var]).expanduser() / "skills" / SKILL_NAME / "runtime"
        return RuntimeResolution(
            host_id=spec.host_id,
            display_name=spec.display_name,
            support_tier=spec.support_tier,
            runtime_root=runtime_root,
            source=f"env:{spec.home_env_var}",
            is_known_host=True,
        )

    return RuntimeResolution(
        host_id=spec.host_id,
        display_name=spec.display_name,
        support_tier=spec.support_tier,
        runtime_root=Path(spec.default_runtime_root).expanduser(),
        source=f"default:{spec.host_id}",
        is_known_host=True,
    )


def enrich_capture_record(record: dict, resolution: RuntimeResolution) -> dict:
    enriched = dict(record)
    enriched.setdefault("runtime_host", resolution.host_id)
    enriched.setdefault("runtime_root", str(resolution.runtime_root))
    enriched.setdefault("runtime_root_source", resolution.source)
    return enriched


def parse_runtime_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return parsed.astimezone()


def default_manifest(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict:
    manifest = {
        "version": 1,
        "runtime_root": str(runtime_root),
        "created_at": datetime.now().astimezone().isoformat(),
        "capture_policy": "medium_plus_write_local_capture",
        "last_review_at": None,
        "notes": "runtime layer stores local experience; repository remains the public validation layer",
        "promotion_governance": "local_auto_promotion_repo_candidate_gated",
    }
    if resolution is not None:
        manifest.update(
            {
                "runtime_host": resolution.host_id,
                "runtime_host_display_name": resolution.display_name,
                "runtime_host_support_tier": resolution.support_tier,
                "runtime_root_resolution_source": resolution.source,
            }
        )
    return manifest


def default_promotion_policy() -> dict:
    return {
        "version": 1,
        "backlog_threshold": 10,
        "default_batch_size": 5,
        "promoted_working_set_ceiling": 20,
        "max_raw_reads": 5,
        "max_promoted_reads": 3,
        "max_reference_reads": 2,
        "max_reviewed_history": 200,
        "dedup_similarity_threshold": 0.52,
        "merge_similarity_threshold": 0.36,
        "keep_raw_max_score": 2,
        "promote_min_score": 3,
        "repo_candidate_min_score": 4,
        "repo_candidate_gate_min": 2,
        "repo_candidate_require_repeat_or_reuse": True,
        "repo_candidate_min_reuse_count": 2,
        "repo_candidate_min_source_sessions": 2,
        "reuse_history_limit": 500,
        "archive_keywords": [
            "smoke test",
            "smoke-test",
            "bootstrap",
            "cli sample",
        ],
        "scoring": {
            "repeat_signal": 2,
            "transfer_signal": 1,
            "specificity_signal": 1,
            "future_judgment_signal": 1,
            "benchmark_signal": 1,
        },
        "notes": (
            "Promotion stays local by default. Repo candidates require stronger evidence, "
            "while dedup, archive, and ceilings apply before new note creation."
        ),
    }


def default_promotion_ledger() -> dict:
    return {
        "version": 1,
        "created_at": datetime.now().astimezone().isoformat(),
        "updated_at": None,
        "last_run_id": None,
        "runs": [],
        "note_stats": {},
    }


def default_reuse_ledger() -> dict:
    return {
        "version": 1,
        "created_at": datetime.now().astimezone().isoformat(),
        "updated_at": None,
        "events": [],
        "note_hits": {},
    }


def ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution | None = None) -> dict:
    return {
        "runtime_root": str(runtime_root.expanduser()),
        "runtime_host": resolution.host_id if resolution else None,
        "runtime_root_source": resolution.source if resolution else None,
        "created": _ensure_runtime_root(runtime_root, resolution),
    }


def _ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution | None) -> list[str]:
    runtime_root = runtime_root.expanduser()
    created = []
    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    defaults = {
        runtime_root / "index" / "by-scene.json": {},
        runtime_root / "index" / "by-pattern.json": {},
        runtime_root / "index" / "by-failure-mode.json": {},
        runtime_root / "inbox" / "review-queue.json": {"pending": [], "reviewed": []},
        runtime_root / "state" / "promotion-policy.json": default_promotion_policy(),
        runtime_root / "state" / "promotion-ledger.json": default_promotion_ledger(),
        runtime_root / "state" / "reuse-ledger.json": default_reuse_ledger(),
        runtime_root / "state" / "runtime-memory-manifest.json": default_manifest(runtime_root, resolution),
    }

    for file_path, data in defaults.items():
        if not file_path.exists():
            file_path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
            continue
        try:
            existing = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(existing, dict) and isinstance(data, dict):
            merged = _merge_missing_defaults(existing, data)
            if merged != existing:
                file_path.write_text(json.dumps(merged, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    readme_path = runtime_root / "README.md"
    if not readme_path.exists():
        readme_text = (
            "# Runtime Memory\n\n"
            "This directory stores local ai-native-loop runtime captures, light indices, review queue, and promoted notes.\n"
        )
        if resolution is not None:
            readme_text += (
                f"\n- Host: `{resolution.display_name}`\n"
                f"- Support tier: `{resolution.support_tier}`\n"
                f"- Resolution source: `{resolution.source}`\n"
            )
        readme_path.write_text(readme_text, encoding="utf-8")

    return created


def validate_capture(record: dict) -> None:
    missing = [field for field in REQUIRED_CAPTURE_FIELDS if field not in record]
    if missing:
        raise ValueError(f"capture record missing required fields: {', '.join(missing)}")

    if record["intervention_level"] not in {"light", "medium", "strong"}:
        raise ValueError("intervention_level must be one of: light, medium, strong")

    if not isinstance(record["artifacts_produced"], list):
        raise ValueError("artifacts_produced must be a list")

    if not isinstance(record["candidate_pattern_tags"], list):
        raise ValueError("candidate_pattern_tags must be a list")

    if not isinstance(record["candidate_failure_tags"], list):
        raise ValueError("candidate_failure_tags must be a list")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _merge_missing_defaults(existing: dict, default: dict) -> dict:
    merged = dict(existing)
    for key, value in default.items():
        if key not in merged:
            merged[key] = value
        elif isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_missing_defaults(merged[key], value)
    return merged


def append_capture(runtime_root: Path, record: dict) -> Path:
    runtime_root = runtime_root.expanduser()
    validate_capture(record)

    timestamp = datetime.fromisoformat(record["timestamp"])
    capture_file = runtime_root / "captures" / f"{timestamp.date().isoformat()}.jsonl"
    with capture_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")

    _update_index(runtime_root / "index" / "by-scene.json", [record["scene"]], record, "scene")
    _update_index(runtime_root / "index" / "by-pattern.json", record["candidate_pattern_tags"], record, "pattern")
    _update_index(runtime_root / "index" / "by-failure-mode.json", record["candidate_failure_tags"], record, "failure_mode")

    if record["promotion_hint"] != "raw_only":
        queue_path = runtime_root / "inbox" / "review-queue.json"
        queue = _load_json(queue_path)
        queue.setdefault("pending", []).append(
            {
                "capture_file": str(capture_file),
                "session_id": record["session_id"],
                "scene": record["scene"],
                "promotion_hint": record["promotion_hint"],
                "timestamp": record["timestamp"],
            }
        )
        _write_json(queue_path, queue)

    return capture_file


def _update_index(index_path: Path, keys: Iterable[str], record: dict, label: str) -> None:
    index = _load_json(index_path)
    for key in keys:
        if not key:
            continue
        entry = index.setdefault(
            key,
            {"count": 0, "latest_timestamp": None, "latest_session_id": None, "label": label},
        )
        entry["count"] += 1
        entry["latest_timestamp"] = record["timestamp"]
        entry["latest_session_id"] = record["session_id"]
    _write_json(index_path, index)


def read_recent_captures(runtime_root: Path, scene: str | None = None, limit: int = 5) -> list[dict]:
    runtime_root = runtime_root.expanduser()
    capture_files = sorted((runtime_root / "captures").glob("*.jsonl"), reverse=True)
    found: list[dict] = []
    for capture_file in capture_files:
        lines = capture_file.read_text(encoding="utf-8").splitlines()
        for line in reversed(lines):
            if not line.strip():
                continue
            record = json.loads(line)
            if scene and record.get("scene") != scene:
                continue
            found.append(record)
            if len(found) >= limit:
                return found
    return found


def read_promoted_field_notes(runtime_root: Path, scene: str | None = None, limit: int = 3) -> list[dict]:
    ranked = rank_promoted_field_notes(runtime_root, scene=scene, limit=limit)
    return [
        {
            "path": item["path"],
            "slug": item["slug"],
            "title": item["title"],
            "excerpt": item["excerpt"],
            "matched_tokens": item["matched_tokens"],
            "weighted_overlap": item["weighted_overlap"],
            "title_overlap": item["title_overlap"],
        }
        for item in ranked[:limit]
    ]


def rank_promoted_field_notes(runtime_root: Path, scene: str | None = None, limit: int | None = None) -> list[dict]:
    runtime_root = runtime_root.expanduser()
    note_files = sorted((runtime_root / "promoted" / "field-notes").glob("*.md"), reverse=True)
    promotion_ledger = _load_json(runtime_root / "state" / "promotion-ledger.json")
    note_stats = promotion_ledger.get("note_stats", {})
    query_tokens = _tokenize_note(scene or "")
    note_entries = []
    token_frequencies: Counter[str] = Counter()

    for note_file in note_files:
        text = note_file.read_text(encoding="utf-8")
        title = _note_title(note_file, text)
        note_tokens = _tokenize_note(f"{note_file.stem} {_retrieval_text(text)}")
        title_tokens = _tokenize_note(f"{note_file.stem} {title}")
        token_frequencies.update(note_tokens)
        note_entries.append(
            {
                "path": str(note_file),
                "slug": note_file.stem,
                "title": title,
                "excerpt": _note_excerpt(text),
                "note_tokens": note_tokens,
                "title_tokens": title_tokens,
                "reuse_count": int(note_stats.get(note_file.stem, {}).get("reuse_count", 0)),
                "recency": note_file.stat().st_mtime,
            }
        )

    token_weights = _token_idf_weights(token_frequencies, max(1, len(note_entries)))
    min_shared_tokens = _minimum_shared_tokens(query_tokens)
    ranked = []
    for entry in note_entries:
        shared_tokens = query_tokens & entry["note_tokens"]
        shared_count = len(shared_tokens)
        title_overlap = _token_overlap(query_tokens, entry["title_tokens"]) if query_tokens else 0.0
        weighted_overlap = _weighted_token_overlap(query_tokens, shared_tokens, token_weights)
        strong_match = (
            shared_count >= min_shared_tokens
            or title_overlap >= 0.55
            or weighted_overlap >= PROMOTED_RETRIEVAL_WEIGHT_FLOOR
        )
        combined_rank_score = weighted_overlap + (0.6 * title_overlap)
        ranked.append(
            entry
            | {
                "matched_tokens": sorted(shared_tokens),
                "matched_token_count": shared_count,
                "title_overlap": round(title_overlap, 4),
                "weighted_overlap": round(weighted_overlap, 4),
                "combined_rank_score": round(combined_rank_score, 4),
                "has_overlap": shared_count > 0,
                "strong_match": strong_match if query_tokens else True,
            }
        )

    ranked.sort(
        key=lambda item: (
            item["strong_match"],
            item["combined_rank_score"],
            item["title_overlap"],
            item["matched_token_count"],
            item["reuse_count"],
            item["recency"],
        ),
        reverse=True,
    )
    if query_tokens:
        strong_matches = [item for item in ranked if item["strong_match"]]
        overlapping = [item for item in ranked if item["has_overlap"]]
        ranked = strong_matches or overlapping or ranked
        if ranked:
            top_score = ranked[0]["combined_rank_score"]
            floor = max(PROMOTED_RETRIEVAL_WEIGHT_FLOOR, top_score * 0.5)
            filtered = [
                item
                for item in ranked
                if item["combined_rank_score"] >= floor or item["title_overlap"] >= 0.5
            ]
            ranked = filtered or ranked[:1]

    for item in ranked:
        item.pop("note_tokens", None)
        item.pop("title_tokens", None)

    if limit is None:
        return ranked
    return ranked[:limit]


def record_promoted_note_reuse(
    runtime_root: Path,
    promoted_notes: list[dict],
    *,
    scene: str | None = None,
    source: str = "read_runtime_context",
    reuse_history_limit: int = 500,
) -> dict:
    runtime_root = runtime_root.expanduser()
    reuse_ledger_path = runtime_root / "state" / "reuse-ledger.json"
    promotion_ledger_path = runtime_root / "state" / "promotion-ledger.json"

    if not promoted_notes:
        return {"recorded": 0, "events": []}

    reuse_ledger = _load_json(reuse_ledger_path)
    promotion_ledger = _load_json(promotion_ledger_path)
    note_stats = promotion_ledger.setdefault("note_stats", {})
    timestamp = datetime.now().astimezone().isoformat()
    seen_slugs: set[str] = set()
    events = []

    for note in promoted_notes:
        slug = note.get("slug") or Path(note["path"]).stem
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        note_path = str(Path(note["path"]).expanduser())
        event = {
            "timestamp": timestamp,
            "source": source,
            "scene": scene,
            "note_slug": slug,
            "note_path": note_path,
        }
        events.append(event)

        hit_entry = reuse_ledger.setdefault("note_hits", {}).setdefault(
            slug,
            {
                "note_path": note_path,
                "count": 0,
                "last_hit_at": None,
                "scenes": [],
                "sources": [],
            },
        )
        hit_entry["note_path"] = note_path
        hit_entry["count"] += 1
        hit_entry["last_hit_at"] = timestamp
        if scene and scene not in hit_entry["scenes"]:
            hit_entry["scenes"].append(scene)
        if source not in hit_entry["sources"]:
            hit_entry["sources"].append(source)

        note_entry = note_stats.setdefault(
            slug,
            {
                "note_path": note_path,
                "title": note.get("title") or slug.replace("-", " "),
                "created_at": timestamp,
                "last_updated_at": timestamp,
                "source_session_ids": [],
                "merge_count": 0,
                "repo_candidate_paths": [],
                "archived": False,
                "archive_reason": None,
                "reuse_count": 0,
                "last_action": None,
            },
        )
        note_entry["note_path"] = note_path
        note_entry["reuse_count"] = int(note_entry.get("reuse_count", 0)) + 1
        note_entry["last_reused_at"] = timestamp
        note_entry["last_updated_at"] = timestamp

    reuse_ledger.setdefault("events", []).extend(events)
    if len(reuse_ledger["events"]) > reuse_history_limit:
        reuse_ledger["events"] = reuse_ledger["events"][-reuse_history_limit:]
    reuse_ledger["updated_at"] = timestamp
    promotion_ledger["updated_at"] = timestamp

    _write_json(reuse_ledger_path, reuse_ledger)
    _write_json(promotion_ledger_path, promotion_ledger)
    return {"recorded": len(events), "events": events}


def _tokenize_note(text: str) -> set[str]:
    tokens = set()
    for token in PROMOTED_NOTE_TOKEN_RE.findall(text.lower()):
        if token in PROMOTED_NOTE_STOPWORDS or len(token) < 3:
            continue
        tokens.add(token)
        for subtoken in token.replace("_", "-").split("-"):
            if subtoken not in PROMOTED_NOTE_STOPWORDS and len(subtoken) >= 3:
                tokens.add(subtoken)
    return tokens


def _token_overlap(query_tokens: set[str], note_tokens: set[str]) -> float:
    if not query_tokens or not note_tokens:
        return 0.0
    return len(query_tokens & note_tokens) / max(1, min(len(query_tokens), len(note_tokens)))


def _retrieval_text(text: str) -> str:
    lines = []
    skip_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            section_title = line[3:].strip().lower()
            skip_section = section_title in RETRIEVAL_EXCLUDED_SECTION_TITLES
            if skip_section:
                continue
        if skip_section:
            continue
        if "/Users/" in line or ".codex/" in line:
            continue
        lines.append(line)
    return "\n".join(lines)


def _minimum_shared_tokens(query_tokens: set[str]) -> int:
    if len(query_tokens) <= 3:
        return 1
    if len(query_tokens) <= 6:
        return 2
    return 3


def _token_idf_weights(token_frequencies: Counter[str], note_count: int) -> dict[str, float]:
    weights = {}
    for token, frequency in token_frequencies.items():
        weights[token] = math.log1p(note_count / max(1, frequency))
    return weights


def _weighted_token_overlap(
    query_tokens: set[str],
    shared_tokens: set[str],
    token_weights: dict[str, float],
) -> float:
    if not query_tokens:
        return 0.0
    shared_weight = sum(token_weights.get(token, 1.0) for token in shared_tokens)
    query_weight = sum(token_weights.get(token, 1.0) for token in query_tokens)
    return shared_weight / max(1.0, query_weight)


def _note_title(note_file: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return note_file.stem.replace("-", " ")


def _note_excerpt(text: str, max_length: int = 220) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
    excerpt = " ".join(lines[:4])
    return excerpt[:max_length].strip()


def validate_runtime_root(runtime_root: Path) -> list[str]:
    runtime_root = runtime_root.expanduser()
    errors = []
    for subdir in RUNTIME_SUBDIRS:
        path = runtime_root / subdir
        if not path.exists() or not path.is_dir():
            errors.append(f"missing directory: {path}")

    json_files = [
        runtime_root / "index" / "by-scene.json",
        runtime_root / "index" / "by-pattern.json",
        runtime_root / "index" / "by-failure-mode.json",
        runtime_root / "inbox" / "review-queue.json",
        runtime_root / "state" / "promotion-policy.json",
        runtime_root / "state" / "promotion-ledger.json",
        runtime_root / "state" / "reuse-ledger.json",
        runtime_root / "state" / "runtime-memory-manifest.json",
    ]

    for json_file in json_files:
        if not json_file.exists():
            errors.append(f"missing file: {json_file}")
            continue
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json in {json_file}: {exc}")

    for capture_file in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line_no, line in enumerate(capture_file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                validate_capture(record)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid capture in {capture_file}:{line_no}: {exc}")

    return errors
