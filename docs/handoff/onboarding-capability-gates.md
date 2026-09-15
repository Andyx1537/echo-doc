# 阶段账本 · onboarding-capability-gates

状态：`CLOSED`
依据：`FRONTEND-TOPOLOGY` FE-04；`DECISIONS` ON2
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 建档候选/细化等按钮跟服务端 `allowedActions` 走，不只看 busy。
- 建档上传只收照片，视频在前后端都拒绝。
- 授权页没有对应 `allowedActions`（后端 `candidate_ready` 只有 select/refine/abandon），同意/暂不同意仍只看 busy。
- 不做：漫画/视频生成、真短信、打 Tag、占 5180/18080、改两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client / echo develop | 已释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 能力门与只收照片 | `done` | `echo@42c205f` `echo-client@abcb002` | `OnboardingApiTest` 13/13；vitest 17；mock 5176 上传拒视频、候选两钮可点 | FE-04 / ON2 |

## 下一块入口

```text
仓库：公共区下一未锁缺口
动作：七单元已关。漫画/视频、真短信、打 Tag 仍后置。不要签完整 QA PASS。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```
