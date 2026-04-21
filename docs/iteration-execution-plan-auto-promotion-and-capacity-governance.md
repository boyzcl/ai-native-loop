# Auto Promotion And Capacity Governance Execution Plan

Date: `2026-04-21`

Based on:

- [auto-promotion-capacity-diagnosis-2026-04-21.md](auto-promotion-capacity-diagnosis-2026-04-21.md)

## Objective

把 `ai-native-loop` 从“自动 capture + 自动入队”的 runtime compounding 机制，推进到“本地自动晋升 + repo 严格门控 + 长期容量可治理”的受限复利系统。

## Current Status Update

截至 `2026-04-21`，本计划的主体实现已不再停留在设计阶段。

已经完成：

- `promotion_worker.py` 已能消费真实 `review queue`
- `promotion-policy.json`、`promotion-ledger.json`、`reuse-ledger.json` 已接入 runtime state
- 本地 `promote / merge / archive / repo candidate` 主链路已跑通
- retrieval 侧已能记录 promoted note reuse
- runtime 指标已能通过治理报表直接读取

当前不再是“是否应该开始实现”问题，而是“当前受限复利机制是否已经足够稳，可以支撑下一阶段判断”。

因此，后续优先级已切换为：

1. retrieval quality forward test
2. `repo candidate` review workflow
3. 更大 backlog / 更长周期压力验证

## Core Decision

本轮不追求：

- 全链路无门槛自动晋升
- 自动把 runtime 经验直接发布为 pattern / failure mode / benchmark

本轮追求：

1. 自动 triage `review queue`
2. 自动把高价值样本晋升到 `promoted field notes`
3. 自动做 dedup / merge / archive
4. 自动生成 `repo candidate`，但不直接自动落到 repo 公开资产

一句话版本：

> 本地自动、仓库门控、读取受限、增长有上限。

## Target State

完成本轮后，系统应达到以下状态：

1. `medium+` capture 默认继续写入 runtime
2. review queue 可被 promotion worker 周期消费
3. 高分样本自动形成或更新 `promoted field note`
4. 低价值样本可自动归档或保持 raw
5. repo candidate 自动生成，但 repo 资产仍需更强 gate
6. runtime 层拥有可观测的 backlog / merge / archive / reuse 指标

## Workstream A: Promotion Worker

### Goal

新增一个真正可运行的 promotion worker，而不是只保留文档规则。

### Deliverables

- `scripts/promotion_worker.py`
- `runtime/state/promotion-ledger.json`
- `runtime/state/promotion-policy.json` 或等价配置

### Responsibilities

promotion worker 至少要能做以下动作：

- 读取 `runtime/inbox/review-queue.json`
- 加载对应 capture
- 计算 promotion score
- 判断：
  - `keep_raw`
  - `promote_to_field_note`
  - `merge_into_existing_note`
  - `create_repo_candidate`
  - `archive`
- 更新 ledger 与 queue

### Minimum Scoring Inputs

- 重复出现信号
- pattern/failure tag 重合度
- `what_worked` / `remaining_risk` / `next_input` 是否足够具体
- 是否明显改变未来判断
- 是否具备 benchmark 潜力

## Workstream B: Capacity Governance

### Goal

把 anti-bloat 规则做成默认机制。

### Deliverables

- `runtime/promoted/archive/` 自动归档逻辑
- promoted note merge 规则
- 工作集上限配置
- 冷热分层说明文档

### Required Policies

#### 1. Pending Backlog Threshold

当 `review queue` 超过阈值时：

- 自动触发 promotion worker 批量 triage

建议初始阈值：

- `pending_count >= 10`

#### 2. Promoted Working-Set Ceiling

promoted field notes 不应无限增长。

建议初始规则：

- 默认工作集上限：`20`
- 超过后优先 merge / archive，而不是继续新建

#### 3. Archive Rule

满足任一条件应优先进入 archive：

- 长期未被读取
- 已被更强版本覆盖
- 与更高质量 note 高度重复
- 只是一次性局部细节

#### 4. Dedup First Rule

所有自动晋升都要先尝试：

1. merge
2. update
3. create

## Workstream C: Repo Candidate Gate

### Goal

把 repo 层从“自动膨胀风险区”变成“严格受控资产层”。

### Deliverables

- `runtime/promoted/repo-candidates/`
- `scripts/evaluate_repo_candidate.py` 或并入 promotion worker

### Repo Candidate Gate

进入 repo candidate 至少满足以下条件中的两项：

- 7 天内重复出现
- 至少一次真实 reuse 被记录
- 已能回答 pattern intake 三项核心问题
- 可明确进入 benchmark 或版本叙事

### Important Boundary

repo candidate 不等于 repo asset。

它只是：

- 待验证
- 待合并
- 待人工或半自动复审

## Workstream D: Reuse And Observability

### Goal

让系统不只知道“写了多少经验”，还知道“哪些经验真的被下次用到”。

### Deliverables

- `runtime/state/reuse-ledger.json`
- retrieval 侧的 note hit 记录
- runtime 指标面板文档

### Required Metrics

已有：

- `capture_write_rate`
- `capture_to_review_rate`
- `review_to_promote_rate`
- `promotion_to_repo_rate`

新增：

- `pending_backlog_size`
- `promoted_note_count`
- `promoted_note_reuse_rate`
- `dedup_merge_rate`
- `archive_rate`
- `repo_candidate_accept_rate`

## Workstream E: Retrieval Budget Protection

### Goal

保证系统知识增长后，下一次调用仍然轻量。

### Required Rules

- raw capture 默认最多读最近 5 条
- promoted field notes 默认最多读 3 条
- pattern / failure references 默认最多读 2 条
- promotion worker 必须输出“读取友好”的压缩知识，而不是只复制原始记录

### Validation Question

每次新增 promoted note 都要反问：

> 它会让下一次调用更轻，还是更重？

如果答案偏向“更重”，优先 merge 或 archive。

## Implementation Order

### Phase 1

- 建 `promotion_worker.py`
- 建 promotion ledger
- 支持自动 `keep_raw / promote / merge / archive`

### Phase 2

- 建 `repo-candidate` 层
- 加入更强 gate
- 建 reuse ledger

### Phase 3

- 建指标与阈值驱动的批量 triage
- 验证 backlog 不再线性积压

## Validation Plan

最小验证不看“代码写完没”，而看三件事：

1. 当前 backlog 跑一轮后，pending 数量明显下降
2. promoted note 数量增长受控，没有无脑暴增
3. 下一次调用能读到刚晋升的知识，而不是继续只读 raw capture

## Risks

### Risk 1

Promotion score 太宽，导致大量低价值 note 晋升。

控制方式：

- 初期把阈值设高
- 默认优先 merge
- 把 repo candidate gate 设得更严

### Risk 2

系统知识层越跑越重，调用效率下降。

控制方式：

- 强制工作集上限
- 建 archive
- 严格执行读取预算

### Risk 3

自动化掩盖错误固化。

控制方式：

- 保留 ledger
- 保留 repo 层 review 门
- 跟踪 reuse 与 accept rate

## Completion Criteria

本轮达到以下条件，可判断为真正开始满足“自动晋升需求”：

1. promotion worker 可以消费 review queue
2. 至少 1 批 pending capture 被自动 triage
3. 至少 1 条 capture 被自动提升为 promoted field note
4. 至少 1 条近似样本被自动 merge，而不是新建重复 note
5. 至少 1 条低价值样本被自动 archive
6. 至少 1 条 promoted note 在后续调用中被真实读取
7. repo 层没有被直接自动污染

## Final Judgment

这一轮的任务，不是造一个“自动长知识”的幻觉系统。

这一轮的任务是：

> 造一个“会自动筛、会自动压、会自动丢、会自动给出候选”的受限复利系统。

只有这样，`ai-native-loop` 才能在长期运行后继续保持：

- 轻
- 准
- 可复用
- 可更新
- 可验证
