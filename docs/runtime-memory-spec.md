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
- `state/`
  - runtime manifest 与最近一次 review 状态

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

## Review Rule

不是每条 capture 都值得升级。

满足任意两项，再优先进入 review queue：

- 暴露重复失败
- 形成可迁移做法
- 改变后续触发、分工或评估方式
- 值得进入 benchmark / pattern / failure mode

## Helper Scripts

- `scripts/init_runtime_memory.py`
  - 初始化 runtime 目录和 bootstrap 文件，支持 `--host` / `--root`
- `scripts/validate_runtime_memory.py`
  - 检查目录结构、JSON 文件和 capture schema
- `scripts/smoke_test_runtime_memory.py`
  - 用临时目录跑一轮端到端 smoke test，并校验 host-aware manifest
- `scripts/write_runtime_capture.py`
  - 读取一条 JSON 记录并追加到 runtime capture，同时补 runtime host 信息
- `scripts/read_runtime_context.py`
  - 按 `scene` 读取最近 captures，供下一轮调用前预读取

## Non-Goals

- 不做全自动 pattern 提炼
- 不做复杂语义检索
- 不在 runtime 层长期保存大段私有原文
- 不把仓库历史资产整批导入 runtime
