# Benchmark Matrix

## Purpose

这份矩阵用于后续评估 `ai-native-loop` 是否真的改善了工作循环，而不是只让输出看起来更结构化。

## Evaluation Rule

每个测例都至少记录：

- 原始请求
- baseline 条件
- candidate 条件
- 初始卡点
- 介入等级
- 产出的核心工件
- 输出结果
- 下一轮输入是否得到改写

默认不再只看单次回放结果，而至少比较：

1. `baseline`
   - 不使用 `ai-native-loop`，或仅给极轻提示
2. `candidate`
   - 使用当前版本 `ai-native-loop`

对重要能力声明，建议再加：

3. `previous`
   - 上一个稳定版本或上一个实验版本

## Benchmark Scenarios

| Scenario | Typical Input | Primary Risk | Expected Artifacts | Pass Criteria |
|---|---|---|---|---|
| 研究分析 | 材料多、结论不稳、来源混杂 | 事实与推断混杂 | Diagnosis Card + Task Packet + Feedback Attribution Card + Re-input Packet | 形成可验证的研究结构，并能显式标注信息缺口 |
| 写作表达 | 有想法、有素材，但无法成稿 | 直接写终稿导致结构漂移 | Diagnosis Card + Task Packet + Re-input Packet | 形成可继续扩写的稳定结构，且下一轮输入更清楚 |
| 产品推进 | 需求、方案、发布准备散乱 | 多部件同时运动导致推进失真 | Diagnosis Card + Task Packet + Feedback Attribution Card | 明确当前轮目标、交付物和检查点 |
| 决策整理 | 信息很多但不能形成判断 | 把价值判断错误外包给 AI | Diagnosis Card + Task Packet + Feedback Attribution Card | 选项、权衡和决策权边界清晰，不替用户做不可逆决定 |
| 多 Agent 协作 | 一个总任务包含多个可分离工作流 | 拆分失当导致并行失真或结果不可回收 | Diagnosis Card + Task Packet + 子 agent 最小输入包 + handoff artifact + Re-input Packet | 明确拆与不拆边界，且主 agent 能稳定整合回收物 |

## Scoring Lens

每个测例建议至少按以下八项打分：

- `clarity`
  当前轮目标是否更清楚。
- `executability`
  是否形成了可执行任务包。
- `boundary_control`
  是否清楚保留用户 / 主 agent 的判断边界。
- `feedback_quality`
  反馈是否进入归因结构。
- `reinput_quality`
  下一轮输入是否真的被改写。
- `transferability`
  该做法是否可迁移到同类任务。
- `context_efficiency`
  是否减少了无关上下文和重复叙事。
- `real_task_helpfulness`
  是否真实降低了当前任务阻塞。

每项可用 1 到 5 分。

统一评分细则见 [evaluation-rubric.md](evaluation-rubric.md)。

## Comparison Workflow

建议顺序：

1. 先判断 `candidate` 是否过最低门槛
2. 再做 `baseline` vs `candidate` pairwise 比较
3. 如果是版本迭代，再看 `previous` vs `candidate`
4. 最后才写总体结论

如果没有 baseline，不应下“明显更好”的强结论。

## Success Bar For v0.2.0

`v0.2.0` 核心通过标准至少应达到：

- 4 个固定测例全部存在
- 每个测例都有四段式记录
- 平均分不低于 4.0
- `reinput_quality` 不得低于 3.5

## Current Status

- 矩阵已建立
- 4 个固定测例已补齐
- 汇总结果见 [benchmark-results-v0.2.0.md](benchmark-results-v0.2.0.md)
- 本轮回放式 benchmark 结果：平均分 `4.70`，`reinput_quality` 平均分 `4.63`，达到 `v0.2.0` 通过标准
- 多 Agent 协作 benchmark 场景已建立，见 [benchmark-05-multi-agent-decomposition.md](benchmarks/benchmark-05-multi-agent-decomposition.md)
- 下一轮目标：把 4 个固定测例升级为 baseline + pairwise 记录，并开始用 [experiment-log-template.md](experiment-log-template.md) 跟踪迭代
