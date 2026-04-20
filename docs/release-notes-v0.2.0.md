# Release Notes v0.2.0

Status: `Draft`

Date: `2026-04-16`

Current release truth lives in [release-manifest.md](release-manifest.md).

## Release Thesis

`v0.2.0` 不是一次“补更多概念”的版本，而是一次把 `ai-native-loop` 从协议层推进到运行层、验证层和初步复利层的版本。

这个版本真正修复的，不是单个文档缺失，而是四类高频失败：

- 协议存在，但没有最小完备动作集
- 任务做完了，但失败模式无法沉淀
- recovery block 存在，但经验不会默认进入下一轮系统
- 首页和路由承诺强于可验证证据

## What Changed

### 1. The Skill Now Has A Local Runtime Memory Layer

本轮最关键的升级，不是再多一个文档，而是把经验沉淀推进到本地 skill 目录中的 runtime 层。

当前默认 runtime root 已改为按 host 解析。

本轮最小可信支持面：

- `Codex`：`~/.codex/skills/ai-native-loop/runtime/`

当前仅有适配草案：

- `Claude Code`：`~/.claude/skills/ai-native-loop/runtime/`

新增内容：

- runtime capture 目录结构
- runtime manifest
- review queue
- promoted field note 分层
- runtime helper scripts

核心文件：

- [runtime-memory-spec.md](runtime-memory-spec.md)
- [runtime-promotion-policy.md](runtime-promotion-policy.md)
- [experience-compounding-loop.md](../references/experience-compounding-loop.md)

### 2. Medium-Plus Interventions Now Require Local Capture

此前中介入以上任务只要求输出末尾保留 `Loop Recovery Block`。

现在规则更硬：

- 主输出末尾保留 `Loop Recovery Block`
- 同结构内容写入本地 runtime capture
- 如果当前环境无法写入，必须明确说明未完成 runtime capture

这意味着“经验进入系统”不再只是叙述，而是有了默认宿主。

### 3. Invocation Contract Is Now Narrower

本轮收紧了调用契约：

- 显式调用优先
- 不把隐式调用当作稳定承诺
- 增加 `Minimum Pass Contract`
- 增加 provisional packet 协议
- 增加 `light / medium / strong` 输出预算

这一步的目标不是把 skill 做小，而是减少误触发和形式主义输出。

### 4. Validation Now Requires Runtime Provenance

benchmark 与实验模板从本轮开始不只比较 baseline / candidate，还要求记录：

- runtime capture 是否写入
- runtime capture 引用是什么
- 下一轮是否真的复用了 runtime 经验

这让“经验会进入下一轮系统”开始有了更硬的验证入口。

### 5. First-Run Packaging Now Matches The Real Mechanism

README 和兼容文档已经不再把这个 skill 表达成“只靠 recovery block 自然复利”的系统，而是明确区分：

- 本地 runtime 层
- 仓库公开资产层
- 推荐使用方式
- 当前证据边界

## Validation

本版本当前具备以下验证基础：

- 4 个固定 benchmark 的统一矩阵
- baseline + pairwise 评估模板
- runtime provenance 字段
- runtime helper scripts
- smoke test 入口
- 一条 bootstrap runtime memory smoke validation sample

当前仍未完成：

- 全量 baseline 补跑
- 多 Agent 实测证据
- 足量 runtime reuse 样本

## What This Release Still Does Not Solve

`v0.2.0` 仍未完全解决以下问题：

- 经验沉淀仍然不是全自动
- runtime capture 仍需要当前运行环境允许文件写入
- 多 Agent benchmark 仍缺公开实测结果
- 外部用户是否会持续贡献有效经验，仍需真实使用验证

## Upgrade Guidance

如果你已经在使用 `v0.1.0` 风格的 `ai-native-loop`，升级到 `v0.2.0` 后，建议默认这样用：

1. 优先显式调用 `$ai-native-loop`
2. 先出 `Diagnosis Card` 和 `Task Packet`
3. 对中介入以上任务，默认写 runtime capture，而不只是在回答末尾留字
4. 遇到重复问题时，先读相关 runtime 经验，再决定是否进入 pattern / failure mode
5. 需要并行协作时，仍按多 Agent 规则层处理，但不要把它当作已充分验证的首页能力承诺

## Release Judgment

这是一个“把协议做成运行系统”的版本，而不是“继续把理念写得更漂亮”的版本。

如果 `v0.1.0` 证明了这个 Skill 值得公开发布，`v0.2.0` 的意义在于：

> 它开始把经验复利从展示层资产推进成默认存在的本地运行层。
