# 阶段账本 · author-home-works

状态：`OPEN`
依据：`DECISIONS` D24 主页；广场已改发 Work，主页墙还在读窗
更新：2026-09-16
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作者主页墙改读公开作品：`GET /users/{id}/works`。
- 点墙上作品进全屏，返回仍回这个人的主页。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/author-home-works` | 占用中 |
| echo-doc `docs/author-home-works` | 占用中 |
| echo | 本块不改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | 主页墙改读作品 |
| 2. 前端：主页墙读 Work | `todo` | | | 点进去进全屏 |
| 3. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
仓库：echo-client
动作：作者主页墙改读公开作品；点进去进全屏，返回回主页
禁止：占 5180/18080；改两份锁住夹具；打 Tag；记 n；做完整后台页
```
