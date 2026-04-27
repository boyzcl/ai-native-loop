# Promotion Trigger Mechanism Plan

Date: `2026-04-27`

## Goal

补上 `promotion_worker.py` 的真实触发层，让系统不再停留在：

- 自动写 capture
- 自动进入 review queue
- 但 promotion 只能靠手动触发

目标不是做一个重型后台系统，而是补一个足够真实、足够稳、可恢复的本地调度层，让 pending queue 能按节奏自动消费。

## Current Diagnosis

当前已经成立：

- `medium+` 任务会自动写入 runtime capture
- capture 会自动进入 `review-queue.json`
- `promotion_worker.py` 已能真实执行 promote / merge / archive / repo-candidate gate

当前缺口：

- 没有持续触发 `promotion_worker.py` 的 scheduler
- 所以 `capture -> pending` 是自动的，但 `pending -> promoted` 仍是半自动

当前现实表现：

- 只要不手动跑 worker，pending 就会继续积压
- backlog 没到阈值也不会“自己开始跑”，因为阈值只在 worker 被调用时才会生效

## Recommended Design

当前决策已从“cycle cron 为主”切到“invocation-driven 为主，reconcile 为辅”。

### A. Invocation-Driven Promotion Cycle

用途：

- 每次 native skill 完成并写入 `medium+` runtime capture 后，立即推进一小步 pending queue
- 让 promotion 绑定在 skill invocation 自身，而不是某个宿主的专属 scheduler

推荐动作：

```bash
python3 scripts/write_runtime_capture.py --host <host> --record-file /path/to/capture.json
```

行为：

- capture 成功写入后，默认立即尝试一次 bounded local promotion cycle
- cycle 运行带锁，冲突时跳过，不污染 capture
- 默认小步消费，避免每次 invocation 都退化成重型后台任务

### B. Daily Reconcile Cycle

用途：

- 做一次 repo candidate reconcile
- 更新治理指标
- 避免 candidate 过宽或长期漂移

推荐节奏：

- 每天 `1` 次
- 建议凌晨或清晨，例如 `03:30`

推荐动作：

```bash
python3 scripts/promotion_worker.py --limit 0
python3 scripts/runtime_governance_report.py
```

说明：

- `--limit 0` 在当前实现里等价于“不处理新的 pending，但执行 reconcile 路径”
- 适合做 repo candidate 收紧和状态整理

## Trigger Host Recommendation

优先推荐两种实现方式，按现实可行性排序：

### Option 1. Host Invocation Path

推荐作为第一实现。

原因：

- 更接近 skill-native trigger，而不是 app-native cron
- 对 `Codex / Claude Code / OpenClaw` 更可迁移
- invocation 结束即可推进，不需要等待下一次定时窗口

当前最小实现：

- `write_runtime_capture.py`
  - capture 写入后默认调用 bounded cycle
- `run_promotion_cycle.py`
  - 负责锁、快照、结构化输出与失败隔离

### Option 2. Local OS Scheduler

如果真的缺少 invocation hook 或 host helper script，再考虑系统级调度：

- `launchd` on macOS

优点：

- 真正宿主外常驻

缺点：

- 配置更重
- repo 内可维护性更差
- 调试和迁移成本更高

## Guardrails

这个触发层必须遵守以下边界：

1. 只推动 runtime promotion
   - 不自动改 repo 公共资产
2. promotion worker 必须保持幂等
   - 重复调用不能造成灾难性重复晋升
3. scheduler 失败不能污染 capture
   - 最坏情况只是 pending 没被及时消费
4. reconcile 与 consume 分开
   - 不把“消费 pending”和“版本级 review 判断”混成一条重任务

## Minimal Implementation Shape

下一次执行时，建议补一个很薄的封装脚本，而不是让 automation 直接拼多条命令。

建议新增：

- `scripts/run_promotion_cycle.py`
  - 读取当前 pending size
  - 记录一次 cycle start/end
  - 调用 `promotion_worker.py`
  - 输出简洁 JSON

- `scripts/run_promotion_reconcile.py`
  - 执行 `promotion_worker.py --limit 0`
  - 执行 `runtime_governance_report.py`
  - 可选落一份 daily report artifact

这样好处是：

- automation 层更薄
- 后续如果要换成 `launchd` 或别的宿主，命令面不需要重写

## Implementation Notes

本轮落地时，触发层额外补两个最小治理件：

- 共享运行锁
  - 避免 automation 与手动触发并发踩写 queue / ledger
- trigger history
  - 每次 cycle / reconcile 写结构化事件到 `runtime/state/promotion-trigger-history.jsonl`

这两项都只留在 runtime 本地，不构成 repo 公开资产。

## Suggested Cadence Policy

第一版建议：

- Promotion cycle:
  - `every 2 hours`
- Reconcile cycle:
  - `daily`

暂时不建议：

- 每次 capture 后立即触发
  - 当前没有可靠 post-task hook
  - 容易把系统做重

- 每 10 分钟轮询
  - 对当前 backlog 规模没必要
  - 容易把“可运行”做成“高噪音”

## Success Criteria

下一轮落地后，至少应验证：

1. 连续 2 到 3 天内，新 capture 不再长期卡在 pending
2. `last_promotion_run_id` 会持续前进
3. `pending_backlog_size` 不再长期停留在大于 0
4. promoted note 数量增长仍受 working-set ceiling 控制
5. repo candidate 不会因调度接通而异常膨胀

## Risks To Watch

### Risk 1. Automation Runs, But Pending Still Grows

含义：

- cadence 太慢
- batch size 太小
- 或 policy 太保守

### Risk 2. Promotion Noise Increases

含义：

- 调度接通后，worker 过于频繁地把弱样本推上 promoted
- 需要回头调 threshold，不要先加更多调度

### Risk 3. Reconcile Logic Becomes Hidden

含义：

- scheduler 把系统推快了，但人不再关注 governance report
- 最终又回到“自动化在跑，但没人知道它在做什么”

## Recommendation

下一次新对话里，不要先改 promotion heuristic。

优先顺序应是：

1. 让 bounded cycle 绑定到 skill invocation 的 capture write
2. 只保留低频 reconcile 作为辅助治理
3. 再观察 2 到 3 天的 backlog / promoted / candidate 指标
4. 最后再决定是否需要继续调阈值

一句话版本：

> 现在缺的不是 promotion 逻辑，而是把 promotion 逻辑接到真实时间节奏上的触发层。
