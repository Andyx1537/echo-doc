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
| echo `backend/i09-anonymous-recovery` | 本线写（尚未检出则从 develop 开） |
| echo-client `frontend/i09-anonymous-recovery` | 本线写（尚未检出则从 develop 开） |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 落 G-38 并开账本 | `done` | 本提交 | 定案进 develop | PH5/ON1–ON3/GN1 |
| 2. 后端：`POST /auth/account/recovery/session` | `todo` | | 相关 surefire | 只收 recoveryCredential；签发匿名会话 |
| 3. 前端：「我」页唤醒入口 | `todo` | | vitest | 用本地恢复凭据；不得提交 accountId |
| 4. 回填 I09 | `todo` | | STATUS | 不宣称浏览器整链；合入等做完再提 |

## 下一块入口

```text
仓库：echo
分支：backend/i09-anonymous-recovery（从 develop 开）
接口：POST /auth/account/recovery/session { recoveryCredential }
禁止改动：BlockSilentFailureTest.java、WindowVisibilityTrimTest.java
```

## 发现

- 通用 `POST /auth/device/session` 对 `recovery_only` 已返回 `device_credential_recovery_required`；缺的是专用消费口。
- 切号 confirm 已签发 `anonymousRecovery.recoveryCredential`，前端写入 `echo.auth.anonymous-recovery.v1`。「我」页绑定态还没有唤醒按钮。
