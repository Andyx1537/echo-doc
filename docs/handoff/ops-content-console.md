# 阶段账本 · ops-content-console

状态：`OPEN`
依据：`OPS-CONTENT-CONSOLE`；`CURRENT-DELIVERY-STATUS` B04
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 把内容运营收成一套台，再按 R0→R1→R2 整改，不再按单个 tab 开账本。
- 先壳（离开手机框），再回忆卡，再开关。举报标未开。
- 不做：看板、TOTP、客服、收入、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| echo-doc `docs/ops-content-console` | 公共区 | `docs/ops-content-console` | 合入后释 |
| echo `backend/ops-content-console` | 公共区 | GET settings | 合入后释 |
| echo-client `frontend/ops-content-console` | 公共区 | 运营台壳 + 三栏 | 合入后释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | | 锁，不改 | |
| 5180 / 18080 | | 不占 | |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 体系落盘 | `doing` | | | `OPS-CONTENT-CONSOLE.md` |
| 2. R0 壳 + R1 回忆卡 + R2 开关 | `todo` | | | 同一交付 |
| 3. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

```text
仓库：echo-client / echo
分支：frontend/ops-content-console · backend/ops-content-console
命令或文件：echo-h5-proto/src/components/OpsConsole.tsx
禁止改动：5180/18080；两份锁住夹具；打 Tag
```

## 发现（当初不知道的）

- 作品默认队列没有已公开栏，上一刀才补 `tab=public|takendown`。卡队列本来就有 handled。
- 开关只有 PATCH，没有 GET，台里读不到当前档。
