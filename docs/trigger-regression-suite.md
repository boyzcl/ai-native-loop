# Trigger Regression Suite

## Purpose

这份文档不是解释理念，而是给 Agent 做触发回归测试。

目标是反复检查一件事：

> `ai-native-loop` 是否只在“闭环出了问题”时触发，而不会在“只差一个答案”时误触发。

## How To Use

对每条用例，Agent 都应该显式给出：

1. `should_trigger`
2. `why`
3. `matched_signals`
4. `recommended_intervention`

判断顺序固定如下：

1. 先问：用户是不是主要要一个直接答案？
2. 如果不是，再问：阻塞是不是出在输入、执行、反馈、再输入之间的连接处？
3. 再数信号：至少命中 2 条才优先触发。

信号列表：

- 输入混乱
- 目标漂移
- 输出难用
- 反馈断裂
- 协作失衡
- 重复失败

## Pass Rule

这份回归集通过的最低标准：

- 所有 `should_trigger` 用例都被判为触发
- 所有 `should_not_trigger` 用例都被判为不触发
- `borderline` 用例至少要给出清楚的理由，而不是模糊表态
- 不允许把“任务复杂”直接当作触发理由
- 不允许把“只差一个直接答案”的请求判成触发

## Expected Output Shape

跑这份回归集时，建议统一输出为：

```md
- case_id:
- decision: should_trigger / should_not_trigger / borderline
- matched_signals:
- stop_rule_hit:
- recommended_intervention:
- why:
```

不要只回答“会”或“不会”。

## Cases

### Case 01

- `id`: `trigger-01-messy-coding-context`
- `label`: 编码上下文混乱
- `expected`: `should_trigger`
- `prompt`:
  - 我在改一个复杂功能，需求、报错、历史尝试和几段代码都混在一起了。先别急着写代码，帮我整理这轮到底该怎么推进。
- `matched_signals`:
  - 输入混乱
  - 目标漂移
- `recommended_intervention`: `medium`
- `why`:
  - 用户不是缺单点答案，而是缺一个当前轮任务包和下一检查点。

### Case 02

- `id`: `trigger-02-feedback-not-entering-next-round`
- `label`: 反馈进不了下一轮
- `expected`: `should_trigger`
- `prompt`:
  - 我已经做了一轮研究，也拿到了 AI 输出，但我不知道哪些反馈值得保留、哪些应该丢掉，以及下一轮输入该怎么改。
- `matched_signals`:
  - 输出难用
  - 反馈断裂
- `recommended_intervention`: `medium`
- `why`:
  - 典型的 feedback -> re-input 问题。

### Case 03

- `id`: `trigger-03-multi-agent-handoff-break`
- `label`: 多 Agent 回收失衡
- `expected`: `should_trigger`
- `prompt`:
  - 我让几个 agent 并行做不同部分，但回来的东西格式不统一、很难整合，感觉总在重复劳动。你先帮我判断这轮该怎么收口。
- `matched_signals`:
  - 协作失衡
  - 输出难用
- `recommended_intervention`: `strong`
- `why`:
  - 核心问题不是产出内容，而是协作协议和回收物失真。

### Case 04

- `id`: `trigger-04-repeat-failure-without-rewrite`
- `label`: 同类失败反复出现
- `expected`: `should_trigger`
- `prompt`:
  - 这个问题我已经试了两轮，每次都得到差不多的错误结果，但我其实没有重写过输入和验收标准。你先帮我看卡点到底在哪。
- `matched_signals`:
  - 重复失败
  - 目标漂移
- `recommended_intervention`: `medium`
- `why`:
  - 已经进入“重复失败但闭环未改写”的典型场景。

### Case 05

- `id`: `trigger-05-writing-output-not-usable`
- `label`: 写作输出能看但不好用
- `expected`: `should_trigger`
- `prompt`:
  - AI 帮我写了一版文章，但结构和重点都不对。我不确定应该继续改这一版，还是重写下一轮输入。先帮我判断。
- `matched_signals`:
  - 输出难用
  - 反馈断裂
- `recommended_intervention`: `light_to_medium`
- `why`:
  - 用户不是缺内容，而是缺保留/丢弃/改写的闭环判断。

### Case 06

- `id`: `no-trigger-01-single-fact-query`
- `label`: 单点事实查询
- `expected`: `should_not_trigger`
- `prompt`:
  - React 19 的 `use` 是做什么的？
- `matched_signals`:
  - none
- `recommended_intervention`: `none`
- `why`:
  - 这是知识查询，不是闭环问题。

### Case 07

- `id`: `no-trigger-02-translation`
- `label`: 翻译
- `expected`: `should_not_trigger`
- `prompt`:
  - 把这个标题翻成英文。
- `matched_signals`:
  - none
- `recommended_intervention`: `none`
- `why`:
  - 机械执行，闭环结构没有出问题。

### Case 08

- `id`: `no-trigger-03-small-direct-edit`
- `label`: 小的直接修改
- `expected`: `should_not_trigger`
- `prompt`:
  - 这段 CSS 帮我把按钮颜色改成蓝色。
- `matched_signals`:
  - none
- `recommended_intervention`: `none`
- `why`:
  - 目标和动作都清楚，只差执行。

### Case 09

- `id`: `no-trigger-04-clear-task-with-clear-bar`
- `label`: 目标和验收标准都清楚
- `expected`: `should_not_trigger`
- `prompt`:
  - 请把这个函数重构成纯函数，并保证现有测试全部通过。只改这一处。
- `matched_signals`:
  - none
- `recommended_intervention`: `none`
- `why`:
  - 这是明确执行任务，不需要闭环重写。

### Case 10

- `id`: `borderline-01-brainstorming`
- `label`: 只是想让 AI 想想
- `expected`: `borderline`
- `prompt`:
  - 你帮我想想这个产品还能加什么功能。
- `matched_signals`:
  - maybe none
- `recommended_intervention`: `none_or_light`
- `why`:
  - 只有在用户真实卡点是“不会推进这轮工作”而不是“想多拿一些点子”时，才应触发。

### Case 11

- `id`: `borderline-02-please-organize-this`
- `label`: 用户说先帮我整理一下
- `expected`: `borderline_but_often_trigger`
- `prompt`:
  - 你先帮我整理一下这个任务。
- `matched_signals`:
  - 输入混乱
  - 目标漂移
- `recommended_intervention`: `light_or_medium`
- `why`:
  - 这通常是高价值入口，但前提是“整理”的对象真的是任务闭环，而不是简单排版。

### Case 12

- `id`: `borderline-03-domain-skill-already-better`
- `label`: 已有更窄 skill
- `expected`: `borderline_but_usually_no_trigger`
- `prompt`:
  - 帮我把这篇中文文章润色成公众号风格。
- `matched_signals`:
  - maybe output style issue
- `recommended_intervention`: `domain_skill_first`
- `why`:
  - 如果只是风格写作，更窄的写作 skill 更合适；只有当用户同时卡在反馈吸收和下一轮输入重写时，才值得触发 `ai-native-loop`。

### Case 13

- `id`: `trigger-06-explicit-skill-request`
- `label`: 用户明确要求使用 ai-native-loop
- `expected`: `should_trigger`
- `prompt`:
  - 用 ai-native-loop 帮我先诊断一下，我现在这轮任务为什么一直推进不顺。
- `matched_signals`:
  - explicit_request
- `recommended_intervention`: `light_or_medium`
- `why`:
  - 用户已经明确要求调用这个 skill；这应高于默认的信号阈值判断。

### Case 14

- `id`: `no-trigger-05-explicit-one-shot-answer`
- `label`: 用户明确只要一个直接答案
- `expected`: `should_not_trigger`
- `prompt`:
  - 不用帮我整理流程，也不要方法论，直接告诉我这个 SQL 为什么报错。
- `matched_signals`:
  - maybe none
- `recommended_intervention`: `none`
- `why`:
  - 用户明确拒绝闭环重写，只要直接答案；除非后续暴露出明显闭环问题，否则不应触发。

## Maintenance Rule

每次发现以下任一情况，就应该给这份回归集加案例：

- 有明显误触发
- 有明显漏触发
- Agent 在同类请求上的判断摇摆
- 新增了一个容易和别的 skill 冲突的场景

不要只改规则，不补回归案例。
