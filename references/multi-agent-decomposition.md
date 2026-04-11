# Multi-Agent Decomposition

## Why This File Exists

`ai-native-loop` 已经声明适用于 agent 协作与多轮任务推进。

如果没有显式分解规则，这种能力就容易停留在口头层：

- 看起来很高级
- 实际上容易重复劳动
- 最后拿不到稳定可回收结果

这份文件的目标不是鼓励凡事拆 agent，而是把“什么时候该拆、怎么拆、怎么回收”写硬。

## Default Position

默认先假设：**不拆**。

只有在以下三个条件同时满足时，才优先考虑拆分：

1. 当前任务存在两个以上相对独立的工作流。
2. 各工作流之间可以通过明确交接物汇总，而不是边做边互相改写。
3. 主 agent 能清楚说出每个子 agent 的拥有范围与回收格式。

如果这三点说不清，先保持单线程。

## When To Split

出现以下信号时，适合分治：

- 任务由多个彼此独立的问题组成，可以并行推进。
- 上下文过大，单个 agent 持续切换任务会显著失真。
- 子任务的输入边界明确，产出物也可以标准化。
- 主 agent 的下一步是整合，而不是亲自完成每个细部动作。

典型场景：

- 研究主线和写作主线并行
- 前端、后端、测试三个切片彼此边界清楚
- 多份材料需要独立评估后再统一汇总
- 大任务中的验证、实现、整理可以分离

## When Not To Split

出现以下任一情况时，默认不要拆：

- 当前任务的真正瓶颈是目标含混，而不是执行负荷。
- 子任务之间强耦合，边做边需要频繁改目标。
- 主 agent 其实还没想清楚统一判断标准。
- 子任务规模过小，拆分成本高于收益。
- 最终结果高度依赖单一连续思考链，而不是多个可汇总工件。

## Fast Decision Test

分治前先过四问：

1. `parallelizable`
   这个任务里是否真的有可以并行的独立块？
2. `bounded`
   每个子块的输入和输出边界能否写清？
3. `integrable`
   主 agent 是否知道最后怎么把结果汇总？
4. `worth_it`
   拆分收益是否明显大于协调成本？

四问里有一项明显答不出来，就先不拆。

## Main Agent Responsibilities

主 agent 必须保留以下职责，不外包：

- 定义本轮总目标
- 决定是否拆分
- 定义每个子 agent 的拥有范围
- 定义统一验收标准
- 回收并整合交接物
- 做最终判断与版本化决策

主 agent 不是更大的执行 agent，而是**任务操作系统**。

## Child Agent Minimum Packet

每个子 agent 至少应收到以下输入：

- `objective`
  这个子任务这轮到底要推进什么。
- `owned_scope`
  它拥有哪些材料、文件、问题域或责任范围。
- `constraints`
  不能做什么，哪些边界不能越过。
- `expected_artifact`
  最终必须回收什么格式的交接物。
- `success_signal`
  这轮什么样算完成。
- `stop_rule`
  遇到什么情况应停止扩张并返回。

如果这些字段没写出来，子 agent 很容易失控。

## Standard Handoff Artifact

每个子 agent 回收时，至少返回：

- `done`
  实际完成了什么。
- `found`
  发现了什么重要信息、风险或缺口。
- `blocked_by`
  卡在什么地方，为什么卡。
- `recommended_next`
  主 agent 下一步最该做什么。

必要时再补：

- 修改了哪些文件
- 哪些判断仍需主 agent 或用户保留

## Recommended Split Shapes

优先使用以下稳定拆法：

### 1. Explore / Execute

- 子 agent A：探索事实、代码或材料
- 主 agent：保留决策与整合

适合：

- 先查清情况，再决定怎么改

### 2. Build / Verify

- 子 agent A：实现
- 子 agent B：验证
- 主 agent：决定是否收敛

适合：

- 实现边界清楚、验证也可独立运行

### 3. Research / Synthesis

- 子 agent A：调查与抽取
- 子 agent B：表达与组织
- 主 agent：统一口径与风险边界

适合：

- 研究写作或复杂信息整理

## Anti-Patterns

以下是高频错误拆法：

### 1. 为了显得高级而拆

没有独立工作流，只是把一个模糊任务丢给多个 agent。

结果通常是：

- 重复劳动
- 标准不一致
- 无法汇总

### 2. 主 agent 丢掉判断权

主 agent 如果不再保留：

- 验收标准
- 取舍边界
- 最终整合

系统就会退化成多个黑箱并行。

### 3. 子 agent 收到“大概做一下”

没有 `owned_scope` 和 `expected_artifact` 的子 agent，几乎必然漂移。

## Integration Rule

主 agent 回收结果后，不直接拼接输出。

先做三步：

1. 对齐：确认各子结果是否回答了同一个总目标。
2. 去重：去掉重复发现和彼此冲突但未经判断的片段。
3. 再决策：把子结果折叠回一个统一 `Task Packet` 或最终交付物。

## Minimal Recommendation

默认最小可行做法是：

- 主 agent 先写一张 `Diagnosis Card`
- 再给每个子 agent 一张最小输入包
- 回收统一 handoff artifact
- 最后主 agent 负责整合和下一轮 `Re-input Packet`

如果做不到这四步，就先不要拆。
