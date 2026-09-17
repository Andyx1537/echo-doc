# 阶段账本 · onboarding-snapshot-prompt

状态：`CLOSED`
依据：`OPS-ONBOARDING-PROMPT`；`CURRENT-DELIVERY-STATUS` B03
更新：2026-09-17 · 已合 `echo@1e8b27a`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 旁白消费四类快照的码，模板升 v2。
- 已合 develop：`echo@1e8b27a`（功能头 `c2f3bca`）。
- 不做：漫画/视频、整段 JSON 进模型、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/onboarding-snapshot-prompt` | 已合 develop `1e8b27a`；占用已释 |
| echo-doc `docs/onboarding-snapshot-prompt` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 体系 + prompt 四行 | `done` | `echo@c2f3bca` | `OnboardingImageGenTest` 7/7 | 不含 freeText / resourceId / 未授权事实 |
| 2. 合入 develop 并回填 | `done` | `echo@1e8b27a` | origin/develop = `1e8b27a` | |

## 下一块入口

```text
动作：本切片已关。漫画/视频另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 旧 prompt 把问卷码写成 `facts=`，和事实层重名。现拆成 `answers=` 与真正的 `facts=`。
