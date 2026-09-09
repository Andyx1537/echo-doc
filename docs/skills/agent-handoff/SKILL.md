---
name: agent-handoff
description: Split implementation into committed stages with a shared checkbox ledger so another agent can continue the same development flow. Use when starting, resuming, or handing off coding work; when another agent may occupy the same files or worktree; when leaving a task unfinished; or when the user asks to stage, checkpoint, sync, or coordinate parallel agents.
---

# Agent Handoff

执行方会被阶段性换掉。对话不是事实源。未提交的改动不算交付。

本 skill 管**实现阶段的交接**。产品切片仍走 `development-readiness` 与 `docs/delivery/<id>/MANIFEST.md`。分支规则仍走 `docs/BRANCHING-WORKFLOW.md`。

权威副本：`echo-doc/docs/skills/agent-handoff/SKILL.md`。工具侧缓存只许做指针。

## 何时读

动手改代码、恢复未完成任务、发现别人的工作树/脏文件、或准备离开当前任务时，先读本页，再读对应阶段账本。

## 开工前

1. 打开 `docs/handoff/`：有未关闭账本且路径重叠，先读账本，不要另起炉灶。
2. 检查三仓工作树、功能分支、未提交文件。脏文件先登记归属，未确认前不改、不丢、不纳入基线。
3. 写或续写一份阶段账本。没有账本就开工，等于只把进度存在对话里。
4. 一次只吃一块。账本里没勾选的下一块以外的事，默认不做。

## 阶段怎么切

一块必须同时满足：

- 能单独提交，提交后对接手方有意义；
- 验收能一句话说清做完没做完；
- 失败时不必回滚相邻块。

禁止用「继续设计」「再看看」充当阶段。那不是开发项。

推荐粒度：盘点 → 止血提交 → 契约/测试对照 → 实现 → 验证 → 合入/推送 → 回填文档。按任务删减，不要凑数。

## 做完一块立刻做这四步

1. 跑这一块的验收（编译、最近测试、或约定的对照命令）。
2. 在账本把该块勾上，写下提交号、验证结果、下一块入口。
3. 提交**这一块的代码或文档**。未提交不算勾完。
4. 推送账本所在分支。远端没有相同提交，不得对接手方说「已同步」。

`/tmp` 补丁、对话摘要、本地 stash 都不是同步。

## 接手时按这个顺序

1. 读账本概述与未勾选的下一块，不要通读历史对话。
2. 核对接手条件：分支、提交号、占用声明、禁止改的路径。
3. 只做下一块。发现账本与仓库冲突，以仓库为准，先改账本再继续。
4. 不重做已勾选且提交号仍在的块。需要改已完成块时，新开一块并写明原因。

## 占用与避让

同一路径、同一分支检出、同一未提交文件，同时只允许一个执行方写。

- 你占着：在账本「占用」栏写路径、分支、工作树、未提交文件。离开前改为释放，或写清谁接着写。
- 别人占着：不抢检出、不改那些文件、不 `reset` / `clean`。用游离提交号做只读对照。
- 发现别人的未提交改动与你的下一块相同：停。在账本注明，让占用方先提交。不要平行改同一文件。

## 失败形态（本项目已发生）

| 做法 | 后果 |
|---|---|
| 测试夹具改完不提交 | 会话一断，修复蒸发；另一执行方后来改了同一对文件 |
| 进度只写在对话里 | 接手方只能猜，或把已做的再做一遍 |
| 用工作树独占分支做只读对照 | 挡住别人的检出；对照应用游离提交号 |
| 一块里同时合并、修测试、改产品 | 失败时分不清新坏旧坏，接手方无法只续一块 |

## 阶段账本

路径：`docs/handoff/<task-id>.md`。`task-id` 用业务编号，如 `I08-archive-integration`，不要写工具名或人名。

模板：`templates/STAGE-LEDGER.md`。

一块勾完的最低字段：状态、提交号、验证、下一块入口命令或文件。缺提交号的勾选视为无效。

任务关闭条件：全部必做块已勾、占用已释放、相关分支已推或已写明为什么不推。关闭后账本保留，状态改为 `CLOSED`，不要删。
