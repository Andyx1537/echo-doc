# 阶段账本 · work-operator-takedown

状态：`CLOSED`
依据：`API-CONTRACT` 19.4；上一账本 `work-operator-moderation` 留下的下架/恢复
更新：2026-09-16 · 已合 `echo@ad088ef`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 已公开作品可下架，广场立刻看不到；再上架不改首次 `reviewedAt`。
- 凭证复用直接公开的作品也落工单。
- 已合 develop：`echo@ad088ef`。
- 不做：申诉、完整后台页、全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-operator-takedown` | 已合 develop `ad088ef`；占用已释 |
| echo-doc `docs/work-operator-takedown` | 合入后释放 |
| echo-client | 本块不改；墙和广场已认 `takendown`/`public` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | 本提交 | | 产品已冻 |
| 2. 后端：下架 / 恢复 + 复用工单 | `done` | `echo@f0bb0b7` | `WorkOperatorModerationTest` 5/5；连带 25 条相关测试全绿 | schema `2026091408`；内存专项 |
| 3. 合入 develop 并回填 | `done` | `echo@ad088ef` | 功能头 `f0bb0b7` | 申诉仍不做 |

## 下一块入口

```text
动作：本切片已关。申诉、完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 合入前已公开、且当时没有工单的复用作品，下架入口对不上；新发布的复用路径已补工单。
