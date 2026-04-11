# Pattern Library

## Purpose

这个目录不是案例展示区，而是经验沉淀层。

每个 pattern 都应该把一个真实案例压缩为可迁移结构，而不是保留成叙事摘要。

## Pattern Format

每个文件默认回答六个问题：

- `scene`
  这类任务通常发生在什么场景。
- `trigger`
  什么信号说明应该触发该模式。
- `intervention`
  适合的介入等级与动作。
- `artifacts`
  应优先产出哪些工件。
- `common_failure`
  最容易出现什么失败。
- `transfer_rule`
  这个模式如何迁移到别的知识工作。

## Current Patterns

- `self-bootstrap.md`
  用于“系统评估自己、修补自己、发布自己”的自举型任务。
- `research-to-report.md`
  用于“研究调查 -> 中间沉淀 -> 最终成稿”的研究写作任务。
- `decision-structuring.md`
  用于“研究或信息已经很多，但还不能直接支持选择”的决策型任务。
- `multi-agent-decomposition.md`
  用于“一个复杂任务需要判断是否拆 agent，以及拆分后如何回收”的分治型任务。

## Intake Utilities

- `pattern-intake-template.md`
  把 field note 压成 pattern 前的统一筛选模板。

## Authoring Rule

新增 pattern 时，不写成案例复述。优先写：

- 什么时候该触发
- 应该出哪几张卡
- 最容易错在哪
- 能迁移到什么场景
