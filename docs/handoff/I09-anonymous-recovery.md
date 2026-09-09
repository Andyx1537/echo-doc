# 阶段账本 · I09-anonymous-recovery

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS.md` I09；`DECISIONS` G-38/`PH5`
更新：2026-09-09
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：切号后，用户能从「我」的账号区唤醒仍保留的匿名会话；唤醒后可继续上传和答题，只能走到手机确认。
- 不做：阿里云、建档内补传、视频当肖像识别、真模型出图、合入 develop、打 Tag、两份锁住的测试夹具。
- 权威来源：`API-CONTRACT §19.8–19.9`、`G-38/PH5`、`ACCEPTANCE TC-PH-03`。
- 接手先读：本页未勾选的下一块。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/i09-anonymous-recovery` | 已推 `6d2b1b3`，未合 develop |
| echo-client `frontend/i09-anonymous-recovery` | 已推 `5c4efde`，未合 develop |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 落 G-38 并开账本 | `done` | 本提交 | 定案进 develop | PH5/ON1–ON3/GN1 |
| 2. 后端：`POST /auth/account/recovery/session` | `done` | `echo@6d2b1b3` | 已编译；Auth PG 测无库 skip | 只收 recoveryCredential；签发匿名会话 |
| 3. 前端：「我」页唤醒入口 | `done` | `echo-client@5c4efde` | vitest 167/167 | 用本地恢复凭据；切号同时收好建档钥匙 |
| 4. 回填 I09 | `todo` | | STATUS | mock 已走切号/我/唤醒；修钥匙后未重跑；真 PG 未接；不合 develop |

## 下一块入口

```text
仓库：echo-client
动作：在 I09 前端重跑 切号→「我」→唤醒→自动回到绑定墙；有隔离 PG 再接 18080
禁止：占用 5180/18080；打 Tag；合入未经验证的功能分支；改两份锁住的测试夹具
```

## 发现

- 通用 `POST /auth/device/session` 对 `recovery_only` 已返回 `device_credential_recovery_required`；缺的是专用消费口。
- 切号 confirm 已签发 `anonymousRecovery.recoveryCredential`，前端写入 `echo.auth.anonymous-recovery.v1`。「我」页绑定态在有恢复凭据时显示「回到未绑定的那份资料」。
- 第一次 mock 浏览器：切号、唤醒按钮、回到游客都过了。两处缺口已修：mock 曾把恢复凭据指到新账号；切号曾清掉建档钥匙。修后未重跑整链。
- 本机 5180/18080 属于他人工作树，本线用 5280 mock，未接真 PG。
