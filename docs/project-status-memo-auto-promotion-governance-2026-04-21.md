# Project Status Memo: Auto Promotion Governance

Date: `2026-04-21`

Scope: 基于当前仓库实现、当前 `Codex` runtime 状态与最近一轮 auto-promotion / reuse / repo-candidate 验证结果，对 `ai-native-loop` 当前所处阶段、真正剩余缺口与下一决策做一次正式收束。

> Note
>
> 这份 memo 是 `2026-04-21` 的阶段性判断。版本真相与发布状态仍以 [release-manifest.md](release-manifest.md) 为准。

## Executive Summary

截至 `2026-04-21`，`ai-native-loop` 已经不再停留在“自动 capture + 自动入队”的阶段，而是已经进入：

> 本地自动晋升 + 容量治理 + reuse 观测 + repo candidate 受控门槛

这意味着系统的主矛盾已经再次变化。

上一阶段的主矛盾是：

- experience 会不会蒸发
- backlog 会不会一直堆
- repo 层会不会被误做成自动发布层

当前阶段的主矛盾变成了：

- retrieval 命中是否足够准，能不能支撑可信 reuse evidence
- repo candidate gate 是否足够稳，不会因一次偶发命中而过宽
- 当前阈值是否已经过了“首轮样本有效”，还是仍需要更大规模和更长周期的压力验证

一句话：

> 系统已经从“能自动留痕”进入“能受限复利”，但还没有到“可以过度承诺长期稳定自治”。

## Current Facts

当前可直接确认的仓库与 runtime 事实：

- `scripts/promotion_worker.py` 已存在并可真实消费 `review queue`
- `runtime/state/promotion-policy.json`、`promotion-ledger.json`、`reuse-ledger.json` 已存在
- `scripts/read_runtime_context.py` 已支持 `--include-promoted --record-reuse`
- `scripts/runtime_governance_report.py` 已能输出 backlog / promote / merge / archive / reuse / repo candidate 指标
- `scripts/set_repo_candidate_status.py` 已提供 `pending / accepted / rejected` 状态入口，但不会自动改 repo 公开资产
- archive policy 已收紧，去掉了会误伤高价值判断的 `one-off` 与通用 `sample` 关键词

当前 `Codex` runtime 指标：

- `pending_backlog_size = 0`
- `reviewed_count = 20`
- `promoted_note_count = 16`
- `archived_note_count = 2`
- `repo_candidate_count = 6`
- `reuse_event_count = 12`
- `promoted_note_reuse_rate = 0.5`
- `repo_candidate_accept_rate = 0.0`

这说明：

- backlog 已从线性积压转为可被 worker 默认清空
- promoted 层已经形成受控工作集，而不是无上限膨胀
- reuse 已不再只是口头概念，而是进入 runtime state
- repo candidate 仍是受控候选层，不是自动发布层

## Diagnosis Card

- 当前循环位置：
  - 主要处于 `反馈 -> 再输入` 阶段。
  - 上一轮实现已经把 promotion 主链路接通，这一轮更需要判断“哪些学习应该冻结为下一阶段 authority”。

- 当前真正瓶颈：
  - 已不再是“有没有 promotion worker”，而是“当前 reuse evidence 与 candidate gate 是否足够稳，足以支撑下一阶段判断”。

- 为什么用 `strong` 介入：
  - 因为这里不只是记录进度，而是要决定系统是否该继续扩自动化、还是该先转向验证与 review workflow。
  - 决策如果错，会直接导致 repo candidate 过宽、误读 reuse、或者过早宣称长期自治成立。

- 当前最重要的边界判断：
  - 不能把“本地自动晋升已经跑通”误说成“repo 层自动复利已经成立”。
  - 不能把“reuse 开始被记录”误说成“长期 reuse 规律已经被验证”。
  - 不能再继续宽方向扩功能，而应优先加固 retrieval 质量、repo candidate review 与压力验证。

## Task Packet

- 本轮目标：
  - 用 `ai-native-loop` 视角正式评估当前阶段，决定下一阶段该做什么、为什么做、做到什么算过关，并把这些判断同步进仓库文档。

- 当前状态：
  - 本地 auto-promotion 已跑通
  - capacity governance 已接通
  - reuse ledger 已接通
  - repo candidate gate 已存在，但仍在首轮真实样本阶段

- 约束：
  - 不把 repo candidate 等同于 repo asset
  - 不因为首轮样本跑通就过度升级版本承诺
  - 更新文档时必须反映真实 runtime 数据，而不是停留在前一阶段 memo

- 成功信号：
  - 仓库里有一份反映今天真实状态的新 memo
  - `release-manifest.md` 不再停留在前一阶段判断
  - 下一阶段优先级被收敛成少数高杠杆动作，而不是继续散扩

- 下一检查点：
  - 是否形成可执行的 repo candidate review workflow
  - retrieval 命中是否在更多真实场景下仍保持高相关
  - 更大 backlog / 更长周期下，当前阈值是否仍能维持低膨胀与低误晋升

## Feedback Attribution Card

当前系统给出的主要反馈不是“代码坏了”，而是三类结构反馈：

### 1. 正向反馈

- promotion worker 已经把“自动 intake”推进成“自动本地晋升”
- archive / dedup / ceiling 不再只是文档规则，而是默认机制
- reuse ledger 已经使“是否真的被下一轮用到”开始可观测

### 2. 负向反馈

- retrieval ranking 仍是启发式，虽然已经比纯 recency 更好，但还不是高置信语义匹配
- repo candidate gate 需要更长周期和更多真实命中来避免偶发样本放大
- archive heuristic 仍有 literal-keyword 风险，本轮就暴露出 `sample` 会误伤“大样本压力测试”类高价值判断
- `repo_candidate_accept_rate` 目前仍为 `0.0`，说明 review workflow 还没有真正跑起来

### 3. 最关键的学习

- 这轮最有价值的不是“又多了几个脚本”，而是发现系统的风险已经从“没有自动化”切到“自动化后的判断是否足够稳”。
- 换句话说，下一轮再继续扩功能，杠杆已经变低；真正高杠杆的是把当前闭环的验证与 review 接牢。

## Re-input Packet

下一阶段不建议继续优先扩写新的自动化分支，而建议收敛为三个连续动作。

### Decision 1

先补 `repo candidate review workflow`，而不是继续扩 promotion breadth。

原因：

- 当前候选层已经存在，但 acceptance 还没有真实流转
- 没有 review workflow，`repo_candidate_accept_rate` 永远只是空指标

最小交付：

- 一份 repo candidate review protocol 文档
- 明确 `pending / accepted / rejected` 的判断标准
- 至少一次真实 candidate review 样本

### Decision 2

把 retrieval quality 当作下一轮最高优先级验证面。

原因：

- reuse ledger 的可信度高度依赖 retrieval 命中质量
- 如果 retrieval 命中不稳，后续 reuse evidence 和 repo candidate gate 都会被污染

最小交付：

- 一个 retrieval forward test / false-positive test
- 至少 3 到 5 个场景的命中质量记录
- 对当前 ranking heuristic 的一次收紧或明确保守边界

### Decision 3

做一次更大 backlog 的压力验证，而不是立刻推进版本发布。

原因：

- 当前阈值是在首轮真实样本上成立
- “长期稳定自治”的说法只有在更大样本、更长周期下仍稳时才成立

最小交付：

- 一次模拟或回放式更大 backlog run
- 观察 promoted working set、archive rate、merge rate、candidate count 是否仍受控

## Current Judgment

当前最合理的阶段判断是：

- 不再把项目描述为“刚接通 runtime compounding”
- 也不把项目描述为“已经达到长期稳定自治”
- 更准确的表述应是：

> `ai-native-loop` 已进入“本地自动晋升 + 有容量治理的受限复利”阶段，下一步应从自动化扩面切换到验证加固与 repo candidate review workflow。

## Recommended Next Move

如果下一轮继续推进，建议直接用下面这个任务包开工：

1. 设计并落地 `repo candidate review workflow`
2. 跑 retrieval quality forward test，并记录 false positive / false negative
3. 用更大 backlog 做一次压力验证，决定是否需要再次收紧阈值

不建议下一轮优先做的事：

- 直接自动把 repo candidate 升为 repo asset
- 继续新增更多自动化类别而不补验证
- 在没有更长周期样本前宣称“长期稳定自治”已经成立
