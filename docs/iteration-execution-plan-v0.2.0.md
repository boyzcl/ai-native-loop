# AI Native Loop v0.2.0 Iteration Execution Plan

## Objective

把 `ai-native-loop` 从“协议完整”推进到“执行完整”。

当前仓库的问题不在理念缺失，而在三个工程缺口：

- 抽象协议还没有被压成最小完备动作集
- 常见失败模式还没有形成显式纠偏层
- 真实案例还没有沉淀成可复用模式库

本轮目标不是继续扩写概念，而是补齐这三个缺口。

## Design Thesis

这轮迭代采用四个高杠杆框架，都是该领域最强做法的共同点。

### 1. Diagnose Before Prescribe

先判断循环断点，再决定怎么介入。

这意味着：

- 不先问“该给什么建议”
- 先问“当前坏在哪一环”

### 2. Minimum Complete Skill

一个协议型 Skill 必须有“最小完备动作集”，否则它只是一套理念。

对 `ai-native-loop` 来说，这个最小完备集收敛为四类工件：

- Diagnosis Card
- Task Packet
- Feedback Attribution Card
- Re-input Packet

### 3. Error-Driven Iteration

真正推动 Skill 变强的，不是补更多原则，而是把高频失败模式写出来。

因此，本轮必须显式沉淀：

- 常见误判
- 典型症状
- 根因判断
- 对应纠偏动作

### 4. Experience Compounding

案例如果只停留在叙述层，就不会复利。

所以需要引入模式层，把案例压缩为：

- 场景
- 触发条件
- 介入方式
- 关键工件
- 可迁移规律

## Target State

完成本轮后，仓库应达到以下状态：

1. Skill 的核心输出可以稳定收敛到四种标准工件。
2. 新用户可以快速判断当前问题属于哪类失败模式。
3. 已有案例可以被读取为模式，而不是只能作为故事阅读。
4. 仓库具备后续 benchmark 和版本迭代的骨架。

## Scope

### This Turn

本次直接执行 `Phase 1`。

### Deferred

以下内容纳入后续阶段，不在本次一次性做完：

- 大规模 benchmark 跑分
- 更多跨领域案例补齐
- 双语 README
- 可视化图表资产

## Execution Phases

## Phase 1: Core Execution Layer

目标：把抽象协议压成可直接调用的执行层。

交付物：

- `references/core-operating-primitives.md`
- `references/failure-modes.md`
- `patterns/README.md`
- 初始模式文件 2 篇
- `docs/benchmark-matrix.md`
- `SKILL.md` 导航与行为更新
- `README.md` 仓库入口更新

验收标准：

- Skill 主体能明确引用四个核心工件
- 至少覆盖 8 个高频失败模式
- 至少有 2 个模式化案例
- Benchmark 矩阵明确 4 类场景和通过标准

## Phase 2: Evidence Layer

目标：把“可用”变成“可验证”。

交付物：

- before/after 触发样例扩充
- benchmark 实测记录
- 研究、写作、产品、决策四类真实任务结果对照

验收标准：

- 至少 4 个固定测例
- 每个测例都有输入、介入、输出、再输入对照

## Phase 3: Release Layer

目标：把迭代变成稳定发布节奏。

交付物：

- `v0.2.0` release notes
- 更清晰的版本约束
- 对外发布说明与升级重点

## Execution Decision For This Turn

本次执行范围确定为：

- 完成 `Phase 1`
- 不在当前回合内追求 `Phase 2` 的完整实测
- 但会把 benchmark 结构先搭好，避免后续继续凭感觉迭代

## Work Breakdown

### Step 1

定义四个核心工件，并明确它们和轻 / 中 / 强介入的映射关系。

### Step 2

补一份失败模式库，把“常见误用”和“该如何纠偏”写成工程说明。

### Step 3

建立模式目录，把 `Case 01` 和 `Case 02` 压缩为复用模式。

### Step 4

补 benchmark 矩阵，让后续迭代可验证。

### Step 5

更新 `SKILL.md`、`README.md`、`CHANGELOG.md` 和 `agents/openai.yaml`，把新增能力接入主入口。

## Risks

### Risk 1

把协议压得太厚，导致一线使用成本上升。

控制方式：

- 四个核心工件必须都支持短版
- 默认优先最小充分输出

### Risk 2

失败模式写成概念总结，而不是可纠偏规则。

控制方式：

- 每条失败模式都必须包含症状、根因、纠偏动作

### Risk 3

模式库退化成案例摘要。

控制方式：

- 每篇模式都必须抽出可迁移规律

## Completion Criteria

当以下条件满足时，可认为本轮执行达标：

- 方案文档已落地
- `Phase 1` 交付物已创建并接入主文档
- 仓库仍保持可用、结构清晰、版本记录完整

## This Turn Status

- 方案输出：已完成
- `Phase 1` 执行：已完成
- 主文档接入：已完成
- 验证：已完成最小有效校验
- 提交：待执行
