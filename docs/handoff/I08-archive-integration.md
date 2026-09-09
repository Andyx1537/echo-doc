# 阶段账本 · I08-archive-integration

状态：`OPEN`（必做合入已完成；第 7 块仍锁，不关闭）
依据：`docs/CURRENT-DELIVERY-STATUS.md` I08
更新：2026-09-09
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：前后端已验证功能分支合入各仓 `develop` 并推远端。
- 不做：不打 `v*` Tag；不碰 `release`/`master`；Plaza Card 对齐不算第 4 单元。
- 接手先读：本页未勾选且占用栏未锁住的下一块。

## 占用

| 资源 | 状态 |
|---|---|
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁。另有工作树未提交改动。公共区不读、不改这两份文件 |
| echo develop | 已推 `c4fbc69`，释放 |
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
| 7. 测试夹具红灯 | `blocked` | | | 占用栏锁住，公共区不做 |

## 下一块入口

```text
仓库：echo-doc
动作：提交本账本与 CURRENT-DELIVERY-STATUS 回填，推 develop
之后：I08 合入部分结束。不要做第 7 块。不要开第 3/4 单元，除非公共账本改了当前 TODO。
```

## 发现

- 前端合入后测试 166 条全绿（含建档/认证合同测试）。
- 第 4 单元仍是 Card，不是 Work。
