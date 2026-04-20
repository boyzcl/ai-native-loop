# AI Native Loop Runtime Compounding Execution Plan

> Historical note: this execution plan was written during the earlier Codex-first phase. Any path examples under `.codex` are historical snapshots, not the current cross-host support contract. Use [host-abstraction.md](host-abstraction.md) and [compatibility-matrix.md](compatibility-matrix.md) for the current truth.

## Objective

把 `ai-native-loop` 从“有经验治理设计的协议型 skill”推进到“经验默认留存在本地 skill 目录、并能在下一次调用时进入迭代”的运行系统。

这份计划同时吸收两类反馈：

- 外部评审报告指出的核心问题：证据弱于能力声明、首试路径偏重、隐式路由过宽、多 Agent 证据未硬化。
- 当前最关键的产品反馈：经验不应散落在各项目输出末尾，而应沉到本地 skill 目录，成为下一次调用可读取、可筛选、可提升的运行时资产。

## Core Decision

下一阶段不再把重点放在“继续补更多文档”，而放在两条主线：

1. 建立 `local-first runtime compounding layer`
   让经验先进入本地 skill 目录，再决定是否提升为 field note / pattern / failure mode / benchmark。
2. 收紧公开承诺与首试路径
   让路由、证据、演示、验证与版本叙事重新对齐。

一句话版本：

> 先把经验做成默认可留存、可再利用的本地运行机制，再把验证和包装补到足以对外成立。

## Decision Lock

本轮先冻结三条关键决策，避免后续再次漂移。

### 1. Runtime Host Path

运行时经验层的默认宿主路径固定为：

- `installed_skill_path`
  - `/Users/boyzcl/.codex/skills/ai-native-loop/`
- `runtime_root`
  - `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/`

原因：

- 这里才是实际被调用的本地 skill 宿主。
- 经验要服务下一次调用，必须跟随被调用副本，而不是只跟随仓库工作副本。
- 这条决策直接回应“经验不能散落在项目目录里”的产品反馈。

### 2. Repository Role

仓库路径固定承担“定义、模板、公开资产、验证与发布”职责：

- `repo_root`
  - `/Users/boyzcl/Documents/AI native/ai-native-loop/`

仓库不承担默认运行时存储职责。

### 3. Sync Direction

本轮先采用单向同步：

- `runtime -> repo`
  本地 runtime 经验经 review / promote 后，才进入仓库资产。
- `repo -> runtime`
  仅同步模板、规则和已发布 pattern，不反向把仓库所有历史文档灌回 runtime。

这样可以避免一开始就把 repo 资产和 runtime 资产混成一层。

## Target State

完成本轮后，项目应达到以下状态：

1. `medium` 及以上调用结束后，经验默认落在本地 skill 目录，而不是只存在于当前项目对话或某个项目文件夹里。
2. 下一次调用 `ai-native-loop` 时，系统可以按任务信号读取相关的本地经验，而不是从零开始。
3. 本地经验可以分层流转为 `raw capture -> promoted field note -> pattern / failure mode / benchmark candidate`。
4. README、`SKILL.md`、agent metadata、benchmark 和版本叙事都明确反映这个新机制。
5. 对外表达收敛为“显式调用优先、验证逐步硬化、多 Agent 仍属证据补强中”。

## Design Principles

### 1. Local-First, Not Project-First

经验的默认宿主应是本地 skill 目录，而不是当前任务所在项目目录。

原因：

- 项目目录是任务上下文，不是 skill 的长期记忆层。
- 只有存到本地 skill 目录，下一次调用才有自然读取入口。
- 项目内留痕可以作为可选导出，不应是默认沉淀位置。

### 2. Runtime Capture Before Editorial Promotion

先保证每次调用后都有低摩擦 runtime capture，再做人工或半自动提升。

顺序必须是：

- 先有默认 capture
- 再有 triage
- 再有 promote
- 最后才有 repo-level documentation

### 3. Separate Runtime Memory From Public Assets

要明确区分两层：

- `runtime layer`
  本地 skill 目录中的用户侧、连续使用侧经验资产。
- `repository layer`
  仓库中的 pattern、failure mode、benchmark、release docs 等公开资产。

前者负责“默认积累”，后者负责“可复用表达与对外证明”。

### 4. Explicit Invocation First

在 runtime compounding 机制跑稳之前，默认使用建议必须继续偏向显式调用 `$ai-native-loop`。

### 5. Evidence Must Follow Capability

任何被保留在首页或主描述里的能力声明，都需要对应的验证入口、演示材料或运行证据。

## New Runtime Architecture

### Local Skill Directory Layout

建议在本地 skill 目录下新增运行时层：

- `runtime/captures/`
  每次 `medium+` 调用后的原始 capture。
- `runtime/index/`
  用于按场景、失败模式、模式标签做轻索引。
- `runtime/inbox/`
  待 review 的候选提升项。
- `runtime/promoted/field-notes/`
  从 runtime capture 升级后的本地 field note。
- `runtime/promoted/archive/`
  低价值或已被合并覆盖的旧经验。
- `runtime/state/`
  记录最近一次 review、promotion、dedup 的状态。

完整宿主结构应落在：

- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/captures/`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/index/`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/inbox/`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/promoted/field-notes/`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/promoted/archive/`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/state/`

### Recommended File Shapes

默认先用轻量文件方案，不引入数据库：

- `runtime/captures/YYYY-MM-DD.jsonl`
- `runtime/index/by-scene.json`
- `runtime/index/by-pattern.json`
- `runtime/index/by-failure-mode.json`
- `runtime/inbox/review-queue.json`
- `runtime/state/runtime-memory-manifest.json`

### Capture Contract

对 `medium` 及以上任务，结束时不只输出 `Loop Recovery Block`，还要把同结构内容写入本地 runtime capture。

最小字段：

- `timestamp`
- `session_id` 或可追溯调用标识
- `scene`
- `objective`
- `initial_block`
- `intervention_level`
- `artifacts_produced`
- `what_worked`
- `remaining_risk`
- `next_input`
- `candidate_pattern_tags`
- `candidate_failure_tags`
- `promotion_hint`

### Capture Record Example

```json
{
  "timestamp": "2026-04-16T21:30:00+08:00",
  "session_id": "codex-thread-20260416-2130",
  "skill_name": "ai-native-loop",
  "scene": "research-to-report",
  "objective": "把分散研究材料压成可继续推进的报告任务包",
  "initial_block": "材料很多，但缺结论结构与下一轮输入",
  "intervention_level": "medium",
  "artifacts_produced": [
    "Diagnosis Card",
    "Task Packet",
    "Re-input Packet",
    "Loop Recovery Block"
  ],
  "what_worked": "先压任务包再给结论，减少了输出漂移",
  "remaining_risk": "引用来源仍未核实，结论强度不足",
  "next_input": "带着来源校验要求重跑报告主线",
  "candidate_pattern_tags": [
    "research-to-report"
  ],
  "candidate_failure_tags": [
    "answer-before-structure"
  ],
  "promotion_hint": "review_for_field_note"
}
```

### Retrieval Contract

下一次调用时，先按当前任务信号读取最多三类相关经验：

- 最近相似 `scene`
- 最近命中的 `failure mode`
- 最近被验证有效的 `pattern`

默认读取预算：

- 最近 5 条 raw captures
- 最多 3 条 promoted field notes
- 最多 2 条 pattern / failure references

禁止全量加载整个经验层。

### Retrieval Decision Order

每次调用按以下顺序检索：

1. 先看当前请求是否命中显式 pattern tag
2. 再看是否命中已知 failure mode
3. 再看最近 7 天内相似 scene 的 raw captures
4. 如果仍无明显相关经验，则回退到零经验模式，不强行引用 runtime 记忆

### Write / Read Lifecycle

运行时闭环固定为六步：

1. 调用开始
   识别当前 `scene`、疑似 `pattern tag`、疑似 `failure mode`
2. 预读取
   从 `runtime/index/` 和 `runtime/promoted/field-notes/` 取少量相关经验
3. 任务执行
   正常产出核心工件
4. 结束 capture
   生成 `Loop Recovery Block` 并写入 `runtime/captures/YYYY-MM-DD.jsonl`
5. 进入 inbox
   满足 promotion hint 条件的记录加入 `runtime/inbox/review-queue.json`
6. 周期 review
   决定保留 raw、升级 field note、合并既有 pattern，或归档

### Promotion Contract

本地 promotion 采用四级流转：

1. `raw capture`
2. `reviewed note`
3. `promoted field note`
4. `repo candidate`

只有进入第 4 级的内容，才应该考虑反哺仓库中的 `patterns/`、`failure-modes.md`、`benchmarks/`、`CHANGELOG.md` 或 `release notes`。

### Promotion Gate

只有同时满足以下至少两项，才可从 runtime 层提升到 repo candidate：

- 7 天内重复出现
- 已能明确抽成 pattern 或 failure mode
- 明显改变下一次任务判断
- 能进入 benchmark 或版本叙事

否则默认停留在 runtime 层，不进入仓库。

## Source Of Truth Matrix

| Layer | Default Path | Role | Update Mode |
|---|---|---|---|
| Runtime capture | `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/captures/` | 日常调用后的最小留痕 | 每次 `medium+` 调用后追加 |
| Runtime promoted notes | `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/promoted/field-notes/` | 本地连续使用中的可复用经验 | review 后更新 |
| Skill contract | `/Users/boyzcl/.codex/skills/ai-native-loop/SKILL.md` | 本地实际运行规则 | 手动更新 |
| Repository assets | `/Users/boyzcl/Documents/AI native/ai-native-loop/` | 公开表达、验证、发布 | 通过 promote 后更新 |
| Release truth | `/Users/boyzcl/Documents/AI native/ai-native-loop/docs/release-manifest.md` | 当前版本单一事实源 | 发布前人工同步 |

## Non-Goals

本轮明确不做以下事情：

- 不做全自动 pattern 提炼
- 不做向量数据库或复杂语义检索
- 不把所有历史 case 批量灌进 runtime 层
- 不把多 Agent 提升成首页主卖点
- 不先做 UI 化 memory browser

## Workstreams

## Workstream A: Runtime Memory Layer

目标：把经验沉淀从“输出尾部协议”升级成“本地 skill 目录中的默认运行机制”。

### Deliverables

- `runtime/` 目录结构规范
- capture 文件格式规范
- retrieval 读取规则
- promotion 阶梯与 review 队列规则
- dedup / archive 规则
- 本地 runtime manifest
- runtime bootstrap 模板文件
- runtime 与 repo 分层说明文档

### Required File Changes

- [SKILL.md](/Users/boyzcl/Documents/AI native/ai-native-loop/SKILL.md)
- [references/experience-compounding-loop.md](/Users/boyzcl/Documents/AI native/ai-native-loop/references/experience-compounding-loop.md)
- 新增 runtime 相关 reference 文档
- 新增 runtime state/template 文件

建议新增的具体文件：

- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/README.md`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/state/runtime-memory-manifest.json`
- `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/inbox/review-queue.json`
- `/Users/boyzcl/Documents/AI native/ai-native-loop/docs/runtime-memory-spec.md`
- `/Users/boyzcl/Documents/AI native/ai-native-loop/docs/runtime-promotion-policy.md`

### Acceptance Criteria

- `medium+` 任务的默认回收动作明确包含“写入本地 runtime capture”
- 文档不再把“输出末尾 recovery block”误写成完整留存机制
- 下一次调用的读取规则清楚、克制、可执行
- 本地运行层和仓库资产层的边界可被一句话说清

## Workstream B: Skill Contract Tightening

目标：收紧调用边界和 done rule，降低误触发与形式主义输出。

### Deliverables

- `显式调用优先` 契约
- `Minimum Pass Contract`
- `light / medium / strong` 输出预算
- `信息不足时的 provisional packet 协议`

### Required File Changes

- [README.md](/Users/boyzcl/Documents/AI native/ai-native-loop/README.md)
- [SKILL.md](/Users/boyzcl/Documents/AI native/ai-native-loop/SKILL.md)
- [agents/openai.yaml](/Users/boyzcl/Documents/AI native/ai-native-loop/agents/openai.yaml)

### Acceptance Criteria

- README 首页明确建议显式调用
- `SKILL.md` 增加运行时 pass contract
- 输出重量被制度化，而不是靠模型自由发挥

## Workstream C: Evidence Hardening

目标：把“结构很强”补成“证据足够硬”。

### Deliverables

- 4 个固定 benchmark 的 baseline 补跑计划
- pairwise rubric 运行流程
- experiment log 使用规范
- 至少 1 个从 runtime capture 提升而来的真实验证样本

### Required File Changes

- [docs/benchmark-matrix.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/benchmark-matrix.md)
- [docs/evaluation-rubric.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/evaluation-rubric.md)
- [docs/experiment-log-template.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/experiment-log-template.md)
- [docs/benchmarks/benchmark-run-template.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/benchmarks/benchmark-run-template.md)

### Acceptance Criteria

- 公开验证不再只依赖 retrospective 叙述
- 至少有一条真实 runtime 经验进入验证层
- benchmark 与版本叙事开始共享同一套失败驱动语言
- 评估报告中的“强结构、弱证明”问题被实质性缩小

## Workstream D: First-Run Packaging

目标：降低首次试用门槛，让用户先看到收益，再进入深层结构。

### Deliverables

- README 首屏重构
- 兼容与前提文档
- 60 秒安装与显式调用路径
- 一个公共 proof pack
- 一个真实输出片段或终端演示

### Required File Changes

- [README.md](/Users/boyzcl/Documents/AI native/ai-native-loop/README.md)
- 新增 `docs/compatibility-and-invocation.md`
- 新增 `docs/proof-pack.md`

### Acceptance Criteria

- 首页只保留高信号信息
- 用户能在 60 秒内理解“什么时候该用、怎么触发、会看到什么”
- 多 Agent 从首页主卖点降级为“规则支持，证据补强中”

## Workstream E: Version Narrative Refactor

目标：把版本迭代从“新增了什么”改成“发现了什么失败，因此修了什么机制”。

### Deliverables

- failure-driven changelog 写法
- release notes 重构
- release manifest 同步新运行机制

### Required File Changes

- [CHANGELOG.md](/Users/boyzcl/Documents/AI native/ai-native-loop/CHANGELOG.md)
- [docs/release-manifest.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/release-manifest.md)
- [docs/release-notes-v0.2.0.md](/Users/boyzcl/Documents/AI native/ai-native-loop/docs/release-notes-v0.2.0.md)

### Acceptance Criteria

- 版本说明开始围绕失败、修正、验证、影响来叙述
- runtime compounding layer 成为版本判断的一部分

## Migration Plan

### Migration Goal

把当前“repo 中已经存在的经验资产”与“未来默认进入 runtime 的经验资产”分开处理，避免历史资产污染运行层。

### Migration Rule

历史仓库资产不直接导入 runtime capture。

只做两类最小迁移：

1. 从仓库 pattern / failure mode 提取标签字典
   供 runtime 检索时打 tag 用。
2. 从仓库里挑 1 到 2 条最典型 field note
   作为 promoted note 样例，而不是作为原始 runtime 历史。

### Why

- 这样可以防止 runtime 一开始被 retrospective 文档淹没。
- 也能保持“runtime 是真实调用沉淀，repo 是公共资产”的边界。

## Privacy And Noise Control

### Default Rule

runtime capture 默认只保留结构化摘要，不保留大段原始项目材料。

### Must-Not-Store

- 完整私有文档正文
- 长篇客户材料
- 凭证、密钥、token
- 与经验提炼无关的大段聊天原文

### Noise Control

以下情况默认不写 runtime capture：

- `light` 介入且没有明显复用价值
- 纯机械执行
- 纯格式调整
- 单点事实查询

## Execution Schedule

基于当前日期 `2026-04-16`，建议按 10 天推进。

### 2026-04-16 To 2026-04-17

- 冻结宿主路径、分层规则、capture schema
- 新建 runtime 目录与 bootstrap 文件
- 在 `SKILL.md` 和 `experience-compounding-loop.md` 中改写留存机制定义

### 2026-04-18 To 2026-04-19

- 补 retrieval 规则、review queue、promotion gate
- 补 `Minimum Pass Contract`、显式调用优先、输出预算

### 2026-04-20 To 2026-04-22

- 选 1 条真实 runtime capture 跑完整 promotion
- 接入 benchmark / experiment log
- 修改 failure-driven changelog 与 release notes

### 2026-04-23 To 2026-04-25

- 重构 README 首页
- 新增 compatibility 文档与 proof pack
- 把多 Agent 承诺从首页主卖点降级

## Phase Plan

### Phase 0: Decision Freeze

目标：冻结下一轮设计决策，避免继续把经验沉淀写成 repo-only 机制。

交付物：

- 本执行计划
- 本地 runtime layer 的宿主决策
- repo layer 与 runtime layer 的分工说明

### Phase 1: Runtime Foundations

目标：先把本地留存机制做成工程事实。

交付物：

- runtime 目录规范
- capture schema
- retrieval rule
- local manifest
- `SKILL.md` runtime capture 合同

验收标准：

- 本地留存位置明确
- capture 结构明确
- 下次调用如何读取明确
- runtime bootstrap 文件已经创建

### Phase 2: Invocation And Contract Tightening

目标：把触发和输出收紧，降低 runtime layer 的噪音输入。

交付物：

- 显式调用优先
- minimum pass contract
- provisional packet 协议
- 输出预算规则

验收标准：

- 路由稳定性优先于覆盖范围
- 中强介入不会再无限膨胀

### Phase 3: Promotion And Validation

目标：把本地沉淀接到验证层，而不是只接到展示层。

交付物：

- runtime capture -> promoted field note 流程
- promoted field note -> benchmark candidate 流程
- baseline + pairwise 实测计划

验收标准：

- 至少一条真实 runtime capture 完成完整晋升
- 证据链不再主要依赖 retrospective
- 评审报告中最关键的“证据短板”已有明确修复入口

### Phase 4: Packaging And Public Trust

目标：把内部机制整理成对外可理解、可信、可试的产品入口。

交付物：

- 新 README
- 兼容文档
- proof pack
- release narrative 更新

验收标准：

- 首试成本明显下降
- 外部用户能理解这是一个“会进化的 skill”，而不是静态文档集

## Priority Order

### P0

- 建立本地 runtime memory layer
- 把 capture 写入本地 skill 目录
- 建立下次调用的 retrieval 规则
- README / SKILL / agent metadata 收紧为显式调用优先

### P1

- 补 `Minimum Pass Contract`
- 补 output budget 与 provisional packet
- 补 baseline + pairwise 验证计划
- 调整版本叙事为 failure-driven

### P2

- proof pack
- 兼容矩阵
- 社区反馈入口
- 高频场景薄适配层

## Success Metrics

本轮至少追踪以下 6 个指标：

- `capture_write_rate`
  - `medium+` 调用中成功写入 runtime capture 的比例
- `capture_to_review_rate`
  - raw capture 进入 review queue 的比例
- `review_to_promote_rate`
  - review 项中成功提升为 promoted field note 的比例
- `promotion_to_repo_rate`
  - promoted note 最终进入 repo candidate 的比例
- `first_run_clarity`
  - 新用户是否能在 60 秒内理解调用方式
- `evidence_hardening_progress`
  - baseline / pairwise / runtime validation 的完成数量

最低通过判断：

- 连续 5 次 `medium+` 调用中，至少 4 次成功写入 runtime capture
- 至少 1 条 runtime capture 进入 promoted field note
- 至少 1 条 promoted note 被用于下一次调用的相关检索

## Risks

### Risk 1

把 runtime layer 做成重型知识库，反而拖慢调用。

控制方式：

- 默认只存最小 capture
- 默认只加载少量相关经验
- 不引入重数据库和复杂检索

### Risk 2

把 repo layer 和 runtime layer 混在一起，导致真相源混乱。

控制方式：

- runtime 负责默认沉淀
- repo 负责公共表达与验证
- promotion 必须有清晰门槛

### Risk 3

继续把多 Agent 作为前台主卖点，证据却跟不上。

控制方式：

- 暂时降级公开承诺
- 待 baseline 与实测补齐后再上调

### Risk 4

capture 太多但没有 review，runtime 很快膨胀。

控制方式：

- 建 review queue
- 建 archive 规则
- 建 dedup 规则

## Completion Criteria

当以下条件同时满足时，本轮可判断为达标：

1. 本地 skill 目录中已有清晰的 runtime 经验层。
2. `medium+` 调用的默认结束动作已从“只在回答末尾留字”升级成“写入本地 capture”。
3. 下一次调用有明确的经验读取规则。
4. README 与主 skill 合同已经反映新机制。
5. 版本叙事与验证层开始围绕 runtime compounding 而不是只围绕文档数量。
6. 用户可以明确回答“经验存在哪、下次怎么被读到、何时会进入仓库”。

## Final Judgment

这一轮的第一优先级不是再补一个新 pattern，也不是再补一篇新 case。

第一优先级是：

> 让 `ai-native-loop` 真正拥有本地运行时经验层，让经验能被默认留下、在下一次调用时被重新读取、并逐步提升为系统资产。

如果这一点不成立，经验沉淀仍然只是“可整理”，还不是“会进化”。
