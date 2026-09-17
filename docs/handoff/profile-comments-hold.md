# 阶段账本 · profile-comments-hold

状态：`CLOSED`
依据：`DECISIONS` D24 ④ 返回栈一次弹一层；上一账本发现：主页全屏进评论会卸掉主页
更新：2026-09-16 · 已合 `echo-client@a027592`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 从主页全屏点「想说的话」时，主页和全屏都不卸，评论叠在上面。
- 返回只关评论，全屏还在，主页还停在原来的滚动位置。
- 已合 develop：`echo-client@a027592`（功能头 `8cacb61`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/profile-comments-hold` | 已合 develop `a027592`；占用已释 |
| echo-doc `docs/profile-comments-hold` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@b564d5c` | | 评论不卸主页 |
| 2. 前端：评论压在主页栈上 | `done` | `echo-client@8cacb61` | 浏览器：墙滚到 520 → 点「第一场雪」→ 想说的话时墙仍 520 → 返回仍是全屏 → 再回主页仍 520 | 广场全屏进评论本块不修 |
| 3. 合入 develop 并回填 | `done` | `echo-client@a027592` | 功能头 `8cacb61` | |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 记 `n` 仍不能诚实做：作品 id 写不进 `t_card_exposure.cardId`，`OM2` 不许另开曝光表。
- 广场全屏点「想说的话」仍卸广场全屏。本块没修。
