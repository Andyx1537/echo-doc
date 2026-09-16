# 阶段账本 · plaza-author-home

状态：`CLOSED`
依据：`DECISIONS` D24 ② 左滑进主页、④ 返回栈一次弹一层
更新：2026-09-16 · 已合 `echo-client@515c240`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 全屏单卡左滑或点「主页」进该作品作者主页（既有 `UserProfileScreen`）。
- 从主页返回回到进来时那张卡，不一次退回网格。
- 已合 develop：`echo-client@515c240`（功能头 `1d65e45`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/plaza-author-home` | 已合 develop `515c240`；占用已释 |
| echo-doc `docs/plaza-author-home` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@e8b9de6` | | 产品已冻：左滑进主页 |
| 2. 前端：左滑进作者主页，返回回全屏 | `done` | `echo-client@1d65e45` | vitest `workFeed` 2/2；浏览器点卡→主页→回全屏同卡 | 主页仍是既有他人主页 |
| 3. 合入 develop 并回填 | `done` | `echo-client@515c240` | 功能头 `1d65e45` | 不记 `n` |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 主页作品墙仍读窗，不读 Work。广场作者因此先看到空墙，不是主页没打开。
