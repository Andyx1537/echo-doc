# 阶段账本 · behavior-phase0-ledger

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` 行为单元；`DECISIONS` G-30 / G-34 / G-37
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：系统能收下受控行为事实，按字典校验、幂等去重、按用途隔离；不改用户眼前这一屏，不进线上排序和私域生成。
- 不做：真短信、真出图、打 Tag、占 5180/18080、两份锁住的测试夹具、改广场排序、把隐式信号写进推荐或生成。
- 权威来源：`API-CONTRACT` 20、`SPEC-behavior-evidence-and-adaptation`、`DECISIONS` BE1–BE7 / FC3 / BC3。
- 接手先读：本页未勾选的下一块。
- 产品已冻，不另拍板。Phase 0 假设和决策必须 `shadow=true`。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/behavior-phase0` | 从 `backend/work-comments-favorites` 开出 |
| echo-client `frontend/behavior-phase0` | 从 `frontend/work-comments-favorites` 开出 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 他人占用，不碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc` 本页 | 产品已冻 | |
| 2. 后端：批量收下事件 | `done` | `echo@51efd61` | `BehaviorApiTest` 4/4 | 字典、幂等、单条失败不拖垮整批 |
| 3. 前端：静默上报客户端事件 | `done` | `echo-client@3316017` | vitest 183/183 | 失败不挡主操作 |
| 4. 服务端成功事实与明确反馈 | `todo` | | | 收藏/绑定等不得由客户端重记 |

## 下一块入口

```text
仓库：echo
动作：收藏/评论/绑定成功由服务端记账；明确反馈改选留历史
禁止：占 5180/18080；改两份锁住的测试夹具；合 develop；改线上排序；客户端重记成功事实
```

## 发现

- DDL 已有四类对象表。本账本验收先走内存 Store，PG 接线可后做。
- 现有 `track()` 是旧漏斗 console，不能当 Phase 0 字典。
- 游客点「我的收藏」现在会落成空页（接口 1002 被前端吞了）。不是本块范围，下一本互动收尾再补登录。
