# ai-native-loop

Release truth: [release-manifest.md](docs/release-manifest.md)

Current public version: `v0.1.0`

Current iteration track: `v0.2.0` draft / validation hardening

当前这一轮重点补的不是更多概念，而是三件更容易失真的基础设施：

- 版本单一事实源
- baseline / pairwise 验证骨架
- `medium` 以上任务默认 `Loop Recovery Block`

`ai-native-loop` 是一个面向广义知识工作的底层协议型 Skill。

它不把 AI 当作单点工具，而把 AI 当作工作环境，帮助用户持续重写输入、执行、反馈与再输入闭环。它适用于编码、研究、写作、产品思考、决策推进、Agent 协作与多轮任务推进。

## 30 秒自测

如果你现在卡住的不是“答案是什么”，而是下面这些问题之一，这个 Skill 基本值得触发：

- 材料很多，但这一轮到底该推进什么并不清楚
- AI 已经输出了内容，但你不知道哪些反馈该进入下一轮
- 任务涉及多阶段或多 Agent，结果很难回收和整合

一次最小成功通常长这样：

1. 原始混乱请求被压成 `Task Packet`
2. 当前卡点被点名成 `Diagnosis Card`
3. 这轮结束时得到下一轮更好的输入，而不是只得到一段答案

如果你只是要一个窄而稳定的一次性答案，这个 Skill 通常不该触发。

## Why It Exists

大多数人已经会“用 AI”，但还没有形成稳定的 AI native 工作循环。

这个 Skill 的目标不是替你完成某一个任务，而是帮助你持续优化：

- 任务如何表达
- 人机如何分工
- 输出如何转成反馈
- 反馈如何进入下一轮输入

## v0.2.0 Focus

这一轮迭代的重点，不是继续补概念，而是补执行层：

- 把协议压成 4 个核心工件
- 补失败模式与纠偏层
- 建立可复用的模式库
- 建立 benchmark 骨架，避免继续凭感觉迭代
- 开始补多 Agent 规则层与经验沉淀 intake 层

## v0.2.0 Current Execution Artifacts

当前主线上已经落地的关键交付：

- [release-manifest.md](docs/release-manifest.md)
  仓库当前版本与发布状态的单一事实源。
- [iteration-execution-plan-v0.2.0.md](docs/iteration-execution-plan-v0.2.0.md)
  这一轮迭代的执行方案与阶段边界。
- [core-operating-primitives.md](references/core-operating-primitives.md)
  四个核心工件的定义、短版示例和介入映射。
- [failure-modes.md](references/failure-modes.md)
  高频失败模式、典型症状和纠偏动作。
- [patterns/README.md](patterns/README.md)
  模式库入口与模式编写规则。
- [benchmark-matrix.md](docs/benchmark-matrix.md)
  后续固定测例、baseline 对照与通过标准。
- [evaluation-rubric.md](docs/evaluation-rubric.md)
  统一评分标准，避免只靠自我感觉打分。
- [experiment-log-template.md](docs/experiment-log-template.md)
  假设驱动的实验记录模板。
- [multi-agent-decomposition.md](references/multi-agent-decomposition.md)
  多 Agent 的拆分边界、最小输入包与回收规则。
- [experience-compounding-loop.md](references/experience-compounding-loop.md)
  经验如何从任务回收物进入 pattern、failure mode、benchmark。
- [field-note-template.md](docs/field-note-template.md)
  显著任务结束后的最小经验 intake 模板。
- [release-notes-v0.2.0.md](docs/release-notes-v0.2.0.md)
  `v0.2.0` 的发布说明草案与版本判断。

## Quick Start

### 安装到 Codex

```bash
git clone https://github.com/boyzcl/ai-native-loop.git ~/.codex/skills/ai-native-loop
```

如果你已经下载了仓库，也可以直接复制整个仓库目录到 `~/.codex/skills/ai-native-loop`。

### 第一次怎么触发

直接这样说就可以：

- `用 $ai-native-loop 帮我把这个任务整理成更适合 AI 协作的闭环。`
- `用 $ai-native-loop 看看我现在卡住的根因是在输入、执行还是反馈。`
- `用 $ai-native-loop 帮我把这轮结果折叠成下一轮输入。`

### 一个 before / after

Before：

> 我在改一个复杂功能，需求、历史尝试、报错和几段代码都混在一起了，你先帮我看看怎么继续。

After：

> 用 `ai-native-loop` 先输出 `Diagnosis Card` 和 `Task Packet`：明确这轮目标、当前状态、约束、成功信号和下一检查点；如果判断为 `medium` 以上介入，再补反馈归因和下一轮输入。

### 三个典型请求

- `我在写一个复杂功能，需求、报错和历史尝试都很乱。用 $ai-native-loop 帮我整理。`
- `我做了一轮研究，但不知道哪些反馈值得进入下一轮。用 $ai-native-loop 帮我归因。`
- `我已经有 AI 输出了，但它还不能直接用。用 $ai-native-loop 帮我改写下一轮输入。`

## 这个 Skill 会怎么介入

### 轻介入

适合：你已经知道要做什么，只是表达不够适合 AI。

Skill 会：

- 重写当前请求
- 补关键缺失字段
- 给你更好的下一检查点

### 中介入

适合：你已经在推进，但任务跨材料、质量不稳、反馈吸收困难。

Skill 会：

- 重建任务包
- 明确人机分工
- 定义检查点和再输入结构

### 强介入

适合：任务高风险、反复失败、跨轮或多 Agent 协作依赖重。

Skill 会：

- 暂停过早求答案
- 重建目标、边界、交付物和验证路径
- 先修工作系统，再恢复执行

## 仓库内容

- `SKILL.md`
  Skill 主体说明。
- `references/`
  按需加载的协议、模板和参考文件。
- `agents/openai.yaml`
  UI 与调用元数据。
- `references/core-operating-primitives.md`
  四个核心工件与最小完备动作集。
- `references/failure-modes.md`
  高频失败模式与纠偏规则。
- `references/multi-agent-decomposition.md`
  多 Agent 分治规则层，而不只是交接模板。
- `references/experience-compounding-loop.md`
  经验从任务回收到版本决策的复利回路。
- `patterns/`
  从真实案例提炼出的可迁移模式库。
- `docs/iteration-execution-plan-v0.2.0.md`
  当前迭代回合的完整执行方案。
- `docs/benchmark-matrix.md`
  固定测例矩阵、baseline 对照与通过标准。
- `docs/evaluation-rubric.md`
  benchmark 与 before/after 对照的统一评分标准。
- `docs/experiment-log-template.md`
  假设驱动的迭代记录模板。
- `docs/benchmark-results-v0.2.0.md`
  4 个真实测例的汇总结果与评分。
- `docs/benchmarks/runs/`
  benchmark 的实际运行记录与准备稿目录。
- `docs/field-notes/`
  真实任务的最小回收物，用于演示和驱动经验升级。
- `docs/benchmarks/benchmark-05-multi-agent-decomposition.md`
  多 Agent 协作的固定扩展 benchmark 场景。
- `docs/field-note-template.md`
  任务结束后最低成本的经验回收模板。
- `docs/release-notes-v0.2.0.md`
  `v0.2.0` 的 release notes 草案。
- `docs/self-evaluation.md`
  使用 `ai-native-loop` 对当前 Skill 做的完成度与质量评估。
- `docs/forward-test.md`
  用真实任务链路对 Skill 做的实际前测。
- `docs/release-readiness.md`
  面向 GitHub 开源发布的完成度检查。
- `docs/cases/case-01-self-bootstrap.md`
  首个正式案例：Skill 用自己完成自评、补齐、验证与发布。
- `docs/cases/case-02-mrna-research-to-report.md`
  外部案例：复杂研究任务如何被组织成调查、技术重建与最终成稿的闭环。
- `docs/cases/case-03-audit-remediation-to-validation-hardening.md`
  仓库治理案例：如何把审计反馈收口为版本单源、验证模板和默认回收路径修复。
- `docs/iteration-assessment-against-web-access.md`
  对标 `web-access` 后形成的迭代评估与优先级清单。
- `docs/trigger-examples.md`
  触发与不触发样例库，帮助判断何时该用这个 Skill。
- `docs/trigger-regression-suite.md`
  给 Agent 用的触发回归测试集，用来检查 should-trigger / should-not-trigger 判断是否稳定。
- `docs/skill-architecture.md`
  解释这个 Skill 由哪些层组成、每层如何工作、为什么这些层有存在的必要。
- `CHANGELOG.md`
  版本记录与发布说明。
- `ai-native-loop-delivery.md`
  设计规格与完整 Skill 方案。

## Skill 定位

这个 Skill 是一个工作协议层，而不是：

- 单次任务顾问
- 提示词美化器
- 编程专用技巧包
- 替用户思考的黑箱代理

它的核心目标是帮助用户形成稳定、可迁移、可迭代的 AI native 工作方式。

## 核心能力

- 把模糊任务重写为 AI-ready task packet
- 在轻介入 / 中介入 / 强介入之间动态切换
- 重组信息结构而不是只润色输入
- 读取反馈并做根因归因
- 把当前轮经验折叠进下一轮输入
- 在不同知识工作之间迁移同一套工作协议

## 当前发布状态

当前正式版本标签：`v0.1.0`

当前主线状态：`v0.2.0` draft / validation hardening

当前主线已经具备：

- 完整 `SKILL.md`
- 动态介入框架
- 工作循环协议文档
- 四个核心工件定义
- 反馈归因框架
- 高频失败模式库
- 模式沉淀目录
- 多 Agent 规则层
- 经验沉淀 intake 层
- 多场景迁移参考
- AI-first 输入模板
- 再输入模板
- 多 Agent 交接模板
- benchmark 矩阵骨架
- GitHub 开源仓库级文档
- 三个正式案例

仍建议继续补充：

- baseline + pairwise benchmark 记录
- 更多 live benchmark 记录
- 更多外部真实案例样本
- 不同领域下的触发边界对照
- 长周期使用后的版本迭代记录
- 多 Agent benchmark 实测结果

当前 `v0.2.0` 版本说明草案见：

- [release-notes-v0.2.0.md](docs/release-notes-v0.2.0.md)
- [release-manifest.md](docs/release-manifest.md)

## License

本仓库当前采用 MIT License。
