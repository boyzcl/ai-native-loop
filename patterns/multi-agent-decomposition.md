# Multi-Agent Decomposition Pattern

## Scene

一个复杂任务包含多个可分离工作流，单线程推进会因为上下文切换、材料过多或验证链条过长而明显失真。

## Trigger

出现以下信号时触发：

- 一个总任务里有两个以上独立子问题
- 子问题之间可以通过标准交接物汇总
- 主 agent 更需要保留判断与整合，而不是亲自完成每个子块

## Intervention

默认 `strong`，但强介入不代表一定多做文书，而是先把分工写硬。

推荐动作：

1. 先用 `Diagnosis Card` 判断当前问题是“该拆”还是“先收敛目标”。
2. 用 `Task Packet` 定义总目标、统一验收标准和分治边界。
3. 给每个子 agent 分发最小输入包。
4. 回收统一 handoff artifact，再由主 agent 做整合与 `Re-input Packet`。

## Artifacts

优先产出：

- 总任务包
- 子 agent 最小输入包
- 标准交接物
- 主 agent 汇总结论
- 下一轮整合输入

## Common Failure

最常见失败：

- 目标没收敛就急着拆
- 子 agent 没有拥有范围
- 回收物格式不统一
- 主 agent 把最终判断也外包出去

## Transfer Rule

这个模式可迁移到：

- 多模块代码实现
- 研究与成稿并行
- 信息抽取与结构整合分离
- 实现与验证双线程推进

核心迁移规律：

> 多 Agent 的价值不在“更多并行”，而在“主 agent 保留决策，子 agent 只承担边界清楚的推进工作”。
