# Auto Promotion Governance Validation

Date: `2026-04-21`

Scope:

- `repo candidate review workflow`
- retrieval quality forward test
- larger backlog / longer-cycle stress validation

## Diagnosis Card

- 当前循环位置：
  - `feedback -> re-input`
- 本轮主风险：
  - retrieval 假阳性会污染 reuse evidence
  - repo candidate 若只靠“重复出现”会在压力回放里膨胀
  - review workflow 若没有真实状态流转，`repo_candidate_accept_rate` 只是空指标
- 介入等级：
  - `strong`

## Task Packet

- 目标：
  - 把本地自动晋升、容量治理、reuse 观测与 repo candidate gate 推进到“已验证、可 review、可继续收紧”的下一阶段
- 权威输入：
  - `project-status-memo-auto-promotion-governance-2026-04-21.md`
  - `release-manifest.md`
  - `iteration-execution-plan-auto-promotion-and-capacity-governance.md`
  - `runtime-memory-spec.md`
  - `runtime-promotion-policy.md`
- 成功信号：
  - review workflow 有真实 `pending / accepted / rejected`
  - retrieval forward test 有真实 baseline / tightened 对比
  - stress replay 下 promoted working set、candidate count、reuse evidence 仍受控

## Repo Candidate Review Result

先在 live runtime 上执行 `promotion_worker.py --limit 0` 进行 tightened gate reconcile：

- 自动撤回 3 个过宽 candidate
- live runtime `repo_candidate_count` 从 `6` 收到 `3`

随后执行显式 review：

- `accepted`
  - `implement-local-auto-promotion-worker-with-bounded-repo-candidate-gate-a`
  - 目标：`pattern`
- `pending`
  - `design-automatic-promotion-architecture-with-capacity-governance-for-lon`
  - 原因：仍需用 post-validation evidence 重写，避免 pre-implementation framing 直接进入 repo drafting
- `rejected`
  - `document-auto-promotion-diagnosis-and-execution-plan-for-bounded-long-te`
  - 原因：仍然更适合作为 runtime authority，而不是 repo drafting asset

live runtime review 后指标：

- `repo_candidate_count = 2`
- `repo_candidate_pending_count = 1`
- `repo_candidate_accepted_count = 1`
- `repo_candidate_rejected_count = 1`
- `repo_candidate_accept_rate = 0.3333`

## Retrieval Forward Test

运行：

```bash
python3 scripts/retrieval_forward_test.py
```

测试集：

- `docs/benchmarks/runtime-retrieval-forward-test-cases.json`
- 共 `7` 个真实 query

baseline 结果：

- `top1_hit_rate = 1.0`
- `top3_hit_rate = 1.0`
- `false_positive_case_rate = 0.1429`
- 典型假阳性：`host aware runtime root ...` 会把 `repo-closeout-git-push` 带进结果

本轮收紧：

- retrieval 不再直接读取整份 field note 正文，而是剔除：
  - `Source Runtime Captures`
  - `Merge History`
  - 绝对路径噪音
- 改为 title-weighted、IDF-like token overlap
- 只保留靠近 top score 的高置信命中

当前结果：

- `top1_hit_rate = 1.0`
- `top3_hit_rate = 1.0`
- `false_positive_case_rate = 0.0`
- `false_negative_case_rate = 0.0`

当前判断：

- heuristic 已明显变稳，不需要立刻继续收紧
- 但这仍然不是语义检索，只是更保守的 lexical heuristic

剩余风险：

- query 语义改写幅度很大时，仍可能出现 false negative
- 当前 forward test 仍偏向本项目治理语料，跨域 query 还需要更多样本

## Stress Validation

运行：

```bash
python3 scripts/runtime_governance_stress_test.py --replay-multiplier 3 --reuse-passes 3
```

方法：

- 用当前 live runtime 作为种子
- 在 temp runtime 回放 `93` 条 replayed captures
- 再做 `3` 轮 retrieval reuse replay
- 不污染主 runtime reuse ledger

结果：

- `seed_capture_count = 31`
- `reviewed_count = 113`
- `promoted_note_count = 20`
- `archived_note_count = 13`
- `repo_candidate_count = 4`
- `archive_rate = 0.0973`
- `merge_rate = 0.6637`
- `promoted_note_reuse_rate = 0.45`

稳定性判断：

- `promoted_working_set_controlled = true`
- `archive_rate_reasonable = true`
- `merge_rate_reasonable = true`
- `repo_candidate_bounded = true`
- `reuse_evidence_trustworthy_enough = true`

## Policy Change

这轮确认“重复出现”本身不足以支撑 repo candidate gate。

因此本轮新增并落地：

- `repo_candidate_min_source_sessions = 2`
- 没有真实 reuse 时，必须同时满足：
  - `source_session_ready`
  - `benchmark_or_release_ready`
- 先 tighten gate，再做 review，而不是先扩更多自动化 breadth

## Current Judgment

更准确的阶段判断是：

> `ai-native-loop` 已进入“本地自动晋升 + 容量治理 + 受控 retrieval + repo candidate review”阶段，但仍不能把这说成长期稳定自治已经成立。

当前可说成立的是：

- review workflow 已接上
- retrieval heuristic 已做过前向验证并完成一次保守收紧
- backlog / longer-cycle replay 下，关键阈值在 temp runtime 中保持受控

当前仍不能过度承诺的是：

- 长周期真实世界语义检索稳定性
- repo-layer 公开资产自动化
- 长期自治已经无需人工 review
