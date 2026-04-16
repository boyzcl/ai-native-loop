# Experiment Log Template

## Purpose

这份模板用于把 `ai-native-loop` 的迭代改成假设驱动，而不是内容驱动。

一次实验只追一个主问题，不同时验证太多结论。

## Template

```md
# Experiment Log: <short title>

## Hypothesis

- 本轮假设是什么？

## Change

- 改了哪条规则、哪份文档或哪种默认行为？

## Expected Effect

- 预期改善哪个维度？
- 预期伤害哪个维度？

## Runtime Memory

- runtime_root:
- capture_written:
- capture_ref:
- expected_runtime_reuse:

## Benchmark Set

- 本轮使用哪些固定测例？
- 有没有新增边界测例？

## Comparison

- baseline:
- candidate:
- optional previous:

## Result

- 哪些维度更好了？
- 哪些维度没变？
- 哪些维度变差了？
- runtime reuse 是否真的发生？

## Decision

- keep / revise / revert

## Follow-up

- 下一轮最值得继续验证什么？
```

## Use Rule

- 没有假设，不开实验
- 没有对照，不下强结论
- 没有 runtime provenance，不对“经验复利”下强结论
- 没有结果差异，不扩大改动范围
