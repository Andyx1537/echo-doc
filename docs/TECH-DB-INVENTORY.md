# 后端表清单与结构盘点

> 盘点时间 2026-08-30 · 对应 `echo@2e56b29` · 数据源：`echo-server/src/main/resources/sql/schema.sql` 与全量 Java 源码交叉核对

## 概述

**37 张表，分属两套互不相识的持久化世界，由同一个 `main` 同时启动。** 这是本次盘点最要紧的一条，
其余问题多半是它的派生物。

已核实的结论：

1. **`module` 世界**（34 个 Java 文件）：Netty / protobuf / WebSocket 入口，用 `@Table` 注解 +
   Aengine class-table 框架，**运行时自动建表、自动加列**（`PgRepository.autoCreate` 与
   `ALTER TABLE ADD COLUMN IF NOT EXISTS`）。独占 7 张表。
2. **`http` 世界**（70 个 Java 文件）：REST 入口，全部手写 SQL，表结构靠 `schema.sql`
   **人工执行**（Docker 首次建卷时由 entrypoint 跑一次）。独占 26 张表。
3. 🔴 **schema 因此有两个事实源**，且只有一个在版本控制里。注解那套改一个字段，
   线上库跟着变，`schema.sql` 不会动，**没有任何检查会发现两者分叉**。
4. 🔴 **两张表被两个世界同时使用**：`t_account`、`t_self_vector`。前者的后果已经显形——
   WS `1001 登录` 只凭客户端给的 `openId` 建号，HTTP 侧有绑定校验，**同一张账号表两套准入标准，
   实际安全水位由弱的那套决定**（`SPEC-security §4.14 E2`）。
5. 🔴 **37 张表里只有 3 张有 `deletedAt`**（`t_resonance`、`t_resonance_text`、`t_work`）。
   **核心内容表 `t_memory_card` 不在其中**——`DECISIONS CM-G0-1`「一律软删」在它上面没有落点。
6. 🔴 **外键极稀**：只有 6 张表声明了外键（合计 15 条），其余 31 张靠应用层自觉。
7. **两张表全仓零引用**：`t_topic`、`t_resonance_type_log`。前者不是废弃品——
   话题树是产品核心概念（卡必须挂到叶子），**表建好了，代码一行没写**。
8. **`t_train_sample` 有表无实现**：代码走 `InMemoryTrainingCorpus`，PG 落库标着 TODO。
   进程一重启训练语料全丢。

🔴 **仍然待定的**：

- **两套世界要不要合并，往哪边合** —— 定它需要先确认 WS 那 8 条入口还有没有客户端在用。
  H5 原型走的全是 HTTP；`unity-legacy/` 走的是 WS。**如果 Unity 那条线确认不再维护，
  module 世界连同它的 7 张独占表可以整体下线**，`t_account` 的双写问题随之消失。
- **`schema.sql` 要不要改成迁移脚本序列** —— 现在是一个「从零建库」的全量脚本，
  没有版本号、不能增量执行。定它需要先定上一条（合并方案会决定迁移工具的选型）。
- **`t_memory_card` 补 `deletedAt` 的代价** —— 该表 7 个索引、被 30 处代码引用，
  补列意味着所有读路径都要加谓词。**漏一处不会报错，只会让删掉的卡重新出现**。
  定它需要先把读路径清点完。

---

## 1. 两套世界的分界

| | `module` 世界 | `http` 世界 |
|---|---|---|
| 入口协议 | WebSocket / protobuf（8 条协议入口） | HTTP REST（75 条） |
| 持久化写法 | `@Table` 注解 + 反射元数据 | 手写 SQL 字符串 |
| 建表方式 | 🔴 **运行时自动建表 + 自动加列** | `schema.sql` 人工执行 |
| Java 文件数 | 34 | 70 |
| 独占表 | 7 | 26 |
| 典型类 | `Account` / `MindProfile` / `MindSpace` | `PgEchoStore` / `PgModerationStore` / `WorkStore` |

两者由 `bootstrap/EchoServer.java` 的同一个 `main` 启动：先起 Netty 网关，
再调 `EchoHttpBootstrap.start(...)`。**同一个进程、同一个数据库、两套建表逻辑。**

### 1.1 为什么这不只是「历史包袱」

自动建表这一侧**会赢**。注解改了字段，进程一起来 `ALTER TABLE` 就执行了；
`schema.sql` 是死文件，不会跟着变。于是：

- 从 `schema.sql` 重建的库，和线上跑了半年的库，**结构可能不一样**
- 而对比它们的唯一办法是人去 diff，没有任何自动检查
- 🔴 **分叉不会报错**——它表现为「本地复现不了线上的问题」

## 2. 按世界分组的表清单

### 2.1 `module` 世界独占（7 张）

| 表 | 实体类 | 说明 |
|---|---|---|
| `t_avatar` | `module/avatar/Avatar` | 形象 |
| `t_mind_profile` | `module/mind/MindProfile` | 意识档案 |
| `t_mind_space` | `module/space/MindSpace` | 意识空间实例 |
| `t_echo` | `module/echo/Echo` | 回响 |
| `t_friendship` | `module/social/Friendship` | 关系链（好友 / 关注） |
| `t_stall` | `module/social/Stall` | 摊位（P1 占位） |
| `t_resonance_record` | `module/resonance/ResonanceRecord` | ⚠️ 已停写。`ResonanceService` 注释写明不再落此表（`TECH-DESIGN-feed-recall-and-exposure §1.1/§2.5.3`），Repository 仅为兼容保留 |

⚠️ `t_friendship`（module）与 `t_relation`（http）**是同一件事的两套实现**。
`t_stall` 标着「P1 占位」——占位表也在自动建表的范围内。

### 2.2 两个世界共用（2 张）

| 表 | 谁在写 | 风险 |
|---|---|---|
| `t_account` | `module/account/Account`（`@Table`）+ http 侧 19 处引用 | 🔴 **两套准入标准**。WS `1001` 只凭 `openId` 字符串建号或登号，无凭证校验；HTTP 侧 `POST /auth/guest` + `POST /auth/bind` 有设备维度与绑定校验。**弱的那套决定实际水位** |
| `t_self_vector` | `module/mind/SelfVector`（`@Table`）+ `infra/vector/PgVectorStore`（手写 SQL） | 🔴 向量列宽在 SQL 侧写死 768，而 `ECHO_EMBED_DIM` 可配任意正整数且**不校验**。配错时启动正常、日志安静，第一次写库才炸，错误指向 SQL 层，排查方向会跑偏 |

### 2.3 `http` 世界独占（26 张）

按域分组：

**账号与宠物**：`t_account_profile`、`t_pet`、`t_pet_echo`、`t_relation`、`t_remember`

**内容**：`t_memory_card`、`t_postcard`、`t_record`、`t_message`、`t_work`、`t_resource`

**互动**：`t_flower_log`、`t_reaction_seen`、`t_resonance`、`t_resonance_text`、
`t_resonance_type`、`t_card_exposure`

**治理**：`t_moderation`、`t_moderation_setting`、`t_report`、`t_audit_log`、
`t_card_visibility_log`、`t_block`、`t_follow`、`t_feature_switch`

**AI**：`t_train_sample`（⚠️ 有表无实现）

### 2.4 零引用（2 张）

| 表 | 列数 | 判定 |
|---|---|---|
| `t_topic` | 10 | 🔴 **不是废弃品，是没开工**。话题树是产品核心概念（话题按维度成树、卡必须挂到叶子、情感类只归类不参与匹配），表已建好，**代码一行没写**。`t_work.topicIds` 存的是 jsonb 数组，与本表没有外键关系 |
| `t_resonance_type_log` | 7 | 待确认。`t_resonance_type` 有 8 处引用，其日志表零引用，疑似写入路径未接 |

## 3. 软删覆盖

| | 张数 | 表 |
|---|---|---|
| 有 `deletedAt` | 3 | `t_resonance`、`t_resonance_text`、`t_work` |
| 无 | 34 | 其余全部，**含 `t_memory_card`** |

🔴 **`DECISIONS CM-G0-1`「一律软删」在 34 张表上没有承接。** 这不等于 34 处违规——
多数表本来就不删（流水、日志）。真正要补的是**用户能删的东西**：

- `t_memory_card` —— 核心内容表，7 个索引、30 处代码引用
- `t_remember` / `t_follow` / `t_block` —— 已知三处物理删除（`unremember` / `unfollow` / `unblock`），
  见待办 L4

⚠️ **补 `deletedAt` 的隐蔽代价**：所有读路径要加 `WHERE deletedAt IS NULL`。
**漏一处不报错，只会让删掉的东西重新出现**，而用户已经以为它没了。
`WorkStore` 是照这条教训写的——它不提供任何「查全部行」的方法。

## 4. 外键覆盖

只有 6 张表声明了外键，合计 15 条：

| 表 | 外键数 |
|---|---|
| `t_resonance` | 6 |
| `t_work` | 2 |
| `t_card_visibility_log` | 2 |
| `t_block` | 2 |
| `t_follow` | 2 |
| `t_memory_card` / `t_moderation` / `t_report` / `t_resource` | 各 1 |

其余 31 张表的引用完整性靠应用层自觉。⚠️ **这一条不建议一次性补齐**——
存量数据里大概率已有孤儿行，加约束会让建表直接失败。要补得先跑一遍孤儿行体检。

## 5. 顺带发现

- 四个类的 Javadoc 里 `schema.sql` 被写成了 `sql/n`（`PgModerationStore`、`PgEchoStore`、
  `EchoStore`、`Models`），疑似历史上一次替换把 `schema.` 吃掉了。指针悬空，已修。
