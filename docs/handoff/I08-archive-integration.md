# 阶段账本 · I08-archive-integration

状态：`OPEN`
依据：`docs/CURRENT-DELIVERY-STATUS.md` I08
更新：2026-09-09
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：把已验证的前后端功能分支与工作区已完成改动归档到各仓 `develop` 并推远端，让 `develop` 成为真实底座。
- 不做：不打 `v*` Tag；不碰 `release`/`master`；不把 Plaza Card 对齐算成第 4 单元（目标是 Work 公开投影）；不改 Codex 占用的两份测试文件。
- 权威来源：`CURRENT-DELIVERY-STATUS.md`、`BRANCHING-WORKFLOW.md`。
- 接手先读：本页未勾选的下一块；不要通读对话。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| 测试夹具（写） | Codex 工作树 | `/Users/andy/.codex/worktrees/3971/echo` 检出 `backend/private-onboarding-integration`；未提交 `echo-server/src/test/java/com/echo/http/BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 占用方提交这两份文件后改本栏为「无」 |
| echo develop（写） | 本线已合并未推 | 工作区 `/Users/andy/Documents/workSpace/echo` @ `c4fbc69`，领先 `origin/develop` 17 个提交 | 推送后释放 |
| echo-client 功能分支（写） | 本线已提交未推 | `frontend/plaza-card-contract` @ `40b5fb9` | 推送后释放 |

只读对照不要再检出 `backend/private-onboarding-integration`。用游离提交 `dc3d196`。

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 盘点三仓与 I08 缺口 | `done` | 无代码提交；结论在本账本 | 文档 `CURRENT-DELIVERY-STATUS` 与 `git branch -a` 交叉核对 | 后端功能分支领先 develop 16；前端 10；前端 develop 上曾有 9 个未提交文件 |
| 2. 抢救前端 Plaza 契约 | `done` | `echo-client@40b5fb9` | `tsc --noEmit` 通过；vitest 147/147 | 分支 `frontend/plaza-card-contract`，**未推**。对齐的是当前 CardView，不是第 4 单元 Work |
| 3. 合并后端集成进 develop | `done` | `echo@c4fbc69` | `merge-tree` 干净；`mvn test` 450 条、2 失败 64 错误 | **未推**。合并前 develop 基线 433/3/48。多出的红灯未完成 A/B（工作树占用打断） |
| 4. 推送 echo develop | `todo` | | `git push origin develop` 后远端哈希 = `c4fbc69` | 不包含测试夹具修复 |
| 5. 合并并推送前端 | `todo` | | `merge-tree` 已确认 `frontend/private-onboarding-integration` 对 develop 干净；4 个文件与 plaza 分支重叠，须先推 plaza 再合，冲突停下报告 | 顺序：推 `frontend/plaza-card-contract` → 合 `frontend/private-onboarding-integration` → 再处理 plaza 合入。plaza 合入后仍不得宣称第 4 单元完成 |
| 6. 回填 I08 状态 | `todo` | | `CURRENT-DELIVERY-STATUS` I08 改为已合入 develop，并写明未打 Tag | 与本账本关闭同一提交 |
| 7. 测试基线 51 红（夹具过时） | `blocked` | | 产品规则不改；只改测试夹具 | **不要做。** Codex 已在占用栏两份文件上改 `guest=false`、广场按卡断言、`petId` 改纯数字。等它提交 |

## 下一块入口

接手方从这里开始：

```text
仓库：echo
分支：develop
命令或文件：git push origin develop ；验证 origin/develop == c4fbc69
禁止改动：BlockSilentFailureTest.java、WindowVisibilityTrimTest.java
```

推送成功后做第 5 块（前端）。第 7 块仍禁止，除非占用栏已释放且那两份文件已有提交号。

对照功能分支自身红灯（只读）：

```text
git -C echo worktree add --detach /tmp/echo-fb-ro dc3d196
cd /tmp/echo-fb-ro && mvn -o test
```

不要 `worktree add` 到分支名 `backend/private-onboarding-integration`。

## 发现（当初不知道的）

- `echo-client` develop 工作区 9 个未提交文件是做完的 Plaza Card 对齐，不是半成品。
- Codex 工作树里未提交的测试改动，与 2026-08-31 被打断未提交的夹具修复同一组文件、同一改法。
- 合并后 `mvn test` 红灯从 51 增到 66，尚未证明是集成引入还是功能分支自带。
