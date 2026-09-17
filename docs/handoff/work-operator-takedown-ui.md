# 阶段账本 · work-operator-takedown-ui

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` B04；`API-CONTRACT` 19.4；上一账本留下的下架入口
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 运营台加「已公开 / 已下架」两栏：公开作品可下架，下架后可再上架，不改首次 `reviewedAt`。
- 队列 `tab=public|takendown` 回已批/已下架工单；处置仍走现有 handle。
- 不做：回忆卡队列、举报、开关、TOTP、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| echo-doc `docs/work-operator-takedown-ui` | 公共区 | `docs/work-operator-takedown-ui` | 合入 develop 后释 |
| echo `backend/work-operator-takedown-ui` | 公共区 | 功能分支 | 合入 develop 后释 |
| echo-client `frontend/work-operator-takedown-ui` | 公共区 | 功能分支 | 合入 develop 后释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | | 锁，不改 | |
| 5180 / 18080 | | 不占 | |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | 产品已冻 |
| 2. 后端：队列 tab=public/takendown | `todo` | | | |
| 3. 前端：已公开下架 / 已下架恢复 | `todo` | | | `?ops=works` |
| 4. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
仓库：echo
分支：backend/work-operator-takedown-ui
命令或文件：WorkModerationStore.queue
禁止改动：5180/18080；两份锁住夹具；打 Tag
```

## 发现（当初不知道的）

- 作品默认队列只回活动态，已通过的工单不在里面，所以运营台上一刀没法下架。
