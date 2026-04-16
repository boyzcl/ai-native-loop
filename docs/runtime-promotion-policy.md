# Runtime Promotion Policy

## Purpose

这份文档定义 runtime 经验如何从默认留痕进入更高层系统资产。

## Promotion Ladder

运行时经验默认按四级流转：

1. `raw capture`
   - 只保留在 `runtime/captures/`
2. `reviewed note`
   - 被加入 `runtime/inbox/review-queue.json`
3. `promoted field note`
   - 升级到 `runtime/promoted/field-notes/`
4. `repo candidate`
   - 值得反哺仓库的 pattern / failure mode / benchmark / release docs

## Promotion Gate

只有同时满足以下至少两项，才应该进入 `repo candidate`：

- 7 天内重复出现
- 已能明确抽成 pattern 或 failure mode
- 明显改变下一次任务判断
- 能进入 benchmark 或版本叙事

否则默认停留在 runtime 层。

## Dedup Rule

进入 repo 前先问：

- 这是不是已有 pattern 的变体？
- 这是不是已有 failure mode 的一个新例子？
- 这是不是已有 benchmark 的局部补充？

默认顺序：

1. 优先合并
2. 其次更新
3. 最后才新增

## Archive Rule

满足任一情况可进入 archive：

- 已被更强版本覆盖
- 长期无人引用
- 只是一次性细节记录

## Runtime / Repo Boundary

runtime 层负责：

- 默认积累
- 下一次调用读取
- 低摩擦 review

repo 层负责：

- 公共表达
- 可复用资产
- 验证
- 版本叙事

一句话：

> runtime 负责让经验留下来，repo 负责让经验被公开复用和证明。
