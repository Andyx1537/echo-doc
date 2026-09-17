# 阶段账本 · work-operator-console

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` B04；`API-CONTRACT` §17.1 / 19.4；上一账本留下的完整后台页
更新：2026-09-17
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 运营用 `?ops=works` 打开作品审核台：待审通过/先不公开，申诉维持/回待审。不进 C 端底栏。
- 走已有 `/admin/moderation/**` 与 `/admin/appeals/:id/handle`，带 `expectedStateVersion`。
- 不做：回忆卡队列、举报、开关、TOTP、下架入口、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 谁 | 路径/分支/工作树 | 释放条件 |
|---|---|---|---|
| echo-doc `docs/work-operator-console` | 公共区 | `docs/work-operator-console` | 合入 develop 后释 |
| echo-client `frontend/work-operator-console` | 公共区 | 功能分支 | 合入 develop 后释 |
| echo | | 本块不改后端 | |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | | 锁，不改 | |
| 5180 / 18080 | | 不占 | |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `doing` | | | 产品已冻，接口已在 |
| 2. 前端：待审 / 申诉处置 | `todo` | | | mock + `?ops=works` |
| 3. 合入 develop 并回填 | `todo` | | | |

## 下一块入口

接手方从这里开始：

```text
仓库：echo-client
分支：frontend/work-operator-console
命令或文件：echo-h5-proto/src/components/WorkOperatorScreen.tsx
禁止改动：5180/18080；两份锁住夹具；打 Tag；漫画/视频/真短信
```

## 发现（当初不知道的）

- 作品队列默认只回活动态；`tab=appealing` 才出申诉。没有 handled tab，处置完从队列消失。
