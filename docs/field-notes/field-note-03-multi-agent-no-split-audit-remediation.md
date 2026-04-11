# Field Note: Multi-Agent Decomposition / No-Split On Audit Remediation

## Scene

- 多 Agent 拆分决策
- Skill 仓库结构修复

## Objective

- 判断“审计修复”这类任务当前轮是否适合拆分为多个 agent

## Initial Block

- 任务包含版本单源、评估文档、README、经验回收与 benchmark 迁移多条线
- 但这些任务在当前轮高度耦合，且优先级和文案边界需要持续同步
- 如果过早拆分，最可能出现的是局部文档优化后又互相打架

## Intervention Level

- `strong`
- 原因：不是因为任务特别大，而是因为在决定是否拆分前，必须先澄清边界与整合成本

## Core Artifacts Produced

- `Diagnosis Card`
- 总任务 `Task Packet`
- no-split judgment
- `Loop Recovery Block`

## What Changed

- 没有为了并行而并行
- 明确判定：当前轮保持单线程，比仓促拆分更稳
- 把“什么时候不该拆”从规则文本落实到真实任务决策

## What Worked

- `parallelizable / bounded / integrable / worth_it` 四问有效阻止了无效拆分
- 主 agent 保留统一版本真相和文档收口责任后，修改链路更稳定

## What Failed Or Remained Risky

- 这条证据只能证明“规则帮助做出 no-split 判断”
- 还不能证明“按规则拆分后一定有效”
- multi-agent 的 live split case 仍需后续补齐

## Re-input

- 保留：先判断拆不拆，而不是默认拆
- 丢弃：把多 Agent 当成默认更高级做法
- 下一轮应补：
  - 一个真的值得拆的复杂任务
  - baseline 单线程 vs candidate 多 Agent 的直接对照

## Promotion Hint

- `pattern`
  - 可作为 `multi-agent-decomposition` 的真实反例证据
- `failure_mode`
  - 对应“为了显得高级而拆”的失败边界
