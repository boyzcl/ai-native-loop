# Benchmark 05: Multi-Agent Decomposition / Rule-Layer Expansion

## Scenario

- Category: 多 Agent 协作
- Type: 扩展 benchmark 场景定义
- Purpose: 用于验证 `ai-native-loop` 是否能把多 Agent 协作从模板层推进到规则层

## Original Request

“面对一个跨研究、实现、验证或整合的复杂任务，判断是否该拆分多个 agent；如果要拆，明确每个 agent 的最小输入包、回收物与主 agent 的保留职责。”

## Primary Risk

- 为了并行而并行
- 目标没收敛就开始拆分
- 子 agent 漂移，主 agent 最后拿不到可整合结果
- 主 agent 把判断权错误外包

## Expected Intervention

默认 `strong`。

原因：

- 这类任务的关键不在多给建议，而在先建立分工与回收规则。
- 如果不先定义边界，协作负担会迅速放大。

## Expected Core Artifacts

这个 benchmark 通过时，至少应出现：

- 一张解释“该拆还是不拆”的 `Diagnosis Card`
- 一份总任务 `Task Packet`
- 至少一个子 agent 最小输入包
- 一个统一 handoff artifact 格式
- 一份由主 agent 输出的整合结论或 `Re-input Packet`

## Pass Criteria

通过标准：

- 明确给出拆分与不拆分的边界
- 主 agent / 子 agent 职责不混淆
- 回收物格式统一
- 最终结果不是多个输出的简单拼接，而是经过主 agent 再整合
- `decomposition_quality` 不低于 4 / 5

## Suggested Scoring Lens

建议沿用通用 rubric：

- `clarity`
- `executability`
- `boundary_control`
- `feedback_quality`
- `reinput_quality`
- `transferability`
- `context_efficiency`
- `real_task_helpfulness`

额外观察项：

- `decomposition_quality`
  是否真的拆在了正确边界上。

统一评分细则见 [evaluation-rubric.md](../evaluation-rubric.md)。

## Required Comparison

这个场景执行时，至少比较：

1. `baseline`
   - 单线程处理，不拆 agent
2. `candidate`
   - 按多 Agent 规则拆分

只有在 `candidate` 明显改善整合质量、上下文噪音或主 agent 负担时，才应判定“拆分有效”。

## Current Status

当前状态：**场景已建立，待执行 baseline / candidate 实测**。

它的作用不是回填一个虚假的高分案例，而是把多 Agent 从“悬空能力声明”变成固定可测场景。
