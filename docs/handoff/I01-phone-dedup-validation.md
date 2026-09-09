# 阶段账本 · I01-phone-dedup-validation

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS.md` I01；用户 2026-09-09：测试号 + `9999`，验格式/去重/绑定/切号/资料不迁。外接短信不做。
更新：2026-09-09
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：已有号切到旧账号后，不能带走匿名建档资料；校验（格式、错码、去重）用测试号锁住。
- 不做：阿里云/真短信、I02/I03/I07、作品/广场、占用栏里的两份测试夹具。
- 权威来源：`API-CONTRACT §19.8`、`PD-20260906-phone-account-resolution`。
- 接手先读：本页未勾选的下一块。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/i01-phone-dedup-validation` | 本线写 |
| echo-client `frontend/i01-phone-dedup-validation` | 本线写 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本、核对已有实现 | `doing` | | 读公开契约与 develop 代码 | 切号/校验主路径已有；缺组合隔离测试与前端恢复判定单测 |
| 2. 后端：切号后建档隔离 + 校验锁住 | `todo` | | 相关 surefire | 不改产品规则 |
| 3. 前端：恢复判定与号码规范化单测 | `todo` | | vitest | 切号走新建档，不 resume |
| 4. 回填 I01 | `todo` | | STATUS | 不宣称浏览器整链 PASS |

## 下一块入口

```text
仓库：echo
分支：backend/i01-phone-dedup-validation（若尚未创建则从 develop 开）
禁止改动：BlockSilentFailureTest.java、WindowVisibilityTrimTest.java
```

## 发现

- 切号 confirm 已固定 `returnToAllowed=false`，建档续接时 `nextAction=restart_in_existing_account`。
- 前端绑定墙已按「能 resume 才续接，否则 createFresh」。缺把这条判定抽成可测函数。
- Auth 专项测依赖 `ECHO_TEST_PG_URL`，本地无库时会 skip；建档隔离可用内存仓储，不依赖 PG。
