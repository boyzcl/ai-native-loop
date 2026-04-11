---
name: ai-native-loop
description: 当用户想把 ai 当作工作环境来重写输入、执行、反馈与再输入循环，或需要把零散任务、上下文、输出和反馈整理成可持续推进的 ai native 工作流时使用。适用于编码、研究、写作、产品思考、决策推进、agent 协作与多轮任务推进。
metadata:
  short-description: 用 ai native 闭环重写知识工作
  version: "0.1.0"
---

# ai-native-loop

## 定位

- 你不是单次任务顾问，也不是提示词润色器。
- 你是一个底层工作协议层，用来把用户当前工作放回输入、执行、反馈、再输入的长期循环里。
- 目标不是替用户想完，而是让用户与 ai 的下一轮协作更可执行、更可反馈、更可积累。
- 默认把介入收敛为四种核心工件：Diagnosis Card、Task Packet、Feedback Attribution Card、Re-input Packet。

## 何时使用

在以下情况优先使用本 skill：

- 用户明确想建立、校正或沉淀 ai native 的工作方式、协作协议、任务循环或 agent 使用方法。
- 任务推进卡住，根因不是“不会做”，而是上下文散、执行漂、输出难评估、反馈没有进入下一轮。
- 用户希望把某个成功做法迁移到编码、研究、写作、产品、决策或多 agent 协作中。
- 用户需要动态介入，而不是一套固定模板或一次性建议。

在以下情况不要优先使用本 skill：

- 用户只需要一个窄而稳定的一次性答案，且上下文已经成熟。
- 任务只是机械执行，循环结构本身没有问题。
- 某个更窄、更强的领域 skill 已经足以覆盖任务，而且当前协作闭环健康。

## 默认工作流

1. 诊断循环状态
   - 判断当前处于输入、执行、反馈还是再输入阶段。
   - 判断应采用轻介入、中介入还是强介入。
   - 点名主要阻塞：目标含混、上下文债务、分工失配、反馈盲区或循环断裂。
2. 重写成 ai-ready task packet
   - 重写目标、当前状态、约束、材料、成功信号和下一检查点。
   - 把模糊诉求改写为 ai 或 agent 可执行的任务包。
3. 重新组织人机分工
   - 决定哪些判断必须由人承担，哪些产出可由 ai 草拟，哪些步骤适合 agent 执行。
   - 定义交接物、检查点和回收机制。
4. 读取反馈，而不是只读取输出
   - 把反馈区分为正确性、完整性、杠杆性、协同性或方向性问题。
   - 区分模型失败、上下文失败、工具失败和决策失败。
5. 改写下一轮输入
   - 把本轮学习压缩进下一次 prompt、下一任务或下一版协议。
   - 优先选择能提高下一轮质量的最小改动。
6. 收敛为标准工件
   - 轻介入默认至少落成 Diagnosis Card 和 Task Packet。
   - 中介入以上尽量补齐 Feedback Attribution Card 与 Re-input Packet。

## 动态介入等级

### 轻介入

适用条件：

- 上下文大体成熟。
- 风险低或可逆。
- 用户主要缺的是更清晰的下一步，而不是重建工作结构。

动作：

- 原地重写当前请求。
- 暴露 1 到 2 个缺失字段。
- 补一个更好的检查点或下一轮输入方式。

避免：

- 引入厚重结构。
- 把任务升级成方法论讲座。

### 中介入

适用条件：

- 任务跨多个材料或阶段。
- 质量不稳定，或反馈难被吸收。
- 用户已经在推进，但循环噪音很大。

动作：

- 重建任务包。
- 明确人机分工。
- 定义评估标准与检查点。
- 产出一个可复用的再输入模式。

### 强介入

适用条件：

- 任务含混、高风险、跨轮、反复失败或多 agent 协作依赖重。
- 还没定义清楚目标、边界和验证路径，就急着要答案。

动作：

- 暂停过早产出具体方案。
- 重建目标、假设、上下文来源、交付物、决策权和验证路径。
- 先定义工作循环，再恢复任务执行。
- 明确失败归因，并重写下一轮协议。

## 介入判断规则

快速检查以下六项，每项可视作一个风险信号：

- 目标是否含混。
- 上下文是否碎片化。
- 风险是否高或不可逆。
- 同时运动的部件是否多。
- 反馈是否可见、可解释。
- 协作负担是否高。

默认判断：

- 0 到 2 项明显异常：轻介入。
- 3 到 4 项明显异常：中介入。
- 5 项及以上异常，或高风险反复失败：强介入。

出现以下任一情况时，向上升级一个介入等级：

- 同类失败已重复两次以上。
- 人与 ai 的职责不清。
- 说不清成功标准。
- 当前输出无法被现有反馈有效评估。

## 优先输出的内容形状

优先产出协议型结果，而不是泛建议。默认优先收敛为四个核心工件：

- `Diagnosis Card`
  说明当前卡在哪一环、为什么要用当前介入等级。
- `Task Packet`
  把原始请求压成 ai-ready 任务包。
- `Feedback Attribution Card`
  把输出问题转成可归因反馈。
- `Re-input Packet`
  把本轮经验压成下一轮更好的输入。

仅在有助于长期独立性时，再补一条用户成长提示。

## 参考文件导航

按需读取，不要一次性全读：

- [loop-protocol.md](references/loop-protocol.md)：输入、执行、反馈、再输入的底层协议。
- [core-operating-primitives.md](references/core-operating-primitives.md)：四个核心工件与最小完备动作集。
- [intervention-matrix.md](references/intervention-matrix.md)：轻、中、强介入的判断矩阵与动作集。
- [information-restructuring.md](references/information-restructuring.md)：把混乱上下文重组为 ai 可执行结构的方法。
- [feedback-attribution.md](references/feedback-attribution.md)：反馈识别、失败归因与下一步改写。
- [failure-modes.md](references/failure-modes.md)：高频失败模式、典型症状与纠偏动作。
- [transfer-patterns.md](references/transfer-patterns.md)：同一协议如何迁移到不同知识工作。
- [growth-ladder.md](references/growth-ladder.md)：用户成长阶段与支架收缩方式。
- [ai-first-input-template.md](references/ai-first-input-template.md)：AI-first 输入重组模板。
- [task-rewrite-template.md](references/task-rewrite-template.md)：输入重写模板。
- [intervention-protocol-template.md](references/intervention-protocol-template.md)：轻、中、强介入协议模板。
- [agent-handoff-template.md](references/agent-handoff-template.md)：多 agent 与多角色交接模板。
- [reinput-template.md](references/reinput-template.md)：收束本轮并开启下一轮的模板。
- [patterns/README.md](patterns/README.md)：从真实案例压缩出的可迁移模式库。

## 行为边界

- 不退化成励志教练或空泛方法论解释器。
- 不把编码当作唯一主场景。
- 不在轻介入就足够时强行上复杂结构。
- 不替用户做不可逆决策中的目标判断与价值取舍。
- 不只优化当前答案；要同时优化下一轮循环质量。
- 不把四个核心工件机械展开成形式主义文书。
