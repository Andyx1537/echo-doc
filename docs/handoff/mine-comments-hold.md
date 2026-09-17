# 阶段账本 · mine-comments-hold

状态：`CLOSED`
依据：`DECISIONS` D24 ④ 返回栈一次弹一层；上一账本发现：我的作品 / 收藏进评论会卸掉那一墙
更新：2026-09-17 · 已合 `echo-client@82ebbd7`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 从「我的作品」或「我的收藏」点进详情时，那一墙不卸，评论叠在上面。
- 返回只关详情，墙还在，不再重新拉一次。
- 已合 develop：`echo-client@82ebbd7`（功能头 `bdd89f1`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/mine-comments-hold` | 已合 develop `82ebbd7`；占用已释 |
| echo-doc `docs/mine-comments-hold` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@b6b89d3` | | 作品墙 / 收藏进评论不卸 |
| 2. 前端：评论压在墙上 | `done` | `echo-client@bdd89f1` | 浏览器：我的作品点「这只杯子」→ 详情时墙仍挂着 → 返回仍是墙，没有重新摆 | 收藏同一套叠层；游客收藏是绑定页，没点开作品 |
| 3. 合入 develop 并回填 | `done` | `echo-client@82ebbd7` | 功能头 `bdd89f1` | |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 记 `n` 仍不能诚实做：作品 id 写不进 `t_card_exposure.cardId`，`OM2` 不许另开曝光表。
