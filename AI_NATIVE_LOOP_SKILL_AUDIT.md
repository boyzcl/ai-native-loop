# ai-native-loop Skill / Agent 仓库审计报告

审计时间：`2026-04-11`  
审计对象：`/Users/boyzcl/Documents/AI native/ai-native-loop`  
审计方法：仓库静态审计 + 外部公开资料对标 + 当前 `git` 状态核对  
输出约束：仅新增本报告，不修改仓库既有代码、配置、脚本、README 或其他文件

## 0. 执行摘要

- `ai-native-loop` 不是“提示词集合”，而是一个以工作闭环为核心的协议型 Skill 仓库；这一定义是成立的，而且边界比大多数同类项目更清楚。
- 仓库目前最强的部分不是理念，而是已经把协议落成了四个核心工件、失败模式、模式库、benchmark 骨架和经验沉淀链。
- 仓库目前最主要的问题不是“内容不够多”，而是**证据体系弱于能力声明**。它已经有很多“看起来像验证”的材料，但真正能抗自证偏差的验证仍然不足。
- 当前评估体系主要由自评、回放式 benchmark 和作者主导的案例链组成，足以支撑内部迭代，不足以支撑“这个仓库已经明显更稳定、更泛化、更值得外部用户采用”的强结论。
- 多 Agent 部分的规则层已经写得不错，但实证层还没跟上。仓库对“适用于 Agent 协作”的声明，比现有实测证据更领先一步。
- 经验沉淀链已经出现雏形，但仍偏“编辑部模式”而不是“产品默认路径”。如果作者不主动运营，经验复利速度会明显下降。
- 仓库在**运行时上下文设计**上总体是对的：`SKILL.md` 聚焦、参考文件按需加载、主文件不臃肿，这与 Anthropic 的技能设计建议一致。
- 仓库在**仓库级维护成本**上开始出现隐性负担：版本状态、阶段判断、自评结论散落在多个文档里，且已经出现事实漂移。
- 审计时真实 `git` 状态显示本地 `HEAD=6d81340`，而 [`docs/project-status-memo-v0.2.0.md`](docs/project-status-memo-v0.2.0.md) 仍写 `HEAD=b27bb0f` 且“已与 origin/main 对齐”。这说明状态文档已不再是可靠单一事实源。
- 总体判断：**继续优化，但必须伴随局部重构**。不建议重定方向；建议把下一轮重点从“继续补内容”切到“收紧证据、收紧版本真相、收紧默认使用路径”。
- 如果只做一件事，优先做：**把“这个 Skill 是否真的变好了”的验证体系做硬**。否则后续再多文档都可能只是叙事增益，不是产品增益。

## 1. 项目理解

### 1.1 该仓库试图解决什么问题

我的理解是：`ai-native-loop` 想解决的不是“如何写一个更好的 prompt”，而是“如何把知识工作持续组织成输入、执行、反馈、再输入的可复利循环”。  
它试图作为一个**协议层 Skill**，服务于编码、研究、写作、产品推进、决策整理和 Agent 协作，而不是某个单点场景的技巧包。

这一判断主要来自以下仓库事实：

- [`README.md`](README.md) 把项目定义为“面向广义知识工作的底层协议型 Skill”，且明确不是单次任务顾问、提示词美化器或黑箱代理。
- [`SKILL.md`](SKILL.md) 把默认介入收敛为四个核心工件：`Diagnosis Card`、`Task Packet`、`Feedback Attribution Card`、`Re-input Packet`。
- [`references/core-operating-primitives.md`](references/core-operating-primitives.md) 已把四个工件写成最小完备动作集。
- [`references/failure-modes.md`](references/failure-modes.md)、[`patterns/`](patterns)、[`docs/benchmark-matrix.md`](docs/benchmark-matrix.md) 说明仓库想从“方法论描述”走向“失败驱动迭代”。

### 1.2 当前呈现出的设计思路

项目目前的设计思路可以概括为四层：

1. 协议层：`SKILL.md` + `loop-protocol` + `intervention-matrix`
2. 工件层：四个核心卡片与相关模板
3. 经验层：field note -> pattern -> failure mode -> benchmark
4. 仓库层：README、案例、benchmark、release notes、status memo、自评等

这套结构的核心优点是：**它不是泛泛谈“AI native”，而是试图把 AI native 工作方式写成最小可执行对象。**

### 1.3 理解边界与不确定性

以下信息仓库中缺失，因此本报告不做过度推断：

- 没有真实外部用户使用日志、安装量、复访率、失败率统计。
- 没有多模型、多 agent 环境下的对照结果。
- 没有独立于作者的人工评审样本。
- 没有长周期版本回归数据。

因此，本报告对“协议设计质量”的判断置信度高；对“外部实际采用效果”的判断置信度中等；对“长期演进后的网络效应”判断置信度有限。

## 2. 外部参照系

### 2.1 样本筛选原则

本次外部参照优先选取两类来源：

- 官方文档/官方 SDK 文档：用于建立一手设计原则
- 已公开、产品化程度较高的相关开源 Skill/Agent 仓库：用于建立可落地的产品化参照

不追求“列很多项目”，只保留能直接形成评判标准的样本。

### 2.2 参考样本与借鉴点

| 参考类别 | 代表案例 | 最值得借鉴的点 | 与本项目的相关性 |
|---|---|---|---|
| Skill 结构与按需加载 | Anthropic Claude Code Skills 文档 | `SKILL.md` 保持聚焦，详细材料放 supporting files，按需加载；技能描述要短且前置 use case；复杂技能要把主文件与参考文件分离 | 直接对应 `ai-native-loop` 的仓库结构与上下文效率 |
| Subagent / context isolation | Anthropic Claude Code Subagents；LangChain Deep Agents Subagents | 高噪声任务要隔离上下文；子 agent 要有清晰描述、最小工具集、独立权限；不要默认继承所有上下文/技能 | 对应本仓库的多 Agent 规则设计和上下文节流 |
| Agent orchestration 边界 | OpenAI Agents SDK `multi_agent` | Manager 持有最终答案时用 agents-as-tools；是否上多 agent 应由收益和边界决定，不应为了“看起来高级”而拆 | 对应本仓库 `references/multi-agent-decomposition.md` 的主 agent 保留职责 |
| 评估与回归 | OpenAI `Evaluate agent workflows` 与 `Evaluation best practices` | 用 traces、graders、datasets、continuous eval 建立飞轮；LLM 评估更适合 pairwise / criteria-based；多 agent 复杂度应由 eval 推动 | 直接对应本仓库当前 benchmark 可信度和后续度量框架 |
| 长流程状态与观测 | LangGraph overview | 长时、状态化工作流要有 persistence、durable execution、human-in-the-loop、observability | 为 `ai-native-loop` 的“经验复利回路”提供更成熟的运行时参照 |
| Skill 产品化样板 | `eze-is/web-access` | 强 README 价值主张、多安装路径、版本更新节奏、风险提示、跨 Agent 兼容说明、站点经验积累 | 对应本仓库的开源产品化、首次理解成本和发布节奏 |

### 2.3 对标后的核心判断标准

基于以上样本，我采用以下标准审这个仓库：

1. 是否把协议写成了最小可执行单元，而不是抽象概念。
2. 是否把主上下文控制在足够轻的规模，并让详细材料按需进入。
3. 是否对多 agent、工具调用、职责边界给出硬规则，而不是口头主张。
4. 是否建立了可复用、可回归、可抗自证偏差的验证机制。
5. 是否有足够清晰的首次使用路径、版本真相和演进证据。

## 3. 总体评估

| 维度 | 当前状态 | 优点 | 问题 | 风险 | 结论 |
|---|---|---|---|---|---|
| 项目定位 | 强 | 定位清楚，不伪装成万能 agent | 对外价值主张仍偏抽象 | 首次理解成本偏高 | 保持方向 |
| Skill 主体设计 | 强 | 四个核心工件足够硬，边界清楚 | 少量表述在仓库文档层重复 | 维护时易漂移 | 保留并收紧 |
| 上下文效率 | 中上 | `SKILL.md` 与 supporting docs 分层合理 | 仓库层重复叙事偏多 | 维护成本增加 | 运行时设计对，仓库层需减重 |
| 多 Agent 设计 | 中上 | 规则写得比多数项目成熟 | 证据不足，benchmark 仍待实测 | 能力声明跑在验证前面 | 先补实证 |
| 经验沉淀 | 中上 | 已有 field note -> pattern -> benchmark 链 | 仍依赖作者主动运营 | 外部用户难形成复利 | 需要产品化默认路径 |
| 评估体系 | 中 | 已有 benchmark 意识，已做固定场景 | 主要是回放、自评、内部打分 | 会误把叙事当改进 | 必须优先强化 |
| 版本与状态管理 | 中下 | 有 changelog、release notes、status memo | 多处真相不一致，状态文档已漂移 | 信任与维护一起受损 | 需要单一事实源 |
| 文档与开源产品化 | 中上 | 文档齐全，案例和说明不少 | 首次试用路径不够短促有力 | 采用门槛高于必要值 | 需要产品化压缩 |

### 总体判断

- 方向：正确
- 结构：已经跨过“只有理念没有工程”的门槛
- 主要瓶颈：证据体系、状态真相、默认路径
- 建议结论：**继续优化 + 局部重构，不建议重定方向**

## 4. 关键问题审计

### [P0] 验证体系的可信度不足，当前还不能强证明“仓库真的变好了”

- 现象/证据：
  - [`docs/self-evaluation.md`](docs/self-evaluation.md) 明确写明“使用 `ai-native-loop` 自己的协议来评估自己”。
  - [`docs/benchmark-results-v0.2.0.md`](docs/benchmark-results-v0.2.0.md) 明确说明这是一轮“回放式 benchmark，不是双盲 A/B 实验”。
  - 当前 benchmark 分数来自内部评分表，尚未看到外部评分者、对照基线、trace 级行为记录或持续回归机制。
  - OpenAI 官方评估文档强调：agent 评估应逐步引入 `traces`、`graders`、`datasets`、`eval runs` 与持续评估；评估方法更适合 pairwise / criteria-based，而不是开放式感受判断。
- 为什么这是问题：
  - 仓库已经进入“系统工程”阶段，最危险的不是没有评估，而是**评估看起来存在，但其实无法有效约束自我叙事**。
  - 一旦没有足够抗偏差的验证，后续版本很容易优化“文档形状”和“评分叙事”，而不是优化真实行为。
- 对实用主义效果的影响：
  - 无法可靠判断某次改动到底改善了可用性、稳定性、token 效率还是只是让输出更像“规范答案”。
  - 很难让后续 CodeX/Agent 接手时知道哪些规则值得保留，哪些只是作者偏好。
- 与外部优秀实践对比：
  - OpenAI 建议先用 traces 找 workflow 级失败，再用数据集和 eval runs 做可重复对比。
  - OpenAI 也明确指出，多 agent 复杂度应由 eval 驱动，而不是先上架构再补理由。
  - LangGraph/ LangSmith 路径进一步说明：可观测性与状态追踪是复杂 agent 体系的基础设施，而不是后补件。
- 建议优化：
  - 建立三层验证栈：
    - 第 1 层：每次典型任务保留 trace-like 运行记录，至少包括原始请求、介入等级、产出工件、失败点、下一轮输入。
    - 第 2 层：每个 benchmark 场景增加 baseline，对比“无 Skill / 轻提示 / 当前 Skill”三种条件。
    - 第 3 层：对关键场景采用 pairwise rubric 评分，至少引入一个外部评分者或外部 judge 模型。
  - 把 benchmark 结果从“总分叙述”改为“改动 -> 指标 -> 结果 -> 结论”的实验格式。
  - 对高价值能力声明单独设通过门槛，例如：多 agent、决策整理、经验回收。
- 预期收益：
  - 真正建立“发现失败 -> 修改协议 -> 验证收益”的迭代飞轮。
  - 降低后续版本被自证偏差带偏的概率。
- 验证方式：
  - 选 10 个固定任务，至少 3 个新任务、3 个历史任务、4 个边界任务。
  - 每个任务在基线与当前版本下各跑 1 次。
  - 用统一 rubric 做 pairwise 评分。
  - 如果 2 轮迭代后没有显著提升，就停止继续补文档，回头改协议或边界。

### [P1] 版本状态与项目真相已经出现漂移，仓库缺少单一事实源

- 现象/证据：
  - [`README.md`](README.md) 仍写当前版本是 `v0.1.0`，`v0.2.0 execution in progress`。
  - [`SKILL.md`](SKILL.md) metadata version 仍是 `0.1.0`。
  - [`CHANGELOG.md`](CHANGELOG.md) 把大量成果仍放在 `Unreleased`。
  - [`docs/project-status-memo-v0.2.0.md`](docs/project-status-memo-v0.2.0.md) 写当前 `HEAD=b27bb0f` 且已与 `origin/main` 对齐；但审计时真实 `git log` 显示本地 `HEAD=6d81340`，远端仍在 `b27bb0f`。
- 为什么这是问题：
  - 当仓库开始依赖大量“状态说明文档”时，**状态文档本身必须高度可信**；否则就会制造新的上下文债务。
  - 对协议型仓库来说，版本叙事本身也是产品的一部分。版本真相不准，会直接损伤外部信任。
- 对实用主义效果的影响：
  - 新接手者很难判断当前到底该基于哪一版继续工作。
  - benchmark、release、README、status memo 之间的关系变得不确定。
- 与外部优秀实践对比：
  - 成熟项目通常会把版本号、当前轨道、release 状态尽量收口到少数事实源。
  - `web-access` 这类产品化仓库在 README 顶部就把版本、更新点、安装方式和能力清单压在一个清晰入口里，不依赖多份状态 memo 共同解释。
- 建议优化：
  - 设一个仓库级单一事实源，例如 `docs/release-manifest.md` 或 `version.json`。
  - README、SKILL metadata、CHANGELOG、release notes 都从这一个源更新。
  - 停止维护“快过时的 snapshot memo”，除非它是自动生成的。
  - 对 status 类文档添加“审计时点”与“已过期”标记。
- 预期收益：
  - 大幅降低接手成本和误判概率。
  - 让版本化本身成为可依赖的工程信号。
- 验证方式：
  - 写一个最小一致性检查表，检查 README / SKILL / CHANGELOG / git tag / release notes 是否一致。
  - 每次准备发布前跑一次。

### [P1] 经验沉淀机制仍然偏作者运营型，还没有变成外部用户的默认路径

- 现象/证据：
  - [`references/experience-compounding-loop.md`](references/experience-compounding-loop.md) 已明确承认当前目标只是先稳定做到 `Level 2` 与 `Level 3`。
  - `field note` 仍需要人工记录、人工 triage、人工 promote。
  - 仓库里已有 promotion chain，但更像“作者会运营时很好用”，而不是“新用户默认就会留下可升级回收物”。
- 为什么这是问题：
  - 协议型 Skill 真正的壁垒不只是理论，而是**经验如何低摩擦进入系统**。
  - 如果经验沉淀只在作者手上发生，仓库的可扩展性会被作者注意力上限锁死。
- 对实用主义效果的影响：
  - 外部用户用了也难以贡献有价值的样本。
  - 经验飞轮会慢，pattern/failure mode/benchmark 更新节奏无法稳定。
- 与外部优秀实践对比：
  - Anthropic 的 Skill 体系强调把主技能与 supporting resources 解耦，并允许脚本和动态上下文注入；成熟系统会努力把默认路径做短，而不是假设用户愿意手工整理。
  - LangGraph 一类框架把状态、持久化、回放和观察作为基础设施，而不是额外习惯。
- 建议优化：
  - 为 `medium` 及以上介入定义统一的“结束回收块”，默认就出现在输出末尾。
  - 提供一个最短 field note 模板和一个升级判断清单，减少人工自由发挥。
  - 让 case/pattern/failure/benchmark 的 promotion 规则从文字说明变成固定表格。
  - 后续再考虑半自动汇总，而不是一开始追求自动升级。
- 预期收益：
  - 把经验沉淀从“高手习惯”变成“系统默认动作”。
  - 提高仓库的复利速度与外部可贡献性。
- 验证方式：
  - 连续记录 20 次中介入以上任务，统计：
    - 有多少次留下最小回收物
    - 有多少次可进入 pattern/failure/benchmark
    - 升级所需人工时间是多少

### [P1] 多 Agent 能力的规则层已经成熟，但证明层明显滞后

- 现象/证据：
  - [`references/multi-agent-decomposition.md`](references/multi-agent-decomposition.md) 已经把“不拆优先”“四问判断”“主 agent 保留职责”“子 agent 最小输入包”“统一回收物”等关键规则写得很硬。
  - [`docs/benchmarks/benchmark-05-multi-agent-decomposition.md`](docs/benchmarks/benchmark-05-multi-agent-decomposition.md) 仍明确写“场景已建立，待执行实测”。
  - README 与 SKILL 都已把 Agent 协作列为覆盖场景之一。
- 为什么这是问题：
  - 仓库现在存在“规则成熟度 > 证据成熟度”的不平衡。
  - 这会让一个本来很稳健的规则文档，变成潜在的过度承诺。
- 对实用主义效果的影响：
  - 用户会自然认为多 agent 是已经被验证的强项，但现有证据并不足以支撑这一印象。
  - 如果后续实测发现某些拆分模式并不稳，修正成本会升高。
- 与外部优秀实践对比：
  - Anthropic subagents 文档强调：适合隔离高噪声任务，但不适合频繁往返共享上下文的任务。
  - OpenAI 官方明确建议：多 agent 复杂度应由 evals 驱动，别过早上多 agent 架构。
  - 这意味着 `ai-native-loop` 的规则方向是对的，但还需要真实案例去证明“这些规则在实际复杂任务里确实有效”。
- 建议优化：
  - 至少补 2 个 live multi-agent case：
    - 一个“应该拆”的场景
    - 一个“看似应该拆，实际不该拆”的场景
  - 对每个 case 记录：
    - 是否真的节省主上下文
    - 是否降低了整合成本
    - 是否提升了结果稳定性
  - 把 benchmark 05 从“定义场景”升级成“可重复执行模板 + 已跑结果”。
- 预期收益：
  - 让多 agent 能力从“好看的规则”变成“可信的能力”。
- 验证方式：
  - 对同一个复杂任务分别跑单线程与多 agent 两个版本。
  - 评估结果质量、主上下文噪声、协调成本、完成时间。

### [P1] 首次上手路径仍然偏重“阅读理解”，不够偏“快速试用”

- 现象/证据：
  - README 内容完整，但更像系统说明入口，不像“30 秒理解是否值得试”的强产品首页。
  - [`agents/openai.yaml`](agents/openai.yaml) 只有最基础的展示字段，缺少更强的 UI-facing 能力指向。
  - [`docs/self-evaluation.md`](docs/self-evaluation.md) 自己也承认首次接触仍需要 README 和前测样例帮助理解。
  - 对比 `web-access` README，后者在顶层就集中回答：为什么存在、解决什么、怎么装、怎么用、最近更新了什么、有哪些风险。
- 为什么这是问题：
  - 协议型 Skill 的最大门槛不是“没有内容”，而是“用户不确定何时值得触发它”。
  - 当首次理解路径太长，外部用户更容易把它当方法论文档，而不是会真正调用的 Skill。
- 对实用主义效果的影响：
  - 降低安装后的真实激活率。
  - 让本来可以通过一两个 before/after 就讲清楚的价值，变成大段阅读成本。
- 与外部优秀实践对比：
  - Anthropic skills 文档明确建议 skill description 要前置关键 use case 且足够短。
  - `web-access` 这类成熟 Skill 仓库优先优化的是“装完马上能试”，而不是“读完更理解理念”。
- 建议优化：
  - 在 README 顶部加入一个 30 秒 smoke test：
    - 什么请求最适合触发
    - 触发后会得到什么
    - 一次最小成功长什么样
  - 加 2 到 3 个 before/after triplet：
    - 原始混乱请求
    - Skill 重写后的任务包
    - 下一轮检查点
  - 把“不该触发”的例子提前到顶层，而不是藏在后面。
- 预期收益：
  - 显著降低首次试错成本。
  - 提高“读完即试”的转化率。
- 验证方式：
  - 找 3 个没参与仓库建设的人，限定 5 分钟内完成首次试用。
  - 记录他们是否能独立判断何时触发、是否知道结果算成功。

### [P2] 仓库级文档开始出现叙事重复，维护成本会先于运行时成本上升

- 现象/证据：
  - `README`、`self-evaluation`、`forward-test`、`project-status memo`、`iteration assessment` 都在重复解释项目价值、状态与下一步。
  - 这类重复并未明显伤害运行时上下文，因为主 Skill 仍采用 supporting files 按需加载；但它正在伤害仓库维护清晰度。
- 为什么这是问题：
  - 重复叙事短期让仓库显得丰满，长期则会制造“哪一份才是现在的判断”的维护摩擦。
  - 当项目继续增长，重复文档会成为事实漂移的温床。
- 对实用主义效果的影响：
  - 仓库接手者需要花更多时间判断“哪份文档是当下有效的”。
  - 后续 CodeX/Agent 更难在低上下文成本下完成版本判断。
- 与外部优秀实践对比：
  - Anthropic 对 skills 的建议是主文件聚焦，细节按需进入；这一原则其实也适用于仓库文档层。
- 建议优化：
  - 仓库文档按角色收束成三类：
    - 用户入口文档
    - 版本/状态文档
    - 研究/实验文档
  - 相似判断只保留一处主叙述，其他地方链接引用。
- 预期收益：
  - 降低后续维护的认知负担。
- 验证方式：
  - 让一个未参与项目的人在 10 分钟内回答：当前版本、当前主风险、下一轮优先级是什么。
  - 如果还需要翻 4 份以上文档，说明收束不够。

## 5. 值得保留的设计

### 5.1 协议定位清楚，而且边界意识强

这个仓库最大的优点，是很少犯“既想做协议层，又想假装自己是万能执行 agent”的错。  
`README` 和 `SKILL.md` 都清楚划出了“不适合什么”“不替用户做什么”“不该何时触发”。

这是值得保留的，因为协议型仓库最怕能力边界模糊。

### 5.2 四个核心工件是一个好抽象，而且足够最小

`Diagnosis Card / Task Packet / Feedback Attribution Card / Re-input Packet` 这四个工件，不是为了形式完整，而是确实对应了闭环中最关键的四个动作。  
它们已经足够小，不属于过度建模。

这是本仓库最值得长期保留的“骨架”。

### 5.3 运行时上下文设计是成熟的

相比很多把一切塞进单个主文件的 Skill 仓库，`ai-native-loop` 已经把主 Skill 与 supporting references 分开。  
这与 Anthropic 官方对 Skill 设计的建议一致：主文件聚焦，详细参考按需加载。

这意味着本仓库的**运行时 token 设计是对的**。  
真正需要减的是仓库层重复，不是把 `SKILL.md` 再拆碎。

### 5.4 经验 promotion chain 已经具备很好的雏形

从 field note 到 pattern、failure mode、benchmark 的链条，是这个仓库未来最有可能形成护城河的部分。  
多数同类仓库停留在“写了一些原则”；这个仓库已经开始试图把经验做成结构资产。

### 5.5 多 Agent 部分的“默认不拆”立场很成熟

这点很重要。  
当前多 agent 相关文档不是在鼓励滥拆，而是强调：

- 默认不拆
- 能否边界化
- 主 agent 保留判断权
- 子 agent 必须有最小输入包与回收物

这与外部成熟实践高度一致，应该保留。

## 6. 优化建议与路线图

### 6.1 方向层（A层）

#### 定位建议

- 保持“协议型 Skill”定位，不要改成通用 agent 框架。
- 但要把项目叙事从“方法论完整”升级为“协议 + 证据 + 版本真相”三位一体。

#### 设计原则建议

1. 能力声明必须落后于实测，而不是领先于实测。
2. 版本真相必须单点维护，不允许多份状态文档同时解释当前状态。
3. 默认路径优先于理想路径，先让外部用户容易触发、容易回收，再谈自动化。
4. 文档增量必须服从验证增量，不能用更多文档代替更强证据。

#### 结构边界建议

- `SKILL.md` 继续做运行时协议入口。
- `references/` 继续做按需加载材料。
- `docs/` 应逐步收束成：
  - `docs/user/`：面向首次使用与案例
  - `docs/evals/`：benchmark、rubric、结果
  - `docs/releases/`：版本、状态、迭代说明

#### 中长期演进建议

- 近期：补验证体系、补状态单源、补默认回收路径。
- 中期：把经验回收做成低摩擦默认流程。
- 远期：如果真实使用量上来，再考虑半自动经验提炼与更正式的实验流水线。

### 6.2 执行层（B层）

| 动作 | 解决的问题 | 优先级 | 预估收益 | 实施难度 | 验证方式 |
|---|---|---|---|---|---|
| 建立 benchmark baseline 与 pairwise rubric | 解决自证偏差与不可比较 | P0 | 高 | 中 | 10 个固定任务对照跑分 |
| 增加 trace-like 任务记录模板 | 解决 workflow 级失败不可观测 | P0 | 高 | 中 | 每次 benchmark 都能回放决策链 |
| 收口版本单一事实源 | 解决 README/SKILL/CHANGELOG/status 漂移 | P1 | 高 | 低 | 版本一致性检查通过 |
| 跑通 2 个 live multi-agent case | 解决多 agent 证明不足 | P1 | 高 | 中 | 单线程 vs 多 agent 对照 |
| 把 medium+ 默认输出附带最小回收块 | 解决经验沉淀仍靠作者主动 | P1 | 高 | 中 | 20 次任务回收率提升 |
| 重写 README 顶部入口为 smoke test + before/after | 解决首次上手成本偏高 | P1 | 中高 | 低 | 5 分钟首次试用成功率 |
| 收束重复状态文档 | 解决维护成本与事实漂移 | P2 | 中 | 中 | 新接手者 10 分钟内可定位现状 |
| 丰富 `agents/openai.yaml` 与 UI-facing metadata | 解决产品面信息不足 | P2 | 中 | 低 | 安装后识别与触发意图更稳定 |

### 6.3 推荐执行顺序

1. 先做验证体系，而不是先写更多案例说明。
2. 再做版本单源和状态收口。
3. 再补 live multi-agent case。
4. 再优化 README 顶部路径。
5. 最后处理仓库级文档减重和 metadata 美化。

哪些先不做：

- 先不追求自动生成完整 case study。
- 先不做大规模目录重构。
- 先不急着扩很多新 pattern。
- 先不把多 agent 做成主卖点，直到证据足够。

## 7. 效果衡量框架

核心问题不是“文档变多了吗”，而是：**如何知道这个 Skill 真的更好用了？**

| 维度 | 衡量定义 | 可观测信号 | 可执行指标 | 低成本评估方法 | 中长期建议 |
|---|---|---|---|---|---|
| 可用性 | 用户是否能在首次接触时成功触发并得到有帮助的工件 | 首次触发成功；知道何时该用/不该用 | 首次试用成功率、5 分钟内完成率 | 让 3-5 个陌生用户做 smoke test | 持续收集首次使用失败样本 |
| 稳定性 | 同类任务下输出结构是否稳定、边界是否一致 | 工件缺失率低；边界违规少 | 四个工件出现率、边界违规率 | 固定 benchmark 回放 | 引入持续回归与变更前后对照 |
| 泛化性 | 同一协议是否能迁移到不同知识工作 | 新场景仍能收敛成同类工件 | 场景覆盖数、跨场景平均分 | 每轮新增 1 个异类场景 benchmark | 保持场景分布平衡，不只围绕作者高频任务 |
| 可维护性 | 后续维护者能否低成本判断现状与下一步 | 版本真相一致；状态文档不冲突 | 版本一致性检查通过率 | 人工 checklist | 最终脚本化一致性检查 |
| 可扩展性 | 新案例、新 failure mode、新 pattern 能否低摩擦进入系统 | promotion 流程顺畅；人工成本可控 | 平均升级耗时、升级成功率 | 统计 20 次 field note promotion | 后续才考虑半自动 triage |
| token / 上下文效率 | 运行时是否尽量少读无关材料，仓库是否避免重复叙事 | `SKILL.md` 保持聚焦；补充材料按需读 | 主 Skill 长度、单任务平均加载文件数 | 人工抽样任务回放 | 增加真实 token 使用观测 |
| 首次上手成本 | 外部用户理解并触发的门槛有多高 | 需要看几份文档才能开跑 | 首次成功所需时间、阅读文件数 | 5 分钟可用性测试 | 长期看激活率与复访率 |
| 复用性 | 成功做法能否从个案抽成模式 | field note 能顺利升级 | field note -> pattern 转化率 | 每月人工 review | 做 pattern 生命周期管理 |
| 输出质量一致性 | 不同任务下是否都能给出稳定而不空泛的结构结果 | 不再大量出现“看起来规范但不好用” | rubric 平均分、标准差 | pairwise rubric 评分 | 建立 judge + 人工混合评审 |
| 对真实任务的帮助程度 | 是否真能减少卡点、推进下一轮，而不只是把问题写漂亮 | 用户能继续推进；下一检查点清晰 | 下一轮推进率、阻塞消除率 | 在 case 中记录“是否推进了真实工作” | 长期收集使用后结果与满意度 |

### 7.1 推荐 rubric 结构

对每个 benchmark，至少打以下 8 项：

1. `clarity`
2. `executability`
3. `boundary_control`
4. `feedback_quality`
5. `reinput_quality`
6. `transferability`
7. `context_efficiency`
8. `real_task_helpfulness`

建议优先采用：

- pairwise 比较
- pass/fail + 说明
- 明确样例的评分标准

不建议主要依赖：

- 单次开放式“总体感觉分”
- 作者自己既当设计者又当唯一评分者

### 7.2 建议 benchmark task set 结构

- 研究分析：1 个作者熟悉场景 + 1 个陌生公开主题
- 写作表达：1 个高材料输入场景
- 产品推进：1 个跨材料、跨阶段场景
- 决策整理：1 个高边界风险场景
- 多 Agent：1 个该拆场景 + 1 个不该拆场景
- 边界任务：1 个明显不该触发 `ai-native-loop` 的任务

### 7.3 before/after 对比思路

每个评测都至少保留：

- 原始请求
- 不使用 Skill 的输出
- 使用 Skill 的输出
- 下一轮是否更容易继续
- 结果由谁评分、按什么 rubric 评分

### 7.4 experiment log 建议

每次迭代只记录四件事：

- 本轮假设是什么
- 改了哪条规则或哪份文档
- 影响哪个 benchmark / 指标
- 结果如何，是否保留

这样才能避免“盲目继续补内容”。

## 8. 后续建议给 CodeX 的工作方式

如果后续继续迭代，我建议 CodeX 按下面方式使用这份报告。

### 8.1 从哪里开始

先从 **P0 验证体系** 开始，不要再优先补新的内容文件。  
当前仓库最缺的不是理论，而是证明。

### 8.2 优先改什么

优先级顺序：

1. benchmark 与 rubric 升级
2. 版本单源
3. live multi-agent case
4. README 顶部试用路径
5. medium+ 默认回收块

### 8.3 如何记录实验

每轮只允许一个核心假设，例如：

- “加入 baseline 后，决策整理场景是否仍保持优势？”
- “默认回收块是否能提升 field note 留存率？”
- “多 agent 是否真的降低主上下文噪声？”

每轮实验都应留下：

- 假设
- 改动
- benchmark
- 结果
- 保留/回滚判断

### 8.4 如何避免盲目重构

- 不动四个核心工件，除非 benchmark 明确显示它们有结构性缺陷。
- 不大改目录，除非版本/状态单源已经建立。
- 不因为“文档看起来多”就继续扩文档；先问它是否增加了可验证能力。

### 8.5 如何逐轮验证收益

- 每轮只追一个主指标。
- 每轮至少跑 3 个固定 benchmark。
- 每轮结束时都回答：
  - 哪项行为更好了？
  - 哪项行为没变？
  - 有没有新副作用？

如果回答不出来，就说明这轮迭代仍然偏叙事，不偏工程。

## 9. 附录

### 9.1 本次审计重点使用的仓库证据

- [`README.md`](README.md)
- [`SKILL.md`](SKILL.md)
- [`agents/openai.yaml`](agents/openai.yaml)
- [`references/core-operating-primitives.md`](references/core-operating-primitives.md)
- [`references/failure-modes.md`](references/failure-modes.md)
- [`references/multi-agent-decomposition.md`](references/multi-agent-decomposition.md)
- [`references/experience-compounding-loop.md`](references/experience-compounding-loop.md)
- [`patterns/README.md`](patterns/README.md)
- [`docs/benchmark-matrix.md`](docs/benchmark-matrix.md)
- [`docs/benchmark-results-v0.2.0.md`](docs/benchmark-results-v0.2.0.md)
- [`docs/benchmarks/benchmark-05-multi-agent-decomposition.md`](docs/benchmarks/benchmark-05-multi-agent-decomposition.md)
- [`docs/project-status-memo-v0.2.0.md`](docs/project-status-memo-v0.2.0.md)
- [`docs/self-evaluation.md`](docs/self-evaluation.md)
- [`docs/forward-test.md`](docs/forward-test.md)
- [`docs/trigger-examples.md`](docs/trigger-examples.md)
- [`docs/iteration-assessment-against-web-access.md`](docs/iteration-assessment-against-web-access.md)

### 9.2 外部参考资料

- Anthropic Claude Code Skills: [https://code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands)
- Anthropic Claude Code Subagents: [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)
- OpenAI Agents SDK, Agent orchestration: [https://openai.github.io/openai-agents-python/multi_agent/](https://openai.github.io/openai-agents-python/multi_agent/)
- OpenAI, Evaluate agent workflows: [https://developers.openai.com/api/docs/guides/agent-evals](https://developers.openai.com/api/docs/guides/agent-evals)
- OpenAI, Evaluation best practices: [https://developers.openai.com/api/docs/guides/evaluation-best-practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- LangGraph overview: [https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)
- LangChain Deep Agents Subagents: [https://docs.langchain.com/oss/python/deepagents/subagents](https://docs.langchain.com/oss/python/deepagents/subagents)
- `eze-is/web-access` README: [https://github.com/eze-is/web-access](https://github.com/eze-is/web-access)

### 9.3 可直接复用的审计 rubric

如果以后继续审类似 Skill / Agent 仓库，可直接沿用这 6 个总问题：

1. 这个仓库到底在解决什么，不解决什么？
2. 核心协议是否已经被压成最小可执行工件？
3. 能力声明与实测证据是否匹配？
4. 经验能否低摩擦进入系统并持续复利？
5. 版本真相和仓库状态是否有单一事实源？
6. 新接手的 Agent/维护者能否低上下文成本继续推进？

### 9.4 尚未充分确认、但值得后续验证的问题

- 外部陌生用户在不读长文档的情况下，能否独立正确触发本 Skill？
- 多 agent 实测中，`ai-native-loop` 的规则是否真能稳定降低协调成本？
- 决策整理场景的低分项，根因是协议本身，还是当前 benchmark 样本选择问题？
- 默认回收块加入后，是否会反向增加轻任务的负担？
- 当前四个核心工件是否已经是最优最小集合，还是未来应进一步收缩？

## 最终判断

`ai-native-loop` 已经是一个**值得继续投入的协议型 Skill 仓库**，它最大的价值不在“讲 AI native”，而在“开始把 AI native 写成可执行、可评估、可沉淀的结构”。  

但它现在也正处在一个很关键的分水岭：

- 再往前走，可以变成“有协议、有证据、有复利机制”的少数派项目。
- 走偏的话，则会变成“文档越来越完整、叙事越来越高级、但很难证明到底变好了没有”的项目。

因此，下一轮最该做的不是再补更多内容，而是**把证据体系和版本真相做硬**。
