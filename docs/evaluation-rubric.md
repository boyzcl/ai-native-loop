# Evaluation Rubric

## Purpose

这份 rubric 用于减少 `ai-native-loop` 评估时的自证偏差。

它不替代人工判断，但要求每次 benchmark、before/after 对照或版本回归，至少按同一组维度打分，而不是只写“整体感觉更好了”。

## Required Comparison Setup

默认至少比较两个条件：

1. `baseline`
   - 不使用 `ai-native-loop`，或仅给极轻提示
2. `candidate`
   - 使用当前版本 `ai-native-loop`

对高风险能力声明，建议加第三个条件：

3. `previous`
   - 使用上一个稳定版本或上一个实验版本

## Primary Dimensions

### 1. `clarity`

- 1：目标仍然混乱，当前轮到底要推进什么不清楚
- 3：目标基本清楚，但检查点或边界仍含混
- 5：目标、成功信号与下一检查点都明确

### 2. `executability`

- 1：没有形成可执行任务包
- 3：形成了可执行任务包，但仍缺少关键字段或行动边界
- 5：任务包足够支持 AI / Agent 立即稳定执行

### 3. `boundary_control`

- 1：越权替用户做判断，或该收口时没有收口
- 3：边界大体合理，但局部仍有越权或失配风险
- 5：责任边界、决策权边界和 stop rule 都清楚

### 4. `feedback_quality`

- 1：反馈仍停留在情绪或泛抱怨层
- 3：已经进入结构化归因，但不够稳定
- 5：反馈被明确归因为可行动的 failure class 和 next change

### 5. `reinput_quality`

- 1：下一轮仍接近从头开始
- 3：有再输入，但保留/丢弃/补充不够明确
- 5：下一轮输入被明显改写，且能直接继续推进

### 6. `transferability`

- 1：高度依赖当前案例，难迁移
- 3：有迁移价值，但触发条件与边界还不够硬
- 5：迁移规律清楚，何时用/不用都明确

### 7. `context_efficiency`

- 1：大量上下文被重复搬运，主输出噪音很高
- 3：有一定收敛，但仍读了过多非必要材料
- 5：主输出聚焦，详细材料按需进入，重复叙事少

### 8. `real_task_helpfulness`

- 1：输出看起来规范，但对真实推进帮助有限
- 3：能帮助推进，但仍有明显阻塞留在系统外
- 5：真实阻塞被有效降低，用户或主 agent 知道下一步怎么继续

## Runtime Evidence Rule

如果评估的问题涉及“经验是否进入下一轮系统”，必须额外检查：

- 是否写入了 runtime capture
- 是否能引用具体 `runtime_capture_ref`
- 下一次调用是否真的复用了 runtime 经验

这些是证据要求，不替代上面的 8 个维度。

## Comparison Rule

优先使用以下评估方式：

- pairwise：比较 `baseline` 与 `candidate` 哪个更好
- pass/fail：先看是否过最低门槛，再看分数
- criteria-first：先按维度判断，再写总结

不建议主要依赖：

- 单一总体分
- 没有 baseline 的自评分
- 只看输出格式感，不看是否推进真实任务

## Minimum Pass Bar

默认通过标准：

- `clarity >= 4`
- `executability >= 4`
- `reinput_quality >= 4`
- `real_task_helpfulness >= 4`
- 不允许 `boundary_control < 3`

对多 Agent 场景额外要求：

- `boundary_control >= 4`
- `context_efficiency >= 4`

对 runtime compounding 相关声明额外要求：

- 存在 `runtime_capture_ref`
- 至少一次 `runtime_reuse_observed = yes`

## Scoring Note

如果使用模型评审：

- 优先要求模型做 pairwise 或 pass/fail
- 不要让同一模型既当主要产出者又当唯一评审者
- 评审结论必须引用具体差异，而不是只给总分
