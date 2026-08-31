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

9. 🔴 **「两套世界」这件事早就裁定过，是实现没照做。** `DECISIONS QA6`：
   **「WS + HTTP 并存，HTTP 真正复用 WS 侧领域服务，不平行自建域」**（交后端落实）；
   `AD6` 又重申一次「共享领域层，不重造域，守 `QA6`」。而实际发生的是
   **HTTP 侧建了一个完整的平行域**——70 个文件、26 张表、95 条手写 SQL、自己的 store 层。
   ⚠️ **本文档 v1 把它写成「待定：两套世界要不要合并」，那是错的**，
   它不待定，它是一条已拍板结论的执行欠账。
10. **方向已定：统一到引擎的注解 / 领域服务那套，不走手写 SQL**（2026-08-31 制作人重申 `QA6`）。
    但引擎现在表达不了 HTTP 侧要的东西，缺口量化见 §6——**先扩引擎，再迁**。
    ⚠️ 这条欠账 `API-CONTRACT` 已用 **`M-6`** 编号在跟，本文档不另起编号，只补量化与执行前置。
    🔴 **已有一个可抄的样板**：`ResonanceService` 是目前唯一被两侧共用的领域服务
    （`TECH-DESIGN-feed-recall-and-exposure §2.5.1`），迁移时照它的形状做。
11. **WS 那 8 条协议入口没有活着的客户端**（2026-08-31 核实）。H5 原型全仓零 WebSocket 引用；
    唯一的 WS 客户端 `unity-legacy/` 功能代码停在 2026-08-28 拆仓那天，之后只改过名，
    且需本地 Unity Editor 手动 Play 才会连。⚠️ **但这不等于可以直接删**——
    `QA6` 裁的是「并存」，删掉 WS 是推翻裁定，要单独走推翻流程。

🔴 **仍然待定的**：

- **`QA6` 的「并存」还作不作数** —— WS 已确认无活跃客户端，但 `QA6`/`AD6` 明写并存。
  🔴 **这条不能由实现侧自行决定**：删 WS 会让 `TECH-P1` 整份传输层规格、7 个 proto 文件、
  `unity-legacy/` 一起失去承接。定它需要制作人对「Unity 那条线是否永久放弃」拍板。
- **`schema.sql` 要不要改成迁移脚本序列** —— 现在是一个「从零建库」的全量脚本，
  没有版本号、不能增量执行。⚠️ 若按 §10 迁到注解，本条自动消解（DDL 由注解生成），
  但**迁移期两者并行时仍需要一个防分叉的检查**。
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

## 5. 盘点方法上的一条教训

本轮一度报出「四个类的 Javadoc 里 `schema.sql` 被写成了 `sql/n`」——**这是假的**，
文件从来没坏过。起因是检索时写了 `rg -rn 'schema.sql'`：`-r` 在 ripgrep 里是
**replace（把匹配替换成给定文本再输出）**，不是 `grep -r` 的递归。于是所有命中的
`schema.sql` 在**输出里**被替换成了 `n`，看起来像文件内容坏了。

🔴 **这个坑在本项目已经踩过第二次。** 记在这里是因为它的失败形态很坏：
**不报错，只是给出一份看起来合理的错误证据**，而据此去"修"会得到一次空提交
（perl 找不到要替换的内容，git 报 nothing to commit——这一步反而是唯一的报警）。

**判准**：用 ripgrep 检索时不要带 `-r`；递归是默认行为，不需要开关。

## 6. 迁到注解那套之前，引擎要先补什么

方向已定（§10：统一到引擎注解 / 领域服务，不走手写 SQL）。这一节记的是**执行前置**——
引擎当前表达不了 HTTP 侧在用的东西，先补齐才谈得上迁。数字为 2026-08-31 实测。

### 6.1 查询端：`IRepository` 只有等值查询

`Aengine/src/main/java/com/aengine/persistence/IRepository.java` 全部 12 个方法：
`get(id)` / `get(field,value)` / `list(field,value)` / `list(Map)` / `listAll()` /
`add` / `save` / `forceSave` / `remove` / `truncateAll`。

`PgRepository` 里 **`ORDER BY`、`LIMIT`、`JOIN` 各 0 处**。`buildWhereSQL` 只拼
`col = ?` 的 AND 串——没有范围、没有 `IS NULL`、没有 `IN`。

🔴 **它的设计假设是「整表装进内存，在 Java 里筛」**，`CachedRepository` /
`DelaySaveRepository` / Redis 那一整套都围绕这个假设。对游戏服的玩家、道具成立；
对一条要 `ORDER BY publishedAt DESC LIMIT 20` 的内容流不成立。

现有 11 个手写 SQL 类、约 95 条语句用到的特性：

| 特性 | 用量 | 引擎 |
|---|---|---|
| `IS NULL`（软删谓词） | 22 | 无 |
| `ORDER BY` | 21 | 无 |
| `LIMIT` | 16 | 无 |
| `ON CONFLICT`（幂等写） | 14 | 无 |
| `jsonb` | 11 | 无 |
| `JOIN` | 2 | 无 |

### 6.2 表定义端：注解表达不了 `schema.sql` 里的多数约束

`@Table` 有 `name` / `index` / `cache` / `clusterBy` / `comment` / `autoCreate` / `charset`；
`@Column` 有 `name` / `notNull` / `defaultValue` / `readOnly` / `length` / `immutable` /
`comment` / `charset`；`@Index` 只有 `name` / `columns` / `type`。
⚠️ **`@Fk` 打开看只是一个索引类型标记，不生成外键约束。**

`schema.sql` 里注解表达不了的：

| 东西 | 数量 |
|---|---|
| `CHECK` 约束 | 30 |
| 外键 | 19 |
| 局部索引（`WHERE ...`） | 23（共 76 个索引） |
| 索引内 `DESC` | 9 |
| `jsonb` 列 | 12 |
| `vector` 列 | 1 |
| 特殊索引类型（ivfflat 等） | 1 |

🔴 **那 23 个局部索引正是软删的守卫**（`WHERE deletedAt IS NULL` 的唯一索引），
迁移时如果表达不出来，「一张卡只能发一个未删除的作品」这类约束会从数据库层掉到应用层——
**掉下去不会报错，只会在并发时偶发重复**。

⚠️ 另注：`@Column.charset()` 默认 `utf8mb4`，说明引擎原本是给 MySQL 写的，
`PgRepository` 是 echo 侧的 PG 适配。扩展时要留意两边的类型映射不是一一对应。

### 6.3 建议留一处例外

`t_self_vector` 的 pgvector 相似度检索。它的意义就是让数据库算距离；
搬进 Java 内存等于把这个能力废掉。建议这一处继续走原生 SQL，并在文档里写明是**刻意例外**，
否则下一个人会当成遗漏顺手"修"掉。
