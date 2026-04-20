# Skill Architecture

## Purpose

这份文档回答一个更基础的问题：

> `ai-native-loop` 不是一堆提示词和模板的集合，而是一个 Skill 运行系统。这个系统由哪些部分组成？每部分如何工作？为什么有必要存在？

它的目标不是重复 README，而是给维护者、评审者和后续 Agent 一个结构图。

## Why This Document Exists

如果一个 Skill 只能靠“看起来很有道理”的零散文档来理解，会长期遇到三类问题：

- 调用边界不稳：Agent 不知道什么时候该调用，什么时候不该调用。
- 迭代方向失焦：后续修改容易变成继续加内容，而不是增强系统。
- 结构不可解释：外部看得到很多文件，但看不出哪些是核心、哪些是配套、哪些在驱动复利。

所以，`ai-native-loop` 需要一个更高层的结构描述。

## First Principle

从 `ai-native` 的视角看，一个真正可运行的 Skill，至少不是：

- 一段大 Prompt
- 一套模板集合
- 一篇方法论说明

它更接近：

> 一个带有调用边界、策略哲学、最小工件集、边界事实和验证复利机制的运行协议。

## The 3-Part Lens

如果用常见的 Skill 设计框架来压缩，它可以先被描述为三部分：

1. `Agent 策略哲学`
2. `最小完备工具集`
3. `必要的事实说明`

这个三段式是有价值的，但对 `ai-native-loop` 来说还不够细。

因为 `ai-native-loop` 不只是运行时 Skill，它还会：

- 判断自己该不该被调用
- 记录经验并进入下一轮
- 用 benchmark / rubric / field note 来校正自己

所以，从更贴近本仓库真实运行方式的角度，推荐把它拆成 5 层。

## The 5-Layer Structure

### 1. Trigger Boundary

先解决：`什么时候该调用这个 skill`

如果入口不清楚，后面一切都会漂。

当前对应文件：

- [SKILL.md](../SKILL.md)
- [trigger-examples.md](trigger-examples.md)
- [trigger-regression-suite.md](trigger-regression-suite.md)
- [openai.yaml](../agents/openai.yaml)

这一层如何工作：

- 先判断：用户缺的是“直接答案”，还是“协作闭环”
- 再判断：阻塞点是否落在输入、执行、反馈、再输入之间
- 再看可观察信号
- 用 stop rule 防止误触发

为什么必要：

- 没有调用边界，Skill 就会退化成“看起来什么都能用”的万能 Prompt
- 万能 Prompt 对 Agent 来说通常等于不稳定

### 2. Strategy Philosophy

再解决：`这个 skill 在这个场景里怎么思考`

这是 Skill 的策略层，不是具体步骤层。

当前对应文件：

- [SKILL.md](../SKILL.md)
- [loop-protocol.md](../references/loop-protocol.md)
- [intervention-matrix.md](../references/intervention-matrix.md)

这一层如何工作：

- 不先追求答案，先看闭环哪里坏了
- 不只优化当前轮，也优化下一轮
- 不默认上重结构，而是动态选择 `light / medium / strong`
- 不替用户做不可逆目标判断

为什么必要：

- 没有这层，四个核心工件会退化成形式主义模板
- 有了这层，Skill 才能迁移到没见过的新任务

### 3. Minimal Complete Operating Set

再解决：`这个 skill 最少靠什么工件就能完成介入`

这就是 `ai-native-loop` 的最小完备运行集。

当前对应文件：

- [core-operating-primitives.md](../references/core-operating-primitives.md)
- [field-note-template.md](field-note-template.md)
- [task-rewrite-template.md](../references/task-rewrite-template.md)
- [reinput-template.md](../references/reinput-template.md)
- [agent-handoff-template.md](../references/agent-handoff-template.md)

最小完备工件：

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`
- `Loop Recovery Block`

这一层如何工作：

- `Diagnosis Card` 负责定位当前阻塞点
- `Task Packet` 负责把混乱输入压成可执行任务包
- `Feedback Attribution Card` 负责把“不满意”改写成可行动反馈
- `Re-input Packet` 负责把这轮结果折成下一轮输入
- `Loop Recovery Block` 负责留下最小经验痕迹

为什么必要：

- 没有这组工件，Skill 只能给抽象建议
- 有了这组工件，Skill 才能稳定产出“能继续推进的结构”

### 4. Necessary Facts And Constraints

再解决：`Agent 在这个 skill 中必须记住哪些硬事实`

这不是外部世界知识，而是运行边界事实。

当前对应文件：

- [failure-modes.md](../references/failure-modes.md)
- [multi-agent-decomposition.md](../references/multi-agent-decomposition.md)
- [trigger-regression-suite.md](trigger-regression-suite.md)
- [SKILL.md](../SKILL.md)

这些硬事实包括：

- 不是所有复杂任务都该触发这个 skill
- 多 Agent 不默认更高级，先判断值不值得拆
- `medium` 以上默认要留 recovery block
- 没有边界时不替用户做不可逆决定
- 没有验证与回收物时，不应做强结论

这一层如何工作：

- 防止 Agent 因刻板印象误判
- 给 Skill 提供 stop rule 和边界控制
- 防止 Skill 漂成“方法论教练”

为什么必要：

- 没有这层，策略哲学会太抽象
- 工件集也会被错误调用

### 5. Validation And Compounding Layer

最后解决：`这个 skill 如何证明自己有效，并持续变强`

这是 `ai-native-loop` 相对普通 Skill 更关键的一层。

当前对应文件：

- [benchmark-matrix.md](benchmark-matrix.md)
- [evaluation-rubric.md](evaluation-rubric.md)
- [experiment-log-template.md](experiment-log-template.md)
- [experience-compounding-loop.md](../references/experience-compounding-loop.md)
- [field-notes/README.md](field-notes/README.md)
- [patterns/README.md](../patterns/README.md)

这一层如何工作：

- 用 benchmark / rubric / experiment log 做验证
- 用 field note / pattern / failure mode 做经验提升
- 把一次任务的得失进入下一轮系统

为什么必要：

- 没有这层，Skill 只能被解释，不能被验证
- 也不能持续修正自己的调用边界与运行方式

## How The 3-Part Lens Maps To The 5 Layers

如果仍想使用更简洁的三段式，可以这样映射：

### Agent 策略哲学

主要对应：

- `Trigger Boundary`
- `Strategy Philosophy`

因为对 `ai-native-loop` 来说，决定“什么时候调用”和“调用后怎么思考”都属于策略层。

### 最小完备工具集

主要对应：

- `Minimal Complete Operating Set`

也就是四个核心工件加上 recovery block。

### 必要的事实说明

主要对应：

- `Necessary Facts And Constraints`
- `Validation And Compounding Layer`

因为对这个 skill 来说，边界事实和验证事实都属于 Agent 必须记住的系统事实。

## Current Judgment

基于当前仓库状态，可以给出下面的判断：

- `Agent 策略哲学`：已经很强，是本 Skill 的核心优势
- `最小完备工具集`：已经存在，但仍可继续压成更显式的“能力表”
- `必要的事实说明`：已经存在，但分散在触发规则、failure mode、多 Agent 边界和验证层中
- `验证复利层`：已经建立骨架，是本 Skill 区别于普通 Prompt 的关键部分

一句话总结：

> `ai-native-loop` 已经不是“提示词 + 模板”型 Skill，而是一个由调用边界、策略哲学、最小工件集、边界事实与验证复利机制共同组成的运行系统。

## Next Useful Refinements

如果继续增强这一结构，优先级建议如下：

1. 增加一张更显式的“工件能力表”
   - 每个工件解决什么问题
   - 何时必需
   - 何时按需追加
2. 把“必要事实说明”进一步压缩成单独清单
   - 让 Agent 更容易在一次加载里读到
3. 给触发回归集补一个自动化执行 harness
   - 把“规则存在”推进到“规则可反复检验”

## Host-Aware Rewrite

如果从“支持多个 agent 宿主”的问题来切，这个仓库现在推荐再用一套四层视角阅读：

1. `协议层`
   - Skill 核心协议与工件，不绑定宿主
2. `宿主层`
   - runtime root、文件系统假设、调用前提
3. `适配层`
   - `agents/*.yaml` 这样的宿主 metadata
4. `验证层`
   - 兼容矩阵、helper scripts、smoke test、runtime provenance

这套四层拆分的详细定义见 [host-abstraction.md](host-abstraction.md)。
