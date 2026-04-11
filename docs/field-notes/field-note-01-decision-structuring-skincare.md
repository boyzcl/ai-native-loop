# Field Note: Decision Structuring / Skincare Category Value

## Scene

- 决策整理
- 研究材料充分，但用户最终需要的是“该不该买、值不值得长期投入”的判断界面

## Objective

- 把已有的护肤品研究与成分分析框架，改写成可支持消费者决策的品类价值结构

## Initial Block

- 原始材料更像研究综述，不是决策界面
- 如果继续按成分或机制输出，用户仍无法判断“要不要买这个品类”
- 任务存在明显越权风险，因为 AI 很容易把研究结论直接包装成购买建议

## Intervention Level

- `medium`
- 原因：问题不在事实缺失，而在研究结构没有被改写成决策结构；需要重写任务对象与边界，而不是继续补材料

## Core Artifacts Produced

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`

## What Changed

- 从“成分或功效是否有效”改写成“这个品类值不值得长期投入”
- 从研究视角改写成决策视角
- 从知识堆积改写成“必要 / 推荐 / 可选 / 不推荐”的决策分层

## What Worked

- `Task Packet` 明确把目标从研究问题收敛成购买决策问题
- `Feedback Attribution Card` 抓到了真正断点：研究结构没有进入决策结构
- `Re-input Packet` 把证据框架折叠成了更适合决策的输出要求

## What Failed Or Remained Risky

- 如果没有显式边界，模型仍容易越权替用户做预算偏好判断
- 决策类任务的 `reinput_quality` 依然是当前 benchmark 里的最低项
- 这类任务需要一个独立 pattern，而不能只依赖 benchmark 记录

## Re-input

- 保留循证框架、证据等级和边界分析
- 不再停留在成分综述
- 下一轮应直接要求：
  - 以品类为单位
  - 给出价值分层
  - 保留证据边界
  - 不替用户做不可逆选择

## Promotion Hint

- `pattern`
  因为这个做法可以迁移到消费决策、资源配置、产品选择等多类任务
- `failure_mode`
  因为它暴露了一个稳定误判：把研究结构直接当成决策结构
- `benchmark`
  因为这是高频、可复测、已具备评分记录的典型场景

## Promotion Trace

- Promoted pattern: [decision-structuring.md](../../patterns/decision-structuring.md)
- Promoted failure mode: [failure-modes.md](../../references/failure-modes.md)
- Validated benchmark: [benchmark-04-decision-structuring-skincare.md](../benchmarks/benchmark-04-decision-structuring-skincare.md)
