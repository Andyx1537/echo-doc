# 合规规格 · 实现缺口核查

> 版本：v0.1 · 2026-08-30  
> 方法：直接读 `echo` 仓源码与 `schema.sql`，**不引用任何文档里的状态描述**。  
> 触发：制作人要求「补齐合规规格 ACD 三组」。核下来结论与这个说法相反——**规格是齐的，代码不齐**。

## 概述

- **A / C / D 三组在文档层面已全部落地，不需要补。** A 组 4 条回改已分别落进
  `ACCEPTANCE`、`AI-CAPABILITIES`、`SPEC-publish-and-ops`、`API-CONTRACT` 四份文档且都留了取代痕迹；
  C 组 `S-1`~`S-8`、D 组 `S-9`~`S-10` 都在 `SPEC-trust-and-compliance §CM-G0S` 里有实质正文
  （最短 551 字，最长 4879 字，另有 v0.4 追加的 `S-11`）。
- 🔴 **真正的缺口在实现侧，而且是红线级的：三个 C 端「取消」动作至今是物理 DELETE。**
  `取消记得`、`取消关注`、`取消拉黑` 各自一条 `DELETE FROM`，
  而 `§CM-G0-1` 正文**点名列举**的例子就是「取消记得」。
- 🔴 **`S-7`（部分唯一索引）现在无法执行，因为它的前提不成立。** 它要求给唯一索引加
  `WHERE "deletedAt" IS NULL`，但那些表**根本没有 `deletedAt` 列**——
  14 条唯一索引里只有 4 条带 partial（都在 `t_resonance` 系），其余 10 条所在的表都没有软删列。
  **顺序是反的**：得先有软删列，`S-7` 才有对象。
- 📋 `DELETE /pet/me` 的处置**合规**：它被 `echo.devRoutes`（缺省 false）门控，
  属于 `A-4` 三个允许选项里的「仅非生产装配」。但它调用的四表级联方法 `deletePet` 仍在代码里。
- 🔴 **待定**：`t_remember`/`t_follow`/`t_block` 改软删属于破坏性 schema 变更，
  且会连带改动去重语义（`ON CONFLICT` 要跟着改）。定它需要制作人拍「本期做还是记进风险台账」。

---

## 1. A 组四条：已落地，逐条有痕

| # | 要求 | 落在哪 | 状态 |
|---|---|---|---|
| A-1 | `ACCEPTANCE TC-29` 级联清理 → 软删口径 | `ACCEPTANCE.md:251` | ✅ TC-29 已改为索引条目，正文拆成 `TC-EXP-01`~`10` |
| A-2 | `AI-CAPABILITIES §7` 四处回改 + 节首加「以 CM-G0 为准」 | `AI-CAPABILITIES.md:6,138,140` | ✅ 整节 v0.2 回改，四处各有「回改留痕」标注 |
| A-3 | `SPEC-publish-and-ops §1.4`「一并清理」→「不可见/停更」 | `SPEC-publish-and-ops.md:62,65,67` | ✅ 已改，v0.2 勘误留痕在 `:67` |
| A-4 | `API-CONTRACT` 的 `DELETE /pet/me` 路径语义冲突 | `API-CONTRACT.md:153-161` | ✅ 正式端点定死 `DELETE /pet/:id`，处置留痕完整 |

## 2. C / D 组：规格有实质正文，不是占位

`SPEC-trust-and-compliance §CM-G0S` 下十一个小节，正文长度：

```
S-1  对外视图穷举 + 三身份遍历      1486 字
S-2  训练链路定义 + 四层判据        1166 字
S-3  打包明示告知 9 要件             968 字
S-4  G0-2 本期可验交付物             964 字
S-5  缺的 API / schema / 数值       1512 字
S-6  未授权时 C 端可见行为            551 字
S-7  部分唯一索引                    630 字
S-8  隐式标识 + 检出 + 派生覆盖      4879 字
S-9  CR 红线例外白名单              1504 字
S-10 存量 5 处物理删除逐处处置       1191 字
S-11 站外分享 AI 标识（v0.4 追加）  56092 字
```

## 3. 🔴 实现缺口：三处 C 端「取消」是物理删除

`§CM-G0-1` 原文：

> **含「开关型取消」**（取消记得、取消置顶、取消勾选等状态回退）：同样**不得物理删行**，
> 改为状态字段 `active=false` + 时间戳。理由不是钻字眼——「谁在什么时候取消了记得」
> 本身就是 CM-D1 要求留底的审计信息。

代码实际：

| 动作 | 端点 | 实现 | 位置 |
|---|---|---|---|
| 取消记得 | `POST /windows/:petId/remember`（`remembered=false`） | `DELETE FROM "t_remember"` | `PgEchoStore.java:512` |
| 取消关注 | `DELETE /users/:id/follow` | `DELETE FROM "t_follow"` | `FollowStore.java:141` |
| 取消拉黑 | `DELETE /accounts/:id/block` | `DELETE FROM "t_block"` | `BlockStore.java:142` |

🔴 **第一条正是规格点名举的例子。** 规格写得很清楚，实现没跟上——
这不是理解分歧，是这三处从来没有按规格改过。

另有三处物理 DELETE，性质不同，分开记：

| 位置 | 语句 | 判断 |
|---|---|---|
| `PgEchoStore.java:353-356` | `deletePet` 连删 `t_pet_echo`/`t_postcard`/`t_remember`/`t_pet` | 🔴 `S-10` 判为「下线」。端点已按 `A-4` 门控到 dev，但**方法本体仍在**，`resetPet` 仍在调 |
| `PgEchoStore.java:617` | `DELETE FROM "t_postcard" WHERE "petId"=?` | 🔴 待判：是否属 `S-10` 已列的 5 处之一 |
| `EchoRepository.java:26` | `DELETE ... WHERE "expireAt" < ?` | 📋 过期清理，多半属 `S-9` 白名单范畴，需对照确认 |

## 4. 🔴 `S-7` 的前提不成立：那些表没有 `deletedAt` 列

`S-7` 要求「所有含唯一键的业务表，唯一索引改为部分索引 `WHERE "deletedAt" IS NULL`」。
逐条核 `schema.sql` 的 14 条唯一索引：

| 表 | 唯一索引 | 表有 `deletedAt` | 索引带 partial |
|---|---|---|---|
| `t_resonance` | 三条（card/author/topic × actor × type） | 有 | ✅ 是 |
| `t_resonance_text` | `uk_card_actor` | 有 | ✅ 是 |
| `t_account` | `uk_open_id` | **无** | 否 |
| `t_account_profile` | `uk_device` | **无** | 否 |
| `t_remember` | `uk_pet_account` | **无** | 否 |
| `t_follow` | `uk_account_target` | **无** | 否 |
| `t_block` | `uk_account_peer` | **无** | 否 |
| `t_relation` | `uk_account_peer` | **无** | 否 |
| `t_friendship` | `uk_account_peer` | **无** | 否 |
| `t_topic` | `uk_slug` | **无** | 否 |
| `t_report` | `uk_reporter_target_open` | **无** | 否 |
| `t_card_exposure` | `uk_card_viewer_day` | **无** | 否 |

**所以「S-7 未实现」这个说法本身是不准确的**：它不是漏做，是**做不了**——
没有 `deletedAt` 列，partial 谓词没有对象。

🔴 **执行顺序必须是：先给 §3 那三张表加软删列并改写取消逻辑，再回来做 S-7。**
反过来做的话，加了 partial 谓词而列恒为 NULL，索引行为与现在完全一样，
**不报错、不生效**——又是一个静默假动作。

## 5. 改动的代价（供拍板）

给 `t_remember`/`t_follow`/`t_block` 加软删，不是加一列那么简单：

1. **去重语义要跟着改。** 现在靠 `ON CONFLICT ("petId","accountId") DO NOTHING` 保证不重复记得。
   改软删后，同一对 (pet, account) 会存在多行（记得 → 取消 → 再记得），
   唯一索引必须同时改成 partial，**两件事必须同一次迁移做完**，
   否则中间态要么撞唯一键要么产生重复行。
2. **读路径要全部带上过滤。** `isRemembered`、关注列表、拉黑判定、
   以及 `hiddenBetween` 这类被广场与窗共用的判断，漏一处就是"取消了还生效"或"取消了还显示"。
3. **存量数据没有历史。** 已经被物理删掉的取消动作找不回来，
   迁移只能让新数据留底；这一点要写进风险台账，不要让协议承诺覆盖到存量。

## 6. 未核的部分

- `S-1`~`S-6`、`S-8` 的实现状态**本轮未核**，只核了 `S-7` 与 `S-10` 相关的删除口径。
- `t_postcard` 那处 DELETE 是否在 `S-10` 已列的 5 处之内，未对照。
- `S-9` 白名单的实际内容与代码里的通用删除（`PgRepository.delete`、
  `EchoRepository` 过期清理）是否对得上，未核。
