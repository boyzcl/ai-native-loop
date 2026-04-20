# Agent Metadata

这个目录只放宿主适配层资产，不放协议层真相。

当前文件：

- `openai.yaml`
  - `Codex` / OpenAI 宿主入口
- `claude-code.yaml`
  - `Claude Code` 适配草案
- `openclaw.yaml`
  - `OpenClaw` 适配草案

新增宿主时，至少要补三件事：

1. 一个清晰命名的 metadata 文件
2. 对应的 runtime root 默认与覆盖规则
3. 在 `docs/compatibility-matrix.md` 中声明支持层级

如果没有验证证据，就只能标成 `experimental` 或 `theoretically portable`。
