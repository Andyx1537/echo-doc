# 阶段账本 · plaza-immersive-n

状态：`OPEN`
依据：`SPEC-feed-surfaces` 概述第 1 条；`SPEC-works` 公开曝光以 workId 记；上一账本留下的全屏不记 n
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 广场网格点进全屏后，用网格那次下发新开一份 `surface=immersive` 快照；驻留满 1000ms 才报曝光、才记 `n`。
- 网格列出、滚过一律不记。快照丢了进得去，只是不记（少记）。
- 不做：全屏另排推荐流、作者主页进全屏记 n、第二套曝光表、漫画/视频、真短信、打 Tag、完整后台页、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| echo `backend/plaza-immersive-n` | 本线 | echo 仓该分支 | 合入 develop 后释 |
| echo-client `frontend/plaza-immersive-n` | 本线 | echo-client 仓该分支 | 合入 develop 后释 |
| echo-doc `docs/plaza-immersive-n` | 本线 | 本账本 | 合入 develop 后释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁 | | 不改 |
| 5180 / 18080 | 不占 | | |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | |
| 2. 后端：全屏快照 + 记 n | `todo` | | | POST /plaza/immersive；网格仍拒 |
| 3. 前端：驻留 1000ms 上报 | `todo` | | | 只报全屏，不报网格 |
| 4. 合入 develop 并回填 | `todo` | | | |

状态只用：`todo` / `doing` / `done` / `blocked`。`done` 必须有提交号。

## 下一块入口

```text
仓库：echo
分支：backend/plaza-immersive-n
动作：POST /plaza/immersive 从网格 fromReqId 新开 immersive 快照；IMMERSIVE_FEED_IMPLEMENTED=true
禁止：占 5180/18080；改两份锁住夹具；打 Tag；另排全屏推荐流
```

## 发现（当初不知道的）

- `t_card_exposure.cardId` 没有指向回忆卡的外键，列名仍叫 cardId；公开流里写入的是作品 id。
