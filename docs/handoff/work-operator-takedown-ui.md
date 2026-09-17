# 阶段账本 · work-operator-takedown-ui

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` B04；`API-CONTRACT` 19.4；上一账本留下的下架入口
更新：2026-09-17 · 已合 `echo@ee7c29f` / `echo-client@7e4d3ba`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 运营台加「已公开 / 已下架」两栏：公开作品可下架，下架后可再上架，不改首次 `reviewedAt`。
- 队列 `tab=public|takendown` 回已批/已下架工单；处置仍走现有 handle。
- 已合 develop：`echo@ee7c29f`（功能头 `fb1e31c`）/ `echo-client@7e4d3ba`（功能头 `e611ffb`）。
- 不做：回忆卡队列、举报、开关、TOTP、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-operator-takedown-ui` | 已合 develop `ee7c29f`；占用已释 |
| echo-client `frontend/work-operator-takedown-ui` | 已合 develop `7e4d3ba`；占用已释 |
| echo-doc `docs/work-operator-takedown-ui` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@e3c32e9` | | 产品已冻 |
| 2. 后端：队列 tab=public/takendown | `done` | `echo@fb1e31c` | `WorkOperatorModerationTest` 11/11 | 内存专项 |
| 3. 前端：已公开下架 / 已下架恢复 | `done` | `echo-client@e611ffb` | Chrome：杯子先收起来后已公开空；已下架能再放回，杯子离开该栏 | mock 5/5 |
| 4. 合入 develop 并回填 | `done` | `echo@ee7c29f` / `echo-client@7e4d3ba` | 功能头 `fb1e31c` / `e611ffb` | |

## 下一块入口

```text
动作：本切片已关。回忆卡队列 / 举报 / 开关另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 作品默认队列只回活动态，已通过的工单不在里面，所以运营台上一刀没法下架。
- 真后端要 `ECHO_ADMIN_ROLES`；没配一律 403。
