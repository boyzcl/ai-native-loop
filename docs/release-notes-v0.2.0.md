# Release Notes v0.2.0

Status: `Draft`

Date: `2026-04-11`

Current release truth lives in [release-manifest.md](release-manifest.md).

## Release Thesis

`v0.2.0` 不是一次“补更多概念”的版本，而是一次把 `ai-native-loop` 从协议层推进到执行层、验证层和初步复利层的版本。

这个版本真正修复的，不是单个文档缺失，而是三类高频失败：

- 协议存在，但没有最小完备动作集
- 任务做完了，但失败模式无法沉淀
- 案例存在，但经验不能稳定进入下一轮系统

## What Changed

### 1. The Skill Now Has Four Stable Operating Primitives

新增并接入四个稳定工件：

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`

这让 `ai-native-loop` 不再只是解释工作流，而能把介入收敛到固定输出形状。

核心文件：

- [core-operating-primitives.md](../references/core-operating-primitives.md)

### 2. Failure Modes Are Now Explicit

新增失败模式层，把常见误判从隐性经验改成显式纠偏规则。

这意味着系统开始围绕失败迭代，而不只是围绕“还能补什么内容”迭代。

核心文件：

- [failure-modes.md](../references/failure-modes.md)

### 3. Experience Now Has A Promotion Path

这个版本补了最关键的复利骨架：

- case
- field note
- pattern
- failure mode
- benchmark

它还不是全自动系统，但已经不再只有作者手工写总结这一条路。

核心文件：

- [experience-compounding-loop.md](../references/experience-compounding-loop.md)
- [field-note-template.md](field-note-template.md)
- [pattern-intake-template.md](../patterns/pattern-intake-template.md)

### 4. Multi-Agent Support Moved From Template To Rule Layer

此前仓库只有多 Agent handoff 模板。

`v0.2.0` 开始把这块写成规则层：

- 什么时候该拆
- 什么时候不该拆
- 子 agent 最小输入包是什么
- 主 agent 必须保留什么
- handoff artifact 应如何统一

核心文件：

- [multi-agent-decomposition.md](../references/multi-agent-decomposition.md)
- [multi-agent-decomposition.md](../patterns/multi-agent-decomposition.md)
- [benchmark-05-multi-agent-decomposition.md](benchmarks/benchmark-05-multi-agent-decomposition.md)

## Validation

本版本目前具备以下验证证据：

- 4 个固定 benchmark 的 retrospective 记录已迁移到统一格式
- 汇总平均分 `4.70`
- `reinput_quality` 平均分 `4.63`
- 当前最弱场景已明确为决策整理
- baseline + pairwise 重跑入口已经建立，但尚未补齐

验证文件：

- [benchmark-matrix.md](benchmark-matrix.md)
- [benchmark-results-v0.2.0.md](benchmark-results-v0.2.0.md)
- [benchmark-run-template.md](benchmarks/benchmark-run-template.md)
- [runs/README.md](benchmarks/runs/README.md)

## Demonstration Chain Added In This Draft

为了避免经验复利层停留在抽象描述，本轮额外补了一条真实示范链：

- Field note: [field-note-01-decision-structuring-skincare.md](field-notes/field-note-01-decision-structuring-skincare.md)
- Pattern: [decision-structuring.md](../patterns/decision-structuring.md)
- Failure mode: [failure-modes.md](../references/failure-modes.md)
- Benchmark: [benchmark-04-decision-structuring-skincare.md](benchmarks/benchmark-04-decision-structuring-skincare.md)

这条链的意义不是多一个案例，而是证明：

> 一次真实任务，现在已经可以从原始回收物被提升为 pattern、failure mode 和 benchmark 资产。

## What This Release Still Does Not Solve

`v0.2.0` 仍未完全解决以下问题：

- 经验沉淀仍然不是全自动
- 多 Agent benchmark 仍只有固定场景，尚无实测结果
- 决策整理仍是当前最弱项
- README 还可以继续增强短促强辨识度的 before/after
- baseline + pairwise 验证刚开始建立，尚未覆盖全部固定测例

## Upgrade Guidance

如果你已经在使用 `v0.1.0` 风格的 `ai-native-loop`，升级到 `v0.2.0` 后，建议默认这样用：

1. 不直接问“给答案”，先让系统先出 `Diagnosis Card` 和 `Task Packet`
2. 对中介入以上任务，默认先保留一个 `Loop Recovery Block`，只有值得沉淀时再扩成 field note
3. 遇到重复问题时，先看它是不是已经能进入 failure mode
4. 需要并行协作时，先过多 Agent 的 split / don't-split 规则

## Release Judgment

这是一个“把协议做成运行系统”的版本，而不是“继续把理念写得更漂亮”的版本。

如果 `v0.1.0` 证明了这个 Skill 值得公开发布，`v0.2.0` 的意义在于：

> 它开始证明这个 Skill 可以围绕失败、证据和经验复利持续变强。
