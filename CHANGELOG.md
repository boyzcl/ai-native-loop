# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Release manifest as the canonical source of truth for current version and track state
- Evaluation rubric and experiment log template for baseline and pairwise validation
- Default loop recovery block to lower-friction experience capture for medium-plus interventions
- README smoke test and before/after trigger example for faster first-run adoption

### Changed

- Benchmark matrix now requires baseline comparison and rubric-driven scoring
- Project status memo is no longer intended to be the live source of version truth

### Previously Added

- v0.2.0 iteration execution plan documenting the next engineering phase for the skill
- Core operating primitives for Diagnosis Card, Task Packet, Feedback Attribution Card, and Re-input Packet
- Failure modes reference covering common loop breakdowns and correction rules
- Multi-agent decomposition rules covering split / don't-split boundaries, child-agent minimum packets, and handoff artifacts
- Experience compounding loop reference plus field-note and pattern-intake templates for lower-friction experience capture
- Pattern library with self-bootstrap, research-to-report, decision-structuring, and multi-agent decomposition patterns
- Multi-agent decomposition pattern and a fixed expansion benchmark scenario for the collaboration track
- Decision-structuring field note to pattern/failure/benchmark demonstration chain
- Benchmark matrix defining fixed scenarios and pass criteria for future evaluation
- Executed 4 retrospective benchmark cases across research, writing, product, and decision workflows with a 4.70 average score
- Case 02 documenting how the skill transfers to a research-and-writing workflow via the Rosie mRNA investigation chain
- Drafted `v0.2.0` release notes to explain the version in failure-driven rather than file-driven terms

## v0.1.0 - 2026-04-11

### Added

- Initial public release of `ai-native-loop`
- Core `SKILL.md` for the AI-native workflow protocol
- Reference docs for loop protocol, intervention matrix, feedback attribution, information restructuring, transfer patterns, and growth ladder
- Templates for task rewrite, AI-first input, re-input, intervention protocol, and multi-agent handoff
- Project-level README, MIT license, release readiness notes, self-evaluation, and forward-test docs
- Case 01 self-bootstrap documentation
- Trigger examples library for deciding when the skill should or should not be invoked

### Changed

- Repository restructured into a skill-first layout with `SKILL.md`, `references/`, and `agents/` at the repository root
- README upgraded with Quick Start, first-use prompts, and clearer product-facing positioning

### Validation

- Root-level skill validation passes successfully
- Public GitHub repository created and pushed
