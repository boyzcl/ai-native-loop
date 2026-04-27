# Release Manifest

Updated: `2026-04-21`

## Purpose

这份文件是仓库当前版本与发布状态的单一事实源。

README、`SKILL.md` metadata、`CHANGELOG.md`、release notes 和状态文档应以本文件为准，不再各自维护一套版本真相。

## Current Release Truth

- `public_version`
  - `v0.2.0`
- `public_skill_metadata_version`
  - `0.2.0`
- `active_iteration_track`
  - `v0.2.0`
- `track_status`
  - `published / local auto-promotion + capacity governance + validated retrieval + repo-candidate review workflow`
- `release_judgment`
  - `v0.2.0` 已完成 runtime memory 骨架、本地 auto-promotion、capacity governance、reuse 观测、repo candidate review workflow、retrieval forward test 与 backlog stress replay，已达到当前公开版本发布门槛；但这些仍主要是本地与 temp-runtime 证据，不应过度承诺长期稳定自治

## Canonical References

- 用户入口：[README.md](../README.md)
- Skill 主体：[SKILL.md](../SKILL.md)
- 版本记录：[CHANGELOG.md](../CHANGELOG.md)
- 发布说明：[release-notes-v0.2.0.md](release-notes-v0.2.0.md)

## Current Decision

当前迭代重点已经从“把 runtime compounding 接通”切换为“让受限复利变得可验证、可 review、可长期维护”。

`2026-04-27` 本地实现继续往前推进到：

- promotion trigger mechanism 已接通到本地 runtime cadence
- pending queue 主路径改为 invocation-driven bounded cycle 自动消费
- host 级 automation 只保留低频 reconcile，不再承担主 cycle 消费
- repo candidate 仍只停留在 runtime 候选层，不等于 repo 公共资产
- 这仍然只是本地可验证触发层，不应过度承诺长期稳定自治已经成立

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

## Version Push Rule

从 `2026-04-21` 起，任何“准备 push 到 GitHub 并作为一个新仓库版本对外表达”的变更，都必须先同步以下版本真相：

- `docs/release-manifest.md`
- `README.md`
- `SKILL.md` metadata version
- `CHANGELOG.md`
- 对应版本的 release notes

执行要求：

1. 先更新版本号与发布状态
2. 再运行 `scripts/check-release-consistency.sh`
3. 通过后才允许 push 这个版本对应的 GitHub 提交

默认规则：

- push 普通开发提交，不强制改 semver
- push 一个明确对外表达的新版本时，必须同步版本号，不能只改代码不改版本真相
