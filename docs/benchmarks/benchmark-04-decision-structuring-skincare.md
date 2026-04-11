# Benchmark 04: Decision Structuring / Skincare Category Value

## Scenario

- Category: 决策整理
- Source materials:
  - `化妆品评估指令.md`
  - `护肤品品类价值评估报告.md`
- Note:
  - 这些源材料保存在仓库外的私有工作目录中，因此这里不提供仓库内跳转链接。

## Original Request

“在营销噪音很大的护肤品市场里，判断哪些品类值得长期购买、值得花多少钱、哪些可以跳过。”

## Initial Block

- 这不是纯研究任务，最终目标是帮助人形成购买决策。
- 如果只做成分综述，用户依然无法判断‘要不要买这个品类’。
- 容易把价值判断错误外包给 AI，或者直接给出空泛推荐。

## Intervention Level

`medium`

原因：

- 需要先重写决策对象：从“成分有效吗”转成“品类值不值得长期投入”。
- 输出必须保留证据逻辑，同时不能越权替用户决定预算偏好。

## Core Artifacts Produced

### Diagnosis Card

- loop_stage: input
- intervention_level: medium
- primary_block: 原问题如果停留在成分综述，无法直接支持购买决策
- risk_note: 把研究结果直接包装成强推荐，会越过用户自己的偏好和预算边界

### Task Packet

- objective: 从消费者购买决策视角评估各护肤品品类的长期价值
- current_state: 有成分与功效研究框架，但缺决策层组织方式
- artifacts: 循证评估指令、品类价值报告
- constraints: 不推荐具体品牌，不替代医疗建议，不掩盖证据不足
- success_signal: 形成“必要 / 推荐 / 可选 / 不推荐”的决策分层，并说明边界
- next_checkpoint: 检查每个品类的价值判断是否有证据依据和边界说明

### Feedback Attribution Card

- signal: 如果只讲研究，不讲价值等级，用户仍不能做选择
- failure_class: decision failure
- root_cause: 研究结构没有被改写成决策结构
- keep: 证据等级、机制说明、边界条件分析
- change: 把成分和证据折叠成品类级价值判断

### Re-input Packet

- preserve: 循证框架、证据等级、有效场景和边界分析
- discard: 只停留在学术综述视角
- add_context: 购买频率、长期使用价值、预算敏感性
- change_request: 用“必要 / 推荐 / 可选 / 不推荐”重组输出
- next_checkpoint: 检查决策结论是否仍然忠于证据层

## Output Result

- 报告成功从“功效研究”转成了“购买决策结构”。
- 决策分层明确，同时没有越权推荐品牌或替用户做不可逆选择。
- 研究和决策之间建立了稳定映射关系。

## Re-input Quality

这里的再输入主要体现为：

- 先有循证框架
- 再把它改写为品类级决策结构

这说明 `ai-native-loop` 在决策场景中的核心价值，是把知识组织成可判断的决策界面。

## Scores

| Dimension | Score | Note |
|---|---:|---|
| clarity | 4.6 | 从研究问题收敛到购买决策问题 |
| executability | 4.5 | 决策分层清楚，可直接支撑后续写作 |
| feedback_quality | 4.4 | 明确识别了“研究不等于决策”的断层 |
| reinput_quality | 4.3 | 研究框架被成功改写成决策框架 |
| transferability | 4.7 | 可迁移到消费、产品选择和资源分配判断 |

## Verdict

通过。

这证明 `ai-native-loop` 在决策整理场景里不是替用户拍板，而是重写信息结构，让决策真正可做。

## Promotion Trace

- Source field note: [field-note-01-decision-structuring-skincare.md](../field-notes/field-note-01-decision-structuring-skincare.md)
- Promoted pattern: [decision-structuring.md](../../patterns/decision-structuring.md)
- Related failure mode: [failure-modes.md](../../references/failure-modes.md)
