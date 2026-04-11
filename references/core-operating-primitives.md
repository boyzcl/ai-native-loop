# Core Operating Primitives

## Why This File Exists

`ai-native-loop` 不能只停留在抽象闭环概念上。

为了让协议稳定执行，所有介入默认尽量收敛为四种核心工件。它们共同构成这个 Skill 的最小完备动作集。

## The Four Primitives

### 1. Diagnosis Card

用途：先判断循环坏在哪，再决定介入强度。

最小字段：

- `loop_stage`
  当前主要卡在输入、执行、反馈还是再输入。
- `intervention_level`
  `light` / `medium` / `strong`
- `primary_block`
  当前最主要的阻塞点。
- `risk_note`
  这轮最需要避免的错误。

短版示例：

```md
Diagnosis Card
- loop_stage: input
- intervention_level: medium
- primary_block: 上下文很多，但没有本轮明确推进目标
- risk_note: 现在直接求答案会继续放大噪音
```

### 2. Task Packet

用途：把原始表达压成 AI 可执行任务包。

最小字段：

- `objective`
- `current_state`
- `artifacts`
- `constraints`
- `success_signal`
- `next_checkpoint`

短版示例：

```md
Task Packet
- objective: 把现有研究材料重组为一篇可继续扩写的长文结构
- current_state: 有零散笔记和初稿，没有统一论点和章节顺序
- artifacts: 研究笔记、历史草稿、参考链接
- constraints: 保留原有论点，不杜撰事实
- success_signal: 形成一版可直接进入扩写的提纲
- next_checkpoint: 先检查提纲是否覆盖关键论点与证据链
```

### 3. Feedback Attribution Card

用途：把“这轮不对劲”变成可归因的反馈，而不是感受性抱怨。

最小字段：

- `signal`
  实际观察到的问题。
- `failure_class`
  模型失败 / 上下文失败 / 工具失败 / 决策失败 / 分工失败
- `root_cause`
  最可能的根因。
- `keep`
  本轮哪些部分仍然有效。
- `change`
  下一轮必须改什么。

短版示例：

```md
Feedback Attribution Card
- signal: 输出结构完整，但关键证据链缺失
- failure_class: context failure
- root_cause: 输入没有明确哪些事实必须被保留
- keep: 提纲层级和整体叙事顺序
- change: 下一轮补一份必须引用的关键事实清单
```

### 4. Re-input Packet

用途：把本轮经验折叠成下一轮更好的起点。

最小字段：

- `preserve`
- `discard`
- `add_context`
- `change_request`
- `next_checkpoint`

短版示例：

```md
Re-input Packet
- preserve: 当前提纲结构与章节顺序
- discard: 过早展开的细节段落
- add_context: 关键事实、引用来源、目标读者
- change_request: 先补证据链，再扩写正文
- next_checkpoint: 检查每节是否都有证据支撑
```

## Mapping To Intervention Levels

### Light

默认只需要：

- `Diagnosis Card`
- `Task Packet`

适用：表达松散，但循环基本健康。

### Medium

默认需要：

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`

适用：任务跨材料、跨阶段，且当前质量不稳。

### Strong

默认仍以这四个工件为核心，但会扩展字段密度。

额外强调：

- 目标与边界澄清
- 决策权归属
- 验证路径
- 不可替用户代做的判断

## Usage Rule

无论场景是什么，默认先问：

1. 现在缺的是哪张卡？
2. 当前轮最小需要生成哪两张卡？
3. 哪张卡必须进入下一轮？

如果这三个问题都说不清，说明介入还没有真正进入执行层。

## Anti-Bloat Rule

不要机械地每次都展开四张完整卡。

优先原则：

- 轻介入：最少两张卡
- 中介入：四张卡的最小版
- 强介入：四张卡扩展版

目标不是增加格式感，而是减少循环失真。

## Tail Capture Rule

`Loop Recovery Block` 不属于四张卡中的任意一张，但对 `medium` 及以上介入，它属于默认结束动作。

- `light`：按需追加。
- `medium` / `strong`：默认追加，并放在整段输出末尾。
- 作用不是补充解释，而是把本轮最小可复用经验压成下一轮入口。

推荐尾部形状：

```md
Loop Recovery Block
- scene:
- initial_block:
- artifacts_produced:
- what_worked:
- remaining_risk:
- next_input:
```
