# Experience Compounding Loop

## Why This File Exists

经验沉淀如果只靠作者事后写长文，总会遇到两个问题：

- 只有作者本人会用
- 开源用户即使用过，也很难把经验低摩擦地贡献回来

因此目标不应是“一步到位全自动”，而应先建立一个默认可执行的经验复利回路。

## The Real Goal

不是让每次任务都产出完整 case study。

真正目标是：

> 让一次任务结束后，至少留下足够结构化的痕迹，以便后续判断它是否值得进入 pattern、failure mode、benchmark 或版本迭代。

## Default Loop

经验复利默认按五步运行：

1. `capture`
   用最小字段记录这轮任务。
2. `triage`
   判断它更像 pattern、failure mode，还是只是一次性样本。
3. `compress`
   把原始记录压成可复用结构，而不是保留成长叙述。
4. `validate`
   判断它是否足以进入 benchmark 或版本决策。
5. `promote`
   把通过筛选的经验提升到对应层级。

## Minimum Field Note

每次显著任务结束后，最少应记录：

- `scene`
  任务发生在什么场景。
- `objective`
  本轮目标是什么。
- `initial_block`
  一开始卡在哪里。
- `intervention_level`
  使用了轻 / 中 / 强中的哪一级。
- `artifacts_produced`
  实际产出了哪些工件。
- `what_changed`
  相比原始请求，最关键的结构变化是什么。
- `what_failed_or_remained_risky`
  哪些问题仍未解决或暴露了风险。
- `next_input`
  下一轮输入被改写成什么。

没有这些字段，后续几乎无法稳定提炼。

## Triage Rules

记录完 field note 后，按下面规则分流。

### Promote To Pattern

满足以下任意两项时，优先考虑进入 pattern：

- 该做法可迁移到多个相似任务
- 成功关键不依赖特定领域知识
- 触发信号和动作边界很清楚
- 能明确说出“什么时候该用，什么时候不该用”

### Promote To Failure Mode

满足以下条件时，优先进入 failure mode：

- 本轮暴露的是重复出现的误判
- 根因可归因为结构问题，而不只是偶然失误
- 有明确纠偏动作可写入系统

### Promote To Benchmark

满足以下条件时，优先进入 benchmark：

- 这是一个高频、典型、可重复的任务场景
- 能明确写出通过标准
- 有稳定工件可以评分

### Keep As Raw Note

如果还看不出可迁移规律，就先保留为 field note，不急着升级。

## Example Promotion Chain

当前仓库已经有一条真实示范链：

- Field note: [field-note-01-decision-structuring-skincare.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/field-notes/field-note-01-decision-structuring-skincare.md)
- Pattern: [decision-structuring.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/patterns/decision-structuring.md)
- Failure mode: [failure-modes.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/failure-modes.md)
- Benchmark: [benchmark-04-decision-structuring-skincare.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-04-decision-structuring-skincare.md)

它演示的是：

- 一次真实任务如何先被记录成最小回收物
- 再被提升为可迁移 pattern
- 再沉淀为 failure mode
- 最后进入固定 benchmark 资产

## Automation Ladder

经验复利不追求一步全自动，而走四级阶梯：

### Level 1

手动记录 field note。

### Level 2

默认输出里自带“回收字段”。

### Level 3

批量 review field note，按规则提升为 pattern / failure mode / benchmark。

### Level 4

把版本更新显式绑定到被验证的 failure mode 和 benchmark 变化。

当前项目目标应先稳定做到 `Level 2` 与 `Level 3`。

## What The Skill Should Eventually Do By Default

对中介入以上任务，Skill 最终应默认保留一段最小回收物：

- 本轮卡点
- 采取了什么介入
- 哪张工件真正起作用
- 哪个风险仍存在
- 下一轮该怎么改写

这不是额外负担，而是经验复利的最低成本入口。

## Non-Goals

当前阶段不追求：

- 自动生成完整 case study
- 自动判断所有沉淀层级
- 没有人工审核就直接改写 benchmark 或 changelog

先把 intake 做稳，比追求全自动更重要。
