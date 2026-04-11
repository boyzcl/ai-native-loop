# Benchmark Results v0.2.0

## Scope

本轮 benchmark 基于 4 个真实知识工作样本，对 `ai-native-loop` 的结构性效果进行回放式评估。

测试场景：

- 研究分析
- 写作表达
- 产品推进
- 决策整理

对应测例：

- [benchmark-01-research-analysis-mrna.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-01-research-analysis-mrna.md)
- [benchmark-02-writing-expression-harness.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-02-writing-expression-harness.md)
- [benchmark-03-product-progression-proxy-fix.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-03-product-progression-proxy-fix.md)
- [benchmark-04-decision-structuring-skincare.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-04-decision-structuring-skincare.md)

## Method Note

这是一轮基于真实工件链的回放式 benchmark，不是双盲 A/B 实验。

它验证的是：

- Skill 是否能把任务压成稳定工件
- 反馈是否能进入归因结构
- 下一轮输入是否真的被改写

它暂时不验证：

- 不同模型之间的统计显著性差异
- 严格受控条件下的输出时间和成本优势

## Score Table

| Scenario | clarity | executability | feedback_quality | reinput_quality | transferability | average |
|---|---:|---:|---:|---:|---:|---:|
| Research Analysis | 5.0 | 4.8 | 4.8 | 4.9 | 4.8 | 4.86 |
| Writing Expression | 4.7 | 4.8 | 4.6 | 4.7 | 4.6 | 4.68 |
| Product Progression | 4.8 | 4.9 | 4.7 | 4.6 | 4.8 | 4.76 |
| Decision Structuring | 4.6 | 4.5 | 4.4 | 4.3 | 4.7 | 4.50 |
| **Overall Average** | **4.78** | **4.75** | **4.63** | **4.63** | **4.73** | **4.70** |

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

结论：**通过**。

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

1. 补决策整理场景的更多模式和失败边界
2. 增加 before/after 触发样例
3. 把这 4 个 benchmark 做成更标准化的可重复测试模板
4. 在后续版本中补充 live benchmark，而不只做回放 benchmark
