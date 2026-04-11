# Benchmark 02: Writing Expression / Harness Report Expansion

## Scenario

- Category: 写作表达
- Source materials:
  - `harness_engineering_instruction.md`
  - `02_大纲.md`
  - `04_自审记录.md`
- Note:
  - 这些源材料保存在仓库外的私有工作目录中，因此这里不提供仓库内跳转链接。

## Original Request

“把已有的 Harness Engineering 研究报告扩充成更完整的综合研究报告，重点补六大组件的执行层细节，并保留可复现性和来源质量。”

## Initial Block

- 这不是从零写文章，而是要扩写既有结构。
- 目标读者分层复杂，既包括工程师，也包括决策者和 OpenClaw 用户。
- 如果直接扩写，很容易变成资料堆叠，而不是结构增强。

## Intervention Level

`medium`

原因：

- 任务边界清楚，但写作对象复杂。
- 已有结构和新增结构之间需要重新编排。
- 输出质量依赖大纲、初稿和自审之间的循环，而不是单次成稿。

## Core Artifacts Produced

### Diagnosis Card

- loop_stage: input -> execution
- intervention_level: medium
- primary_block: 扩写任务容易退化成补资料，而不是重组报告结构
- risk_note: 新增内容如果没有组织层，会破坏原报告整体性

### Task Packet

- objective: 把已有研究报告扩写为六大组件可复现的综合研究报告
- current_state: 有现成报告和扩写目标，但需要新的组织方式
- artifacts: 扩充指令、大纲、初稿、自审记录
- constraints: 不生成代码，保留来源质量和整体连贯性
- success_signal: 六大组件都达到逻辑可复现深度，且全文连贯
- next_checkpoint: 检查新增章节是否和旧结构构成有机整体

### Feedback Attribution Card

- signal: 初稿完成后仍可能出现层级不一致、时间线错位、章节过渡不自然
- failure_class: feedback failure
- root_cause: 写作类任务的质量问题主要暴露在自审阶段，而不是首稿阶段
- keep: 大纲结构、六大组件覆盖和受众映射成立
- change: 把自审显式纳入流程，修复结构性问题再出终稿

### Re-input Packet

- preserve: 六大组件的章节架构和组件内部统一结构
- discard: 标题层级不一致和时间线排序错误
- add_context: 对各类读者的价值映射和来源标注一致性
- change_request: 先完成自审和修正，再输出终稿
- next_checkpoint: 检查终稿是否同时服务实操工程师与决策者

## Output Result

- 大纲把扩写任务从“补内容”改成了“重组整篇报告”。
- 自审记录让质量问题进入显式反馈层，而不是隐性留在终稿里。
- 写作流程形成了“指令 -> 大纲 -> 初稿 -> 自审 -> 终稿”的稳定闭环。

## Re-input Quality

本案例中的再输入主要体现为：

- 大纲不是终点，而是初稿输入。
- 自审记录不是附录，而是终稿修订输入。

这说明 `ai-native-loop` 在写作场景里能把“写一篇文章”改写为“运行一个写作系统”。

## Scores

| Dimension | Score | Note |
|---|---:|---|
| clarity | 4.7 | 扩写目标被压成结构性写作任务 |
| executability | 4.8 | 阶段产物清楚，写作流程稳定 |
| feedback_quality | 4.6 | 自审把问题显式化 |
| reinput_quality | 4.7 | 大纲和自审都进入下一轮 |
| transferability | 4.6 | 可迁移到长文、报告和知识产品写作 |

## Verdict

通过。

这证明 `ai-native-loop` 在写作表达场景中的价值，不在“写得更像文章”，而在“把写作流程变成可迭代结构”。
