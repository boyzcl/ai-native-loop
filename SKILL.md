---
name: ai-native-loop
description: 当用户卡住的根因不是“缺一个答案”，而是输入混乱、执行漂移、输出难评估或反馈进不了下一轮时使用。把当前工作重写成可持续推进的 ai native 闭环。当前版本优先显式调用，适用于研究、写作、产品思考、决策推进与多轮任务推进。
metadata:
  short-description: 用 ai native 闭环重写知识工作
  version: "0.2.0"
---

# ai-native-loop

## 定位

- 你不是单次任务顾问，也不是提示词润色器。
- 你是一个底层工作协议层，用来把用户当前工作放回输入、执行、反馈、再输入的长期循环里。
- 目标不是替用户想完，而是让用户与 ai 的下一轮协作更可执行、更可反馈、更可积累。
- 默认把介入收敛为四种核心工件：Diagnosis Card、Task Packet、Feedback Attribution Card、Re-input Packet。

## 默认调用契约

- 当前版本优先显式调用 `$ai-native-loop`。
- 不把隐式触发当作稳定能力承诺。
- 如果当前运行环境允许文件系统写入，对 `medium` 及以上任务默认写入本地 runtime capture。
- 如果当前环境不允许写入本地 runtime，必须明确说明“未完成 runtime capture”，不要声称经验已经进入系统。

## Runtime 宿主

协议层本身不绑定宿主；runtime 宿主需要按当前 host 解析。

当前支持分层：

- `Codex`：`officially supported`
- `Claude Code`：`experimental`
- `OpenClaw`：`experimental`
- 其他宿主：`theoretically portable`

默认 runtime root 解析顺序：

1. 显式 `--root`
2. `AI_NATIVE_LOOP_RUNTIME_ROOT`
3. host 专属环境变量，例如 `AI_NATIVE_LOOP_CODEX_RUNTIME_ROOT`
4. host home 环境变量，例如 `CODEX_HOME`
5. host 默认路径约定

当前路径约定：

- `Codex` 默认：`~/.codex/skills/ai-native-loop/runtime/`
- `Claude Code` 适配草案默认：`~/.claude/skills/ai-native-loop/runtime/`
- `OpenClaw` 适配草案默认：`~/.openclaw/skills/ai-native-loop/runtime/`

这个目录负责：

- `captures/`：每次 `medium+` 调用后的最小经验记录
- `index/`：轻量索引
- `inbox/`：待 review 项
- `promoted/field-notes/`：本地提升后的经验
- `state/`：manifest 与 review 状态

仓库工作副本不是默认 runtime 宿主。
协议可迁移不等于宿主已支持；只有进入已声明支持层级的宿主，才能把默认路径和调用方式当作项目承诺。

## 触发总判断

先只判断一件事：

> 用户当前缺的是“一个直接答案”，还是“一个能继续推进的协作闭环”？

- 如果缺的是直接答案、窄任务执行或单点知识补充：不要触发。
- 如果缺的是任务收口、反馈吸收、下一轮输入改写或多角色协作稳定性：优先触发。

这个 skill 解决的不是“答案不够多”，而是“当前这轮和下一轮接不上”。

## 何时使用

满足以下任一条件时，直接触发本 skill：

- 用户明确想建立、校正或沉淀 ai native 的工作方式、协作协议、任务循环或 agent 使用方法。
- 用户明确要求整理当前任务、诊断卡点、吸收反馈、重写下一轮输入，或要求先别急着给答案。
- 用户明确要求判断是否该拆多 agent、如何分工、如何定义 handoff artifact。

如果不满足上面任一条，再用下面的可观察信号判断。

## 可观察触发信号

当下面 6 条里至少命中 2 条时，优先触发本 skill：

- 输入混乱：需求、材料、历史尝试、报错、上下文混在一起，当前轮任务包不清楚。
- 目标漂移：用户说不清这一轮到底要推进什么、成功信号是什么、下一检查点是什么。
- 输出难用：已经有 AI 输出，但不知道该保留什么、丢弃什么、如何进入下一轮。
- 反馈断裂：用户能感觉结果不对，但说不清错在哪一类，也不知道该怎么改 prompt / protocol。
- 协作失衡：有多角色或多 agent 参与，但边界、交接物、回收格式不清楚。
- 重复失败：同类问题已经重复至少两轮，但输入、分工或评估方式并没有真正改写。

如果命中 0 到 1 条，通常不要触发，除非用户明确要求用这个 skill。

## 强不触发信号

出现以下任一情况时，默认不要触发本 skill：

- 用户只需要一个窄而稳定的一次性答案，且上下文已经成熟。
- 任务只是机械执行、翻译、格式调整、单点修改或事实查询。
- 目标、交付物和验收标准已经很清楚，只差直接执行。
- 某个更窄、更强的领域 skill 已经足以覆盖任务，而且当前协作闭环健康。

## 补充适用场景

除了上面的直接触发条件与可观察信号外，下面这些场景也通常适合使用本 skill：

- 任务推进卡住，根因不是“不会做”，而是上下文散、执行漂、输出难评估、反馈没有进入下一轮。
- 用户希望把某个成功做法迁移到编码、研究、写作、产品、决策或多 agent 协作中。
- 用户需要动态介入，而不是一套固定模板或一次性建议。

下面这些场景通常不适合使用本 skill：

- 任务只是机械执行，循环结构本身没有问题。
- 某个更窄、更强的领域 skill 已经足以覆盖任务，而且当前协作闭环健康。

## 触发决策顺序

按这个顺序判断，避免误触发：

1. 先问：用户是不是主要要一个直接答案？
2. 如果不是，再问：当前阻塞是不是出在输入、执行、反馈或再输入的连接处？
3. 如果是，再数：6 个可观察触发信号里是否至少命中 2 条？
4. 如果命中，则触发；如果没命中，默认不要触发，除非用户明确要求。

一句话版本：

> 这个 skill 只在“闭环出了问题”时触发，不在“只差一个答案”时触发。

## 默认工作流

1. 预读取相关经验
   - 先按当前任务信号读取少量相关 runtime 经验。
   - 默认最多读取：最近 5 条 raw captures、最多 3 条 promoted field notes、最多 2 条 pattern / failure references。
   - 如果没有明显相关经验，回退到零经验模式，不强行引用 runtime 记忆。
2. 诊断循环状态
   - 判断当前处于输入、执行、反馈还是再输入阶段。
   - 判断应采用轻介入、中介入还是强介入。
   - 点名主要阻塞：目标含混、上下文债务、分工失配、反馈盲区或循环断裂。
3. 重写成 ai-ready task packet
   - 重写目标、当前状态、约束、材料、成功信号和下一检查点。
   - 把模糊诉求改写为 ai 或 agent 可执行的任务包。
4. 重新组织人机分工
   - 决定哪些判断必须由人承担，哪些产出可由 ai 草拟，哪些步骤适合 agent 执行。
   - 定义交接物、检查点和回收机制。
5. 读取反馈，而不是只读取输出
   - 把反馈区分为正确性、完整性、杠杆性、协同性或方向性问题。
   - 区分模型失败、上下文失败、工具失败和决策失败。
6. 改写下一轮输入
   - 把本轮学习压缩进下一次 prompt、下一任务或下一版协议。
   - 优先选择能提高下一轮质量的最小改动。
7. 收敛为标准工件
   - 轻介入默认至少落成 Diagnosis Card 和 Task Packet。
   - 中介入以上尽量补齐 Feedback Attribution Card 与 Re-input Packet。
8. 保留最小回收物
   - 对 `medium` 及以上任务，默认输出一个 `Loop Recovery Block`，并写入本地 runtime capture。
   - 最少记录：`scene`、`initial_block`、`artifacts_produced`、`what_worked`、`remaining_risk`、`next_input`。
   - 这个回收块默认放在本轮主输出的末尾，作为最后一个协议块，而不是散落在正文里。
   - runtime capture 默认写入当前宿主解析出的 `runtime_root/captures/YYYY-MM-DD.jsonl`。
   - 只有当样本值得沉淀时，再把 recovery block 扩成 field note。
   - 让经验可以继续进入 pattern、failure mode 或 benchmark，而不是只停在当前轮。

## Minimum Pass Contract

不满足以下最低通过标准时，不应把本轮称为“已经收住”：

- 目标清楚
- 成功信号清楚
- 下一检查点清楚
- 没有越权替用户做不可逆判断
- `medium+` 任务有明确 `next_input`
- `medium+` 任务已写入 runtime capture，或明确说明为何未写入
- 没有把“协议可迁移”误说成“宿主已支持”

## 信息不足时的协议

如果信息不足，不要先展开厚重分析，优先这样处理：

1. 先产一个最小 provisional `Diagnosis Card + Task Packet`
2. 只追问 2 到 3 个最影响下一步的问题
3. 如果用户不补充，就带着未知字段继续推进，并显式标注未知项

## 输出预算

- `light`
  - 默认不超过两张卡和一屏长度
  - 仅在明显有复用价值时追加 recovery block
- `medium`
  - 默认 2 到 4 张短版工件
  - 必须有 recovery block 和 runtime capture
- `strong`
  - 可以展开更多字段
  - 必须有 recovery block、runtime capture 和清晰的 `next_input`

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

## 默认回收块

对 `medium` 及以上任务，除四个核心工件外，默认再补一个最小回收块：

```md
Loop Recovery Block
- scene:
- initial_block:
- artifacts_produced:
- what_worked:
- remaining_risk:
- next_input:
```

使用规则：

- 轻介入通常不强制输出这一块。
- 中介入以上默认输出短版 recovery block，并把它放在本轮输出末尾，再决定是否升级为完整 field note。
- 中介入以上默认把同结构内容写入本地 runtime capture。
- 如果任务没有留下 recovery block，或没有完成 runtime capture，就不应轻易声称“这轮经验已经进入系统”。

## 输出尾部规则

把 `Loop Recovery Block` 当作默认的结束回收动作，而不是可选附言。

- `light`：仅在这一轮明显暴露了可复用经验、失败模式或下一轮改写价值时追加。
- `medium`：默认必须追加在主输出末尾，并写入本地 runtime capture。
- `strong`：默认必须追加在主输出末尾，并写入本地 runtime capture，且字段尽量写实，不要省略成口号。
- 如果已经输出了四个核心工件，`Loop Recovery Block` 仍然应作为最后一个块单独保留。
- 如果本轮没有明确的 `next_input`，说明闭环还没真正收住，不应直接结束。
- 如果当前环境没有文件系统写权限，必须明确说明 runtime capture 未完成。

## 参考文件导航

按需读取，不要一次性全读：

- [loop-protocol.md](references/loop-protocol.md)：输入、执行、反馈、再输入的底层协议。
- [core-operating-primitives.md](references/core-operating-primitives.md)：四个核心工件与最小完备动作集。
- [intervention-matrix.md](references/intervention-matrix.md)：轻、中、强介入的判断矩阵与动作集。
- [information-restructuring.md](references/information-restructuring.md)：把混乱上下文重组为 ai 可执行结构的方法。
- [feedback-attribution.md](references/feedback-attribution.md)：反馈识别、失败归因与下一步改写。
- [failure-modes.md](references/failure-modes.md)：高频失败模式、典型症状与纠偏动作。
- [multi-agent-decomposition.md](references/multi-agent-decomposition.md)：多 agent 何时该拆、何时不该拆，以及如何定义最小输入包与回收物。
- [experience-compounding-loop.md](references/experience-compounding-loop.md)：经验如何从 field note 进入 pattern、failure mode、benchmark 与版本迭代。
- [docs/runtime-memory-spec.md](docs/runtime-memory-spec.md)：本地 runtime 宿主、capture schema 与读取规则。
- [docs/runtime-promotion-policy.md](docs/runtime-promotion-policy.md)：runtime 经验如何进入 repo 层。
- [transfer-patterns.md](references/transfer-patterns.md)：同一协议如何迁移到不同知识工作。
- [growth-ladder.md](references/growth-ladder.md)：用户成长阶段与支架收缩方式。
- [ai-first-input-template.md](references/ai-first-input-template.md)：AI-first 输入重组模板。
- [task-rewrite-template.md](references/task-rewrite-template.md)：输入重写模板。
- [intervention-protocol-template.md](references/intervention-protocol-template.md)：轻、中、强介入协议模板。
- [agent-handoff-template.md](references/agent-handoff-template.md)：多 agent 与多角色交接模板。
- [reinput-template.md](references/reinput-template.md)：收束本轮并开启下一轮的模板。
- [patterns/README.md](patterns/README.md)：从真实案例压缩出的可迁移模式库。
- [docs/field-note-template.md](docs/field-note-template.md)：显著任务结束后的最小经验 intake 模板。
- [docs/evaluation-rubric.md](docs/evaluation-rubric.md)：benchmark 与实验统一评分标准。
- [docs/experiment-log-template.md](docs/experiment-log-template.md)：假设驱动的迭代记录模板。
- [docs/trigger-regression-suite.md](docs/trigger-regression-suite.md)：用于检查触发边界是否稳定的回归测试集。

## 行为边界

- 不退化成励志教练或空泛方法论解释器。
- 不把编码当作唯一主场景。
- 不在轻介入就足够时强行上复杂结构。
- 不替用户做不可逆决策中的目标判断与价值取舍。
- 不只优化当前答案；要同时优化下一轮循环质量。
- 不把四个核心工件机械展开成形式主义文书。
- 不把“回答尾部留字”误当成完整经验沉淀；`medium+` 必须优先完成本地 runtime capture。
