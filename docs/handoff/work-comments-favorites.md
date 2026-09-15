# 阶段账本 · work-comments-favorites

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 评论收藏单元；`DECISIONS` G-31 / G-34 / G-35
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 作品详情有两层评论（默认热门三加二）；匿名只能看预览，展开要绑手机；收藏只进自己的收藏页，作者看不到人数。
- 已合 develop（`echo@63567e7` / `echo-client@2c4d975`）。真短信、真出图、打 Tag、占 5180/18080 仍不做。
- 热门精确权重未定：本账本用「可见回复数 + 时间」，`RANKING_VERSION=1` 写进游标。
- 下一本：行为账本。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/work-comments-favorites` | 已释 @ `2bf949a` |
| echo-client `frontend/work-comments-favorites` | 已释 @ `3e1dd90` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc` 本页 | 产品已冻 | |
| 2. 后端：评论两层与收藏 | `done` | `echo@2bf949a` | `WorkSocialApiTest` 3/3 | 匿名无完整游标；写操作要绑定 |
| 3. 前端：详情评论、展开登录、收藏页 | `done` | `echo-client@3e1dd90` | vitest 181/181；5177 详情三加二、展开出登录 | 不本地重排 |

## 下一块入口

```text
仓库：echo-doc
动作：本账本已关。下一本是行为账本，未开账本前不要开工。
禁止：占 5180/18080；改两份锁住的测试夹具；合 develop
```

## 发现

- 现有窗留言不能替代作品评论。收藏不得出现在作品公开 DTO 的计数里。
- schema 升到 `2026091403`（评论/收藏/互动幂等表）。未跑 schema.sql 的库对不上。Store 当时验收走内存；`2026-09-15` 已接线，见组合账本块 4。
- Continuation 类型只有 `none` | 建档，没改鉴权契约；`returnTo=workId+rootCommentId` 是前端状态。
- 游客进收藏页曾把 1002 当成空列表。补修不在本账本重开：`echo-client@78da741`。
