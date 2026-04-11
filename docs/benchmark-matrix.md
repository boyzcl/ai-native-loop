# Benchmark Matrix

## Purpose

这份矩阵用于后续评估 `ai-native-loop` 是否真的改善了工作循环，而不是只让输出看起来更结构化。

## Evaluation Rule

每个测例都至少记录：

- 原始请求
- 初始卡点
- 介入等级
- 产出的核心工件
- 输出结果
- 下一轮输入是否得到改写

## Benchmark Scenarios

| Scenario | Typical Input | Primary Risk | Expected Artifacts | Pass Criteria |
|---|---|---|---|---|
| 研究分析 | 材料多、结论不稳、来源混杂 | 事实与推断混杂 | Diagnosis Card + Task Packet + Feedback Attribution Card + Re-input Packet | 形成可验证的研究结构，并能显式标注信息缺口 |
| 写作表达 | 有想法、有素材，但无法成稿 | 直接写终稿导致结构漂移 | Diagnosis Card + Task Packet + Re-input Packet | 形成可继续扩写的稳定结构，且下一轮输入更清楚 |
| 产品推进 | 需求、方案、发布准备散乱 | 多部件同时运动导致推进失真 | Diagnosis Card + Task Packet + Feedback Attribution Card | 明确当前轮目标、交付物和检查点 |
| 决策整理 | 信息很多但不能形成判断 | 把价值判断错误外包给 AI | Diagnosis Card + Task Packet + Feedback Attribution Card | 选项、权衡和决策权边界清晰，不替用户做不可逆决定 |

## Scoring Lens

每个测例建议按以下五项打分：

- `clarity`
  当前轮目标是否更清楚。
- `executability`
  是否形成了可执行任务包。
- `feedback_quality`
  反馈是否进入归因结构。
- `reinput_quality`
  下一轮输入是否真的被改写。
- `transferability`
  该做法是否可迁移到同类任务。

每项可用 1 到 5 分。

## Success Bar For v0.2.0

至少应达到：

- 4 个固定测例全部存在
- 每个测例都有四段式记录
- 平均分不低于 4.0
- `reinput_quality` 不得低于 3.5

## Current Status

- 矩阵已建立
- 固定测例待逐步补齐
