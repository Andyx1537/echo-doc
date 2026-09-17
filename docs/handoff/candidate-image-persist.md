# 阶段账本 · candidate-image-persist

状态：`CLOSED`
依据：`OPS-CANDIDATE-PERSIST`；`CURRENT-DELIVERY-STATUS` B03
更新：2026-09-17 · 已合 `echo@6cc7d2a`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 定妆候选落到本方存储，带隐式标识；没编码就失败。
- 已合 develop：`echo@6cc7d2a`（功能头 `62a8ff2`）。
- 不做：漫画/视频、编造编码、阿里云桶、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/candidate-image-persist` | 已合 develop `6cc7d2a`；占用已释 |
| echo-doc `docs/candidate-image-persist` | 合入后释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 体系落盘 | `done` | 本提交 | | `OPS-CANDIDATE-PERSIST.md` |
| 2. persist 不再回供应商链 | `done` | `echo@62a8ff2` | `OnboardingImageGenTest` 6/6 | 未配编码失败；有编码落到 `/api/v1/files/` |
| 3. 合入 develop 并回填 | `done` | `echo@6cc7d2a` | origin/develop = `6cc7d2a` | |

## 下一块入口

```text
动作：本切片已关。真出图联调须先配 ECHO_AIGC_PROVIDER_CODE。漫画/视频另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag；编造生产编码
```

## 发现

- 万相客户端只回供应商 URL、不带回字节。落盘必须先拉取再写入；拉失败就失败，不再把那条临时链写进候选。
