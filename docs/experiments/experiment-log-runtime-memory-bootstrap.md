# Experiment Log: Runtime Memory Bootstrap

> Historical note: this log captures an earlier Codex-hosted run. The `.codex` runtime path below is evidence for that run, not the current generic host contract.

## Hypothesis

- 把 `medium+` 任务的经验默认写入本地 runtime capture 后，`ai-native-loop` 的“经验进入下一轮系统”将从叙述变成可验证机制。

## Change

- 新增 runtime memory 目录结构
- 新增 runtime helper scripts
- 收紧 `SKILL.md` 为显式调用优先
- 对 `medium+` 任务增加 runtime capture 合同

## Expected Effect

- 预期改善：`reinput_quality`、`real_task_helpfulness`、runtime provenance
- 预期伤害：如果没有读取预算，可能增加噪音

## Runtime Memory

- runtime_root: `~/.codex/skills/ai-native-loop/runtime/`
- capture_written: yes
- capture_ref: `/Users/boyzcl/.codex/skills/ai-native-loop/runtime/captures/2026-04-16.jsonl#bootstrap-runtime-smoke-20260416`
- expected_runtime_reuse: subsequent calls can retrieve by `scene=runtime-memory-smoke-test`

## Benchmark Set

- runtime-memory-smoke-test
- existing fixed benchmark matrix retained for future pairwise reruns

## Comparison

- baseline: repo-only recovery block design
- candidate: local-first runtime compounding layer
- optional previous: n/a

## Result

- 更好了：runtime host, runtime provenance, review queue, local retrieval path
- 没变：长期真实用户复用证据仍未积累
- 变差风险：runtime 层如果没有持续 review，可能膨胀
- runtime reuse 是否真的发生：bootstrap retrieval by scene passed; repeated real-user reuse still pending

## Decision

- keep

## Follow-up

- 用真实连续任务继续验证 runtime reuse
- 把 runtime provenance 接入更多 benchmark runs
