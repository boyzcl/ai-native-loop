# Benchmark 01: Research Analysis / mRNA Investigation

## Scenario

- Category: 研究分析
- Source materials:
  - [执行指令.md](/Users/boyzcl/Documents/A/存量文章撰写/mRNA/执行指令.md)
  - [findings.md](/Users/boyzcl/Documents/A/存量文章撰写/mRNA/findings.md)
  - [pipeline.md](/Users/boyzcl/Documents/A/存量文章撰写/mRNA/pipeline.md)
  - [report.md](/Users/boyzcl/Documents/A/存量文章撰写/mRNA/report.md)

## Original Request

“深度调查 Rosie 个性化 mRNA 疫苗事件，还原事件与技术流水线，并最终产出调查报告与操作手册。”

## Initial Block

- 任务同时包含新闻调查、技术溯源、可信度判断和技术手册写作。
- 如果直接写终稿，事实、推断和技术背景会混在一起。
- 需要多个中间工件，否则研究过程不可回收。

## Intervention Level

`medium`

原因：

- 目标清晰，但执行链路复杂。
- 来源多、可信度不一。
- 最终输出至少包含调查层、手册层和整合层。

## Core Artifacts Produced

### Diagnosis Card

- loop_stage: input -> execution
- intervention_level: medium
- primary_block: 复杂研究任务缺少中间工件，直接成稿风险高
- risk_note: 如果不区分已确认、推断、缺口，最终报告会失真

### Task Packet

- objective: 还原 Rosie 事件与技术流水线，形成可验证的调查结构
- current_state: 有明确主题，但需要从公开来源重建完整链路
- artifacts: 新闻源、社交媒体线索、研究背景文献、已有中间文件
- constraints: 必须区分事实、推断和公开缺口
- success_signal: 形成调查报告、技术手册和整合报告三层结构
- next_checkpoint: 检查每个技术节点是否都有可信度标注

### Feedback Attribution Card

- signal: 某些关键技术节点公开信息不足
- failure_class: context failure
- root_cause: 公开材料对具体测序细节、算法和配方披露有限
- keep: 时间线、人物、关键转折和流程框架都可成立
- change: 在最终报告中显式保留信息缺口和推断边界

### Re-input Packet

- preserve: 时间线、人物档案、技术节点拆解、可信度地图
- discard: 对未公开细节的过度补全冲动
- add_context: 背景技术文献与行业标准流程
- change_request: 把中间产物折叠成终稿，同时保留读者可见的证据边界
- next_checkpoint: 检查终稿是否把调查层和技术层自然接合

## Output Result

- 形成了一份可验证的事件调查结构。
- 技术流程被单独拆成 `pipeline.md`，避免被叙事层吞掉。
- 最终 `report.md` 将调查层和技术层合并，但保留了信息缺口意识。

## Re-input Quality

本案例中，再输入不是停留在“继续写”，而是把：

- `findings.md`
- `pipeline.md`

折叠成了新的输入，最终得到 [report.md](/Users/boyzcl/Documents/A/存量文章撰写/mRNA/report.md)。

## Scores

| Dimension | Score | Note |
|---|---:|---|
| clarity | 5.0 | 原始复杂主题被压成可管理的三层结构 |
| executability | 4.8 | 中间工件清晰，能持续推进 |
| feedback_quality | 4.8 | 明确区分已确认、推断、缺口 |
| reinput_quality | 4.9 | 中间产物直接进入终稿生成 |
| transferability | 4.8 | 可迁移到其他复杂研究任务 |

## Verdict

通过。

这证明 `ai-native-loop` 在研究分析场景中不仅能改善表达，还能改善研究结构和反馈利用方式。
