# 阶段账本 · onboarding-consent-gate

状态：`CLOSED`
依据：`FRONTEND-TOPOLOGY` FE-04；上一账本 `onboarding-capability-gates` 留下的授权页
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 选完候选后下发 `set_consent`；授权页同意/暂不同意跟这条能力走。
- 确认页只有授权已给才下发 `confirm`（mock 对齐后端）。
- 不做：全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、改两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client / echo develop | 已释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 授权能力门 | `done` | `echo@b60ff77` `echo-client@28c6c3b` | `OnboardingApiTest` 14/14；vitest 17；mock 5176 授权两钮可点，同意后进确认 | FE-04 授权页 |

## 下一块入口

```text
仓库：公共区下一未锁缺口
动作：七单元已关。漫画/视频、真短信、打 Tag、全屏层仍后置。不要签完整 QA PASS。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```
