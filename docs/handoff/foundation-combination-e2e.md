# 阶段账本 · foundation-combination-e2e

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 第七单元；`IMPLEMENTATION-SLICES` 整线组合
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 广场上的「它最后一个下午」点进去还是这一条；游客看到三加二，写和展开要绑手机；收藏不露人数；收藏成功由服务端记账。
- 已随整线合入 develop：`echo@63567e7` / `echo-client@2c4d975`。没有占 5180/18080。
- 身份与建档主链沿用已经走过的证据，本账本没有再占别人的真接口重跑。
- 真短信、真出图、打 Tag 仍后置。之后开发就在 develop 上做。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/foundation-combination` | 已释 @ `208fec3` |
| echo-client `frontend/foundation-combination` | 已释 @ `23e3a06` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc` 本页 | 不另拍板 | |
| 2. 后端：广场到评论收藏行为一条链 | `done` | `echo@208fec3` | `FoundationCombinationTest` 1/1 | 同一 workId |
| 3. 前端：mock 与 5177 走同一条 | `done` | `echo-client@23e3a06` | vitest 186/186；5177 点进同一条 | 不占 5180 |

## 下一块入口

```text
仓库：echo-doc
动作：本账本已关。七单元已合 develop。打 Tag 仍后置。之后开发在 develop 上做。
禁止：占 5180/18080；改两份锁住的测试夹具；从 master 开功能
```

## 发现

- 行为分支已经叠着作品、广场、评论。整线组合只拼 Router 和已有 mock，没有另砌一套实现。
- Phase 0 字典没有评论成功事件，组合链里也不会被两端各记一次。
