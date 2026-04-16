# Experience Compounding Loop

## Why This File Exists

经验沉淀如果只靠作者事后写长文，总会遇到两个问题：

- 只有作者本人会用
- 开源用户即使用过，也很难把经验低摩擦地贡献回来

因此当前目标不应是“一步到位全自动”，而应先建立一个本地可执行、默认可留痕的经验复利回路。

## The Real Goal

不是让每次任务都产出完整 case study。

真正目标是：

> 让一次任务结束后，至少留下足够结构化的本地 runtime 痕迹，以便下一次调用可以读取，并在后续判断它是否值得进入 pattern、failure mode、benchmark 或版本迭代。

## Two Layers

经验层现在明确分成两层：

### 1. Runtime Layer

默认宿主：

- `~/.codex/skills/ai-native-loop/runtime/`

负责：

- 每次 `medium+` 调用后的最小 capture
- 最近相关经验的轻量读取
- review queue
- promoted field notes

### 2. Repository Layer

默认宿主：

- 仓库中的 `docs/`、`patterns/`、`references/`

负责：

- 公开表达
- 可复用 pattern
- failure mode
- benchmark
- release / changelog 叙事

原则：

> 先在 runtime 层默认积累，再决定哪些经验值得进入 repo 层。

## Default Loop

经验复利默认按六步运行：

1. `read`
   调用开始前，按任务信号读取少量相关 runtime 经验。
2. `capture`
   用最小字段记录这轮任务。
3. `triage`
   判断它更像 pattern、failure mode，还是只是一次性样本。
4. `compress`
   把原始记录压成可复用结构，而不是保留成长叙述。
5. `validate`
   判断它是否足以进入 benchmark 或版本决策。
6. `promote`
   把通过筛选的经验提升到对应层级。

## Local Runtime Capture

在当前阶段，`capture` 的默认动作不是直接写完整 case study，而是：

1. 在主输出末尾保留一个最小 `Loop Recovery Block`
2. 把同结构内容写入本地 `runtime capture`

最小字段：

- `timestamp`
- `session_id`
- `scene`
- `objective`
- `initial_block`
- `intervention_level`
- `artifacts_produced`
- `what_worked`
- `remaining_risk`
- `next_input`
- `candidate_pattern_tags`
- `candidate_failure_tags`
- `promotion_hint`

## End-Of-Response Capture Rule

为了把经验沉淀从“作者记得做”变成“系统默认做”，当前阶段统一采用下面的结束规则：

- `light`：可选追加 `Loop Recovery Block`，默认不写 runtime capture
- `medium`：默认必须在主输出末尾追加 `Loop Recovery Block`，并写入 runtime capture
- `strong`：默认必须在主输出末尾追加 `Loop Recovery Block`，并写入 runtime capture，字段不要空转
- 如果没有尾部 recovery block，本轮只能算完成了任务推进，不能算完成了经验 capture
- 如果当前环境无法写入本地 runtime，必须明确说明“未完成 runtime capture”

## Retrieval Rule

默认不要全量读取经验层，只按当前任务信号按需加载：

- 最近相似 `scene`
- 最近命中的 `failure mode`
- 最近被验证有效的 `pattern`

默认读取预算：

- 最近 5 条 raw captures
- 最多 3 条 promoted field notes
- 最多 2 条 pattern / failure references

原则不是“经验越多越好”，而是“相关经验能被低成本取到”。

## Minimum Field Note

当某个 runtime capture 值得继续升级时，再扩成 field note。每次显著任务结束后，field note 最少应记录：

- `scene`
- `objective`
- `initial_block`
- `intervention_level`
- `artifacts_produced`
- `what_changed`
- `what_failed_or_remained_risky`
- `next_input`
- `source_runtime_capture`

没有 runtime capture 或 field note，后续几乎无法稳定提炼。

## Promotion Gate Checklist

看到 runtime capture 后，先用最小清单判断是否值得升级为 field note。

- 是否暴露了一个重复出现的失败模式？
- 是否形成了一个可迁移到其他任务的做法？
- 是否改变了后续的触发、分工或评估判断？
- 是否值得进入 benchmark、pattern 或 failure mode？

满足任意两项，再优先升级为 field note；否则先保留在 runtime 层。

## Promote To Pattern

满足以下任意两项时，优先考虑进入 pattern：

- 该做法可迁移到多个相似任务
- 成功关键不依赖特定领域知识
- 触发信号和动作边界很清楚
- 能明确说出“什么时候该用，什么时候不该用”

## Promote To Failure Mode

满足以下条件时，优先进入 failure mode：

- 本轮暴露的是重复出现的误判
- 根因可归因为结构问题，而不只是偶然失误
- 有明确纠偏动作可写入系统

## Promote To Benchmark

满足以下条件时，优先进入 benchmark：

- 这是一个高频、典型、可重复的任务场景
- 能明确写出通过标准
- 有稳定工件可以评分
- 可以关联到真实 runtime provenance

## Keep As Runtime Note

如果还看不出可迁移规律，就先保留在 runtime 层，不急着升级。

## Anti-Bloat Rules

经验复利的风险，不是经验太少，而是经验越来越多后失去压缩性。

如果没有治理规则，系统会很快退化成：

- runtime capture 越来越多但无人 review
- pattern 越来越重复
- failure mode 越来越碎
- benchmark 越来越像历史档案

所以当前阶段应默认遵守以下四条轻量治理规则。

### 1. Promotion Rule

不是每条经验都值得升级。

只有同时满足以下至少两项，才应从 runtime note / field note 升到更高层：

- 重复出现
- 明显可迁移
- 能改变未来判断
- 不只是当前案例的细节记录

### 2. Dedup Rule

新增经验前先问：

- 这是不是已有 pattern 的变体？
- 这是不是已有 failure mode 的一个新例子？
- 这是不是已有 benchmark 的局部补充？

如果答案是“是”，优先合并已有资产，而不是新建一个近似文件。

### 3. Load Rule

单次任务的默认加载必须越来越少。

runtime 层是默认宿主，不代表默认全读。

### 4. Archive Rule

当某条经验已经低价值、被更强版本覆盖，或长期没有被引用时，应考虑归档。

## Current Decision

当前仓库与安装副本都不需要引入重型数据库。

当前最合适的做法是：

- 用 `jsonl + json` 做 runtime capture 与轻索引
- 用 promoted field note 做中间层
- 继续沿用现有 pattern / failure mode / benchmark 结构
- 等到真实冗余明显出现后，再考虑更重的索引或自动化治理

## Example Promotion Chain

当前仓库已经有一条真实示范链：

- Field note: [field-note-01-decision-structuring-skincare.md](../docs/field-notes/field-note-01-decision-structuring-skincare.md)
- Pattern: [decision-structuring.md](../patterns/decision-structuring.md)
- Failure mode: [failure-modes.md](failure-modes.md)
- Benchmark: [benchmark-04-decision-structuring-skincare.md](../docs/benchmarks/benchmark-04-decision-structuring-skincare.md)

下一阶段的关键，不是再多写几条示范链，而是让类似链条可以先从本地 runtime 层稳定长出来。

## Automation Ladder

经验复利不追求一步全自动，而走五级阶梯：

### Level 1

手动记录 field note。

### Level 2

默认输出里自带 `Loop Recovery Block`。

### Level 3

默认写入本地 runtime capture。

### Level 4

批量 review runtime capture，按规则提升为 pattern / failure mode / benchmark。

### Level 5

把版本更新显式绑定到被验证的 failure mode、runtime evidence 和 benchmark 变化。

当前项目目标应先稳定做到 `Level 3` 与 `Level 4`。

## Non-Goals

当前阶段不追求：

- 全自动 pattern 提炼
- 全量历史资产回灌 runtime
- 重型数据库或复杂语义检索
- 只靠 runtime 就替代 benchmark 与 release judgment
