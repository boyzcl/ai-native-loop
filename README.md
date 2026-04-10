# ai-native-loop

`ai-native-loop` 是一个面向广义知识工作的底层协议型 Skill。

它不把 AI 当作单点工具，而把 AI 当作工作环境，帮助用户持续重写输入、执行、反馈与再输入闭环。它适用于编码、研究、写作、产品思考、决策推进、Agent 协作与多轮任务推进。

## 仓库内容

- `skill/`
  可直接安装和使用的 Skill 本体。
- `docs/self-evaluation.md`
  使用 `ai-native-loop` 对当前 Skill 做的完成度与质量评估。
- `docs/forward-test.md`
  用真实任务链路对 Skill 做的实际前测。
- `docs/release-readiness.md`
  面向 GitHub 开源发布的完成度检查。
- `docs/cases/case-01-self-bootstrap.md`
  首个正式案例：Skill 用自己完成自评、补齐、验证与发布。
- `ai-native-loop-delivery.md`
  设计规格与完整 Skill 方案。

## Skill 定位

这个 Skill 是一个工作协议层，而不是：

- 单次任务顾问
- 提示词美化器
- 编程专用技巧包
- 替用户思考的黑箱代理

它的核心目标是帮助用户形成稳定、可迁移、可迭代的 AI native 工作方式。

## 安装方式

把 `skill/` 目录复制到你的 Codex skills 目录中，例如：

```bash
cp -R skill ~/.codex/skills/ai-native-loop
```

如果目录名不是 `ai-native-loop`，请改成该名称，以匹配 Skill frontmatter 中的 `name`。

## 核心能力

- 把模糊任务重写为 AI-ready task packet
- 在轻介入 / 中介入 / 强介入之间动态切换
- 重组信息结构而不是只润色输入
- 读取反馈并做根因归因
- 把当前轮经验折叠进下一轮输入
- 在不同知识工作之间迁移同一套工作协议

## 当前发布状态

当前版本已经具备：

- 完整 `SKILL.md`
- 动态介入框架
- 工作循环协议文档
- 反馈归因框架
- 多场景迁移参考
- AI-first 输入模板
- 再输入模板
- 多 Agent 交接模板
- GitHub 开源仓库级文档

仍建议继续补充：

- 3 到 5 个更完整的真实案例样本
- 不同领域下的触发边界对照
- 长周期使用后的版本迭代记录

## 许可证

本仓库当前采用 MIT License。
