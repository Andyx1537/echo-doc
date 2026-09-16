# 阶段账本 · profile-work-stack

状态：`CLOSED`
依据：`DECISIONS` D24 ④ 返回栈一次弹一层；上一账本发现：主页进全屏会卸掉主页
更新：2026-09-16 · 已合 `echo-client@05ffe53`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 从作者主页点作品进全屏时，主页不卸掉，藏在全屏下面。
- 返回只关全屏，墙还停在原来的滚动位置，不再重新拉一次。
- 已合 develop：`echo-client@05ffe53`（功能头 `9dfdb48`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/profile-work-stack` | 已合 develop `05ffe53`；占用已释 |
| echo-doc `docs/profile-work-stack` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@04634eb` | | 主页进全屏不卸挂 |
| 2. 前端：主页压在全屏下 | `done` | `echo-client@9dfdb48` | 浏览器：墙滚到 520 → 点「第一场雪」→ 返回仍 520，未重拉；再返回仍是进来的那张全屏 | 评论浮层仍会卸（本块不修） |
| 3. 合入 develop 并回填 | `done` | `echo-client@05ffe53` | 功能头 `9dfdb48` | |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 记 `n` 仍不能诚实做：作品 id 写不进 `t_card_exposure.cardId`，`OM2` 不许另开曝光表。
- 从主页全屏再点「想说的话」仍会卸掉主页（评论层独占）。返回评论后主页会重挂。本块没修。
