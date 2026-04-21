# Runtime Promotion Policy

## Purpose

这份文档定义 runtime 经验如何从默认留痕进入更高层系统资产。

## Promotion Ladder

运行时经验默认按四级流转：

1. `raw capture`
   - 只保留在 `runtime/captures/`
2. `reviewed note`
   - 被加入 `runtime/inbox/review-queue.json`
3. `promoted field note`
   - 升级到 `runtime/promoted/field-notes/`
4. `repo candidate`
   - 值得反哺仓库的 pattern / failure mode / benchmark / release docs

## Promotion Gate

只有同时满足以下至少两项，才应该进入 `repo candidate`：

- 7 天内重复出现
- 已能明确抽成 pattern 或 failure mode
- 明显改变下一次任务判断
- 能进入 benchmark 或版本叙事

否则默认停留在 runtime 层。

第一版 worker 里，这个 gate 被工程化为：

- 默认先满足本地 promotion score
- 再检查重复出现、明确可抽象、下一轮判断影响、benchmark / release relevance
- 默认不再让“重复出现”单独构成 repo candidate 充分条件
- `reuse` 初始门槛保持 `>= 2` 次命中，避免一次偶发读取就把 note 推成 repo candidate
- 如果没有真实 reuse，则至少还要满足：
  - `source_session_ready`
  - `benchmark_or_release_ready`
- `source_session_ready` 第一版默认要求 `source_session_count >= 2` 或已发生 merge
- 命中 archive / smoke / sample 等低价值关键词时，直接阻断 repo candidate
- repo candidate 只落在 `runtime/promoted/repo-candidates/`，不自动改 repo 公开资产
- repo candidate 默认带 `pending` review 状态，可被显式标记为 `accepted / rejected`，但这仍然不等于自动发布 repo 资产

## Dedup Rule

进入 repo 前先问：

- 这是不是已有 pattern 的变体？
- 这是不是已有 failure mode 的一个新例子？
- 这是不是已有 benchmark 的局部补充？

默认顺序：

1. 优先合并
2. 其次更新
3. 最后才新增

第一版实现把 `merge_similarity_threshold` 和更高的 `dedup_similarity_threshold` 分开：

- 强匹配先 merge
- 软匹配只在样本不够强、不值得新建 note 时 merge
- 避免把 repo-candidate gate 误用成 field-note 膨胀器

## Archive Rule

满足任一情况可进入 archive：

- 已被更强版本覆盖
- 长期无人引用
- 只是一次性细节记录

第一版默认还会把带有 `smoke test`、`bootstrap`、`cli sample` 等明显 bootstrap / demo 关键词的低价值样本优先归档，避免 bootstrap 噪音占用 promoted working set。

这里去掉了过宽的 `one-off` 与通用 `sample` 关键词，因为它们都会误伤高价值治理样本，只要正文里提到“一次性误判”或“大样本压力测试”之类描述，就可能被错误归档。

## Capacity Governance

本轮把容量规则从文档声明推进到默认机制：

- `pending backlog threshold`: 默认 `>= 10` 时 worker 会批量消费 pending
- `promoted working-set ceiling`: 默认 `20`
- `archive` 不再是事后清理，而是 promotion 流程内动作
- `repo candidate` 可以被 reconcile 收紧，不符合门槛时自动撤回
- `reuse ledger` 会记录 retrieval 命中，并反哺 repo candidate gate
- `2026-04-21` 的 stress replay 证明 tightening 前的 candidate gate 过宽，因此新增 `repo_candidate_min_source_sessions = 2`

## Runtime / Repo Boundary

runtime 层负责：

- 默认积累
- 下一次调用读取
- 低摩擦 review

repo 层负责：

- 公共表达
- 可复用资产
- 验证
- 版本叙事

一句话：

> runtime 负责让经验留下来，repo 负责让经验被公开复用和证明。

## Review Workflow

`repo candidate` 进入 review 后，默认只允许三种状态：

- `pending`
  - 继续保留候选，但不进入 repo drafting
- `accepted`
  - 允许进入 repo drafting backlog，但仍不自动改 repo 公共资产
- `rejected`
  - 退回 runtime-only，保留本地经验价值

权威流程见：

- [repo-candidate-review-workflow.md](repo-candidate-review-workflow.md)
