# 阶段账本 · plaza-immersive

状态：`CLOSED`
依据：`DECISIONS` D24 / XC4；`SPEC-feed-surfaces` 信息流两层；上一账本留下的全屏层
更新：2026-09-16 · 已合 `echo-client@c1bf7c9`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 广场网格点作品进全屏单卡：一屏一条，沿进入时那份列表上下翻。
- 右滑或返回回网格。想说的话仍进既有详情。
- 已合 develop：`echo-client@c1bf7c9`（功能头 `aff700a`）。
- 不做：`surface=immersive` 配比与记 `n`（作品 id 还写不进卡曝光表）、左滑进主页、漫画/视频、真短信、打 Tag、完整后台页、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/plaza-immersive` | 已合 develop `c1bf7c9`；占用已释 |
| echo-doc `docs/plaza-immersive` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | 本提交 | | 产品已冻：点网格进全屏 |
| 2. 前端：全屏单卡 + 上下翻 | `done` | `echo-client@aff700a` | vitest `workFeed` 1/1；浏览器点卡→全屏→下一条→想说的话→回全屏→回网格 | 沿用进入时列表 |
| 3. 合入 develop 并回填 | `done` | `echo-client@c1bf7c9` | 功能头 `aff700a` | 不记 `n` |

## 下一块入口

```text
动作：本切片已关。记 n / 左滑进主页 / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 全屏顺序用进入时那份 `works` 数组，不是瀑布两列的视觉顺序。
- 作品 id 仍写不进 `t_card_exposure.cardId`，全屏这一层继续少记 `n`。
