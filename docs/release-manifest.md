# Release Manifest

Updated: `2026-04-16`

## Purpose

这份文件是仓库当前版本与发布状态的单一事实源。

README、`SKILL.md` metadata、`CHANGELOG.md`、release notes 和状态文档应以本文件为准，不再各自维护一套版本真相。

## Current Release Truth

- `public_version`
  - `v0.1.0`
- `public_skill_metadata_version`
  - `0.1.0`
- `active_iteration_track`
  - `v0.2.0`
- `track_status`
  - `draft / runtime compounding + validation hardening`
- `release_judgment`
  - `v0.2.0` 已完成执行层、模式层、初始 benchmark、runtime memory 骨架与首轮调用收紧，但验证体系仍在加固，尚未正式发布

## Canonical References

- 用户入口：[README.md](../README.md)
- Skill 主体：[SKILL.md](../SKILL.md)
- 版本记录：[CHANGELOG.md](../CHANGELOG.md)
- 发布说明：[release-notes-v0.2.0.md](release-notes-v0.2.0.md)

## Current Decision

当前迭代重点不是继续扩写概念，而是补四类发布前缺口：

1. 验证体系从回放式 benchmark 升级为 baseline + pairwise rubric + runtime provenance + experiment log
2. `medium` 以上任务默认保留最小回收块并写入本地 runtime capture
3. README 与 agent metadata 优先优化首次试用路径并收紧为显式调用优先
4. 版本叙事开始围绕 failure correction 与 runtime compounding，而不是只围绕新增文件

## Runtime Source Of Truth

默认运行时经验层宿主：

- `~/.codex/skills/ai-native-loop/runtime/`

仓库不作为默认 runtime 存储层，只作为公开定义、验证与发布层。

## Sync Checklist

每次准备发布或改版本状态时，至少同步检查：

- `README.md` 的版本与状态描述
- `SKILL.md` 的 metadata version
- `CHANGELOG.md` 的 release 分段
- 对应 release notes 的状态字段
- benchmark 与验证文档是否匹配当前发布判断
- runtime 相关文档与 helper scripts 是否匹配当前声明
