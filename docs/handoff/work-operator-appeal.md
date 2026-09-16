# 阶段账本 · work-operator-appeal

状态：`CLOSED`
依据：`API-CONTRACT` 19.4 / §17.2；`DECISIONS` MOD2；上一账本留下的申诉
更新：2026-09-16 · 已合 `echo@cab832a`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 一条作品一生只能申诉一次，判据是工单 `appealAt` 已写入；推翻原判也不退还。
- 驳回或下架可申；维持原判回去；推翻只回待审，不直接公开。投稿名额被占则失败关闭。
- 已合 develop：`echo@cab832a`。
- 不做：完整后台页、全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-operator-appeal` | 已合 develop `cab832a`；占用已释 |
| echo-doc `docs/work-operator-appeal` | 合入后释放 |
| echo-client | 墙已有「申诉中」文案；本块未改前端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | 本提交 | | 产品已冻 |
| 2. 后端：作者申诉 + 主管维持/推翻 | `done` | `echo@5de226d` | `WorkOperatorModerationTest` 10/10；连带 30 条相关测试全绿 | schema `2026091409`；内存专项 |
| 3. 合入 develop 并回填 | `done` | `echo@cab832a` | 功能头 `5de226d` | 完整后台页仍不做 |

## 下一块入口

```text
动作：本切片已关。完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 推翻回待审时若作者另有占用名额的作品，必须失败关闭，不能把两条同时放进 pending。
- `appealAt` 有库触发器挡住事后改写；申诉中工单仍占「同一作品仅一张未完结工单」。
