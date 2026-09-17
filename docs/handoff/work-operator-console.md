# 阶段账本 · work-operator-console

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` B04；`API-CONTRACT` §17.1 / 19.4；上一账本留下的完整后台页
更新：2026-09-17 · 已合 `echo-client@a35bf1b`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 运营用 `?ops=works` 打开作品审核台：待审通过/先不公开，申诉维持/回待审。不进 C 端底栏。
- 走已有 `/admin/moderation/**` 与 `/admin/appeals/:id/handle`，带 `expectedStateVersion`。
- 已合 develop：`echo-client@a35bf1b`（功能头 `98b30aa`）。
- 不做：回忆卡队列、举报、开关、TOTP、下架入口、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/work-operator-console` | 已合 develop `a35bf1b`；占用已释 |
| echo-doc `docs/work-operator-console` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@4d9bfa5` | | 产品已冻，接口已在 |
| 2. 前端：待审 / 申诉处置 | `done` | `echo-client@98b30aa` | Chrome：待审两条 → 通过后剩一条；申诉「钥匙串」回到待审后申诉栏空 | mock 4/4；http 路径断言绿 |
| 3. 合入 develop 并回填 | `done` | `echo-client@a35bf1b` | 功能头 `98b30aa` | |

## 下一块入口

```text
动作：本切片已关。回忆卡队列 / 举报 / 开关 / 下架入口另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 作品队列默认只回活动态；`tab=appealing` 才出申诉。没有 handled tab，处置完从队列消失。
- 真后端要 `ECHO_ADMIN_ROLES`；没配一律 403，不是默认放行。
