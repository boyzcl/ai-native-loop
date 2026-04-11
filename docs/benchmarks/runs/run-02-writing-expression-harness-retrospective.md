# Benchmark Run: Writing Expression / Harness Report Expansion

## Scenario

- benchmark_ref: [benchmark-02-writing-expression-harness.md](../benchmark-02-writing-expression-harness.md)
- date: `2026-04-11`
- evaluator: retrospective migration from existing benchmark result

## Input

- original_request:
  - 把已有的 Harness Engineering 研究报告扩充成更完整的综合研究报告，重点补六大组件的执行层细节，并保留可复现性和来源质量。
- initial_block:
  - 扩写任务容易退化成资料堆叠，而不是结构增强。

## Comparison Setup

### baseline

- prompt_or_workflow:
  - pending
- notable_limit:
  - 尚未重跑 baseline。

### candidate

- prompt_or_workflow:
  - 使用 `ai-native-loop` 将写作改写为“指令 -> 大纲 -> 初稿 -> 自审 -> 终稿”的循环。
- version:
  - `v0.2.0 draft / validation hardening`

### optional previous

- prompt_or_workflow:
  - n/a
- version:
  - n/a

## Artifacts Observed

- baseline_artifacts:
  - pending
- candidate_artifacts:
  - `02_大纲.md`
  - `04_自审记录.md`
  - 终稿链路
- optional_previous_artifacts:
  - n/a

## Scores

| Dimension | baseline | candidate | optional_previous | notes |
|---|---:|---:|---:|---|
| clarity |  | 4.7 |  | 扩写目标被压成结构性写作任务 |
| executability |  | 4.8 |  | 阶段产物清楚 |
| boundary_control |  | 4.5 |  | 受众与结构边界总体合理 |
| feedback_quality |  | 4.6 |  | 自审进入显式反馈层 |
| reinput_quality |  | 4.7 |  | 大纲与自审都进入下一轮 |
| transferability |  | 4.6 |  | 适合长文与报告写作 |
| context_efficiency |  | 4.5 |  | 通过阶段工件降低了一次性成稿噪音 |
| real_task_helpfulness |  | 4.7 |  | 真正推动了扩写链路 |

## Pairwise Judgment

- candidate_vs_baseline:
  - pending，需补 baseline 重跑
- candidate_vs_previous:
  - n/a

## Result

- what_improved:
  - 已完成统一 run record 迁移。
- what_did_not_improve:
  - 未补 baseline。
- new_regression_or_risk:
  - 如果没有 baseline，很难证明闭环写作一定优于直接扩写。

## Decision

- conditional_pass

## Next Action

- 继续保留什么：
  - 大纲与自审进入循环的写法
- 下一轮要改什么：
  - 补 baseline 并做 pairwise 评审
