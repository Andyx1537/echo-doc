# 阶段账本 · I01-phone-dedup-validation

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS.md` I01；用户 2026-09-09：测试号 + `9999`，验格式/去重/绑定/切号/资料不迁。外接短信不做。
更新：2026-09-09
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 已交付：切号后不能带走匿名建档资料；格式/错码/去重用测试号锁在专项测试里。
- 不做：阿里云/真短信、I02/I03/I07、作品/广场、占用栏里的两份测试夹具、浏览器整链 PASS。
- 功能分支未合 `develop`。要合入另开一步，不要在本账本重开产品讨论。
- 权威来源：`API-CONTRACT §19.8`、`PD-20260906-phone-account-resolution`。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/i01-phone-dedup-validation` | 已推 `20759ac`，未合 develop |
| echo-client `frontend/i01-phone-dedup-validation` | 已推 `54298de`，未合 develop |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本、核对已有实现 | `done` | `echo-doc@77c86da` | 读公开契约与 develop 代码 | 切号/校验主路径已有 |
| 2. 后端：切号后建档隔离 + 校验锁住 | `done` | `echo@20759ac` | `OnboardingApiTest` 11/11 | `PgAuthServiceTest` 切号续接断言已加；无 `ECHO_TEST_PG_URL` 时 skip |
| 3. 前端：恢复判定与号码规范化单测 | `done` | `echo-client@54298de` | vitest 168/168 | 只在 `returnToAllowed && resume` 时续接 |
| 4. 回填 I01 | `done` | 本提交 | STATUS | 不宣称浏览器整链 PASS |

## 下一块入口

```text
仓库：echo-doc
动作：I01 隔离已关。唤醒入口走 I09，合入等 I09 做完再提。
禁止：打 Tag；改 BlockSilentFailureTest.java、WindowVisibilityTrimTest.java
```

## 发现

- 切号 confirm 已固定 `returnToAllowed=false`，建档续接时 `nextAction=restart_in_existing_account`，即使 ContinuationPolicy 允许源草稿也不续接。
- 切到旧账号后 GET 匿名草稿返回 `onboarding_forbidden`；该账号上 create 是空草稿，源素材和答案仍挂在匿名账号。
- 前端恢复判定已抽出 `shouldResumePrivateOnboarding`；号码规范化统一为任意 11 位转 `+86`。
- Auth 专项测仍依赖 `ECHO_TEST_PG_URL`；建档隔离测走内存仓储，不依赖 PG。
