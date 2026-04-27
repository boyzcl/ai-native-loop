# Runtime Memory Spec

## Purpose

这份文档定义 `ai-native-loop` 的本地运行时经验层。

目标不是做一个重型知识库，而是让 `medium+` 调用后的经验有默认宿主，并能在下一次调用时被低成本读取。

## Host Path

runtime root 不再被协议层写死为单一路径，而是按宿主解析。

解析顺序：

1. 显式 `--root`
2. `AI_NATIVE_LOOP_RUNTIME_ROOT`
3. host 专属环境变量，例如 `AI_NATIVE_LOOP_CODEX_RUNTIME_ROOT`
4. host home 环境变量，例如 `CODEX_HOME`
5. host 默认路径约定

当前路径约定：

- `Codex`：`~/.codex/skills/ai-native-loop/runtime/`
- `Claude Code`：`~/.claude/skills/ai-native-loop/runtime/`
- `OpenClaw`：`~/.openclaw/skills/ai-native-loop/runtime/`

仓库工作副本不是默认 runtime 宿主。

## Directory Layout

- `captures/`
  - 每次 `medium+` 调用后的原始 capture，按日期存为 `YYYY-MM-DD.jsonl`
- `index/`
  - 轻索引，按 `scene`、`pattern`、`failure mode` 汇总
- `inbox/`
  - 待 review 的候选提升项
- `promoted/field-notes/`
  - 从 runtime capture 升级后的本地 field note
- `promoted/archive/`
  - 低价值或已被合并覆盖的旧经验
- `promoted/repo-candidates/`
  - 通过更强 gate 的 repo 候选资产，但不会自动写回 repo 公共层
- `state/`
  - runtime manifest、promotion policy、promotion ledger、reuse ledger 与最近一次 review 状态

## Capture Schema

最小字段：

- `timestamp`
- `session_id`
- `skill_name`
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

## Write Rule

对 `medium` 及以上任务：

1. 主输出末尾保留 `Loop Recovery Block`
2. 同结构内容写入 runtime capture

如果当前环境无法写入本地文件，必须明确说明未完成 runtime capture。
如果当前宿主只处于 `experimental` 或 `theoretically portable`，也不能把默认路径约定说成已验证事实。

## Read Rule

下一次调用时，只按需读取少量相关经验：

- 最近相似 `scene`
- 最近命中的 `failure mode`
- 最近被验证有效的 `pattern`

默认读取预算：

- 最近 5 条 raw captures
- 最多 3 条 promoted field notes
- 最多 2 条 pattern / failure references

当 retrieval 显式请求 promoted notes 且启用 reuse 记录时：

- note hit 会写入 `runtime/state/reuse-ledger.json`
- 对应 promoted note 的 `reuse_count` 会回写到 `promotion-ledger`
- 后续 repo candidate gate 可以使用真实 reuse 信号，而不只靠写作形态推断
- `2026-04-21` 起，promoted retrieval 会剔除 `Source Runtime Captures` / `Merge History` / 绝对路径噪音，并优先返回 title-weighted 的高置信命中，避免 host path 与 source path 污染 reuse evidence

## Review Rule

不是每条 capture 都值得升级。

满足任意两项，再优先进入 review queue：

- 暴露重复失败
- 形成可迁移做法
- 改变后续触发、分工或评估方式
- 值得进入 benchmark / pattern / failure mode

## Promotion Worker Rule

新增 `scripts/promotion_worker.py` 后，runtime review queue 默认可被周期消费。

最小动作边界：

- 自动 triage `review queue`
- 自动判定 `keep_raw / promote_to_field_note / merge_into_existing_note / archive`
- 只生成 `repo candidate`，不自动改 repo 公开资产
- 先执行 dedup / merge，再考虑新建
- backlog、working-set ceiling、archive 一起生效，避免只做 promotion 不做容量治理
- 周期触发层应通过薄封装脚本接入，避免把宿主 automation 逻辑直接写进多条命令拼接

## Helper Scripts

- `scripts/init_runtime_memory.py`
  - 初始化 runtime 目录和 bootstrap 文件，支持 `--host` / `--root`
- `scripts/validate_runtime_memory.py`
  - 检查目录结构、JSON 文件和 capture schema
- `scripts/smoke_test_runtime_memory.py`
  - 用临时目录跑一轮端到端 smoke test，并校验 host-aware manifest
- `scripts/write_runtime_capture.py`
  - 读取一条 JSON 记录并追加到 runtime capture，同时补 runtime host 信息；对 `medium+` 且进入 review queue 的样本默认立即尝试一次 bounded local promotion cycle
- `scripts/read_runtime_context.py`
  - 按 `scene` 读取最近 captures；加 `--include-promoted` 时同时返回相关 promoted field notes；加 `--record-reuse` 时写入 reuse ledger
- `scripts/promotion_worker.py`
  - 消费 review queue，执行本地自动晋升、merge、archive 与 gated repo candidate 生成
- `scripts/run_promotion_cycle.py`
  - 以本地 cadence 触发一次 bounded promotion cycle，带运行锁、前后快照和结构化 JSON 输出
- `scripts/run_promotion_reconcile.py`
  - 以 `--limit 0` 方式触发 repo candidate reconcile，并附带 governance report 与结构化 JSON 输出
- `scripts/runtime_governance_report.py`
  - 输出 backlog、promote、merge、archive、reuse、repo candidate 的治理指标
- `scripts/review_repo_candidates.py`
  - 列出并更新 `pending / accepted / rejected` repo candidate review 状态
- `scripts/retrieval_forward_test.py`
  - 对 promoted retrieval 跑 baseline / current forward test，记录 false positive / false negative 风险
- `scripts/runtime_governance_stress_test.py`
  - 基于当前 runtime 做 temp replay，验证更大 backlog / 更长周期下的容量治理是否稳定

## Trigger Telemetry Rule

本地触发层不应把 scheduler 元信息直接塞进 repo 层，也不应默认把每次调度都提升成新的 review 样本。

第一版约束：

- 主触发优先是 invocation-driven，而不是 host cron
- trigger run history 写入 `runtime/state/promotion-trigger-history.jsonl`
- 并发运行靠 `runtime/state/locks/` 下的共享锁避免互相踩写
- 如需把 trigger 运行写入 runtime capture，默认只允许 `raw_only`
- trigger capture 只作为本地运行证据，不进入 repo 自动发布链路
- host 级自动化默认只保留低频 reconcile，不再承担主 cycle 消费职责

## Non-Goals

- 不做全自动 pattern 提炼
- 不做复杂语义检索
- 不在 runtime 层长期保存大段私有原文
- 不把仓库历史资产整批导入 runtime
