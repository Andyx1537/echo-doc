# 阶段账本 · work-author-appeal

状态：`CLOSED`
依据：`API-CONTRACT` 17.2；后端申诉入口已合 `echo@cab832a`
更新：2026-09-16 · 已合 `echo-client@7decd24`
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作者在「我的作品」对驳回/下架看到「看看为什么」；`appealable=true` 才能申一次。
- 申诉中只出状态，不再出入口。不改审核结论，不直接公开。
- 已合 develop：`echo-client@7decd24`。
- 不做：完整后台页、全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、两份锁住夹具。

## 占用

| 资源 | 状态 |
|---|---|
| echo-client `frontend/work-author-appeal` | 已合 develop `7decd24`；占用已释 |
| echo-doc `docs/work-author-appeal` | 合入后释放 |
| echo | 本块未改后端 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 不占 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | 本提交 | | 产品已冻 |
| 2. C 端：看看为什么 + 提交申诉 | `done` | `echo-client@0caff8f` | vitest 申诉相关全绿；390 宽墙/说明页已出图 | mock + http + 墙 |
| 3. 合入 develop 并回填 | `done` | `echo-client@7decd24` | 功能头 `0caff8f` | 完整后台页仍不做 |

## 下一块入口

```text
动作：本切片已关。完整后台页另开账本。
禁止：占 5180/18080；改两份锁住夹具；打 Tag
```

## 发现

- 列表不下发 `appealable`，入口先按驳回/下架露出「看看为什么」，能不能申以 moderation 回执为准。
