# Host Abstraction

Updated: `2026-04-20`

## Purpose

这份文档把 `ai-native-loop` 从 `Codex-first` 重写为四层：

1. `协议层`
2. `宿主层`
3. `适配层`
4. `验证层`

目标不是把 README 换个说法，而是把“什么能迁移”和“什么已支持”拆开。

## 1. 协议层

这一层是宿主无关的。

包含：

- 触发边界
- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`
- `Loop Recovery Block`
- `medium+` 必须保留 recovery block 并写 runtime capture 的规则

判断标准：

- 换一个宿主，这层仍然成立
- 不依赖 `.codex`、`.claude` 或某个 CLI 的固定行为

## 2. 宿主层

这一层回答：

> 当前在哪个 agent 宿主里运行？这个宿主的默认 runtime root、文件系统能力和调用约定是什么？

当前仓库把宿主层显式化为：

- host id：`codex`、`claude-code`、`openclaw`
- support tier：`officially supported` / `experimental` / `theoretically portable`
- runtime root resolution order：
  - `--root`
  - `AI_NATIVE_LOOP_RUNTIME_ROOT`
  - host 专属 runtime env
  - host home env
  - host 默认路径约定

宿主层的责任：

- 解析默认 runtime root
- 说明默认值从哪里来
- 防止把单宿主路径当成协议真相

## 3. 适配层

这一层回答：

> 某个具体宿主要怎样暴露这个 skill？

当前仓库里的适配层资产：

- `agents/openai.yaml`
  - `Codex` / OpenAI 宿主入口
- `agents/claude-code.yaml`
  - `Claude Code` 适配草案
- `agents/openclaw.yaml`
  - `OpenClaw` 适配草案
- `agents/README.md`
  - 新宿主接入位说明

适配层只做宿主相关内容：

- metadata
- invocation phrasing
- 宿主级默认说明

它不重新定义协议层。

## 4. 验证层

这一层回答：

> 我们怎么知道自己不是“看起来支持”？

当前验证层由这些部分构成：

- helper scripts 的统一 host-aware 解析
- `smoke_test_runtime_memory.py`
- [compatibility-matrix.md](compatibility-matrix.md)
- [runtime-memory-spec.md](runtime-memory-spec.md)
- benchmark / rubric / experiment log 文档

当前验证边界：

- `Codex`：有最小可信验证链
- `Claude Code`：只有适配草案，还没有端到端宿主验证
- `OpenClaw`：已有适配草案，还没有端到端宿主验证

## Design Rule

以后新增宿主时，必须按这个顺序推进：

1. 先确认协议层不用改
2. 再声明宿主层默认路径与覆盖规则
3. 再补适配层 metadata
4. 最后补验证层证据

如果第 4 步还没完成，就不能把该宿主写成 `officially supported`
