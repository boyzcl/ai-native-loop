# Auto Promotion And Capacity Diagnosis

Date: `2026-04-21`

Scope: 基于当前 `ai-native-loop` 的 runtime 数据、promotion 规则、已有 helper scripts 与项目状态文档，对“自动晋升为系统知识”这一需求做一次正式诊断，并明确长期容量治理约束。

## Executive Summary

截至 `2026-04-21`，`ai-native-loop` 已经完成了：

- `medium+` 调用自动写入 runtime capture
- 自动更新轻索引
- 自动把大多数 capture 加入 review queue

但它还没有完成：

- 从 `raw capture` 自动进入 `promoted field note`
- 从 `promoted field note` 自动形成受控的 `repo candidate`
- 对长期运行下的 backlog、去重、归档、读取预算做程序化治理

换句话说：

> 当前系统已经具备“自动采集”，但尚不具备“自动晋升”，更不具备“有容量上限的自动复利”。

这意味着项目的主要矛盾已经从“经验会不会蒸发”转移为：

> 怎样在不制造知识膨胀和错误固化的前提下，让高价值经验自动进入本地系统知识层，并把 repo 层保持为稀缺、稳定、可验证的公开资产层。

## Current Facts

以下事实可直接确认：

### 1. Capture 层已经健康

运行时经验会被自动写入：

- `runtime/captures/YYYY-MM-DD.jsonl`

并自动进入：

- `runtime/index/`
- `runtime/inbox/review-queue.json`

这说明 intake 已经是默认发生的，而不是纯手工整理。

### 2. Promotion 层仍然偏手工

当前仓库和安装副本已有：

- `runtime-promoted/field-notes/` 这一层结构
- promotion gate、dedup rule、archive rule 等文档化规则

但缺失的是：

- 一个真正运行中的 promotion worker
- 自动 triage / score / merge / archive 过程
- 对 repo candidate 的持续门控流程

### 3. Capacity Governance 规则存在，但仍未工程化

当前文档已经有清楚的 anti-bloat 原则：

- 不是每条经验都值得升级
- 优先合并已有资产
- 默认读取预算必须保持小
- 低价值或长期无人引用的经验应归档

问题在于，这些仍主要是“规则声明”，还不是“默认运行机制”。

## Core Diagnosis

当前真正的瓶颈不是 capture 不足，而是缺少一个中间层：

> `promotion worker + capacity governance layer`

如果没有这一层，系统会落入两个坏结果之一。

### 坏结果 A：继续偏手工

表现：

- raw capture 持续增加
- review queue 持续积压
- promoted field note 增长缓慢
- repo 层仍依赖作者主动抽取

后果：

- 经验可留痕，但不会自然复利
- backlog 越来越大，最终 review 成本越来越高
- 用户感知上会觉得“系统好像记住了，但并没有真正变强”

### 坏结果 B：过度全自动

表现：

- capture 只要命中 promotion hint 就持续自动升级
- field note 数量快速膨胀
- 近似 pattern / failure mode 越来越多
- repo 层开始被会话级细节污染

后果：

- 读取成本上升
- dedup 失控
- 错误模式被过早固化
- 系统知识层从“压缩资产”退化成“历史仓库”

## Strategic Judgment

本项目不应追求“全链路无门槛自动晋升”。

正确方向应当是：

> 本地自动、仓库门控、容量受限、证据驱动。

更具体地说，自动化应该只做到：

### 1. Runtime Local Knowledge Automation

允许自动完成：

- `raw capture -> triaged review item`
- `reviewed note -> promoted field note`
- `merge into existing promoted note`
- `archive low-value runtime note`

这一层属于本地系统知识层，目标是让“下一次调用能读到更好的经验”，而不是直接对外发布。

### 2. Repo Asset Promotion Should Stay Gated

不建议直接自动完成：

- `field note -> pattern`
- `field note -> failure mode`
- `field note -> benchmark`
- `field note -> release narrative`

更合理的做法是自动生成：

- `repo candidate`

但继续保留更严格的晋升门槛与一次 review。

原因很简单：

- repo 层是公开资产层，不是连续会话的工作内存层
- repo 层一旦污染，会反过来伤害读取质量与项目可信度

## Capacity Model

为保证长期运行后仍能正常演化，系统知识必须分层管理。

### Layer 1: Raw Runtime Capture

角色：

- 原始 intake 层
- 保留最小结构化痕迹

要求：

- 允许增长
- 不参与默认全量读取
- 可以按日期切片保存

### Layer 2: Promoted Field Notes

角色：

- 本地系统知识层
- 下一次调用的主要可复用经验源

要求：

- 必须压缩
- 必须去重
- 必须可归档
- 必须保持工作集尺寸受控

### Layer 3: Repository Assets

角色：

- 公开表达层
- 稀缺、稳定、可验证的知识资产层

要求：

- 必须稀缺
- 必须有证据
- 必须经过 dedup 与 gate
- 不接受会话级流水账直接进入

一句话：

> raw 层允许增长，promoted 层必须压缩，repo 层必须稀缺。

## Non-Negotiable Design Rules

要达成自动晋升需求，同时保证长期稳定，后续设计必须锁定以下规则：

### 1. Auto Promotion Must Be Scored, Not Freeform

promotion worker 不应靠自由生成判断，而应基于现有 gate 规则打分：

- 重复出现
- 可迁移性
- 是否改变未来判断
- 是否值得进入 benchmark / pattern / failure mode

### 2. Dedup Must Happen Before New Asset Creation

任何自动晋升都必须先问：

- 是否已有近似 promoted note
- 是否只是已有 pattern 的变体
- 是否只是已有 failure mode 的新例子

默认顺序必须是：

1. merge
2. update
3. create

### 3. Repo Promotion Must Require Stronger Evidence Than Local Promotion

本地 field note 可以更积极一些；
repo candidate 必须更保守。

repo candidate 至少应要求：

- 最近周期内重复出现
- 至少一次真实 reuse 被观测到
- 已能回答 pattern intake 的关键问题
- 可以明确挂到 benchmark 或版本叙事

### 4. Read Budget Must Stay Small Forever

长期运行的系统最怕“知识越积越多，调用越来越重”。

因此：

- 默认只读最近少量 raw capture
- 只读少量 promoted field notes
- 只读极少数 pattern / failure references

自动晋升的目标不是“让系统知道更多”，而是“让系统默认读到更准的少数知识”。

### 5. Archive Is Part Of Promotion, Not A Cleanup Afterthought

如果没有持续 archive：

- runtime 会膨胀
- promoted 层会重复
- 误导性旧经验会长期驻留

归档应视为自动晋升流程的一部分，而不是后期人工大扫除。

## Product-Level Decision

下一阶段的正确决策不是：

- 再补更多理念文档
- 直接承诺全自动系统知识生长
- 让 repo 层也默认自动晋升

下一阶段的正确决策应是：

> 建一个受限的 promotion worker，把自动化锁定在 runtime 层；把 repo 层保持为更严格的候选晋升层；同时把 dedup、archive、budget、quota 一起工程化。

## What Success Looks Like

当以下条件成立时，可以说“自动晋升需求开始被真实满足”：

1. raw capture 不再只是堆积，而会周期性被自动 triage
2. 高价值 capture 能自动进入 promoted field note
3. promoted field note 总量保持受控，不无限膨胀
4. 至少一部分 promoted note 被下一次调用真实复用
5. repo 层增长速度远慢于 runtime 层，并保持高信噪比
6. 长期运行后，系统仍然能明确回答：
   - 经验存在哪
   - 哪些经验会自动晋升
   - 哪些经验会被归档
   - 哪些经验有资格进入 repo

## Final Judgment

当前系统最需要补的，不是更多知识本体，而是：

> 一个“会做选择的自动晋升机制”。

这套机制必须同时满足四件事：

- 自动留下来
- 自动筛一遍
- 自动压一层
- 自动淘汰一批

如果只做前两件，不做后两件，系统会越来越重；
如果只做前一件，不做后三件，系统会越来越假。

因此，这一轮的核心判断是：

> `ai-native-loop` 应该实现“受限复利系统”，而不是“无限自动生长系统”。
