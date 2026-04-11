# Benchmark Run Prep: Multi-Agent Decomposition

## Purpose

这不是实测结果，而是 benchmark 05 的执行准备稿。

它的作用是把“待执行 baseline / candidate 实测”进一步压成可直接开跑的记录入口，避免下次从头定义比较条件。

## Scenario

- benchmark_ref: [benchmark-05-multi-agent-decomposition.md](../benchmark-05-multi-agent-decomposition.md)
- current_status: prep_only

## Recommended Test Shape

- task_type:
  - 一个跨研究、实现、验证或整合的复杂任务
- baseline:
  - 单线程处理，不拆 agent
- candidate:
  - 按 `ai-native-loop` 多 Agent 规则进行拆分

## Required Evidence

- baseline 与 candidate 的输入形式
- 主 agent 是否保留总目标与验收标准
- 子 agent 最小输入包
- handoff artifact
- 最终整合结果
- `decomposition_quality` 判断

## Pass Bar

- `candidate` 不只是“更忙”，而是：
  - 整合质量更高，或
  - 上下文噪音更低，或
  - 主 agent 协调负担更低

如果这些都没有明显改善，则应判定“不值得拆”。

## Next Action

下一次真实执行时：

1. 直接复制 [benchmark-run-template.md](../benchmark-run-template.md)
2. 先跑 baseline
3. 再跑 candidate
4. 最后再写 `decomposition_quality`
