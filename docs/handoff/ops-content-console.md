# 阶段账本 · ops-content-console

状态：`CLOSED`
依据：`OPS-CONTENT-CONSOLE`；`CURRENT-DELIVERY-STATUS` B04
更新：2026-09-17 · R4 已合 `echo-client@f45eabd`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 内容运营收成一套台：作品 / 回忆卡 / 开关；举报标未开。离开手机框。
- 已合 develop：`echo@206c1ab` / `echo-client@f45eabd`（功能头 `2fb9fa2`）。
- R4：超时只信服务端 `slaBreached`。
- 不做：看板、TOTP、客服、收入、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/ops-content-console` | 已合 develop `206c1ab`；占用已释 |
| echo-client `frontend/ops-card-sla` | 已合 develop `f45eabd`；占用已释 |
| echo-doc `docs/ops-card-sla` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 体系落盘 | `done` | `echo-doc@b6585db` | | `OPS-CONTENT-CONSOLE.md` |
| 2. R0 壳 + R1 回忆卡 + R2 开关 | `done` | `echo@7361097` / `echo-client@cec8cf6` | Chrome：壳四栏；卡待审通过后剩一条；开关写下时间；举报写未开 | GET settings 须先于 `:id` |
| 3. 合入 develop 并回填 | `done` | `echo@206c1ab` / `echo-client@94d1f00` | | |
| 4. R3 回忆卡下架 | `done` | `echo-client@15c003f` / develop `9cc1f07` | Chrome：已处置公开卡「先收起来」后变已下架，无再上架 | |
| 5. R4 SLA 展示 | `done` | `echo-client@2fb9fa2` / develop `f45eabd` | mock：待审一条 `slaBreached=true`，已处置没有 | 前端不算时差 |

## 下一块入口

```text
动作：本切片已关。看板 / TOTP / 客服 / 收入 / 举报提交另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag；给回忆卡加运营直接恢复；前端自算超时
```

## 发现

- 开关只有 PATCH，没有 GET，台里读不到当前档。GET 必须注册在 `/admin/moderation/:id` 前面，否则 `settings` 会被当成工单 id。
- 回忆卡 `takendown` 不在运营允许集里，不能像作品那样再上架；只能等作者申诉后推翻回待审。
- 作品队列目前不下发 `slaBreached`，本轮只在回忆卡栏展示。
