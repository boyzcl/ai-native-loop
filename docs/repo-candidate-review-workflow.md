# Repo Candidate Review Workflow

Updated: `2026-04-21`

## Purpose

这份流程定义 `runtime/promoted/repo-candidates/` 如何进入显式 review，而不是把 repo candidate 误当成 repo 公开资产自动发布。

一句话：

> repo candidate 只是“可被 review 的候选层”，不是 repo asset。

## Review Boundary

- `accepted`
  - 仅表示“允许进入 repo-layer drafting backlog”
  - 不会自动改写 `patterns/`、`references/`、`benchmarks/`、release docs 或任何 repo 公共资产
- `pending`
  - 表示自动 gate 已通过，但 repo 层目标、证据或表达仍不足
- `rejected`
  - 表示保留为 runtime 本地经验，不进入 repo drafting backlog

## Decision Criteria

### `pending`

满足以下情况之一时保持 `pending`：

- note 已通过自动 gate，但还缺更清晰的 repo target
- reuse 已出现，但仍停留在 pre-validation framing
- note 值得保留为 repo candidate，却还不该进入 repo drafting

### `accepted`

只有在以下条件成立时才应 `accepted`：

- note 仍然只是 repo candidate，不触发任何自动发布
- `pattern intake` 结构完整：`What Worked / What Failed Or Remained Risky / Re-input`
- 且满足以下至少一条：
  - 已记录真实 reuse，且内容已具有明确 repo-pattern / benchmark / release drafting 价值
  - 多 source / merge 后仍稳定成立，并具备明确 benchmark / release relevance

### `rejected`

满足以下任一情况应 `rejected`：

- note 更适合作为 runtime 本地 authority，而不是 repo 公共资产草稿
- note 过于 session-specific、项目私有或 handoff-specific
- tightened gate 已经不再支持它继续留在 candidate 层
- review 认为它仍然有价值，但价值只属于 runtime 层

## Operating Steps

1. 用 `scripts/review_repo_candidates.py` 列出当前 candidate 与推荐状态
2. 用 `scripts/promotion_worker.py --limit 0` 先 reconcile tightened gate，清掉明显过宽候选
3. 对剩余 candidate 做显式 review：
   - `accepted` 时写 `target_kind`
   - `pending` 时写清继续等待什么证据
   - `rejected` 时写清为什么留在 runtime-only
4. review 结果写入：
   - `runtime/state/promotion-ledger.json`
   - 对应 candidate markdown 的 `## Review Status`

## Commands

列出当前候选：

```bash
python3 scripts/review_repo_candidates.py
```

把一个 candidate 标记为 `accepted`：

```bash
python3 scripts/review_repo_candidates.py \
  --slug implement-local-auto-promotion-worker-with-bounded-repo-candidate-gate-a \
  --status accepted \
  --target-kind pattern \
  --reason "validated implementation note with reuse evidence and direct repo-pattern value"
```

## Current Sample

`2026-04-21` 这轮真实 review 样本：

- `implement-local-auto-promotion-worker-with-bounded-repo-candidate-gate-a`
  - `accepted`
- `design-automatic-promotion-architecture-with-capacity-governance-for-lon`
  - `pending`
- `document-auto-promotion-diagnosis-and-execution-plan-for-bounded-long-te`
  - `rejected`

另有 3 个旧 candidate 在 tightened gate reconcile 时被自动撤回，不再保留 candidate 文件。
