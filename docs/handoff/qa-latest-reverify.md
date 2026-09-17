# 阶段账本 · qa-latest-reverify

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS`；用户 2026-09-17 核对表
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 本轮只核对并验收「还欠的」：独立 mock 主链、定妆落盘重开可读。不签完整 PASS。
- 漫画/视频/真短信不算欠账。夹具红灯仍锁，公共区未做、账本仍 OPEN。
- 真万相重开未见：本机没有 `ECHO_AIGC_PROVIDER_CODE` / 出图钥匙，未编造编码，未起库。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/candidate-reopen` | 已合 develop `a45ee24`；占用已释 |
| echo-doc `docs/qa-latest-reverify` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未读未改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 定妆落盘重开可读 | `done` | `echo@7d4138b` / develop `a45ee24` | `OnboardingImageGenTest` 通过；换新 `LocalDiskStorage` 仍读到 `/api/v1/files/` 与隐式标识 | 不是万相实网 |
| 2. 最新 mock 主链独立复验 | `done` | 本提交 | Chrome DOM `http://127.0.0.1:5197/` | 广场作品 → 全屏同条 → 作者主页墙 → 返回仍停在该条 → 想说的话叠在全屏上；游客收藏出绑定；我的作品有未通过/看看为什么 |
| 3. 夹具红灯 | `blocked` | | 文件名在仓，公共区不读不改 | 合入块早已完成；第 7 块仍锁 |

## 下一块入口

```text
动作：本核对已关。完整私域 PASS 仍要真库 + 真出图编码。夹具红灯等占用释放。
禁止：占 5180/18080；改两份锁住夹具；打 Tag；编造服务提供者编码
```

## 发现

- 当前进程未监听 5432/5433/55433，也没有出图环境变量。独立 QA 只能做到 mock 主链 + 落盘专项，不能冒称万相重开或 PG 整线。
- 从全屏返回广场会重新「轻轻摆出来」，广场网格本次没有保持挂载。不是本轮整改范围。
