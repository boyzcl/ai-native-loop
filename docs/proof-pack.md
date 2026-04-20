# Proof Pack

## Goal

这份 proof pack 用一条最短路径证明三件事：

1. 这个 skill 不只是会输出结构化卡片
2. `medium+` 任务结束后会有明确的本地 runtime 宿主
3. 经验可以进入下一次调用，而不只是留在当前回答里

## Install

当前最小可信安装路径先以 `Codex` 为准：

```bash
git clone https://github.com/boyzcl/ai-native-loop.git ~/.codex/skills/ai-native-loop
python3 ~/.codex/skills/ai-native-loop/scripts/init_runtime_memory.py --host codex
```

如果你在其他宿主下验证，必须显式写出 `--host` 或 `--root`，不要默认把 `.codex` 路径当成通用事实。

## Trigger

```text
用 $ai-native-loop 帮我把当前研究任务整理成可继续推进的闭环，并在 medium 以上介入时写入 runtime capture。
```

## Expected Output Shape

- `Diagnosis Card`
- `Task Packet`
- `Feedback Attribution Card`
- `Re-input Packet`
- `Loop Recovery Block`

## Expected Runtime Artifact

写入当前宿主解析出的 runtime root，例如：

- `Codex`：`~/.codex/skills/ai-native-loop/runtime/captures/YYYY-MM-DD.jsonl`
- `Claude Code` 草案：`~/.claude/skills/ai-native-loop/runtime/captures/YYYY-MM-DD.jsonl`

记录最少应包含：

- `scene`
- `initial_block`
- `artifacts_produced`
- `what_worked`
- `remaining_risk`
- `next_input`

一个最小 CLI 写入例子：

```bash
python3 ~/.codex/skills/ai-native-loop/scripts/write_runtime_capture.py --host codex --record-file /path/to/capture.json
```

一个最小 CLI 读取例子：

```bash
python3 ~/.codex/skills/ai-native-loop/scripts/read_runtime_context.py --host codex --scene research-to-report --limit 3
```

## Validation Path

1. 用 [validate_runtime_memory.py](../scripts/validate_runtime_memory.py) 检查目录结构
2. 用 [smoke_test_runtime_memory.py](../scripts/smoke_test_runtime_memory.py) 跑端到端烟雾测试
3. 用 [benchmark-run-template.md](benchmarks/benchmark-run-template.md) 记录 runtime provenance
4. 参考 [experiment-log-runtime-memory-bootstrap.md](experiments/experiment-log-runtime-memory-bootstrap.md) 查看一条已执行实验样本
