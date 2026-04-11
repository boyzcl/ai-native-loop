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

在当前阶段，`capture` 的默认动作不是直接写完整 case study，而是先留下一个最小 `Loop Recovery Block`。

## Loop Recovery Block

对 `medium` 及以上任务，默认先保留：

- `scene`
- `initial_block`
- `artifacts_produced`
- `what_worked`
- `remaining_risk`
- `next_input`

这个回收块的目标不是完整复盘，而是保证后续还看得见这轮真正发生了什么。

## Minimum Field Note

当某个 recovery block 值得继续升级时，再扩成 field note。每次显著任务结束后，field note 最少应记录：

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

没有 recovery block 或 field note，后续几乎无法稳定提炼。

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

## Anti-Bloat Rules

经验复利的风险，不是经验太少，而是经验越来越多后失去压缩性。

如果没有治理规则，系统会很快退化成：

- field note 越来越多
- pattern 越来越重复
- failure mode 越来越碎
- benchmark 越来越像历史档案

所以当前阶段应默认遵守以下四条轻量治理规则。

### 1. Promotion Rule

不是每条经验都值得升级。

只有同时满足以下至少两项，才应从 raw note / field note 升到更高层：

- 重复出现
- 明显可迁移
- 能改变未来判断
- 不只是当前案例的细节记录

如果达不到，就停留在较低层，不要为了“看起来丰富”而升级。

### 2. Dedup Rule

新增经验前先问：

- 这是不是已有 pattern 的变体？
- 这是不是已有 failure mode 的一个新例子？
- 这是不是已有 benchmark 的局部补充？

如果答案是“是”，优先合并已有资产，而不是新建一个近似文件。

默认原则：

- 优先合并
- 其次更新
- 最后才新增

### 3. Load Rule

经验资产可以越来越多，但单次任务的默认加载必须越来越少。

默认不要全量读取经验层，只按当前任务信号按需加载：

- 触发判断问题：读 trigger docs
- 多 Agent 拆分问题：读 multi-agent rules
- 失败归因问题：读 failure modes
- 验证问题：读 benchmark / rubric

原则不是“经验越多越好”，而是“相关经验能被低成本取到”。

### 4. Archive Rule

当某条经验已经低价值、被更强版本覆盖，或长期没有被引用时，应考虑降级或归档。

可接受的动作包括：

- pattern 合并后删除旧变体
- benchmark 迁移到 archive / historical 状态
- field note 保留，但不再作为主动加载入口

不要让主经验层无限膨胀。

## Current Decision

当前仓库不需要为经验治理引入重型系统。

当前最合适的做法是：

- 先把升级、去重、加载、归档规则写死
- 继续沿用现有 field note / pattern / failure mode / benchmark 结构
- 等到真实冗余明显出现后，再考虑更重的索引或自动化治理

也就是说：

> 现在优先补“经验治理规则层”，而不是“经验管理基础设施层”。

## Example Promotion Chain

当前仓库已经有一条真实示范链：

- Field note: [field-note-01-decision-structuring-skincare.md](../docs/field-notes/field-note-01-decision-structuring-skincare.md)
- Pattern: [decision-structuring.md](../patterns/decision-structuring.md)
- Failure mode: [failure-modes.md](failure-modes.md)
- Benchmark: [benchmark-04-decision-structuring-skincare.md](../docs/benchmarks/benchmark-04-decision-structuring-skincare.md)

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

默认输出里自带 `Loop Recovery Block`。

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
