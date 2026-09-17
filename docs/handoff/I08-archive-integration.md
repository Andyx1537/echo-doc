# 阶段账本 · I08-archive-integration

状态：`CLOSED`
依据：`docs/CURRENT-DELIVERY-STATUS.md` I08
更新：2026-09-17 · 夹具占用已清：滞留修复合入 develop，17/17 绿
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 前后端功能分支早已合入各仓 `develop`。夹具占用不是别人在改，是 9 月 8 日工作树两份未提交夹具修复被后来账本抄成「锁，不改」。
- 那两份修复已合入 `echo@417b22b` / develop `bb08f86`：已绑定主体、数字窗 id、广场按卡 id 断言。占用工作树已还原干净。
- 不做：不打 `v*` Tag；不碰 `release`/`master`。

## 占用

| 资源 | 状态 |
|---|---|
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 已释放。修复在 develop，不再锁 |
| echo develop | 已推 `bb08f86`，释放 |
| echo-client 功能分支 | 已推并合入 `55053e5`，释放 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 盘点三仓与 I08 缺口 | `done` | 账本 | 与 STATUS 交叉核对 | |
| 2. 抢救前端 Plaza 契约 | `done` | `echo-client@40b5fb9` | 当时 tsc + 147 tests | 过渡件，不是第 4 单元 |
| 3. 合并后端集成进 develop | `done` | `echo@c4fbc69` | merge-tree 干净 | |
| 4. 推送 echo develop | `done` | `origin/develop` = `c4fbc69` | `git push` 成功 | |
| 5. 合并并推送前端 | `done` | `echo-client@55053e5` | tsc 通过；vitest 166/166 | 先合建档集成，再合 plaza；未宣称第 4 单元完成 |
| 6. 回填 I08 状态 | `done` | 本提交 | STATUS I08 已改为合入完成、未打 Tag | |
| 7. 测试夹具红灯 | `done` | `echo@417b22b` / develop `bb08f86` | `BlockSilentFailureTest` 5 + `WindowVisibilityTrimTest` 12 全绿 | 占用已清，文件留下当守卫 |

## 下一块入口

```text
动作：本账本已关。未打 Tag。真出图落盘仍要合规侧的 ECHO_AIGC_PROVIDER_CODE 和出图钥匙。
禁止：占 5180/18080；编造服务提供者编码；打 Tag
```

## 发现

- 前端合入后测试 166 条全绿（含建档/认证合同测试）。
- 第 4 单元仍是 Card，不是 Work。
- 占用原因：2026-09-03 基线保护 + Codex 工作树 `/Users/andy/.codex/worktrees/3971/echo` 从 9 月 8 日起只脏这两份测试。develop 上原文件从未改过，所以「锁」被各账本空转了 9 天。
