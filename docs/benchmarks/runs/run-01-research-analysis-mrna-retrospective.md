# Benchmark Run: Research Analysis / mRNA Investigation

## Scenario

- benchmark_ref: [benchmark-01-research-analysis-mrna.md](../benchmark-01-research-analysis-mrna.md)
- date: `2026-04-11`
- evaluator: retrospective migration from existing benchmark result

## Input

- original_request:
  - 深度调查 Rosie 个性化 mRNA 疫苗事件，还原事件与技术流水线，并最终产出调查报告与操作手册。
- initial_block:
  - 研究、技术溯源、可信度判断与最终成稿同时存在，直接成稿风险高。

## Comparison Setup

### baseline

- prompt_or_workflow:
  - pending
- notable_limit:
  - 本次未重跑 baseline，仅迁移既有结果到统一模板。

### candidate

- prompt_or_workflow:
  - 使用 `ai-native-loop` 的 `Diagnosis Card + Task Packet + Feedback Attribution Card + Re-input Packet` 组织研究链路。
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
  - `findings.md`
  - `pipeline.md`
  - `report.md`
- optional_previous_artifacts:
  - n/a

## Scores

| Dimension | baseline | candidate | optional_previous | notes |
|---|---:|---:|---:|---|
| clarity |  | 5.0 |  | 复杂主题被压成调查层、技术层、整合层 |
| executability |  | 4.8 |  | 中间工件链清楚 |
| boundary_control |  | 4.8 |  | 明确保留事实、推断与公开缺口边界 |
| feedback_quality |  | 4.8 |  | 缺口与可信度进入显式结构 |
| reinput_quality |  | 4.9 |  | `findings` 与 `pipeline` 进入终稿输入 |
| transferability |  | 4.8 |  | 可迁移到复杂研究任务 |
| context_efficiency |  | 4.7 |  | 通过中间工件降低了直接成稿噪音 |
| real_task_helpfulness |  | 4.9 |  | 真实推进了调查与成稿链路 |

## Pairwise Judgment

- candidate_vs_baseline:
  - pending，需补 baseline 重跑
- candidate_vs_previous:
  - n/a

## Result

- what_improved:
  - 已把候选方案迁移到统一 run record 结构。
- what_did_not_improve:
  - 仍未获得 baseline 对照。
- new_regression_or_risk:
  - 如果长期只保留 retrospective 分数，会继续存在自证偏差。

## Decision

- conditional_pass

## Next Action

- 继续保留什么：
  - 三层工件链与可信度边界写法
- 下一轮要改什么：
  - 补 baseline 执行并完成 pairwise 判断
