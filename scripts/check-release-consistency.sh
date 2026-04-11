#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$ROOT/docs/release-manifest.md"
README="$ROOT/README.md"
SKILL="$ROOT/SKILL.md"
CHANGELOG="$ROOT/CHANGELOG.md"

extract_value() {
  local key="$1"
  awk -v key="$key" '
    $0 ~ "`" key "`" { getline; gsub(/^[[:space:]-]+|[[:space:]]+$/, "", $0); gsub(/`/, "", $0); print $0; exit }
  ' "$MANIFEST"
}

public_version="$(extract_value public_version)"
metadata_version="$(extract_value public_skill_metadata_version)"
active_iteration_track="$(extract_value active_iteration_track)"
track_status="$(extract_value track_status)"
RELEASE_NOTES="$ROOT/docs/release-notes-$active_iteration_track.md"

fail() {
  echo "release consistency check failed: $1" >&2
  exit 1
}

grep -Fq "Current public version: \`$public_version\`" "$README" || fail "README public version out of sync"
grep -Fq "Current iteration track: \`$active_iteration_track\` $track_status" "$README" || fail "README track status out of sync"
grep -Fq "version: \"$metadata_version\"" "$SKILL" || fail "SKILL metadata version out of sync"
[[ -f "$RELEASE_NOTES" ]] || fail "release notes file missing for $active_iteration_track"
grep -Fq "Current release truth lives in [release-manifest.md]" "$RELEASE_NOTES" || fail "release notes missing manifest pointer"
grep -Fq "Release manifest as the canonical source of truth" "$CHANGELOG" || fail "CHANGELOG missing manifest entry"

echo "release consistency check passed"
