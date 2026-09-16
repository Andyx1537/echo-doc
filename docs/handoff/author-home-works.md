# 阶段账本 · author-home-works

状态：`CLOSED`
依据：`DECISIONS` D24 主页；广场已改发 Work，主页墙还在读窗
更新：2026-09-16 · 已合 `echo-client@f20e8c7`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作者主页墙改读公开作品：`GET /users/{id}/works`。
- 点墙上作品进全屏，返回仍回这个人的主页。
- 已合 develop：`echo-client@f20e8c7`（功能头 `ba55c73`）。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/author-home-works` | 已合 develop `f20e8c7`；占用已释 |
| echo-doc `docs/author-home-works` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@19e220a` | | 主页墙改读作品 |
| 2. 前端：主页墙读 Work | `done` | `echo-client@ba55c73` | 浏览器：主页出作品；点另一条进全屏；返回仍是林的主页 | 点进去进全屏 |
| 3. 合入 develop 并回填 | `done` | `echo-client@f20e8c7` | 功能头 `ba55c73` | |

## 下一块入口

```text
动作：本切片已关。记 n / 完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 从主页进全屏会卸掉主页再挂上，返回会重新拉一次墙，不是停在原来的滚动位置。
