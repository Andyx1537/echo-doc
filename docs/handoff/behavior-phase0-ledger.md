# 阶段账本 · behavior-phase0-ledger

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS` 行为单元；`DECISIONS` G-30 / G-34 / G-37
更新：2026-09-15
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 系统能收下受控行为事实，按字典校验、幂等去重；收藏和绑定由服务端记账；明确反馈改选留历史；可以关个性化、软清除某一域。不改用户眼前这一屏，不进线上排序和私域生成。
- 已合 develop（`echo@63567e7` / `echo-client@2c4d975`）。真短信、真出图、打 Tag、占 5180/18080 仍不做。
- 影子假设怎么算还没有冻结算法，本账本不编一套打分。
- 下一本：整线组合，未开账本前不要开工。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/behavior-phase0` | 已释 @ `8e0497d` |
| echo-client `frontend/behavior-phase0` | 已释 @ `c92f94a` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc` 本页 | 产品已冻 | |
| 2. 后端：批量收下事件 | `done` | `echo@51efd61` | `BehaviorApiTest` | 字典、幂等、单条失败不拖垮整批 |
| 3. 前端：静默上报客户端事件 | `done` | `echo-client@3316017` | vitest | 失败不挡主操作 |
| 4. 服务端成功事实与明确反馈 | `done` | `echo@f4239d1` / `echo-client@c2f627d` | `BehaviorApiTest`；`WorkSocialApiTest` | 客户端重记会被拒 |
| 5. 画像开关与软清除 | `done` | `echo@8e0497d` / `echo-client@c92f94a` | `BehaviorApiTest` 清开关不删事实 | 不改排序 |

## 下一块入口

```text
仓库：echo-doc
动作：本账本已关。下一本是整线组合，未开账本前不要开工。
禁止：占 5180/18080；改两份锁住的测试夹具；合 develop；把隐式信号写进推荐
```

## 发现

- DDL 已有四类对象表。本账本验收走内存 Store。
- 现有 `track()` 是旧漏斗 console，不能当 Phase 0 字典。
- Phase 0 字典没有评论成功事件，所以评论不会被两端各记一次。
- 游客点「我的收藏」曾把接口 1002 吞成空页。已修 `echo-client@78da741`：按 `code === 1002` 出绑定提示，成功后重拉；空列表只给已绑定且无收藏。不是本账本范围。
- 切号（switch_existing）不记 `onboarding_binding_completed`，只记升级原号的绑定。
