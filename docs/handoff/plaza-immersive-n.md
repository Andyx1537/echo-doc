# 阶段账本 · plaza-immersive-n

状态：`CLOSED`
依据：`SPEC-feed-surfaces` 概述第 1 条；`SPEC-works` 公开曝光以 workId 记；上一账本留下的全屏不记 n
更新：2026-09-17 · 已合 `echo@22a190d` / `echo-client@dfc48cc`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 广场网格点进全屏后，用网格那次下发新开一份 `surface=immersive` 快照；驻留满 1000ms 才报曝光、才记 `n`。
- 网格列出、滚过一律不记。快照丢了进得去，只是不记（少记）。
- 已合 develop：`echo@22a190d`（功能头 `c6e2ed4`）/ `echo-client@dfc48cc`（功能头 `fc9c617`）。
- 不做：全屏另排推荐流、作者主页进全屏记 n、第二套曝光表、漫画/视频、真短信、打 Tag、完整后台页、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/plaza-immersive-n` | 已合 develop `22a190d`；占用已释 |
| echo-client `frontend/plaza-immersive-n` | 已合 develop `dfc48cc`；占用已释 |
| echo-doc `docs/plaza-immersive-n` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@1949263` | | |
| 2. 后端：全屏快照 + 记 n | `done` | `echo@c6e2ed4` | PlazaImmersiveExposureTest 3/3；ExposureRecorderTest 16/16 | 网格仍拒；快照丢了少记 |
| 3. 前端：驻留 1000ms 上报 | `done` | `echo-client@fc9c617` | vitest workExposure 2/2、http 19/19 | mock 不记 n |
| 4. 合入 develop 并回填 | `done` | `echo@22a190d` `echo-client@dfc48cc` | 功能头 `c6e2ed4` / `fc9c617` | |

状态只用：`todo` / `doing` / `done` / `blocked`。`done` 必须有提交号。

## 下一块入口

```text
动作：本切片已关。全屏另排推荐流 / 作者主页记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现（当初不知道的）

- `t_card_exposure.cardId` 没有指向回忆卡的外键，列名仍叫 cardId；公开流里写入的是作品 id。
