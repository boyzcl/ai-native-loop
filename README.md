# ai-native-loop

`ai-native-loop` 是一个协议型工作流 Skill。

它现在把两层东西分开维护：

- 宿主无关的闭环协议
- 宿主相关的 runtime / invocation / metadata 适配

它解决的不是“再给我一个答案”，而是：

- 输入太乱，当前轮任务包不清楚
- AI 已经有输出，但反馈进不了下一轮
- 任务跨阶段或多 Agent，结果难回收
- 经验用过一次就蒸发，下次还要重新摸索

一句话说：

> 当你真正卡住的是协作闭环，而不是单点答案时，用 `ai-native-loop`。

## Release Status

- Release truth: [release-manifest.md](docs/release-manifest.md)
- Current public version: `v0.2.0`
- Current iteration track: `v0.2.0` published / local auto-promotion + capacity governance + validated retrieval + repo-candidate review workflow

## 60-Second Start

### Install

官方支持面的快速安装先以 `Codex` 为准：

```bash
git clone https://github.com/boyzcl/ai-native-loop.git ~/.codex/skills/ai-native-loop
python3 ~/.codex/skills/ai-native-loop/scripts/init_runtime_memory.py --host codex
```

如果你不在 `Codex` 宿主里，先看 [compatibility-and-invocation.md](docs/compatibility-and-invocation.md) 和 [compatibility-matrix.md](docs/compatibility-matrix.md)，再用 `--host` 或 `--root` 初始化 runtime。

### Use It Explicitly

当前版本默认建议显式调用：

- `用 $ai-native-loop 帮我把这个任务整理成更适合 AI 协作的闭环。`
- `用 $ai-native-loop 看看我现在卡住的根因是在输入、执行还是反馈。`
- `用 $ai-native-loop 帮我把这轮结果折叠成下一轮输入，并写入 runtime capture。`

不要依赖隐式触发来判断项目是否“可用”。

### What You Will See

典型输出会收敛为：

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`
- `Loop Recovery Block`

对 `medium` 及以上介入，默认还应把这轮结构化经验写入当前宿主解析出的 runtime root：

- `Codex` 默认：`~/.codex/skills/ai-native-loop/runtime/captures/`
- `Claude Code` 适配草案默认：`~/.claude/skills/ai-native-loop/runtime/captures/`
- 任意宿主都可被 `AI_NATIVE_LOOP_RUNTIME_ROOT` 或 `--root` 覆盖

## When To Use

优先在下面这些情况使用：

- 需求、材料、历史尝试、报错混在一起，当前轮任务包不清楚
- 已经有 AI 输出，但不知道该保留什么、丢弃什么、怎么进入下一轮
- 你能感觉结果不对，但说不清错在哪，也不知道 prompt / protocol 该怎么改
- 多角色或多 Agent 协作边界不清，回收物难整合
- 同类问题已经重复至少两轮，但输入、分工或评估方式没有真正改写

通常不要在下面这些情况使用：

- 单点事实查询
- 翻译、改格式、改单个小项、机械执行
- 目标、交付物和验收标准都很清楚，只差直接执行
- 已有更窄、更强的领域 skill 足够解决

更完整的触发规则见 [SKILL.md](SKILL.md)、[trigger-examples.md](docs/trigger-examples.md) 和 [trigger-regression-suite.md](docs/trigger-regression-suite.md)。

## Why This Version Is Different

`v0.2.0` 的关键变化不只是多了几份文档，而是把经验沉淀从“回答尾部的协议块”推进成“本地 skill 目录中的默认运行层”：

- `medium+` 任务结束后保留 `Loop Recovery Block`
- 同结构内容写入本地 `runtime capture`
- 下一次调用时只按需读取少量相关经验
- 值得提升的样本再进入 field note / repo candidate，repo 公开资产继续保持 gate

运行时规格见 [runtime-memory-spec.md](docs/runtime-memory-spec.md)，四层拆分见 [host-abstraction.md](docs/host-abstraction.md)。

## Before / After

Before：

> 我在改一个复杂功能，需求、历史尝试、报错和几段代码都混在一起了，你先帮我看看怎么继续。

After：

> 用 `ai-native-loop` 先输出 `Diagnosis Card` 和 `Task Packet`：明确这轮目标、当前状态、约束、成功信号和下一检查点；如果判断为 `medium` 以上介入，再补反馈归因、下一轮输入，并把 recovery block 写入本地 runtime capture。

## Compatibility

当前推荐使用方式与已验证前提见：

- [compatibility-and-invocation.md](docs/compatibility-and-invocation.md)
- [compatibility-matrix.md](docs/compatibility-matrix.md)

一句话版本：

- `Codex`：`officially supported`
- `Claude Code`：`experimental`
- `OpenClaw`：`experimental`
- 其他宿主：`theoretically portable`
- 推荐触发方式：显式调用 `$ai-native-loop`
- 当前不推荐把隐式触发当作稳定能力承诺

## Proof Pack

如果你只想快速判断它是否值得试，先看：

- [proof-pack.md](docs/proof-pack.md)

这里包含：

- 一个可复制输入
- 一个目标输出形状
- 一个 runtime capture 示例
- 一个验证入口

## Validation

这个仓库已经不只是在写理念，也在补验证与经验复利层：

- 版本与状态单一事实源： [release-manifest.md](docs/release-manifest.md)
- Skill 结构图： [skill-architecture.md](docs/skill-architecture.md)
- 宿主抽象与四层拆分： [host-abstraction.md](docs/host-abstraction.md)
- 兼容矩阵： [compatibility-matrix.md](docs/compatibility-matrix.md)
- 运行时经验层规格： [runtime-memory-spec.md](docs/runtime-memory-spec.md)
- 运行时晋升策略： [runtime-promotion-policy.md](docs/runtime-promotion-policy.md)
- 触发边界与回归集： [trigger-examples.md](docs/trigger-examples.md), [trigger-regression-suite.md](docs/trigger-regression-suite.md)
- benchmark 矩阵： [benchmark-matrix.md](docs/benchmark-matrix.md)
- 统一评分标准： [evaluation-rubric.md](docs/evaluation-rubric.md)
- 实验模板： [experiment-log-template.md](docs/experiment-log-template.md)
- 当前 benchmark 汇总： [benchmark-results-v0.2.0.md](docs/benchmark-results-v0.2.0.md)

## Runtime Helpers

本轮新增的 runtime helper scripts 已统一支持 `--host` / `--root`：

- `scripts/init_runtime_memory.py`
- `scripts/validate_runtime_memory.py`
- `scripts/smoke_test_runtime_memory.py`
- `scripts/write_runtime_capture.py`
- `scripts/read_runtime_context.py`
- `scripts/promotion_worker.py`
- `scripts/runtime_governance_report.py`
- `scripts/review_repo_candidates.py`
- `scripts/retrieval_forward_test.py`
- `scripts/runtime_governance_stress_test.py`
- `scripts/set_repo_candidate_status.py`

它们分别用于：

- 初始化本地 runtime 目录
- 校验 runtime 结构与 capture schema
- 用临时目录跑一轮端到端 smoke test
- 把一条结构化记录追加到本地 runtime capture
- 按 `scene` 读取最近的 runtime 经验，并可带上 promoted field notes；必要时把命中写回 reuse ledger
- 消费 review queue，执行本地自动晋升、merge、archive 与 gated repo candidate
- 输出 backlog / promote / merge / archive / reuse / repo candidate 的治理指标
- 列出并更新 repo candidate review workflow 的 `pending / accepted / rejected`
- 对 promoted retrieval 跑 forward test，并记录 false positive / false negative 风险
- 用 temp runtime replay 更大 backlog / 更长周期，验证 working set 与 candidate count 是否仍受控
- 为 repo candidate 写入 `pending / accepted / rejected` 的 review 状态，而不直接改 repo 公共资产
- 根据宿主、环境变量和显式参数解析默认 runtime root

## Feedback Loop

repo 侧已经补了最小反馈入口：

- `False Positive Trigger`
- `False Negative Trigger`
- `Share Runtime Capture`

这些模板的目标不是做社区装饰，而是把触发边界和 runtime 经验层真正推向外部反馈。

## Repo Map

如果你第一次看这个仓库，最值得先读的是这些文件：

- [SKILL.md](SKILL.md)
- [docs/host-abstraction.md](docs/host-abstraction.md)
- [docs/compatibility-matrix.md](docs/compatibility-matrix.md)
- [docs/runtime-memory-spec.md](docs/runtime-memory-spec.md)
- [docs/runtime-promotion-policy.md](docs/runtime-promotion-policy.md)
- [references/core-operating-primitives.md](references/core-operating-primitives.md)
- [references/experience-compounding-loop.md](references/experience-compounding-loop.md)
- [docs/benchmark-matrix.md](docs/benchmark-matrix.md)
- [docs/benchmark-results-v0.2.0.md](docs/benchmark-results-v0.2.0.md)

## License

MIT
