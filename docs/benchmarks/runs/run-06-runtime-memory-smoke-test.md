# Benchmark Run: runtime-memory-smoke-test

> Historical note: this benchmark run records a Codex-hosted validation sample. The `.codex` runtime reference below is provenance for that dated run, not the current cross-host contract.

## Scenario

- benchmark_ref: runtime-memory-smoke-test
- date: 2026-04-16
- evaluator: local smoke validation

## Input

- original_request: verify that `medium+` skill runs now write a local runtime capture on the installed skill copy
- initial_block: previous mechanism only guaranteed a response-tail recovery block, not a reusable local host

## Comparison Setup

### baseline

- prompt_or_workflow: old repo-only recovery block design
- notable_limit: no guaranteed local runtime capture and no retrieval host for next round

### candidate

- prompt_or_workflow: local-first runtime memory layer with helper scripts and runtime capture contract
- version: v0.2.0 draft

## Artifacts Observed

- baseline_artifacts: recovery block only
- candidate_artifacts: runtime directory, capture file, index updates, review queue entry, promoted local field note

## Runtime Memory Provenance

- runtime_capture_written: yes
- runtime_capture_ref: `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/captures/2026-04-16.jsonl#bootstrap-runtime-smoke-20260416`
- runtime_read_refs: bootstrap smoke test validated retrieval by `scene=runtime-memory-smoke-test`
- runtime_reuse_observed: partial

## Scores

按 [evaluation-rubric.md](../../evaluation-rubric.md) 逐项评分：

| Dimension | baseline | candidate | optional_previous | notes |
|---|---:|---:|---:|---|
| clarity | 2 | 5 |  | runtime host and boundary are now explicit |
| executability | 2 | 5 |  | helper scripts and runtime layout make the mechanism runnable |
| boundary_control | 3 | 4 |  | runtime and repo responsibilities are now separated |
| feedback_quality | 2 | 4 |  | failure is now framed as repo-only storage vs local-first storage |
| reinput_quality | 1 | 4 |  | next-round input now has a real local host to read from |
| transferability | 2 | 4 |  | mechanism can apply to future medium-plus tasks |
| context_efficiency | 2 | 4 |  | retrieval budget is defined and bounded |
| real_task_helpfulness | 1 | 4 |  | installed skill now has a concrete runtime layer instead of only documentation |

## Pairwise Judgment

- candidate_vs_baseline: candidate is materially better because the experience compounding claim now has a real local host and runnable helpers
- candidate_vs_previous: n/a

## Result

- what_improved: local runtime capture, review queue, scene index, and validation scripts are all now present
- what_did_not_improve: this run does not yet prove repeated real-user reuse
- new_regression_or_risk: runtime data can still bloat without ongoing review discipline

## Decision

- pass

## Next Action

- 继续保留什么：local-first runtime host, explicit invocation, runtime provenance requirement
- 下一轮要改什么：collect repeated real-user runtime captures and verify true next-round reuse
