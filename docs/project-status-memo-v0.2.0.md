# Project Status Memo and Next Decision

Date: `2026-04-11`

Scope: 基于当前仓库文件、讨论记录与 `git` 状态，对 `ai-native-loop` 的真实进度、结构性缺口与下一步决策做一次正式收束。

## Executive Summary

截至 `2026-04-11`，`ai-native-loop` 已经完成了从“协议完整”到“第一层执行完整”的跃迁，但还没有完成从“作者可运作”到“外部用户可复利”的跃迁。

更准确地说：

- `v0.1.0` 是当前正式版本。
- `v0.2.0` 的核心工程交付已经在主线上完成，并已有 benchmark 结果支撑，但尚未形成正式 release。
- 当前最主要的未闭环问题，不再是协议内容不够，而是两类“操作系统级缺口”：
  - 多 Agent 协作规则只有模板，没有分解与回收规则。
  - 经验沉淀机制已经存在，但仍然主要依赖作者手动触发，尚未变成开源用户默认可受益的机制。

因此，下一阶段不应继续泛化补内容，而应优先补“运行机制层”。

## Current Snapshot

项目当前的可确认事实如下：

- 仓库路径：[/Users/boyzcl/Documents/AI native/ai-native-loop](/Users/boyzcl/Documents/AI%20native/ai-native-loop)
- 当前分支：`main`
- 当前 HEAD：`b27bb0f`
- 本地工作区：干净
- 远端同步状态：已与 `origin/main` 对齐
- 当前 tag：`v0.1.0`

版本判断：

- [README.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/README.md) 仍声明当前版本为 `v0.1.0`，并将 `v0.2.0` 标记为 “execution in progress”。
- [SKILL.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/SKILL.md) 的 metadata version 仍是 `0.1.0`。
- [CHANGELOG.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/CHANGELOG.md) 中新增成果仍位于 `Unreleased`。

这意味着：

> `v0.2.0` 的事实状态是“已实质完成 Phase 1，并已补齐 benchmark 证据，但尚未正式发布”。

## What Is Already True

以下能力已经不是计划，而是仓库中的既成事实。

### 1. 四个核心工件已经落地

[references/core-operating-primitives.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/core-operating-primitives.md) 已经把 `Diagnosis Card`、`Task Packet`、`Feedback Attribution Card`、`Re-input Packet` 写成稳定工件，并接入 [SKILL.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/SKILL.md)。

这代表项目已经具备“最小完备动作集”，不再只是理念集合。

### 2. 失败模式层已经存在

[references/failure-modes.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/failure-modes.md) 已覆盖高频误判、根因与纠偏动作。

这代表项目已经开始从“补更多原则”转向“围绕真实失败修系统”。

### 3. 经验沉淀链条已经出现雏形

当前仓库已经具备以下链条：

- case: [docs/cases/](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/cases)
- pattern: [patterns/README.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/patterns/README.md)
- failure mode: [references/failure-modes.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/failure-modes.md)
- benchmark: [docs/benchmark-matrix.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmark-matrix.md) 与 [docs/benchmark-results-v0.2.0.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmark-results-v0.2.0.md)

这说明经验沉淀已经从“案例展示”升级成“可评估的结构化沉淀”。

### 4. 第一轮 benchmark 已经跑通

[docs/benchmark-results-v0.2.0.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmark-results-v0.2.0.md) 给出了 4 个固定测例与总平均分 `4.70`。

这代表当前项目已经不再只靠作者主观判断，而开始具备最小验证能力。

## What Is Not Yet True

以下能力在讨论中被反复提到，但目前还没有被真正做成工程事实。

### 1. 多 Agent 协作还没有规则层

当前仓库与多 Agent 直接相关的内容，主要只有：

- [references/agent-handoff-template.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/agent-handoff-template.md)
- [references/failure-modes.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/references/failure-modes.md) 中关于 “多 Agent 协作没有交接物” 的失败模式

缺失的是独立的规则层文档，用来写硬：

- 什么时候该拆 agent
- 什么时候不该拆
- 拆分粒度如何判断
- 主 agent 保留什么
- 子 agent 的最小输入包是什么
- 如何定义回收物与汇总格式
- 什么情况下分治比单线程更差

因此，当前项目只能说“支持多 Agent 场景”，还不能说“已经具备多 Agent 操作系统”。

### 2. 经验沉淀机制仍然是作者运营型，不是用户默认型

这是当前最关键的结构判断。

现有链条 `case -> pattern -> failure mode -> benchmark -> 反哺 SKILL` 是成立的，但它仍然主要靠作者主动整理、主动提炼、主动补档。

这意味着它具备的是：

- 经验可沉淀
- 经验可复盘
- 经验可被二次结构化

但它还不具备：

- 默认使用过程中自然产生沉淀
- 外部用户不懂内部机制也能贡献有效经验
- 沉淀材料能低摩擦地流入 pattern / failure mode / benchmark

换句话说，当前机制更像“编辑部流程”，还不是“产品内生机制”。

## Strong-Brain Frame

如果用该领域最强的产品/系统脑来处理这个问题，通常不会从“再多补一点内容”开始，而会先做三层拆分。

### 1. 区分协议完整、执行完整、复利完整

这是最基本的成熟度框架。

- 协议完整：理念、边界、动作集是否成立
- 执行完整：能否稳定产出标准工件
- 复利完整：每次使用是否能低摩擦地反哺系统

`ai-native-loop` 现在已经越过了前两层的主要门槛，但第三层明显还没完成。

### 2. 优化默认路径，而不是优化理想路径

强系统不会假设用户会额外做整理，也不会假设作者永远在线做二次加工。

真正有开源参考意义的机制，必须优先优化：

- 第一次使用时会自然发生什么
- 一次成功/失败之后，最少需要补什么就能进入系统
- 没有作者参与时，系统是否仍能累积有效经验

如果默认路径不工作，再强的 pattern 库都只是展示层资产。

### 3. 用“自动化阶梯”而不是“全自动幻觉”

这个领域里最稳健的做法，不是追求一开始就全自动，而是做自动化阶梯：

1. 手动
2. 手动但有标准 intake
3. 默认带模板输出
4. 半自动汇总
5. 自动进入版本迭代循环

现在的 `ai-native-loop` 大体停在第 1 到第 2 阶段之间，还没有进入“默认带结构沉淀”的阶段。

## Core Diagnosis

当前真正的瓶颈，不是项目缺少文档，而是项目还缺一个“经验操作层”。

这个瓶颈具体表现为三点：

### 1. 模式提炼不在默认工作流中

pattern 现在存在，但 case 不会自然变成 pattern，仍需要作者主动抽取。

### 2. benchmark 还是回放式，不是持续式

benchmark 已经有用，但它更像阶段性验证，不是持续运行的质量回路。

### 3. 失败模式与版本叙事还没有绑定

当前 [CHANGELOG.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/CHANGELOG.md) 仍以 “新增了什么” 为主，而不是 “发现了什么失败，因此修了什么机制”。

这会削弱开源用户对项目迭代逻辑的理解，也削弱经验复利。

## Decision

下一阶段的核心决策应当是：

> 不把重点放在“再补更多内容”，而把重点放在“让经验沉淀变成默认可发生的机制”。

这条决策下，优先级应改写为：

### P0. 建立多 Agent 规则层

原因不是它最炫，而是它是当前唯一明确悬空的高优先级能力声明。

建议新增：

- `references/multi-agent-decomposition.md`
- `patterns/multi-agent-decomposition.md`
- `docs/benchmarks/benchmark-05-multi-agent-decomposition.md`

### P0. 建立经验沉淀 intake 层

这是当前最该补的“运行机制层”。

目标不是直接全自动，而是把经验沉淀从“作者手工写文档”升级成“默认有 intake，再由系统提炼”。

建议新增：

- `references/experience-compounding-loop.md`
- `docs/field-note-template.md`
- `patterns/pattern-intake-template.md`

应明确四件事：

- 一次任务结束后，最少记录哪些字段
- 哪些信号说明它值得进入 pattern
- 哪些信号说明它应该进入 failure mode
- 哪些样本值得进入 benchmark

### P1. 把版本迭代改成假设驱动

建议把版本叙事改写成：

- 发现了哪类失败
- 该失败为何反复出现
- 本版本加入了哪条规则或工件
- 预期改善哪个评分维度

这一步会显著提升项目的可解释性与可信度。

### P1. 补短促强辨识度的 before/after

这不是装饰，而是降低首次理解成本。

README 现在更像结构化入口，但还不是“看一眼就知道为什么有用”的入口。

## Recommended Execution Model

建议按三段推进，而不是一次性继续摊大。

### Track A: Rule Layer

目标：把多 Agent 从模板能力升级为规则能力。

交付物：

- `references/multi-agent-decomposition.md`
- 一个对应 pattern
- 一个对应 benchmark

验收标准：

- 明确拆与不拆的边界
- 明确主 agent / 子 agent 的最小输入包
- 明确固定回收物格式

### Track B: Intake Layer

目标：把经验沉淀从“作者手写总结”升级成“默认可采集结构”。

交付物：

- `docs/field-note-template.md`
- `patterns/pattern-intake-template.md`
- `references/experience-compounding-loop.md`
- `SKILL.md` 中一段明确的使用后回收规则

验收标准：

- 一次任务完成后，能用统一模板记录
- 记录内容足以判断是否进入 pattern / failure mode / benchmark
- 沉淀动作不依赖长篇回顾

### Track C: Release Layer

目标：让 `v0.2.0` 与后续版本具备更强的假设驱动感。

交付物：

- `v0.2.0` release notes
- 按失败模式重写的 changelog 叙事
- README 的短示例区

验收标准：

- 外部读者能看出“这个版本在修什么”
- 不是只看到“新增了哪些文件”

## Why This Order

这个顺序背后的判断很简单：

- 如果先继续补案例，只会继续放大“作者运营型沉淀”
- 如果先补多 Agent 规则和 intake 机制，后续案例才会真正进入复利结构
- 如果没有复利结构，benchmark 很快会变成一次性展示资产

因此，下一阶段的目标不是“更多”，而是“更能自己长”。

## Non-Goals For The Next Turn

下一阶段不建议优先投入：

- 大量新增泛案例
- 继续扩写方法论文本
- 追求全自动经验沉淀
- 大规模视觉化资产

这些都不是当前最短板。

## Bottom Line

`ai-native-loop` 现在最值得肯定的地方，是它已经证明自己不是只会讲理念，而是已经具备一套可验证、可迁移、可基准测试的协议结构。

它现在最需要补的，也已经很清楚：

不是更多内容，而是更强的运行机制。

下一阶段最正确的方向，不是继续把仓库写得更满，而是把下面这条链真正做顺：

> 使用 -> intake -> pattern / failure mode -> benchmark -> version decision

一旦这条链跑顺，`ai-native-loop` 才会从“高质量作者项目”进入“外部用户也能持续受益的开源系统”。
