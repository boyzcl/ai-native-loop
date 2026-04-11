# Field Note: Audit Remediation / Validation Hardening

## Scene

- Skill 仓库治理
- 审计发现修复
- 版本与验证体系加固

## Objective

- 根据外部审计报告，优先修复 `ai-native-loop` 在验证体系、版本单源、默认回收路径和首次试用路径上的结构性缺口

## Initial Block

- 仓库已经有协议、案例和 benchmark，但证据体系弱于能力声明
- 版本状态分散在多个文档里，容易漂移
- 经验沉淀规则存在，但默认路径不够短
- benchmark 缺少统一 run template 与 baseline / pairwise 迁移入口

## Intervention Level

- `medium`
- 原因：目标和方向都清楚，不需要重建项目定位；但需要同时治理多个相互耦合的结构缺口

## Core Artifacts Produced

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`
- `Loop Recovery Block`

## What Changed

- 版本真相被收口到 `release-manifest.md`
- benchmark 体系从“总分文件”进一步推进到 rubric、experiment log、run template 与 retrospective run records
- `medium` 以上任务默认加入 `Loop Recovery Block`
- README 增加 30 秒自测和 before/after 触发路径

## What Worked

- 先修单一事实源，再修 README 与 release notes，减少了状态漂移
- 先补 run template，再迁移固定 benchmark 结果，避免继续只有抽象要求
- 把 recovery block 接进 `SKILL.md` 与经验文档后，经验沉淀路径明显更短

## What Failed Or Remained Risky

- 4 个固定 benchmark 仍未完成真实 baseline 重跑
- 多 Agent 仍没有 live split execution，只补了 `no-split` 决策证据和 split prep
- 现有 retrospective run records 仍不能替代真实对照实验

## Re-input

- 保留：release manifest、evaluation rubric、run templates、recovery block
- 丢弃：只靠总分和自评支撑版本结论
- 下一轮应直接执行：
  - 4 个固定 benchmark 的 baseline 重跑
  - 1 个多 Agent split candidate 实测

## Promotion Hint

- `pattern`
  - 可迁移到其他 Skill / Agent 仓库的审计修复任务
- `failure_mode`
  - 暴露了“证据体系落后于能力声明”的稳定风险
- `raw_note`
  - 还缺完整 baseline 对照，不宜过早提升为正式 benchmark
