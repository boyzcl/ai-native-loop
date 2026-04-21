# Release Manifest

Updated: `2026-04-21`

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
  - `draft / local auto-promotion + capacity governance + validated retrieval + repo-candidate review workflow`
- `release_judgment`
  - `v0.2.0` 已完成 runtime memory 骨架、本地 auto-promotion、capacity governance、reuse 观测、repo candidate review workflow、retrieval forward test 与 backlog stress replay；但这些仍主要是本地与 temp-runtime 证据，尚不能过度承诺长期稳定自治或正式发布

## Canonical References

- 用户入口：[README.md](../README.md)
- Skill 主体：[SKILL.md](../SKILL.md)
- 版本记录：[CHANGELOG.md](../CHANGELOG.md)
- 发布说明：[release-notes-v0.2.0.md](release-notes-v0.2.0.md)

## Current Decision

当前迭代重点已经从“把 runtime compounding 接通”切换为“让受限复利变得可验证、可 review、可长期维护”。

当前优先级：

1. 继续积累更长周期的真实 reuse 样本，确认 retrieval heuristic 在真实任务里仍稳定
2. 继续用 `pending / accepted / rejected` review workflow 管住 repo candidate，不把它误当成自动发布层
3. 只在有足够 review 与 drafting 证据时，才把单个 accepted candidate 转成 repo 层公共资产
4. 继续保持 repo 层 gate，不把本地候选层误当成自动发布层

## Runtime Source Of Truth

默认运行时经验层宿主改为“按 host 解析的 runtime root”。

当前最小可信支持面：

- `Codex`：`~/.codex/skills/ai-native-loop/runtime/`

当前仅有适配草案，不构成完全支持承诺：

- `Claude Code`：`~/.claude/skills/ai-native-loop/runtime/`
- `OpenClaw`：`~/.openclaw/skills/ai-native-loop/runtime/`

仓库不作为默认 runtime 存储层，只作为公开定义、验证与发布层。

## Sync Checklist

每次准备发布或改版本状态时，至少同步检查：

- `README.md` 的版本与状态描述
- `SKILL.md` 的 metadata version
- `CHANGELOG.md` 的 release 分段
- 对应 release notes 的状态字段
- benchmark 与验证文档是否匹配当前发布判断
- runtime 相关文档与 helper scripts 是否匹配当前声明
