# 基础能力最小逻辑单元

> 上层索引：`PD-20260903-product-foundation-v34` v4.2。本文只拆开发单元，不重新定义产品方向。

## 拆分原则

每个单元只有一个用户结果、一个主对象/状态机和一个主责系统。相邻系统只提供冻结边界，不把其内部实现并入当前任务。单元分别验收，最后另建组合联调任务。

| 顺序 | 单元 | 单一用户结果 | 主对象与主责系统 | 最小边界 | 本单元明确不做 |
|---|---|---|---|---|---|
| 1 | `private-onboarding-session` | 匿名用户完成单宠素材、主体、问卷和候选确认，刷新/失败后可恢复 | `OnboardingSession` / 建档系统 | 生成前只消费 Auth 返回的 `phoneBound/accountId` | 不实现短信、不实现公开发布、不接推荐 |
| 2 | `phone-account-resolution` | 用户完成新手机号绑定或切回已有账号，得到正确会话和返回结果 | `PhoneChallenge/Resolution` / 身份系统 | 向 Onboarding/评论返回 `returnToAllowed/nextAction` | 不迁移匿名资料、不实现建档页面 |
| 3 | `work-publication-review` | 用户创建一个 Work，并得到公开、待审或明确失败结果 | `Work/ReviewEvidence/Moderation` / 作品审核系统 | 只读取来源 Card 冻结快照和授权结果 | 不实现 Plaza 排序、不实现评论 |
| 4 | `plaza-work-read` | 用户在 Plaza 只看到 Work，并进入同一 Work 详情 | `PlazaBatch/WorkProjection` / 分发读取系统 | 消费公开 Work 投影 | 不迁移旧 Card 互动、不实现发布审核 |
| 5 | `work-comments-favorites` | 用户在 Work 详情读取、评论、回复、治理和收藏 | `WorkComment/Favorite` / 作品互动系统 | 只消费身份结果和 Work 可见性 | 不实现手机号供应商、不改变 Plaza 排序 |
| 6 | `behavior-phase0-ledger` | 系统可靠记录受控行为证据，但不改变用户当前体验 | 四类行为账本 / 行为系统 | 接收各业务域约定事件 | 不接线上排序、不进入私域生成 |
| 7 | `foundation-combination-e2e` | 六个已通过单元组合后跑通私域建档、发布、浏览和互动主线 | 仅组合验证 | 固定各单元已验收构建与契约 | 不在联调中新增产品规则或重写单元内部 |

## 当前推进位置

`private-onboarding-session` 的手机号依赖已解除；2026-09-08新号绑定续建窗真实浏览器主路径已通，当前收尾与异常组合仍待验收。完整清单与两专业架构入口见 [当前执行进展](../../CURRENT-DELIVERY-STATUS.md)。

第2单元固定验证码开发增量已通过QA；现推进第1单元与身份结果的组合收尾，并逐项记录任务恢复、媒体生成、补素材等缺失。后续Work、Plaza、评论仍按独立单元推进。
