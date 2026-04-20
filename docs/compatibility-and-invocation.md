# Compatibility And Invocation

## Core Distinction

先分清两件事：

- 协议可迁移：`ai-native-loop` 的 Diagnosis / Task Packet / Feedback / Re-input 结构可以迁到别的宿主
- 宿主已支持：仓库已经为某个宿主给出清晰的 runtime root、metadata、调用方式和验证边界

不要把前者直接说成后者。

## Recommended Invocation

- 显式调用 `$ai-native-loop`

不建议：

- 把隐式调用当作稳定能力承诺
- 仅凭首页描述就假设 runtime capture 会自动成功

## Why Explicit First

当前项目的核心优势在协议层与运行层，而不是隐式路由猜测。

因此：

- 显式调用优先保证稳定触发
- 也更容易判断 runtime capture 是否真的执行

## Runtime Root Resolution

runtime root 统一按下面顺序解析：

1. 显式 `--root`
2. `AI_NATIVE_LOOP_RUNTIME_ROOT`
3. host 专属环境变量，例如 `AI_NATIVE_LOOP_CODEX_RUNTIME_ROOT`
4. host home 环境变量，例如 `CODEX_HOME`
5. host 默认路径约定

当前默认路径约定：

- `Codex`：`~/.codex/skills/ai-native-loop/runtime/`
- `Claude Code`：`~/.claude/skills/ai-native-loop/runtime/`
- `OpenClaw`：`~/.openclaw/skills/ai-native-loop/runtime/`

后两者目前只是适配约定，不代表已经完成端到端验证。

## Tested Expectations

当前版本可以稳定承诺的，是：

- 协议型输出结构
- `medium+` 的 runtime capture 规则
- `Codex` 的默认 runtime path 与 helper script 解析
- baseline / pairwise / runtime provenance 的验证模板

当前仍在补强的，是：

- `Claude Code` 的端到端宿主验证
- 多 Agent 公开实测证据
- 隐式路由稳定性
- 足量 runtime reuse 样本

更完整的支持边界见 [compatibility-matrix.md](compatibility-matrix.md)。
