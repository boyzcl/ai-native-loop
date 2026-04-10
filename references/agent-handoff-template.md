# Agent Handoff Template

## 用途

当任务需要多 agent、多角色或人机多段协作时，用这份模板定义交接物，避免重复劳动和上下游脱节。

## 模板

```md
## shared-objective
- 共同目标：

## agent-or-role
- 角色名称：

## owned-scope
- 该角色负责的边界：

## inputs-received
- 上游交付给它的材料：

## output-contract
- 它必须返回的内容形状：

## done-criteria
- 什么条件下算完成：

## dependencies
- 它依赖谁、谁依赖它：

## risk-notes
- 当前最可能的交接风险：

## return-format
- 返回时的固定格式：结论 / 证据 / 未决问题 / 建议下一步
```

## 使用原则

- 每个角色只拥有一段清晰责任边界。
- 交接物必须可检查，不要只写“继续推进”。
- 返回格式统一，才能让多轮汇总不失真。
