# Claude Code Adapter Draft

Updated: `2026-04-20`

## Status

`Claude Code` 当前是 `experimental`，不是 `officially supported`。

这份文档的作用是把适配边界写清楚，而不是提前宣称“已经支持 Claude Code”。

## What This Draft Covers

- 宿主 id：`claude-code`
- 默认 runtime root 约定：`~/.claude/skills/ai-native-loop/runtime/`
- helper scripts 可通过 `--host claude-code` 或环境变量解析到该路径
- 已提供 `agents/claude-code.yaml` 作为宿主 metadata 草案

## What This Draft Does Not Claim

- 不声称已经验证 Claude Code 的完整安装路径和 skill 注册机制
- 不声称隐式触发已稳定
- 不声称 runtime capture 已在真实 Claude Code 会话中完成回读验证

## Current Invocation Draft

推荐仍然使用显式调用：

- `用 $ai-native-loop 帮我先做 Diagnosis Card 和 Task Packet。`

runtime 初始化草案：

```bash
python3 /path/to/ai-native-loop/scripts/init_runtime_memory.py --host claude-code
```

如果默认路径不适用，显式覆盖：

```bash
python3 /path/to/ai-native-loop/scripts/init_runtime_memory.py --host claude-code --root /custom/runtime/root
```

## Promotion Gate To Official Support

要把 `Claude Code` 从 `experimental` 升到 `officially supported`，至少还需要：

1. 一条真实可重复的安装与发现路径
2. 一次端到端 runtime capture 写入与回读验证
3. 一份宿主侧 invoke proof，而不是只在 repo 内部自测
