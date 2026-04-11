# Benchmark Results v0.2.0

## Scope

本轮 benchmark 基于 4 个真实知识工作样本，对 `ai-native-loop` 的结构性效果进行回放式评估。

测试场景：

- 研究分析
- 写作表达
- 产品推进
- 决策整理

对应测例：

- [benchmark-01-research-analysis-mrna.md](benchmarks/benchmark-01-research-analysis-mrna.md)
- [benchmark-02-writing-expression-harness.md](benchmarks/benchmark-02-writing-expression-harness.md)
- [benchmark-03-product-progression-proxy-fix.md](benchmarks/benchmark-03-product-progression-proxy-fix.md)
- [benchmark-04-decision-structuring-skincare.md](benchmarks/benchmark-04-decision-structuring-skincare.md)

## Method Note

这是一轮基于真实工件链的回放式 benchmark，不是双盲 A/B 实验。

它验证的是：

- Skill 是否能把任务压成稳定工件
- 反馈是否能进入归因结构
- 下一轮输入是否真的被改写

它暂时不验证：

- 不同模型之间的统计显著性差异
- 严格受控条件下的输出时间和成本优势

这意味着：

- 当前结果可作为 `v0.2.0` 的内部验证证据
- 不能直接当作“外部强证明”
- 下一轮必须迁移到 baseline + pairwise 的统一记录格式

统一执行模板见 [benchmark-run-template.md](benchmarks/benchmark-run-template.md)。
第一批迁移后的 run records 见 [runs/README.md](benchmarks/runs/README.md)。

## Retrospective Score Table

| Scenario | clarity | executability | feedback_quality | reinput_quality | transferability | average |
|---|---:|---:|---:|---:|---:|---:|
| Research Analysis | 5.0 | 4.8 | 4.8 | 4.9 | 4.8 | 4.86 |
| Writing Expression | 4.7 | 4.8 | 4.6 | 4.7 | 4.6 | 4.68 |
| Product Progression | 4.8 | 4.9 | 4.7 | 4.6 | 4.8 | 4.76 |
| Decision Structuring | 4.6 | 4.5 | 4.4 | 4.3 | 4.7 | 4.50 |
| **Overall Average** | **4.78** | **4.75** | **4.63** | **4.63** | **4.73** | **4.70** |

## Migration Plan To Baseline Evaluation

下一轮不再只保留 retrospective 分数，而是对每个固定测例至少补三段：

1. `baseline`
   - 不使用 `ai-native-loop`，或仅给极轻提示
2. `candidate`
   - 使用当前版本 `ai-native-loop`
3. `optional previous`
   - 如有版本实验，再补上一版

并按 [evaluation-rubric.md](evaluation-rubric.md) 做 pairwise 结论。

## Current Interpretation Boundary

当前这份结果最适合支持以下结论：

- `ai-native-loop` 已经具备内部最小验证能力
- 它在研究分析、产品推进场景里表现更强
- 决策整理仍是当前最弱项

当前这份结果不适合直接支持以下强结论：

- 相比 baseline 已有稳定显著优势
- 多 Agent 能力已经得到实测验证
- 输出成本和时间优势已被证明

## Result Against v0.2.0 Success Bar

`benchmark-matrix.md` 定义的通过标准是：

- 4 个固定测例全部存在
- 每个测例都有四段式记录
- 平均分不低于 4.0
- `reinput_quality` 不得低于 3.5

本轮结果：

- 固定测例：已满足
- 四段式记录：已满足
- 平均分：`4.70`
- `reinput_quality` 平均分：`4.63`

结论：**通过 `v0.2.0` 当前内部通过线，但仍需升级为 baseline 评估格式。**

## Main Findings

### 1. Research 和 Product 场景最强

这两个场景的共同特征是：

- 多工件并行
- 风险和反馈都很可见
- 任务天然需要检查点

`ai-native-loop` 在这类场景里最容易发挥结构优势。

### 2. Writing 场景的价值在于“把写作流程系统化”

它不是简单提高文笔，而是把：

- 大纲
- 初稿
- 自审
- 终稿

压成有回收物的循环。

### 3. Decision 场景仍然是当前最低分

最低分不是因为失效，而是因为：

- 决策类任务更容易越过用户自己的判断边界
- `reinput_quality` 更难做得很强

这说明下一轮迭代最值得继续增强的是决策整理相关模式。

## Next Iteration Implication

如果继续推进 `v0.2.0`，优先级建议如下：

1. 用 [benchmark-run-template.md](benchmarks/benchmark-run-template.md) 重跑 4 个固定测例
2. 为每个测例补 baseline + pairwise 判断
3. 补决策整理场景的更多模式和失败边界
4. 在后续版本中补充 live benchmark，而不只做回放 benchmark
