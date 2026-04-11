# Decision Structuring Pattern

## Scene

用户手上已经有不少信息、材料或研究，但这些内容还不能直接支持实际判断；最终目标不是“理解更多”，而是“把判断真正做出来”。

## Trigger

出现以下信号时触发：

- 用户说“我看了很多资料，但还是不知道怎么选”
- 输出一旦停留在研究综述，用户仍无法采取行动
- 任务包含明显的价值判断边界，AI 不能越权替用户拍板

## Intervention

默认 `medium`。

推荐动作：

1. 先用 `Diagnosis Card` 确认断点是不是“研究层没有进入决策层”。
2. 用 `Task Packet` 重写决策对象、约束、成功信号与边界。
3. 用 `Feedback Attribution Card` 抓住“用户为什么仍不能做决定”。
4. 用 `Re-input Packet` 把研究框架折叠成选项、权衡、分层与边界。

## Artifacts

优先产出：

- 决策导向的任务包
- 选项或品类级分层结构
- 显式边界说明
- 下一轮决策输入

## Common Failure

最常见失败：

- 把研究结构直接当成决策结构
- AI 用强推荐替代用户自己的偏好判断
- 输出很多分析，但用户仍无法做选择

## Transfer Rule

这个模式可迁移到：

- 消费决策
- 工具选型
- 产品路线优先级判断
- 预算配置与资源取舍

核心迁移规律：

> 决策任务最需要的不是更多材料，而是把材料重组为可判断的选项、边界和权衡。

## Source Trace

- Source field note: [field-note-01-decision-structuring-skincare.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/field-notes/field-note-01-decision-structuring-skincare.md)
- Validated benchmark: [benchmark-04-decision-structuring-skincare.md](/Users/boyzcl/Documents/AI%20native/ai-native-loop/docs/benchmarks/benchmark-04-decision-structuring-skincare.md)
