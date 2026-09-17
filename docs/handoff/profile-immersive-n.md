# 阶段账本 · profile-immersive-n

状态：`OPEN`
依据：`SPEC-feed-surfaces` 概述第 1 条；上一账本 `plaza-immersive-n` 留下的作者主页不记 n
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作者主页墙上点进全屏：墙上那页签发网格快照，再换 immersive 快照；驻留满 1000ms 才记 `n`。
- 看自己的墙不签发快照（不是对别人的投放）。墙上列出、滚过一律不记。
- 不做：全屏另排推荐流、第二套曝光表、漫画/视频、真短信、打 Tag、完整后台页、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| echo `backend/profile-immersive-n` | 本线 | echo 仓该分支 | 合入 develop 后释 |
| echo-client `frontend/profile-immersive-n` | 本线 | echo-client 仓该分支 | 合入 develop 后释 |
| echo-doc `docs/profile-immersive-n` | 本线 | 本账本 | 合入 develop 后释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁 | | 不改 |
| 5180 / 18080 | 不占 | | |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | |
| 2. 后端：作者墙签发 reqId | `todo` | | | 他人墙才签；自己的墙不签 |
| 3. 前端：主页进全屏上报 | `todo` | | | 复用 POST /plaza/immersive |
| 4. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
仓库：echo
分支：backend/profile-immersive-n
动作：GET /users/:id/works 给他人墙签发网格 reqId
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现（当初不知道的）

- 还没有。
