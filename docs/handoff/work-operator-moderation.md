# 阶段账本 · work-operator-moderation

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` B04；`BACKEND-TOPOLOGY` BE-G06；`API-CONTRACT` 19.4；`DECISIONS` G-37 / FC8
更新：2026-09-16 · 已合 `echo@ed46982`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 自制上传送审落 `t_work_moderation`；运营通过后公开且 `reviewedAt` 只写一次；驳回释放投稿名额；处置带 `expectedStateVersion` CAS。
- 已合 develop：`echo@ed46982`。
- 不做：完整管理后台页面、下架/恢复/申诉、全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-operator-moderation` | 已合 develop `ed46982`；占用已释 |
| echo-doc `docs/work-operator-moderation` | 合入后释放 |
| echo-client | 本块不改 C 端；过审后既有作品墙/广场读 `public` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | 本提交 | | 产品已冻，不另拍板 |
| 2. 后端：工单 + 通过/驳回 + CAS | `done` | `echo@4611488` | `WorkOperatorModerationTest` 3/3；连带 28 条相关测试全绿 | schema `2026091407`；内存专项，未跑真 PG |
| 3. 合入 develop 并回填拓扑 | `done` | `echo@ed46982` | 功能头 `4611488` 已在 develop | 下架/申诉/后台页仍不做 |

## 下一块入口

```text
动作：本切片已关。下架/恢复/申诉、完整管理后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 旧 `lastModerationId` 只是雪花，没有工单行。自制上传因此永远停在 pending，广场只能靠凭证复用那条路出内容。
- 作品工单必须另表：`t_moderation.cardId` 外键指向回忆卡，不能拿 Work id 顶上去。
