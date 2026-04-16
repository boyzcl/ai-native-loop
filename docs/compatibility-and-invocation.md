# Compatibility And Invocation

## Recommended Environment

当前推荐环境：

- 本地 Codex skill 宿主
- 安装路径：`~/.codex/skills/ai-native-loop`
- 当前运行环境允许文件系统写入

## Recommended Invocation

当前版本默认建议：

- 显式调用 `$ai-native-loop`

不建议：

- 把隐式调用当作稳定能力承诺
- 仅凭首页描述就假设 runtime capture 会自动成功

## Why Explicit First

当前项目的核心优势在协议层与运行层，而不是隐式路由猜测。

因此：

- 显式调用优先保证稳定触发
- 也更容易判断 runtime capture 是否真的执行

## Tested Expectations

当前版本可以稳定承诺的，是：

- 协议型输出结构
- `medium+` 的 runtime capture 规则
- baseline / pairwise / runtime provenance 的验证模板

当前仍在补强的，是：

- 多 Agent 公开实测证据
- 隐式路由稳定性
- 足量 runtime reuse 样本
