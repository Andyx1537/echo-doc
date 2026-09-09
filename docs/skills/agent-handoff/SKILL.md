---
name: agent-handoff
description: Treat the workspace as a shared public space. On entry, only summarize overall status and the current-stage TODOs, then advance those public TODOs. Use when starting or resuming implementation, coordinating multiple agents, or handing off unfinished work.
---

# Agent Handoff

工作区是公共空间。进来的执行方是同一个角色，不按工具区分身份。

完成公共区摊派的任务。不要去别人自留地探索。要的是效果，不是两套做法互相覆盖。

权威副本：`echo-doc/docs/skills/agent-handoff/SKILL.md`。

## 每次进场只做两件事

1. **总体情况归纳** —— 读 `docs/CURRENT-DELIVERY-STATUS.md` 和 `docs/handoff/` 里未关闭的账本。用几句话说清现在在哪。
2. **当前阶段 TODO** —— 只列出账本里未勾选、且占用栏未锁住的下一块。

然后按这块推进。梳理保持短。不要为了「了解全貌」去翻对话、去翻别人的工作树、去扫未登记的目录。

## 推进规则

- 一次只做当前 TODO。做完：验收、勾选、写提交号、提交、推送账本。
- 占用栏锁住的路径、分支检出、未提交文件，视为自留地。不读、不改、不 `reset`、不抢检出。
- 未提交不算交付。进度只认账本和 git。
- 产品切片仍走 `development-readiness`。分支仍走 `BRANCHING-WORKFLOW.md`。

## 阶段账本

路径：`docs/handoff/<task-id>.md`。模板：`templates/STAGE-LEDGER.md`。

`done` 必须有提交号。任务关闭：必做块勾完、占用释放、该推的已推。账本保留，状态改 `CLOSED`。
