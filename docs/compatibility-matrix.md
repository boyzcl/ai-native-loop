# Compatibility Matrix

Updated: `2026-04-20`

## Support Tiers

- `officially supported`
  - 仓库已提供宿主 metadata、默认 runtime root 解析、helper script 支持和明确文档边界
- `experimental`
  - 仓库已提供适配草案和路径约定，但还没有足够的端到端宿主验证证据
- `theoretically portable`
  - 协议层预计可迁移，仓库只预留扩展位；没有把该宿主当作当前支持承诺

## Matrix

| Host | Tier | Runtime root default | Metadata in repo | Validation status | What is actually promised |
| --- | --- | --- | --- | --- | --- |
| `Codex` | `officially supported` | `~/.codex/skills/ai-native-loop/runtime/` | `agents/openai.yaml` | helper scripts + smoke test + docs aligned | 显式调用、runtime root 解析、medium+ capture 规则 |
| `Claude Code` | `experimental` | `~/.claude/skills/ai-native-loop/runtime/` | `agents/claude-code.yaml` | adapter draft only; no end-to-end host validation yet | 可按同协议运行，并可用 `--host claude-code` / env 显式配置 runtime |
| `OpenClaw` | `experimental` | `~/.openclaw/skills/ai-native-loop/runtime/` | `agents/openclaw.yaml` | adapter draft only; no end-to-end host validation yet | 可按同协议运行，并可用 `--host openclaw` / env 显式配置 runtime |
| Other hosts | `theoretically portable` | none | none | none | 必须先补 adapter + validation，不能直接宣称支持 |

## Read This Correctly

- `Codex` 是当前最小可信支持面。
- `Claude Code` 不是“已经支持”，而是“已有清晰适配草案和代码入口”。
- `OpenClaw` 现在与 `Claude Code` 同级，属于“已有清晰适配草案和代码入口”，但还没有真实宿主验证。

## Validation Gate

一个宿主要从 `experimental` 升到 `officially supported`，至少需要：

1. 明确的宿主 metadata 文件
2. 默认 runtime root 解析和覆盖规则
3. 一条端到端安装 / 调用 / capture / 读取验证路径
4. 文档中不再存在把实验宿主写成既成事实的表述
