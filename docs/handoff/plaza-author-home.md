# 阶段账本 · plaza-author-home

状态：`OPEN`
依据：`DECISIONS` D24 ② 左滑进主页、④ 返回栈一次弹一层
更新：2026-09-16
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 全屏单卡左滑进该作品作者主页（既有 `UserProfileScreen`）。
- 从主页返回必须回到进来时那张卡，不许一次退回网格。
- 不做：记 `n`、完整后台页、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/plaza-author-home` | 占用中 |
| echo-doc `docs/plaza-author-home` | 占用中 |
| echo | 本块不改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | 产品已冻：左滑进主页 |
| 2. 前端：左滑进作者主页，返回回全屏 | `todo` | | | 主页仍是既有他人主页 |
| 3. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
仓库：echo-client
动作：全屏左滑进作者主页；返回仍停在进来的那张卡
禁止：占 5180/18080；改两份锁住夹具；打 Tag；记 n；做完整后台页
```
