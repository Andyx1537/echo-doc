# 阶段账本 · work-publication-review

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` 作品单元；`DECISIONS` G-33 / G-36 / G-37
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：每个用户同一时间只能有一条进行中的投稿；「我的作品墙」能看到占用和允许动作；驳回后同一作品可改再提。
- 不做：真短信、真出图、打 Tag、占 5180/18080、两份锁住的测试夹具、共鸣厅/评论（下一本账本）。
- 权威来源：`API-CONTRACT` 19.10、`ACCEPTANCE` 投稿名额与驳回重提、`DECISIONS` G-33 / G-36。
- 接手先读：本页未勾选的下一块。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-submission-slot` | 已推 `ae6631f` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 他人占用，不碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@c253ac1` | | 产品已冻，不另拍板 |
| 2. 后端：用户级唯一投稿名额 | `done` | `echo@ae6631f` | WorkSubmissionSlotTest 3/3 | pending 占用；二次 POST 拒绝 |
| 3. 前端：作品墙读能力字段 | `todo` | | | 不自推算名额 |
| 4. 驳回修改重提 | `todo` | | | 同一 workId，新内容版本 |
| 5. 审核凭证复用 | `todo` | | | 内容变则失效 |

## 下一块入口

```text
仓库：echo-client
动作：作品墙读 submissionCapability，不自推算名额
禁止：占 5180/18080；改两份锁住的测试夹具
```

## 发现

- 现有 `POST /works` 直接落 `pending`，没有用户级占用检查。
- 名额检查在 insert 前；并发双发还要靠后续唯一约束，本块先锁单线程占用。
