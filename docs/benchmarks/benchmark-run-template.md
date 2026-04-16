# Benchmark Run Template

## Purpose

这份模板用于把单个 benchmark 场景的执行记录标准化。

它的目标不是写漂亮总结，而是保证一次 benchmark 至少留下可比较、可回放、可复评的证据。

## Template

```md
# Benchmark Run: <scenario-name>

## Scenario

- benchmark_ref:
- date:
- evaluator:

## Input

- original_request:
- initial_block:

## Comparison Setup

### baseline

- prompt_or_workflow:
- notable_limit:

### candidate

- prompt_or_workflow:
- version:

### optional previous

- prompt_or_workflow:
- version:

## Artifacts Observed

- baseline_artifacts:
- candidate_artifacts:
- optional_previous_artifacts:

## Runtime Memory Provenance

- runtime_capture_written:
- runtime_capture_ref:
- runtime_read_refs:
- runtime_reuse_observed:

## Scores

按 [evaluation-rubric.md](../evaluation-rubric.md) 逐项评分：

| Dimension | baseline | candidate | optional_previous | notes |
|---|---:|---:|---:|---|
| clarity |  |  |  |  |
| executability |  |  |  |  |
| boundary_control |  |  |  |  |
| feedback_quality |  |  |  |  |
| reinput_quality |  |  |  |  |
| transferability |  |  |  |  |
| context_efficiency |  |  |  |  |
| real_task_helpfulness |  |  |  |  |

## Pairwise Judgment

- candidate_vs_baseline:
- candidate_vs_previous:

## Result

- what_improved:
- what_did_not_improve:
- new_regression_or_risk:

## Decision

- pass / conditional_pass / fail

## Next Action

- 继续保留什么：
- 下一轮要改什么：
```

## Use Rule

- 没有 baseline 时，可以先记 `candidate`，但不能下“明显更好”的强结论
- 如果是版本迭代，优先补 `previous`
- 对多 Agent 场景，必须额外写清 `decomposition_quality`
- 对 runtime compounding 相关声明，必须写清 `runtime_capture_ref` 与 `runtime_reuse_observed`
