# 阶段账本 · work-publication-review

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 作品单元；`DECISIONS` G-33 / G-36 / G-37
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份已齐：同一时间只能有一条进行中的投稿；并发双发靠 `t_work_uk_author_inflight`；作品墙能看到占用和允许动作；驳回后同一条可改再提；改过就不能拿旧审核结论直接公开。
- 不做：真短信、真出图、打 Tag、占 5180/18080、两份锁住的测试夹具、共鸣厅/评论（下一本账本）。
- 权威来源：`API-CONTRACT` 19.1 / 19.10、`DECISIONS` G-33 / G-36 / WP2 / WR3 / FC6。
- 必做块勾完，占用已释。已随整线合入 develop（`echo@63567e7` / `echo-client@2c4d975`）。共鸣厅及后续账本均已关。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-submission-slot` | 已推 `ae6631f`；占用已释 |
| echo `backend/work-resubmit` | 已推 `9ddf557`；占用已释 |
| echo `backend/work-review-evidence` | 已推 `bf59890`（含上两支）；占用已释 |
| echo-client `frontend/work-submission-slot` | 已推 `e8a75ae`；占用已释 |
| echo-client `frontend/work-resubmit` | 已推 `6779c2d`；占用已释 |
| echo-client `frontend/work-review-evidence` | 已推 `8d0d522`（含上两支）；占用已释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 已停（9 月 8 日旧栈） |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@c253ac1` | | 产品已冻，不另拍板 |
| 2. 后端：用户级唯一投稿名额 | `done` | `echo@ae6631f` | WorkSubmissionSlotTest 3/3 | pending 占用；二次 POST 拒绝 |
| 3. 前端：作品墙读能力字段 | `done` | `echo-client@e8a75ae` | vitest 172/172；mock 占用/空闲两态已看过 | 只读 submissionCapability |
| 4. 驳回修改重提 | `done` | `echo@9ddf557` / `echo-client@6779c2d` | WorkResubmitTest 3/3；vitest 174/174；同一条改标题后再提已看过 | 草稿保持 rejected |
| 5. 审核凭证复用 | `done` | `echo@bf59890` / `echo-client@8d0d522` | WorkReviewEvidenceTest 4/4；vitest 177/177；原样「已经在广场上了」、改标题「已提交」已看过 | 内容变则失效 |
| 6. 并发双发唯一约束 | `done` | `echo@0c5e9ce` | WorkSubmissionSlotTest 5/5；schema `t_work_uk_author_inflight` | 先查再插不够 |

## 下一块入口

```text
动作：本账本已关，已合 develop。之后开发在 develop 上做。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```

## 发现

- 名额检查在 insert 前挡不住并发双发。已补 `t_work_uk_author_inflight` 与内存槽锁（schema `2026091404`）。
- mock 种子改为当前用户一条 `rejected`：不占名额，才能同时验「还能发新的」和「同一条改完再提」。旧 localStorage 里若还是 `pending`，要清 `echo.mock.db.works` 才看得到新种子。
- 本后端分支 schema 升到 `2026091402`（作品版本列 + 公开审核凭证表）。未跑 schema.sql 的库对不上，不要拿别人的 18080 来验。
- 内存态重提先改同一份对象再 CAS，不能再用改后的 status 去对 `rejected`。
- 当前生成没有「允许公开」结论，无凭证按 `evidence_missing` 降级进完整审核，不会假装私域可送达等于可公开。
- 对照入口 `?fromCard=card_reuse_ok` 是临时的。撤：删 App 里这段查询，以及 `worksMock` 里 `REUSE_DEMO_*` 常量。
