# Benchmark 03: Product Progression / Codex Proxy Fix

## Scenario

- Category: 产品推进
- Source materials:
  - `CODEX_PROXY_FIX_IMPLEMENTATION_BLUEPRINT.md`
  - `RELEASE_READINESS_PLAN.md`
  - `RELEASE_NOTES_v0.1.0-alpha.1.md`
  - `README.md`
- Note:
  - 这些源材料保存在仓库外的私有工作目录中，因此这里不提供仓库内跳转链接。

## Original Request

“把一个能缓解 Codex reconnecting 问题的工具，从可工作 MVP 推到一个足够安全的公开 alpha 发布候选。”

## Initial Block

- 任务不只是写代码，还涉及产品边界、平台支持、回滚能力、文档、发布准备。
- 如果直接推进功能实现，很容易忽略 release-critical gap。
- 这类任务同时运动的部件很多，最容易在发布前失真。

## Intervention Level

`medium`

原因：

- 项目已经有实现骨架，不需要强介入重建目标。
- 但发布链路存在多个结构性缺口，需要显式治理。

## Core Artifacts Produced

### Diagnosis Card

- loop_stage: execution -> feedback
- intervention_level: medium
- primary_block: 产品已能工作，但发布层不完整
- risk_note: 如果不先定义 release bar，功能推进会掩盖发布风险

### Task Packet

- objective: 把 working MVP 推到可公开 alpha 的 release candidate
- current_state: CLI 能运行，但回滚、文档、支持边界和验证链路未齐
- artifacts: 实现蓝图、release readiness plan、release notes、README
- constraints: 不夸大平台支持，不跳过回滚和验证
- success_signal: 明确 alpha 版本可公开、可回滚、可解释
- next_checkpoint: 检查 release-critical gaps 是否逐项关闭

### Feedback Attribution Card

- signal: 工具已经可用，但仓库还不够安全地对外发布
- failure_class: decision failure
- root_cause: 项目目标从“做出来”切换到“能发布”时，验收标准变了
- keep: CLI 主路径和平台目标清晰
- change: 把发布 readiness 独立成一份治理计划和验收条目

### Re-input Packet

- preserve: 工具实现主线、命令入口和平台定位
- discard: 把 alpha 发布误当成只需要功能跑通
- add_context: rollback、docs、license、support boundary、verification checklist
- change_request: 逐项关闭 release-critical gap 后再发布
- next_checkpoint: 根据 release bar 判断是否达到公开 alpha 条件

## Output Result

- 项目从“功能开发”转成了“发布治理”状态。
- 发布准备被拆成可执行的 gap 列表，而不是含糊的“再完善一下”。
- 支持边界、风险和 release bar 被写死，降低了过度承诺风险。

## Re-input Quality

这里的再输入不是“继续写代码”，而是把反馈改写为：

- rollback 机制
- install/uninstall 真值反馈
- README 升级
- 验证与打包

也就是把工程反馈转成下一轮项目推进任务包。

## Scores

| Dimension | Score | Note |
|---|---:|---|
| clarity | 4.8 | 从 MVP 推到 alpha 的目标很清楚 |
| executability | 4.9 | release-critical gaps 可逐项执行 |
| feedback_quality | 4.7 | 发布风险被显式识别和分类 |
| reinput_quality | 4.6 | 反馈直接转成下一轮发布任务 |
| transferability | 4.8 | 可迁移到其他 CLI 或工具产品发布 |

## Verdict

通过。

这证明 `ai-native-loop` 在产品推进场景里可以把“继续做项目”改写为“围绕验收标准推进项目”。
