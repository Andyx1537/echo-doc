# 阶段账本 · plaza-comments-hold

状态：`CLOSED`
依据：`DECISIONS` D24 ④ 返回栈一次弹一层；上一账本发现：广场全屏进评论会卸掉全屏
更新：2026-09-17 · 已合 `echo-client@59fea15`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 从广场全屏点「想说的话」时，全屏不卸，评论叠在上面。
- 返回只关评论，还停在进来的那张卡。
- 已合 develop：`echo-client@59fea15`（功能头 `22dbf60`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/plaza-comments-hold` | 已合 develop `59fea15`；占用已释 |
| echo-doc `docs/plaza-comments-hold` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@55ca40e` | | 广场全屏进评论不卸 |
| 2. 前端：评论压在广场全屏上 | `done` | `echo-client@22dbf60` | 浏览器：点「它最后一个下午」→ 想说的话时全屏仍挂着 → 返回仍是同一张卡，不是网格 | 验收看 DOM，不出新对比图 |
| 3. 合入 develop 并回填 | `done` | `echo-client@59fea15` | 功能头 `22dbf60` | |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 记 `n` 仍不能诚实做：作品 id 写不进 `t_card_exposure.cardId`，`OM2` 不许另开曝光表。
- 返回后两案都是同一张全屏，屏幕上看不出差别，本块不出对比图。
