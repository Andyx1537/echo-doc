# 阶段账本 · plaza-work-read

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 共鸣厅单元；`DECISIONS` WP1
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 共鸣厅只出已公开作品；点进去是同一条作品，不是私域卡。匿名每两小时一批约 30 条，绑定后不限。
- 未接作品库时 `GET /plaza` 仍发卡，锁住的窗裁剪测试不改。
- 已合 develop（`echo@63567e7` / `echo-client@2c4d975`）。真短信、真出图、打 Tag、占 5180/18080 仍不做。
- 下一本：评论收藏。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/plaza-work-read` | 已释 @ `36e8796` |
| echo-client `frontend/plaza-work-read` | 已释 @ `a997d62` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc` 本页 | 产品已冻 | |
| 2. 后端：广场下发公开作品 | `done` | `echo@36e8796` | `PlazaWorkReadTest` 2/2 | 未接作品库仍发卡 |
| 3. 前端：共鸣厅画作品、点进同一条 | `done` | `echo-client@a997d62` | vitest 179/179；5177 点进「它最后一个下午」 | 主键 workId |
| 4. 匿名两小时一批 | `done` | 同上两笔 | 单测锁 30 条且两小时内顺序不变 | 绑定后不限 |

## 下一块入口

```text
仓库：echo-doc
动作：本账本已关。下一本是评论收藏，未开账本前不要开工。
禁止：占 5180/18080；改两份锁住的测试夹具；合 develop
```

## 发现

- `WindowVisibilityTrimTest` 断言广场 items 里还有窗/卡 id。只有 `workStore != null` 才改发作品。
- 锁住的窗用例在本分支上原本就会红（广场早已改发卡、未装配 cardStore 时是空页；记得墙要绑手机）。本账本没改那份夹具。
- 当前生成没有「允许公开」结论。广场只认作品 `public`，不会把私域可达当成可公开。
