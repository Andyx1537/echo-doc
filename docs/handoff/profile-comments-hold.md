# 阶段账本 · profile-comments-hold

状态：`OPEN`
依据：`DECISIONS` D24 ④ 返回栈一次弹一层；上一账本发现：主页全屏进评论会卸掉主页
更新：2026-09-16 · 开账
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 从主页全屏点「想说的话」时，主页和全屏都不卸，藏在评论下面。
- 返回只关评论，全屏还在，主页还停在原来的滚动位置。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/profile-comments-hold` | 占用 |
| echo-doc `docs/profile-comments-hold` | 占用 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | 评论不卸主页 |
| 2. 前端：评论压在主页栈上 | `todo` | | 浏览器：滚墙 → 点作品 → 想说的话 → 返回仍是全屏；再回主页仍停在原处 | 广场全屏进评论本块不修 |
| 3. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
动作：本切片做完即关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 记 `n` 仍不能诚实做：作品 id 写不进 `t_card_exposure.cardId`，`OM2` 不许另开曝光表。
