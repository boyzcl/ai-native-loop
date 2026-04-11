# Intervention Protocol Template

## 用途

当你已经判断当前任务需要轻介入、中介入或强介入时，用这份模板快速输出协议，而不是临场散讲。

## 模板

```md
## intervention-level
- light | medium | heavy

## why-this-level
- 触发这一档的核心原因：

## primary-breakpoint
- 当前闭环最主要断点：输入 / 执行 / 反馈 / 再输入

## what-to-do-now
- 本轮立即动作 1：
- 本轮立即动作 2：
- 本轮立即动作 3：

## what-not-to-do-now
- 当前不该做的事：

## handoff-or-checkpoint
- 下一检查点或交接物：

## next-reinput
- 下一轮应如何改写输入：

## output-tail
- 是否需要 `Loop Recovery Block`：yes / no
- 如果是 `medium` / `heavy`，默认 yes，并放在输出末尾
```

## 使用原则

- `light` 只做局部矫正，不重建整个系统。
- `medium` 重点修循环稳定性。
- `heavy` 先修系统，再恢复生产。
- `medium` 与 `heavy` 的最终输出，默认以 `Loop Recovery Block` 收尾。
