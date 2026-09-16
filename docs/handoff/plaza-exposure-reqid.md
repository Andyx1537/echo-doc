# 阶段账本 · plaza-exposure-reqid

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 共鸣厅收尾；`DECISIONS` G-2
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 广场下发的 `reqId` 快照落到 `t_feed_request`（`echo@c9348a6`，schema `2026091406`），换实例仍能按同一份快照做曝光校验。
- 无库时仍是进程内存；那时声明多副本继续拒绝启动。网格层曝光仍不记 `n`。
- 不做：全屏层、Redis、漫画/视频、真短信、打 Tag、占 5180/18080、改两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo develop | 已释 @ `c9348a6` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 快照落库，换实例可反查 | `done` | `echo@c9348a6` | 曝光单测 16/16、多实例 3/3；隔离库 `FeedRequestRegistryPgTest` 1/1 | schema `2026091406`；验完已停库 |

## 下一块入口

```text
仓库：echo-doc
动作：本账本已关。漫画/视频、真短信仍后置；全屏 UI 已另开 `plaza-immersive` 合入，网格与全屏仍不记 n。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```
