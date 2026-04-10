# Iteration Assessment Against `web-access`

## Why Compare To `web-access`

参考仓库 [`eze-is/web-access`](https://github.com/eze-is/web-access) 的价值，不在于直接照搬它的功能，而在于它已经把“一个 Skill 如何从内部可用，走到外部可安装、可理解、可传播、可持续迭代”这件事做成了一个成熟样板。

对 `ai-native-loop` 来说，最值得借鉴的不是它的联网能力，而是它的开源产品化完成度。

## Important Boundary

`ai-native-loop` 和 `web-access` 不是同一类 Skill：

- `web-access` 是工具能力型 Skill，强调浏览器、代理、路由、脚本和站点经验。
- `ai-native-loop` 是工作协议型 Skill，强调输入、执行、反馈、再输入的闭环。

所以本评估的目标不是“让 `ai-native-loop` 看起来像 `web-access`”，而是回答：

> 在不损失协议型 Skill 本质的前提下，我们当前仓库还缺哪些“产品化层”的东西？

## Current Judgment

如果以“内部设计完成度”来打分，`ai-native-loop` 已经在 9.5 左右。

但如果以“面向 GitHub 公开传播和外部安装的开源产品化完成度”来打分，我会给当前版本：

**8.7 / 10**

主要短板不在 Skill 思想本身，而在：

- 分发形态
- 安装体验
- 首次理解成本
- 版本化与发布节奏
- 外部案例密度

## What `web-access` Is Doing Better

基于其 README 和仓库结构，`web-access` 目前在以下几个方面明显更成熟。

### 1. 它的仓库形态天然适合“直接安装”

`web-access` 的仓库根目录就是 Skill 主体：

- 根目录有 `SKILL.md`
- 根目录有 `references/`
- 根目录有 `scripts/`
- 根目录还有插件相关目录

这意味着用户看到仓库 URL 后，更容易直接把它当作“一个可安装的 Skill 包”。

相比之下，`ai-native-loop` 当前是：

- 仓库根目录是项目包装层
- 真正的 Skill 在 `skill/` 子目录下

这更适合项目管理，但不够适合 Skill 分发。

### 2. 它的安装路径非常明确

`web-access` 在 README 里给了多种安装方式：

- 包管理器式安装
- 让 Agent 自动安装
- Plugin 安装
- 手动安装

而 `ai-native-loop` 目前只有偏手动的复制说明，对外部用户不够友好。

### 3. 它的能力展示更像一个“产品页面”

`web-access` README 会快速回答：

- 它能干什么
- 为什么和默认能力不同
- 它有哪些关键能力
- 最近版本更新了什么

相比之下，`ai-native-loop` 当前 README 更偏理念说明，对第一次接触的用户来说，“到底怎么用、何时触发、和普通提示词有什么差别”还可以更直给。

### 4. 它有更强的版本意识与持续发布感

`web-access` README 中明确出现版本号、更新说明和迭代历史，这会增强外部用户对项目持续维护的信心。

`ai-native-loop` 当前还没有正式版本号、release notes 或 changelog 入口。

### 5. 它的可验证性更强

`web-access` 通过脚本、前置检查、能力矩阵和技术说明，让用户更容易相信“这个 Skill 真的能工作”。

`ai-native-loop` 当前的验证证据主要来自：

- 自评文档
- self-bootstrap case
- 结构校验

这些已经有价值，但外部用户更容易被“多场景真实案例 + 清晰触发示例”打动。

## What `ai-native-loop` Is Already Better At

这个对比也不是一边倒。`ai-native-loop` 在某些方面其实已经比很多 Skill 更成熟：

### 1. 方法论深度更强

它不是功能列表，而是一套完整工作协议。

### 2. 结构化思考非常完整

闭环模型、介入机制、迁移性、成长路径和边界都已经成系统。

### 3. 文档体系已经成形

目前已经有：

- 设计规格
- 自评
- 前测
- 发布检查
- 正式案例

这对协议型 Skill 来说是很好的基础。

## Highest Priority Gaps

下面是我认为最值得优先补的部分，按优先级排序。

### P0. 仓库分发形态还不够“Skill-first”

这是当前最重要的问题。

如果用户通过 GitHub URL 认识 `ai-native-loop`，他们更自然的预期是：

- 仓库本身就是 Skill
- 根目录就能看到 `SKILL.md`
- 安装时不需要再理解“项目包装层”和 `skill/` 子目录的区别

当前仓库结构更像“一个包含 Skill 的项目”，不够像“一个可直接安装的 Skill 仓库”。

#### 建议方向

二选一：

- 方案 A：把 `skill/` 提升为仓库根主体，把文档保留在根目录的 `docs/`
- 方案 B：保留当前结构，但显式增加 `release/ai-native-loop/` 或安装导出目录，并把 README 改成面向安装的主入口

我更推荐方案 A，因为它更符合 GitHub 上 Skill 仓库的直觉形态。

### P0. 安装与首次使用路径不够强

当前 README 有基本安装说明，但还缺以下内容：

- Codex / Claude / Cursor 等环境的安装示例
- 一句话触发方式
- 第一次使用时应该怎么开口
- 轻 / 中 / 强介入最直观的区别示例

#### 建议方向

在 README 增加一个 `Quick Start`：

- 安装
- 一句触发示例
- 三个典型请求示例
- Skill 会如何介入

### P0. 外部案例还不够

目前我们最强的案例是 self-bootstrap case，这个案例很好，但仍偏“元任务”。

如果要提升仓库说服力，至少还应再补两个外部案例：

- 一个研究/分析案例
- 一个写作/表达或产品推进案例

这样外部用户才能更快理解这个 Skill 的迁移性不是停留在理论上。

## P1 Gaps

### P1. README 还可以更产品化

当前 README 已经清楚，但还不够像一个成熟开源项目首页。

可以继续增强：

- 开头加入一句更强的价值主张
- 增加“适合什么，不适合什么”
- 增加使用前后对比
- 增加图示或流程图

### P1. 缺少正式版本号和发布节奏

建议尽快定义：

- 当前版本，例如 `v0.1.0`
- 一个最简单的 changelog 或 release notes 页面
- 后续每轮迭代的版本更新说明

### P1. 缺少明确的触发样例库

协议型 Skill 最大的理解门槛通常不是理念，而是：

- 什么请求会触发它
- 什么请求不该触发它
- 它介入后会把请求改写成什么样

建议补一页 `docs/trigger-examples.md`。

### P1. `agents/openai.yaml` 还比较基础

当前 `openai.yaml` 只包含基础展示字段。

后续可以继续增强：

- 更强的 `default_prompt`
- 如果有品牌资产，再补 icon 与 brand color
- 更清晰的 UI-facing short description

## P2 Gaps

### P2. 语言覆盖有限

当前主要内容偏中文。如果目标是更广范围的 GitHub 传播，可以考虑：

- README 中英双语
- 或新增 `README.en.md`

### P2. 缺少轻量可视化资产

比如：

- 一张输入 → 执行 → 反馈 → 再输入的示意图
- 一张轻 / 中 / 强介入判断图

这会显著降低首次理解成本。

## Suggested Iteration Order

我建议下一轮按这个顺序推进：

1. 调整仓库分发形态，让仓库更像“可直接安装的 Skill 包”
2. 强化 README 的安装与 Quick Start
3. 补两个外部案例
4. 增加版本号与发布说明
5. 增加触发样例页
6. 视需要补双语 README 和可视化资产

## Bottom Line

当前 `ai-native-loop` 最大的问题，不是 Skill 本身不成熟，而是：

> 它已经像一个高质量内部项目，但还没有完全长成一个“外部用户一看就会装、一装就会试、一试就能理解价值”的 Skill 产品。

这也是它当前最值得继续优化迭代的地方。
