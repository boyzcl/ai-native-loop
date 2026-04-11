# ai-native-loop

`ai-native-loop` 是一个工作协议层 Skill。

它解决的不是“再给我一个答案”，而是：

- 输入太乱，当前轮不知道该推进什么
- AI 已经有输出，但反馈进不了下一轮
- 任务跨阶段或多 Agent，结果很难回收和整合

一句话说：

> 当你真正卡住的是协作闭环，而不是单点答案时，用 `ai-native-loop`。

## Release Status

- Release truth: [release-manifest.md](docs/release-manifest.md)
- Current public version: `v0.1.0`
- Current iteration track: `v0.2.0` draft / validation hardening

## When To Use

优先在下面这些情况使用：

- 需求、材料、历史尝试、报错混在一起，当前轮任务包不清楚
- 已经有 AI 输出，但不知道该保留什么、丢弃什么、怎么进入下一轮
- 你能感觉结果不对，但说不清错在哪，也不知道 prompt / protocol 该怎么改
- 多角色或多 Agent 协作边界不清，回收物难整合
- 同类问题已经重复至少两轮，但输入、分工或评估方式没有真正改写

通常不要在下面这些情况使用：

- 单点事实查询
- 翻译、改格式、改单个小项、机械执行
- 目标、交付物和验收标准都很清楚，只差直接执行
- 已有更窄、更强的领域 skill 足够解决

更完整的触发规则见 [SKILL.md](SKILL.md)、[trigger-examples.md](docs/trigger-examples.md) 和 [trigger-regression-suite.md](docs/trigger-regression-suite.md)。

## What It Produces

这个 Skill 默认把介入收敛成一组固定工件，而不是泛建议：

- `Diagnosis Card`
  - 当前卡在哪一环，为什么要用当前介入等级
- `Task Packet`
  - 把原始请求压成 AI / Agent 可执行的任务包
- `Feedback Attribution Card`
  - 把“结果不对”改写成可行动的反馈归因
- `Re-input Packet`
  - 把本轮结果折成下一轮更好的输入
- `Loop Recovery Block`
  - 对 `medium` 及以上任务，留下最小经验痕迹

核心工件定义见 [core-operating-primitives.md](references/core-operating-primitives.md)。

## Quick Start

### Install

```bash
git clone https://github.com/boyzcl/ai-native-loop.git ~/.codex/skills/ai-native-loop
```

### Trigger

直接这样说就可以：

- `用 $ai-native-loop 帮我把这个任务整理成更适合 AI 协作的闭环。`
- `用 $ai-native-loop 看看我现在卡住的根因是在输入、执行还是反馈。`
- `用 $ai-native-loop 帮我把这轮结果折叠成下一轮输入。`

### Before / After

Before：

> 我在改一个复杂功能，需求、历史尝试、报错和几段代码都混在一起了，你先帮我看看怎么继续。

After：

> 用 `ai-native-loop` 先输出 `Diagnosis Card` 和 `Task Packet`：明确这轮目标、当前状态、约束、成功信号和下一检查点；如果判断为 `medium` 以上介入，再补反馈归因和下一轮输入。

## How It Works

这个 Skill 的核心不是固定流程，而是动态介入：

- `light`
  - 上下文大体成熟，只缺更清晰的下一步
- `medium`
  - 任务跨材料或阶段，循环噪音较大
- `strong`
  - 任务高风险、反复失败、跨轮或多 Agent 协作依赖重

它背后的工作循环是：

1. 诊断当前卡点
2. 重写任务包
3. 重新组织人机 / 多 Agent 分工
4. 读取反馈，而不是只读取输出
5. 改写下一轮输入
6. 为经验复利用最小成本留下痕迹

更完整的架构说明见 [skill-architecture.md](docs/skill-architecture.md)。

## Why It Exists

大多数人已经会“用 AI”，但还没有形成稳定的 AI native 工作循环。

这个 Skill 的目标不是替你做完某一个任务，而是让你和 AI 的协作越来越：

- 可执行
- 可反馈
- 可回收
- 可迁移

它不是：

- 单次任务顾问
- 提示词美化器
- 编程专用技巧包
- 替用户思考的黑箱代理

## Proof And Validation

这个仓库已经不只是在写理念，也在补验证和经验复利层：

- 版本与状态单一事实源： [release-manifest.md](docs/release-manifest.md)
- Skill 结构图： [skill-architecture.md](docs/skill-architecture.md)
- 触发边界与回归集： [trigger-examples.md](docs/trigger-examples.md), [trigger-regression-suite.md](docs/trigger-regression-suite.md)
- benchmark 矩阵： [benchmark-matrix.md](docs/benchmark-matrix.md)
- 统一评分标准： [evaluation-rubric.md](docs/evaluation-rubric.md)
- 实验模板： [experiment-log-template.md](docs/experiment-log-template.md)
- 当前 benchmark 汇总： [benchmark-results-v0.2.0.md](docs/benchmark-results-v0.2.0.md)
- 经验复利规则： [experience-compounding-loop.md](references/experience-compounding-loop.md)

## Repo Map

如果你第一次看这个仓库，最值得先读的是这些文件：

- [SKILL.md](SKILL.md)
  - Skill 主体与调用规则
- [core-operating-primitives.md](references/core-operating-primitives.md)
  - 四个核心工件与最小完备动作集
- [skill-architecture.md](docs/skill-architecture.md)
  - 这个 Skill 的结构图
- [trigger-regression-suite.md](docs/trigger-regression-suite.md)
  - 触发边界回归测试集
- [experience-compounding-loop.md](references/experience-compounding-loop.md)
  - 经验如何进入下一轮系统
- [benchmark-results-v0.2.0.md](docs/benchmark-results-v0.2.0.md)
  - 当前验证结果与边界

## License

MIT
