# 阶段账本 · profile-immersive-n

状态：`CLOSED`
依据：`SPEC-feed-surfaces` 概述第 1 条；上一账本 `plaza-immersive-n` 留下的作者主页不记 n
更新：2026-09-17 · 已合 `echo@56542d7` / `echo-client@d1ec754`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作者主页墙上点进全屏：墙上那页签发网格快照，再换 immersive 快照；驻留满 1000ms 才记 `n`。
- 看自己的墙不签发快照（不是对别人的投放）。墙上列出、滚过一律不记。
- 已合 develop：`echo@56542d7`（功能头 `afaecfe`）/ `echo-client@d1ec754`（功能头 `90573c4`）。
- 不做：全屏另排推荐流、第二套曝光表、漫画/视频、真短信、打 Tag、完整后台页、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/profile-immersive-n` | 已合 develop `56542d7`；占用已释 |
| echo-client `frontend/profile-immersive-n` | 已合 develop `d1ec754`；占用已释 |
| echo-doc `docs/profile-immersive-n` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@207978f` | | |
| 2. 后端：作者墙签发 reqId | `done` | `echo@afaecfe` | AuthorHomeImmersiveExposureTest 2/2 | 他人墙才签；自己的墙不签 |
| 3. 前端：主页进全屏上报 | `done` | `echo-client@90573c4` | vitest http 20/20 | 复用 POST /plaza/immersive |
| 4. 合入 develop 并回填 | `done` | `echo@56542d7` `echo-client@d1ec754` | 功能头 `afaecfe` / `90573c4` | |

## 下一块入口

```text
动作：本切片已关。全屏另排推荐流 / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现（当初不知道的）

- 看自己的墙不签发快照，避免把自己浏览算进投放次数。
