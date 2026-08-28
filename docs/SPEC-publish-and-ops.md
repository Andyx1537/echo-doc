# SPEC · 回忆卡发布 / 运营审核后台 / 精选·主题池（GTM §10 落地）

| 项 | 内容 |
|---|---|
| 角色 | 产品规格（给前端/后端/运营直接开工）；**v0.7 · 2026-08-25** |
| **v0.7 变更** | 🔴 **`MOD4` 回改（`DECISIONS §G⁗⁗⁗⁗`）**：§1.8.3b 末段 `originType` 变更留痕，由 ~~「`changeRole` 记为 `ops`」~~ 改为 **「`changedRole` 记为 `moderator`」**（原文划除保留）。两处都错——字段名是 `changedRole`，取值只能是 `author`/`moderator`/`system`。⚠️ 🔴 **`ops` 违反 §1.8.5 的 CHECK 约束、根本写不进去**，而该 INSERT 与 `originType` 变更同事务，照原文实现是**整个改判动作失败**；🔴 **且不得用放宽 CHECK 的方式绕过**（那会制造出两套并存的运营语义，追溯能力永久损失）。<br>⚠️ **`OM1` 模型登记（`DECISIONS §G⁗⁗⁗⁗`）**：窗口/卡层级模型已定——**窗是容器（一只宠物一个窗）· 回忆卡是窗里发出来的一条 · 🔴 共鸣厅流的是卡**。🔴 **本轮只在 §1.1 加标注，不改任何接口或字段定义**；不一致点清单见 `DECISIONS §G⁗⁗⁗⁗` 三。 |
| v0.6 变更 | 🔴 **`A6` 时间类型统一为 `bigint`（UTC 毫秒 epoch）**：§1.5 字段表 `createdAt/updatedAt/publishedAt` 由 `timestamptz` 回改为 `bigint`。依据 = §1.8 实现约定「以**实现现状**为准」，且已核对 `echo-server/src/main/resources/sql/schema.sql`——全库时间列**无一处 `timestamptz`**，`t_account.createTime` 等一律 `bigint`，结论与实现现状一致。§1.8 那段「§1.5 与实现现状不符」的临时说明同步改为正式表述（**问题记录不是规格**）。<br>🔴 **`A7` §4 概述表格行回改为真源口径**：「公开卡**发布后** 7 天…（记得/心意/回响）」→ **自过审时刻 `reviewedAt` 起算 7 天、计入 `R1`–`R5`、`R6`/`R7` 与平台兜底回应不计入**，与 `SPEC-admin-console §2.1.1` 一致。原注记保留作依据与作废留痕。<br>⚠️ **通病提醒**：靠注记覆盖正文的写法不成立——研发读到表格那一行就照着实现，不会往下看注记。 |
| **v0.5 变更** | 🔴 **补 `PRODUCT-MINDMAP §6.2a` 台账 `B12` 判定的规格缺口**（**不是口径冲突，是缺口**）：`SPEC-admin-console §0.2` 指出本规格 §2「只定义了规则与表，没有定义任何 API 路径」，研发照现状开工只能自行发挥。<br>① **分工划线**：端点契约（路径 / 入参出参 / 错误码 / 鉴权 / 幂等）写进 **`API-CONTRACT.md §17`**（依据其自身定位「前后端并行的唯一真源」），**本规格只写流程与落库时机并指向前者**，不两处各写一套。<br>② 🆕 **§2.2 加端点清单速查表**（运营侧 6 条 + 🔴 **作者侧 2 条** —— 后者是 `SPEC-admin-console §6.4` 清单里缺掉的一半，缺则 `TC-MOD-03` 无法实现）。<br>③ 🆕 **§2.2.1 状态迁移合法性封闭表**：明确 `takendown` 不得由审核台直接放行、`overturn` 只回 `pending` 不直接 `public`、软删卡无任何审核动作。<br>④ 🆕 **§2.2.2 三条落库时机**（与既有裁定直接相关）：**「通过」同事务写 `reviewedAt` 且只写一次**（北极星 7 天窗口起点，§1.8.3）· 🔴 **审核动作一律不得改 `originType`**（官方号内容整条不进北极星分母，正向白名单）· **状态变更必落 `t_card_visibility_log` + `t_audit_log` 双流水，同一事务**。<br>⑤ 🆕 **§2.6.1 补申诉五列**：原字段表有 `state='appealing'` 但**无任何字段承载申诉本身**。「一次」以 `appealAt IS NOT NULL` 为唯一判据（**刻意不用计数列**）。<br>⑥ 新增验收 **`TC-MOD-06~10`**。<br>⚠️ **明确未补**（不代拟）：C 端举报提交端点与举报表 / 理由码字典 / `/ops/*`→`/admin/*` 前缀迁移（后者前置条件"待 QA 复签"未满足），逐条理由见 `API-CONTRACT §17.6` |
| **v0.4 变更** | ① 🔴 **`t_resonance_type` 补 `countsToAcceptance` 与 `slug` 两列，并撤销 v0.3「口径绝不入表」那条边界**（顾虑对、结论错，理由见 §1.8.2 顶部的自我推翻说明）。列名与排序侧**收敛成一套**：采纳 `slug`/`name`/`countsToAcceptance`，保留 `targetScope`（与事实表同名，排序侧的 `targetType` 需回改）。<br>② 🔴 **给这一列加硬锁**：触发器**禁 UPDATE 口径列 / 身份列**、**禁 DELETE 整行**（堵"删了再插"的绕过路径）、新增审计流水表 `t_resonance_type_log` 全量留痕。措辞类列（`name`/`status`/`sort`）允许改但留痕。<br>③ 种子数据灌满 **`R1`–`R7`**（`R6`=关注题材 / `R7`=关注 ta，两者 `countsToAcceptance=false`）。<br>④ 🆕 **补 `t_memory_card.originType` + `assistedByOps`**（§1.8.3b）——排序侧与后台侧整套官方号隔离规则此前**无字段可落地**；含 CHECK、索引、改判留痕规则。<br>⑤ 全文术语改名：关系侧「订阅」→「**关注**」（`AD28`：「订阅」专属付费）。<br>⑥ 新增验收 **`TC-CARD-14~18`** |
| 来源 | `OPERATION-GTM-MEMORIAL-ECOSYSTEM.md §10` 运营最小能力清单 |
| 关联 | `DECISIONS.md`(D3/D4/D5/D9/D20/G⁗ 两层和谐、**G⁗″ CM-D1 软删**)、`PRD-echo-social.md §2.1/§2.4/§2.15`、`COPY-GUIDE.md §2.4`、`API-CONTRACT.md`、`ACCEPTANCE.md`、**`SPEC-trust-and-compliance.md §G0-1`（删除语义唯一口径）**、**`SPEC-admin-console.md §2.1.1`（北极星实现口径）/`§10.1b`（本轮字段缺口来源）** |
| **v0.3 变更** | 新增 **§1.8 数据模型补齐**，落地 `SPEC-admin-console §10.1b` 的四项阻塞缺口：🔴 **新表 `t_resonance`**（承载 R1–R7 及**关注转化归因**字段，🔴 归因三列不参与北极星）· 类型字典 `t_resonance_type` · `t_memory_card.reviewedAt`（首次过审时刻，触发器保证只写一次）· `t_account.accountType` · **新表 `t_card_visibility_log`**。均含完整 DDL、索引、外键与不可变约束，新增验收 `TC-CARD-07~13` |

> **上位原则（两层和谐，见 DECISIONS G⁗）**：底=私域"我的它"(接收 AI 抚慰)；皮=共鸣厅(善意观光)。**回忆卡发布到共鸣厅=开窗，永远可选、私密默认**；作者随时可收回；对外**不显数字/排名**；公开内容**必过审核**。本规格三块能力都是这层"皮"的运营基建，绝不冲淡私域主轴。

---

## 1. 回忆卡（Memory Card）

### 1.1 是什么
**回忆卡 = 共鸣厅里可被他人观光的最小分享单元**。它不是新的一套内容体系，而是把用户已有的私域素材（一段记录 / 生命之书里的一页 / 一张明信片 / 一条 AI 近况）**挑一条、封装成可对外呈现的卡片**。内部字段沿用既有 `record/window` 数据，回忆卡只是它们的一个"对外发布态"。

> 🆕 ⚠️ **`OM1` 层级模型（2026-08-25 已定，🔴 模型已定、实现待对齐）** —— `DECISIONS §G⁗⁗⁗⁗ OM1`：
> ① **窗口是容器**：一只宠物一个窗，窗是「它」这个对象的对外门面。
> ② **回忆卡是窗里发出来的一条**：卡属于某个窗，一个窗可以有多条卡。
> ③ 🔴 **共鸣厅流的是卡，不是窗。**
>
> ⚠️ 🔴 **本条只登记模型，不改任何接口或字段定义。** 现有实现与规格**两边都按「共鸣厅流窗口」在跑**（`API-CONTRACT §6` `GET /plaza` 的 item 是 `Window`；`SPEC-recommendation-ranking §12` 明记「`t_memory_card` 不存在，当前『窗口』= `t_pet`」）。改造前须先摸清**前端 / 后端 / 规格**三边现状，🔴 **那是另一条线的活**。
> ⚠️ **本节这段「沿用既有 `record/window` 数据、卡只是它们的对外发布态」的表述，方向与 `OM1` 一致但措辞会被读成「卡就是窗的一个视图」**，与「窗是容器、卡是其中一条」有细微出入；🔴 **本轮刻意不改**，留待三边对齐时一并处理。完整不一致点清单见 `DECISIONS §G⁗⁗⁗⁗` 第三节。

### 1.2 组成（一张卡的内容）
| 元素 | 说明 | 必填 |
|---|---|---|
| 封面 | 1 张图（用户素材或定妆形象） | 是 |
| 标题/一句话 | ≤ 30 字，温柔克制 | 是 |
| 正文 | 一个习惯 / 一个瞬间 / 一段话，≤ 500 字 | 否 |
| 关联的它 | 指向某个 pet（回忆集），显示昵称 | 是 |
| 主题标签 | 从"主题池"选 0–3 个（见 §3） | 否 |
| 可见性 | 私密 / 挚友可见 / 公开（见 1.3） | 是（默认私密） |
| 互动开关 | 是否允许"记得 / 留一束心意 / 回响"（见 1.4） | 默认开，可关 |

> 素材来源必须是用户已建档内容；**发布不改变原素材**，只生成一个引用态卡片。

### 1.3 可见性三档（=D2 定案，直白三档）
| 档 | 谁能看 | 进不进共鸣厅 |
|---|---|---|
| **私密** | 仅本人（+共同守护者） | 否 |
| **挚友可见** | 本人 + 亲友列表授权者 | 否（只在挚友主页/reel 出现） |
| **公开** | 任何人（含游客态） | **是**，且**必须先过审核**（§2） |

- **默认私密**；升到"公开"是一次显式动作，弹一次轻确认（措辞见 COPY-GUIDE），不催、不诱导。
- 公开卡在过审前处于 `pending`，共鸣厅不可见。

### 1.4 作者主权：发布 / 撤回 / 编辑 / 关闭互动 / 删除（状态机）
```
draft(草稿)
  └─发布→ [私密/挚友] active      ┐
  └─发布公开→ pending(待审)        │作者随时可：
        ├─过审→ public(已公开)     ├─ 编辑(公开卡编辑后回 pending 复审)
        ├─驳回→ rejected(可改再报) ├─ 收回可见性(降级为私密) = 立即从共鸣厅消失
        └─运营下架→ takendown      ├─ 关闭互动(保留展示，停止记得/心意/回响)
                                   └─ 删除(软删置位 + 关联互动一并转为不可见/停更，不做数据清理)
```
- **收回/降级/关闭互动/删除 = 即时生效**，共鸣厅、他人已看列表、reel 同步消失或停更。
- **删除的确切含义（`SPEC-trust-and-compliance G0-1` / `DECISIONS CM-D1`）**：置软删标识位 `deletedAt/deletedBy/deleteReason`，**数据留底**；卡片本体与其关联互动（记得 / 心意 / 回响）**一并转为不可见并停止计入**，但**一行都不删**。owner 本人同样不可见（`CM-D11`）；找回走人工客服，无自助入口（`CM-D2`）。

> **⚠️ v0.2 勘误（2026-08-24）**：取代 v0.1 原文「删除(软删 + 关联互动**一并清理**)」。「软删」是对的，「一并清理」字面就是级联清理，与 `DECISIONS CM-D1`「禁止物理删除与级联清理」冲突；且**同一份文档内**与 §1.7 `TC-CARD-03`「即时同步**消失/停更**」两种说法打架（QA 复签报告 不一致-3 / A-3）。意图本是"一并不可见"，现按此改写。
- 作者对每张卡可**独立控制互动**：可只开"记得"、关"回响"等（多维回声作者控制，=GTM §10.4）。

### 1.5 数据字段（新增表 `t_memory_card`）

> ⚠️ **本表还缺四组字段，补齐在 §1.8**（不要只照这张表建库）：`reviewedAt` + 软删三列（§1.8.3）· 🆕 **`originType` + `assistedByOps`**（§1.8.3b，🔴 **官方号隔离的唯一落点**）。

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint PK | |
| ownerId | bigint | 作者（含游客账号） |
| petId | bigint | 关联回忆集 |
| sourceType | text | record / book_page / postcard / echo |
| sourceRef | text | 原素材引用 id |
| coverKey | text | 封面对象存储 key |
| title | text | ≤30 |
| body | text | ≤500，入库前过《温柔词表》 |
| topicIds | jsonb | 主题标签 id 数组（0–3） |
| visibility | text | private / friends / public |
| status | text | draft/active/pending/public/rejected/takendown/deleted |
| interaction | jsonb | `{remember:bool, heart:bool, echo:bool}` 作者互动开关 |
| createdAt / updatedAt / publishedAt | bigint | 🔴 **UTC 毫秒 epoch**（不是 `timestamptz`），与 `schema.sql` 现状及全库其余时间列一致，见 §1.8 实现约定 |

### 1.6 API（遵循 `API-CONTRACT.md` 约定：列表一律 `{items,nextCursor}`）
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/cards` | 新建/发布回忆卡（body 含可见性、互动开关） |
| PATCH | `/cards/:id` | 编辑（公开卡编辑→回 pending）、改可见性、开关互动 |
| DELETE | `/cards/:id` | **软删置位**（`status=deleted` + `deletedAt/deletedBy/deleteReason`），关联互动一并转为不可见/停更；**不做物理删除、不做级联清理**（`SPEC-trust-and-compliance G0-1`） |
| GET | `/cards/mine` | 我的卡（含各状态），`{items,nextCursor}` |
| GET | `/plaza` | 共鸣厅信息流（仅 public 且过审），`{items,nextCursor}`；**不返回精确互动数**，记得只给 `warmthLevel`+`faces`，无 count/rank |

### 1.7 验收（并入 ACCEPTANCE，编号 TC-CARD-xx）
- **TC-CARD-01** 新建卡默认 `private`；不选公开时永不进共鸣厅。
- **TC-CARD-02** 升"公开"须显式确认；确认后 `status=pending`，`/plaza` 查不到。
- **TC-CARD-03** 收回可见性/删除/关闭互动 → 共鸣厅与他人视图**即时**同步消失/停更（**上限 5 秒**，见 `SPEC-trust-and-compliance §CM-G0S S-1`）；删除后**数据仍留底、无物理删除**，逐视图遍历判据以 `ACCEPTANCE §1E TC-EXP-03/04` 为准。
- **TC-CARD-04** 公开卡编辑后自动回 `pending` 复审。
- **TC-CARD-05** `/plaza` 与 `/cards/*` 响应体**不含任何精确互动数字与排名**（记得只暖光+面孔）。
- **TC-CARD-06** 正文/标题入库经《温柔词表》过滤，命中禁用词按替换表处理或退回提示。

---

### 1.8 数据模型补齐（v0.3 新增 · 解 `SPEC-admin-console §10.1b` 的 R-14~R-17）

> **为什么补这四项**：`SPEC-admin-console §2.1.1` 把北极星「被接住的发布率」的口径定死之后，发现本规格缺了**承载它的数据结构**——最要紧的是**根本没有一张表承载 R1–R6 回声**。缺这四项，北极星、深共鸣率、兜底回应触发率、零回应卡占比**四个指标全部无源**。
>
> **实现约定（沿 `echo-server/src/main/resources/sql/schema.sql` 现状，非新立规矩）**：
> - 标识符**双引号 + mixedCase**；主键为**雪花 ID（bigint，应用层赋值，非自增）**；json 以 text 存。
> - ⚠️ **时间列一律 `bigint`（UTC 毫秒 epoch），全库不使用 `timestamptz`**，与现有 `t_account.createTime` 等保持一致。本规格 §1.5 的 `createdAt/updatedAt/publishedAt` **同样是 `bigint` 毫秒**。
>   🔴 **不得两套时间类型并存**——并存会让聚合层每张表都要先判断一次时间列是什么类型，北极星与健康度指标的每一条 SQL 都要为此分叉。
> - 🔴 **一切外键 `ON DELETE RESTRICT`，全库禁止 `ON DELETE CASCADE`**：级联删除直接违反 `DECISIONS CM-D1`「禁止物理删除与级联清理」与 `SPEC-trust-and-compliance G0-1`。删除一律走软删置位。
> - 软删三列统一为 `deletedAt bigint` / `deletedBy bigint` / `deleteReason varchar(64)`（`G0-1`）。
>
> ⚠️ **建表顺序（本节按"重要性"排版，不是按执行顺序，照抄会失败）**：
> `t_account` / `t_topic` / `t_memory_card` → **§1.8.2 `t_resonance_type`（含初始化数据）** → **§1.8.1 `t_resonance`** → §1.8.5 `t_card_visibility_log`。
> `t_resonance` 的 `type` 外键指向字典表，字典表必须先建好并灌入 `R1–R7`；`t_topic` 目前**只在本规格 §3.2 定义、尚未进 `schema.sql`**，`t_resonance_fk_topic` 需等它建好后再加。

---

#### 1.8.1 🔴 `t_resonance` —— 回声表（R-15，最阻塞项）

**承载什么**：一条「某人对某个对象做出的一次共鸣表达」。覆盖 `PRD-RESONANCE-PUBLISHING §4` 的 `R1` 记得 / `R2` 留脚印 / `R3` 留一句话 / `R4` 我也想起一件事 / `R5` 共同留一束心意 / `R6` 关注题材 / `R7` 关注 ta（见 §1.8.2 字典表）。

```sql
-- ---------------------------- 回声（共鸣表达） -------------------------------
CREATE TABLE IF NOT EXISTS "t_resonance" (
    "id"                bigint      NOT NULL,               -- 雪花 ID
    "type"              varchar(16) NOT NULL,               -- R1..R7 / 后续新增类型，见 t_resonance_type
    "targetScope"       varchar(8)  NOT NULL,               -- card | author | topic
    -- ---- 对象（按 targetScope 三选一，由下方 CHECK 约束保证） ----
    "cardId"            bigint,                             -- scope=card：这条回声作用的那张卡
    "targetAuthorId"    bigint,                             -- scope=author：被关注的发布者
    "targetTopicId"     bigint,                             -- scope=topic：被关注的主题/窗口
    -- ---- 关注转化归因（🔴 只服务关注指标，不参与北极星，见下方红线；可空） ----
    "attributedCardId"  bigint,                             -- 触发该次关注的那张卡（"哪张卡带来了这次涨粉"）
    "attributionSource" varchar(24),                        -- 归因方式，如 entry_card / last_view / explicit
    "attributionVer"    varchar(16),                        -- 归因规则版本，便于口径变更后区分历史
    -- ---- 行为主体 ----
    "actorAccountId"    bigint      NOT NULL,
    "actorType"         varchar(8)  NOT NULL,               -- 🔴 无 DEFAULT：写入时必须显式声明（快照）
    -- ---- 载荷与审核 ----
    "payloadRef"        varchar(64),                        -- R3 文本 id / R4 相连卡 id / R5 心意笔数引用
    "moderationStatus"  varchar(16) NOT NULL DEFAULT 'passed',  -- passed | pending | rejected
    "abnormal"          boolean     NOT NULL DEFAULT false, -- 被判异常（刷量/恶意），口径同 S1′
    -- ---- 时间与软删 ----
    "createdAt"         bigint      NOT NULL DEFAULT 0,     -- UTC 毫秒
    "deletedAt"         bigint,
    "deletedBy"         bigint,
    "deleteReason"      varchar(64),
    PRIMARY KEY ("id"),

    -- 🔴 对象完整性：scope 决定哪一列必填，且另两列必须为空（防"既指卡又指作者"的脏数据）
    CONSTRAINT "t_resonance_ck_target" CHECK (
        ("targetScope" = 'card'   AND "cardId"         IS NOT NULL
                                  AND "targetAuthorId" IS NULL AND "targetTopicId" IS NULL)
     OR ("targetScope" = 'author' AND "targetAuthorId" IS NOT NULL
                                  AND "cardId"         IS NULL AND "targetTopicId" IS NULL)
     OR ("targetScope" = 'topic'  AND "targetTopicId"  IS NOT NULL
                                  AND "cardId"         IS NULL AND "targetAuthorId" IS NULL)
    ),
    -- actorType 白名单（三值封闭，新增身份类型需显式改约束——这是刻意的）
    CONSTRAINT "t_resonance_ck_actor_type" CHECK ("actorType" IN ('user','ops','system')),
    CONSTRAINT "t_resonance_ck_scope"      CHECK ("targetScope" IN ('card','author','topic')),
    -- 归因三列同生同灭：有归因卡就必须说清是怎么归的，否则口径无法追溯
    CONSTRAINT "t_resonance_ck_attribution" CHECK (
        ("attributedCardId" IS NULL     AND "attributionSource" IS NULL)
     OR ("attributedCardId" IS NOT NULL AND "attributionSource" IS NOT NULL)
    ),
    -- 🔴 外键一律 RESTRICT，禁止 CASCADE（CM-D1 禁止级联清理）
    CONSTRAINT "t_resonance_fk_card"    FOREIGN KEY ("cardId")
        REFERENCES "t_memory_card" ("id") ON DELETE RESTRICT,
    CONSTRAINT "t_resonance_fk_attr"    FOREIGN KEY ("attributedCardId")
        REFERENCES "t_memory_card" ("id") ON DELETE RESTRICT,
    CONSTRAINT "t_resonance_fk_actor"   FOREIGN KEY ("actorAccountId")
        REFERENCES "t_account" ("id")     ON DELETE RESTRICT,
    CONSTRAINT "t_resonance_fk_author"  FOREIGN KEY ("targetAuthorId")
        REFERENCES "t_account" ("id")     ON DELETE RESTRICT,
    CONSTRAINT "t_resonance_fk_topic"   FOREIGN KEY ("targetTopicId")
        REFERENCES "t_topic" ("id")       ON DELETE RESTRICT,
    CONSTRAINT "t_resonance_fk_type"    FOREIGN KEY ("type")
        REFERENCES "t_resonance_type" ("code") ON DELETE RESTRICT
);
```

##### 🆕 🔴 先读这一条：本字段**不是** `t_audit_log.actorType`（2026-08-25 · `DECISIONS §G⁗⁗⁗⁗″ MOD6`）

🔴 **项目里有两个 `actorType`，取值域不同：**

| | 本表 `t_resonance.actorType` | `t_audit_log.actorType`（`API-CONTRACT §15.4`）|
|---|---|---|
| 取值 | `user` / **`ops`** / `system` | `user` / **`staff`** / `system` |
| 记的是 | **这条回声是谁产生的** | 谁做了这次后台或系统操作 |

⚠️ 🔴 **别顺手把本表的 `ops` 改成 `staff` 去「对齐」** —— 后果不是报错这么简单：`CHECK` 会拒绝写入；而若同时放宽 CHECK 去修好它，🔴 **四个指标的 SQL 里写的是字面量 `'ops'`，改完匹配不到任何行，指标不会报错、只会变成 0**。⚠️ 而「兜底回应触发率恒 0」恰好是 `SPEC-admin-console §2.6` 里「**兜底事实上没运行**」的告警形态 —— 🔴 **一次改名会伪装成一个运营问题，查的人会去查运营。**

📌 **若将来确要统一，须同批改**：本表 CHECK + 🔴 **`t_account.accountType`**（下方触发器要求两者相等，只改一边必然全表写入失败）+ 四个指标 SQL + `TC-CARD-09`/`TC-CARD-10`。🔴 **那是一次数据迁移，不是一次改名。**

##### 🔴 `actorType` 的两条硬约束（写成触发器，不只写在文字里）

`SPEC-admin-console §2.1.1 ③` 要求：`actorType` **写入时从账号类型快照**、**一经写入禁止 UPDATE**。理由是这两件事直接决定北极星能不能被自己刷满：

- **必须快照而不是查询时 join `t_account`**：否则某个员工离职后账号类型被改成 `user`（或反之），**历史北极星会被追溯性改写**，违反「历史数字不得被偷偷改写」。
- **必须禁止 UPDATE**：否则"把一行 `ops` 改成 `user`"就是**一键刷北极星**。

```sql
-- 触发器：① INSERT 时校验 actorType 与账号当时的 accountType 一致（真快照，不是随手填）
--         ② UPDATE 时禁止修改 actorType（历史不可改写）
CREATE OR REPLACE FUNCTION "t_resonance_guard_actor_type"() RETURNS trigger AS $$
DECLARE
    v_account_type varchar(8);
BEGIN
    IF (TG_OP = 'INSERT') THEN
        SELECT "accountType" INTO v_account_type
          FROM "t_account" WHERE "id" = NEW."actorAccountId";
        IF v_account_type IS NULL THEN
            RAISE EXCEPTION 't_resonance: actorAccountId % 不存在，无法快照 actorType',
                            NEW."actorAccountId";
        END IF;
        IF NEW."actorType" <> v_account_type THEN
            RAISE EXCEPTION 't_resonance: actorType(%) 与账号当前 accountType(%) 不一致，'
                            '拒绝写入（必须是真实快照，不允许手填）',
                            NEW."actorType", v_account_type;
        END IF;
        RETURN NEW;
    END IF;

    IF (TG_OP = 'UPDATE') AND (NEW."actorType" IS DISTINCT FROM OLD."actorType") THEN
        RAISE EXCEPTION 't_resonance.actorType 不可变更（% -> %）：'
                        '改它等于篡改北极星，任何修正请软删后重写一行',
                        OLD."actorType", NEW."actorType";
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "t_resonance_trg_actor_type" ON "t_resonance";
CREATE TRIGGER "t_resonance_trg_actor_type"
    BEFORE INSERT OR UPDATE ON "t_resonance"
    FOR EACH ROW EXECUTE FUNCTION "t_resonance_guard_actor_type"();
```

> ⚠️ **实现注意**：`PgRepository` 按实体注解自动建表/补字段，**不会生成 CHECK 约束、外键与触发器**。上述约束必须**由 `schema.sql` 显式建立**并纳入部署流程，否则线上是一张没有任何护栏的裸表。这一条要写进 DEPLOY 检查项。

##### 去重唯一索引（按 scope 分三条 partial unique）

```sql
-- scope=card：同一人对同一张卡的同一类回声只能有一条（防"找朋友刷五种回声"之外的重复计数）
CREATE UNIQUE INDEX IF NOT EXISTS "t_resonance_uk_card_actor_type"
    ON "t_resonance" ("cardId", "actorAccountId", "type")
    WHERE "targetScope" = 'card' AND "deletedAt" IS NULL;

-- scope=author：同一人对同一发布者的同一类互动（如「关注 ta」）只能有一条
CREATE UNIQUE INDEX IF NOT EXISTS "t_resonance_uk_author_actor_type"
    ON "t_resonance" ("targetAuthorId", "actorAccountId", "type")
    WHERE "targetScope" = 'author' AND "deletedAt" IS NULL;

-- scope=topic：同一人对同一主题的同一类互动（R6 持续共鸣）只能有一条
CREATE UNIQUE INDEX IF NOT EXISTS "t_resonance_uk_topic_actor_type"
    ON "t_resonance" ("targetTopicId", "actorAccountId", "type")
    WHERE "targetScope" = 'topic' AND "deletedAt" IS NULL;
```

> **为什么加 `WHERE "deletedAt" IS NULL`**：取消关注 / 取消记得 = **软删**（`G0-1`，不物理删）。带上这个条件，用户「取关后再关注」才能成功写入新行；不带则第二次会撞唯一键。
> 🔴 **随之而来的口径要求（必须写给聚合层）**：一个人对同一对象**取关又关注**会留下**多行**。所以人数类指标一律按 **`COUNT(DISTINCT (对象, actorAccountId))`** 去重，**不能直接 `COUNT(*)`**——否则反复取关关注就能刷数。

##### 查询索引（对准 `SPEC-admin-console §2.1.1` 那两个 CTE）

```sql
-- ① 支撑 caught CTE：JOIN cardId + 过滤 actorType + createdAt 落在 7 天窗口内
--    列序按「等值 → 等值 → 范围」排，让范围条件能用上索引
CREATE INDEX IF NOT EXISTS "t_resonance_idx_card_actor_time"
    ON "t_resonance" ("cardId", "actorType", "createdAt")
    WHERE "deletedAt" IS NULL AND "abnormal" = false AND "moderationStatus" = 'passed';

-- ② 支撑按类型的分层统计（深共鸣率只看 R3/R4；兜底回应触发率只看 ops/system）
CREATE INDEX IF NOT EXISTS "t_resonance_idx_type_time"
    ON "t_resonance" ("type", "createdAt") WHERE "deletedAt" IS NULL;

-- ③ 支撑关注转化归因回溯：某张卡带来了多少次关注（只服务 §2.5 ④-b，不服务北极星）
CREATE INDEX IF NOT EXISTS "t_resonance_idx_attributed_card"
    ON "t_resonance" ("attributedCardId", "type") WHERE "attributedCardId" IS NOT NULL;

-- ⑥ 支撑关注关系的维度去重（净新增 / 取关率 / 30 日回访都按关系对聚合）
CREATE INDEX IF NOT EXISTS "t_resonance_idx_author_actor"
    ON "t_resonance" ("targetAuthorId", "actorAccountId", "createdAt")
    WHERE "targetScope" = 'author';

-- ④ 支撑用户维度查询（客服排障、我的互动列表）
CREATE INDEX IF NOT EXISTS "t_resonance_idx_actor_time"
    ON "t_resonance" ("actorAccountId", "createdAt");

-- ⑤ 支撑发布者维度（关注者列表、被接住的作者）
CREATE INDEX IF NOT EXISTS "t_resonance_idx_author_time"
    ON "t_resonance" ("targetAuthorId", "createdAt") WHERE "targetAuthorId" IS NOT NULL;
```

> **索引 ① 的 partial 条件是刻意的**：北极星只数「有效回声」（未软删、非异常、已过审）。把这三个条件下沉进索引，`caught` CTE 就变成一次纯索引扫描；否则每次都要回表判 `abnormal`/`moderationStatus`。**代价是被判异常的回声查起来慢**——那是运营排查场景，可以慢。
>
> ⚠️ **与上面 `t_memory_card` 索引的区别（别照抄错）**：这里的 partial 谓词**允许**带当前状态，因为回声是聚合当时就落进 `t_metric_daily` 的，而按 `SPEC-admin-console §2.7 约定 9`，**重跑只允许覆盖最近 7 天（迟到事件），7 天以外的历史数字冻结**。
> 🔴 **由此产生一条实现铁律：超过 7 天的历史区间一律读 `t_metric_daily` 的冻结值，不得拿今天的 `t_resonance` 重算**——事后被清掉的脏回声会让重算结果只往"好看"的方向偏，而且没人会发现。

##### 关于「素材/授权外键」这条项目硬约束的适用性

项目已定：**素材与其派生数据之间必须有外键，使用前须能校验授权状态**（`DECISIONS CM-D4/CM-D17`、`SPEC-trust-and-compliance G0-10`）。**`t_resonance` 当前不属于这一类**，理由要说清楚，免得后人以为漏了：

| 回声 | 载荷是什么 | 是否素材派生物 |
|---|---|---|
| `R1` 记得 / `R2` 留脚印 | 一个布尔行为，无内容 | ❌ 否 |
| `R3` 留一句话 | **回应者自己写的**文本 | ❌ 否（不是从作者素材派生出来的）|
| `R4` 我也想起一件事 | `payloadRef` 指向**回应者自己新建的那张卡**，素材与授权归那张卡自己管 | ❌ 否（授权在被指向的 `t_memory_card` 上）|
| `R5` 共同留一束心意 | 心意笔数引用 | ❌ 否 |
| `R6` 关注题材 / `R7` 关注 ta | 关注关系，无内容 | ❌ 否 |

🔴 **但预留一条硬约束**：**若未来回声支持携带素材**（例如"回应里附一张图"），则**必须同时**：① 新增 `materialRef` + `consentRef` 两列并建外键；② 取用前经 `IConsentGate.assertUsable(materialRef, capability)`；③ 纳入 `G0-10 ④` 的日跑核查 SQL。
**并且 `payloadRef` 不得被挪用来指向素材**——它是"同库内业务对象引用"，一旦用它偷偷存素材 key，就绕过了整条授权链。这条要写进 CR 检查点。

##### 🔴 归因三列的用途边界（防回流红线）

`attributedCardId` / `attributionSource` / `attributionVer` 三列的用途是**唯一的**：回答「**哪张卡带来了这次涨粉**」，服务 `SPEC-admin-console §2.5 ④-b` 的**关注曝光转化率**。

🔴 **这三列不参与北极星「被接住的发布率」的任何计算。**
制作人已裁定关注与北极星是**两件事、不揉在一起**（原话：「你把粉丝订阅的单独实现设计，不要跟北极星的相关信息扯上关系不就好了」）。关注（`R6` 关注题材与 `R7` 关注 ta）**不进** `SPEC-admin-console §2.1.1 ⑥` 的 `caught` CTE。
*为什么要专门写这条*：这三列长得**很像**一座能把关注接回北极星的桥——后人看到"关注已经能归因到具体某张卡了"，很容易顺手把它 JOIN 进分子。**建这三列不是为了给北极星留后门**，这句话必须留在表旁边，而不只留在会议记录里。

---

#### 1.8.2 `t_resonance_type` —— 回声类型字典（可扩展性的落点）

**为什么要有这张表**：回声类型会增加（`R7`「关注 ta」就是新增的一类）。如果 `type` 写成 `CHECK (type IN ('R1',...,'R6'))`，那么新增一类互动就要改约束、改枚举、动 DDL。用字典表则**加一行数据即可**。

##### ⚠️ v0.4 的一次自我推翻：`countsToAcceptance` 从"绝不入表"改为"入表 + 加锁"

v0.3 这里写过一条**刻意的设计边界**，原话是「字典表绝不存『这个类型算不算被接住』，因为改一行数据就能改北极星的定义，不留审批痕迹、不进代码评审」。**这条判断的顾虑是对的，但结论是错的，现整条撤销。**

| | v0.3 的做法 | v0.4 的做法 |
|---|---|---|
| 「什么算被接住」存在哪 | 散落在聚合层 SQL 的 `IN ('R1'..'R5')` 里 | 字典表一列 `countsToAcceptance` |
| 改它需要什么 | 改一处 SQL 文件 → 走 CR | 🔴 **数据库直接拒绝**（触发器禁 UPDATE、禁 DELETE）→ 只能新增类型 + 停用旧类型，且留审计流水 |

**为什么反过来更安全**：v0.3 的顾虑是"配置项比代码好改"，但它默认了"改 SQL 一定会被 CR 拦住"——**而聚合 SQL 里一个 `IN` 列表加一个元素，是评审时最容易被放过的一行 diff**。更要紧的是，散落写法**没有唯一真源**：北极星、深共鸣率、零回应卡占比、冷启动毕业判定四处各写一遍白名单，改漏一处就是四个数互相矛盾，而且没人会发现。

落进字典表 + 加硬约束之后，三件事同时成立：① **唯一真源**，四处聚合读同一列；② **可审计**，"什么算被接住"是一行能被 SELECT 出来、能被截图给合规看的数据；③ **比改 SQL 更难改**，因为数据库会拒绝。🔴 **关键在于第③条——没有下面那道锁，v0.3 的顾虑就完全成立，这一列就不该存在。**

##### 列名收敛（两侧原本各叫各的，本节定为唯一一套）

`SPEC-recommendation-ranking` 引用的是 `code / slug / name / targetType / countsToAcceptance`，本规格 v0.3 建的是 `code / label / targetScope / attributable`。**收敛原则：每一列都取"这个名字在本项目别处已经出现过"的那一个**，不折中、不新造。

| 最终列名 | 来自 | 依据 |
|---|---|---|
| `code` | 两侧一致 | 无争议，主键 |
| **`slug`** | 采纳排序侧 | `t_topic` / `t_tag` 都已有 `slug` 列，且它要与埋点事件名（`follow_author`）对齐 |
| **`name`** | 采纳排序侧（弃用本规格的 `label`）| `t_topic { id, name, slug, ... }`、`t_tag { id, dimension, name, slug, ... }` 用的都是 `name`。`label` 在本项目里没有第二处用例 |
| **`targetScope`** | 保留本规格（排序侧的 `targetType` 需回改）| 🔴 **决定性依据**：事实表 `t_resonance` 的列就叫 `targetScope`（§1.8.1）。字典列与事实表列**必须同名**，否则每个写查询的人都要先想一遍"这两个是不是一回事" |
| **`countsToAcceptance`** | 采纳排序侧 | 本规格原本没有这一列（这就是被补的缺口）|
| `attributable` / `status` / `sort` / `createdAt` | 本规格独有 | 排序侧未涉及，无冲突 |

**一句话**：`name`/`slug` 跟字典表的既有惯例走，`targetScope` 跟事实表走，`countsToAcceptance` 照排序侧原名。**唯一需要排序侧回改的是 `targetType` → `targetScope`。**

```sql
-- ------------------------- 回声类型字典（可扩展） ---------------------------
CREATE TABLE IF NOT EXISTS "t_resonance_type" (
    "code"        varchar(16) NOT NULL,        -- R1..R7 / 后续新增（编号由产品分配）
    "slug"        varchar(32) NOT NULL,        -- 机器名，与埋点事件名对齐，如 follow_author
    "name"        varchar(32) NOT NULL,        -- 中文名，如「记得」
    "targetScope" varchar(8)  NOT NULL,        -- 该类型作用于 card | author | topic（与 t_resonance 同名）
    -- 🔴 这一列直接决定北极星分子。无默认值：新增类型必须显式表态，漏写则报错
    "countsToAcceptance" boolean NOT NULL,
    "attributable" boolean    NOT NULL DEFAULT false, -- 是否需要归因到某张卡
    "status"      varchar(8)  NOT NULL DEFAULT 'on',  -- on | off（下线不删行，历史数据还引用着）
    "sort"        integer     NOT NULL DEFAULT 0,
    "createdAt"   bigint      NOT NULL DEFAULT 0,
    PRIMARY KEY ("code"),
    CONSTRAINT "t_resonance_type_uk_slug"  UNIQUE ("slug"),
    CONSTRAINT "t_resonance_type_ck_scope" CHECK ("targetScope" IN ('card','author','topic')),
    CONSTRAINT "t_resonance_type_ck_status" CHECK ("status" IN ('on','off'))
);

-- 种子数据。🔴 countsToAcceptance 必须逐行显式写出，不允许依赖默认值
INSERT INTO "t_resonance_type"
    ("code","slug","name","targetScope","countsToAcceptance","attributable","sort","createdAt") VALUES
    ('R1','remember',      '记得',           'card',  true,  false, 1, 0),
    ('R2','footprint',     '留脚印',         'card',  true,  false, 2, 0),
    ('R3','leave_words',   '留一句话',       'card',  true,  false, 3, 0),
    ('R4','me_too',        '我也想起一件事', 'card',  true,  false, 4, 0),
    ('R5','shared_flower', '共同留一束心意', 'card',  true,  false, 5, 0),
    -- 🔴 R6/R7 是「持续关注」，不是「对某一条发布的表达」→ 不计入被接住
    ('R6','follow_topic',  '关注题材',       'topic', false, true,  6, 0),
    ('R7','follow_author', '关注 ta',        'author',false, true,  7, 0)
ON CONFLICT ("code") DO NOTHING;
```

> **`R1`–`R5` 的 `slug`**：本规格新拟（此前只有 `code`，埋点侧对这五类沿用既有事件名）。若埋点侧已有不同机器名，**以埋点侧为准**改这五个字符串即可——它们不参与任何口径判断，判断一律用 `code` 与 `countsToAcceptance`。
> **`R6`/`R7` 的 `slug`** 则**不可自行更改**：`follow_topic` / `follow_author` 与 `SPEC-recommendation-ranking §10.1` 的埋点事件名是同一个词，改一边就断了。

##### 🔴 防静默修改：一道触发器 + 一张审计流水（不是文字约定）

**要防的是什么**：`UPDATE t_resonance_type SET "countsToAcceptance"=true WHERE code='R7'` —— 一条语句，北极星分子当天变宽，四个指标同时失真，**没有 diff、没有 CR、没有人知道**。

```sql
-- ---------------- 类型字典的变更审计流水（只追加，与审计账本同性质） -------------
CREATE TABLE IF NOT EXISTS "t_resonance_type_log" (
    "id"          bigint      NOT NULL,
    "code"        varchar(16) NOT NULL,
    "action"      varchar(8)  NOT NULL,        -- insert | update
    "beforeRow"   jsonb,                       -- 变更前整行（insert 时为 null）
    "afterRow"    jsonb       NOT NULL,
    "dbUser"      text        NOT NULL,        -- current_user，落库者身份
    "changedAt"   bigint      NOT NULL,
    PRIMARY KEY ("id")
);
CREATE INDEX IF NOT EXISTS "t_resonance_type_log_idx_code_time"
    ON "t_resonance_type_log" ("code", "changedAt");

-- ---------------- 口径列禁改 + 禁删 + 全量留痕 -------------------------------
CREATE OR REPLACE FUNCTION "t_resonance_type_guard"() RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        -- 🔴 必须禁 DELETE：否则「删掉 R7 再以 countsToAcceptance=true 重新 INSERT」
        --    就是一条绕过下面禁改逻辑的完整路径。外键 RESTRICT 只挡"已被引用"的行，
        --    一个还没产生过数据的新类型是删得掉的。
        RAISE EXCEPTION 't_resonance_type 不允许删除行（code=%）：'
                        '类型下线请改 status=''off''，历史数据仍引用着这一行', OLD."code";
    END IF;

    IF TG_OP = 'UPDATE' THEN
        -- 身份列与口径列一律禁改（用 IS DISTINCT FROM，null 安全）
        IF NEW."countsToAcceptance" IS DISTINCT FROM OLD."countsToAcceptance" THEN
            RAISE EXCEPTION 't_resonance_type.countsToAcceptance 不可修改（% : % -> %）：'
                            '它直接决定北极星分子，改它等于改指标定义。'
                            '需要变更口径请新增一个类型并把旧类型 status 置 off，'
                            '让新旧口径在时间轴上可区分，而不是把历史一起改掉',
                            OLD."code", OLD."countsToAcceptance", NEW."countsToAcceptance";
        END IF;
        IF NEW."code" IS DISTINCT FROM OLD."code"
           OR NEW."slug" IS DISTINCT FROM OLD."slug"
           OR NEW."targetScope" IS DISTINCT FROM OLD."targetScope"
           OR NEW."attributable" IS DISTINCT FROM OLD."attributable" THEN
            RAISE EXCEPTION 't_resonance_type 的 code/slug/targetScope/attributable 均不可修改（code=%）：'
                            'slug 与埋点事件名绑定、targetScope 决定去重键，改它们会让历史数据对不上',
                            OLD."code";
        END IF;
        -- 允许改的只有 name（改中文措辞）、status（上下线）、sort（排序），且照样留痕
    END IF;

    INSERT INTO "t_resonance_type_log"
        ("id","code","action","beforeRow","afterRow","dbUser","changedAt")
    VALUES (
        -- 实现侧用雪花 ID；此处示意
        (EXTRACT(EPOCH FROM clock_timestamp()) * 1000)::bigint,
        NEW."code",
        lower(TG_OP),
        CASE WHEN TG_OP = 'UPDATE' THEN to_jsonb(OLD) ELSE NULL END,
        to_jsonb(NEW),
        current_user,
        (EXTRACT(EPOCH FROM clock_timestamp()) * 1000)::bigint
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "trg_t_resonance_type_guard" ON "t_resonance_type";
CREATE TRIGGER "trg_t_resonance_type_guard"
    BEFORE INSERT OR UPDATE OR DELETE ON "t_resonance_type"
    FOR EACH ROW EXECUTE FUNCTION "t_resonance_type_guard"();
```

**为什么是"禁改"而不是"改了记账"**：留痕能事后追责，但**追责的前提是有人去看那张流水表**——而指标注水恰好是那种"没人会去查"的事故（数字变好了，谁会去查为什么）。所以口径列用**硬拒绝**，只有措辞类列（`name`/`status`/`sort`）走"允许改 + 留痕"。

**口径要真的变更时，正确路径是**：新增一个 `code`（如 `R3b`）显式写死它的 `countsToAcceptance`，把旧 `code` 的 `status` 置 `off`。这样**历史数据引用的仍是旧类型、旧口径**，新旧在时间轴上可区分——而 UPDATE 一行会把历史一起改掉，这正是 `SPEC-admin-console §2.7`「历史数字不得被偷偷改写」要禁的事。

🔗 **与聚合层的分工没有变**：`SPEC-admin-console §2.1.1 ⑥` 的白名单**仍然要写**（那是"锁二"）。字典表这一列是**唯一真源**，聚合层负责**显式读它、不用反向条件**。两者不是二选一——字典表管"事实是什么"，聚合层管"怎么正确地用这个事实"。推荐写法：

```sql
-- ✅ 聚合层从字典表取白名单，而不是硬编码，也不是反向条件
AND r."type" IN (SELECT "code" FROM "t_resonance_type" WHERE "countsToAcceptance")
```

---

#### 1.8.3 `t_memory_card` 补字段：`reviewedAt` + 软删三列（R-14）

**`reviewedAt` = 卡片首次进入 `status='public'` 的时刻**，即**内容真正可被他人看见的那一刻**。它是北极星 7 天窗口的**起点**（`SPEC-admin-console §2.1.1 ①`），取代原先的 `publishedAt`——因为卡片压在审核队列里的那段时间对任何人都不可见，**不可能被接住**，用 `publishedAt` 等于把审核积压的时长白扣在产品头上。

```sql
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "reviewedAt"    bigint;      -- 首次过审时刻，只写一次
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "deletedAt"     bigint;
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "deletedBy"     bigint;
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "deleteReason"  varchar(64);

-- 🔴 只写一次、写后不可变（写在触发器里，不靠应用层自觉）
CREATE OR REPLACE FUNCTION "t_memory_card_guard_reviewed_at"() RETURNS trigger AS $$
BEGIN
    -- 用 IS DISTINCT FROM 而不是 <>：否则"把 reviewedAt 改成 NULL"会因三值逻辑而漏过
    IF OLD."reviewedAt" IS NOT NULL
       AND NEW."reviewedAt" IS DISTINCT FROM OLD."reviewedAt" THEN
        RAISE EXCEPTION 't_memory_card.reviewedAt 首次写入后不可变更（% -> %）：'
                        '它是北极星 7 天窗口的起点，改它等于给这张卡续窗口期',
                        OLD."reviewedAt", NEW."reviewedAt";
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "t_memory_card_trg_reviewed_at" ON "t_memory_card";
CREATE TRIGGER "t_memory_card_trg_reviewed_at"
    BEFORE UPDATE ON "t_memory_card"
    FOR EACH ROW EXECUTE FUNCTION "t_memory_card_guard_reviewed_at"();

-- 支撑 eligible_cards CTE：按 reviewedAt 取区间
CREATE INDEX IF NOT EXISTS "t_memory_card_idx_reviewed_at"
    ON "t_memory_card" ("reviewedAt") WHERE "reviewedAt" IS NOT NULL;

CREATE INDEX IF NOT EXISTS "t_memory_card_idx_owner_reviewed"
    ON "t_memory_card" ("ownerId", "reviewedAt") WHERE "reviewedAt" IS NOT NULL;  -- 续发率、作者维度
```

> 🔴 **这两条 partial 索引的谓词只能用 `reviewedAt IS NOT NULL`，不要写进 `visibility='public'`。**
> *为什么*：`visibility` 描述的是**卡片当前的可见性**，而分母问的是**"这张卡当时是否曾公开过"**。按 `SPEC-admin-console §2.1.1 ④③`，一张卡在 7 天窗口**结束之后**才被作者收回，**必须仍然留在历史分母里**；一旦索引谓词带上 `visibility='public'`，这张卡就从索引里消失，**上个月的北极星会在这个月悄悄变高**。窗口内是否撤回，一律由 §1.8.5 的流水表按**时点**判断，**不看当前状态**。
> ⚠️ **`deletedAt IS NULL` 是另一回事，别一起否掉**：按已拍板的 `Q3` 软删口径，软删的卡**本来就要从分子分母同时追溯排除**（那是刻意的）。所以 `deletedAt IS NULL` 出现在**查询**里是对的；只是**不建议写进索引谓词**——口径条件留在 SQL 里可读、可改，焊进索引里就成了隐形口径。

**写入时机（沿 §2.2 审核状态机，只在 `reviewedAt IS NULL` 时写）**：

| 迁移 | 是否写 `reviewedAt` |
|---|---|
| 人工审核**通过** `pending → public` | ✅ 写 |
| 自动预审判**低风险直接放行** `提交 → public`（先发后审）| ✅ 写（**内容此刻已可见，不等后补的人工复核**）|
| 公开卡编辑后复审再过审（`TC-CARD-04`）| ❌ **不写、不刷新**——一张卡一生只有一个 7 天窗口，否则作者靠反复微编辑就能给自己续期 |
| 下架后重新上架 | ❌ 不刷新（同上）|

> 🔴 **`reviewedAt` 与 `publishedAt` 并存、各有其用**，不要合并：`publishedAt` = 作者点发布（用于"作者行为"与审核时长统计），`reviewedAt` = 内容可被看见（用于北极星窗口）。**两者的差值本身就是一个有用的运营指标：审核积压时长。**

---

#### 1.8.3b `t_memory_card` 再补字段：`originType` + `assistedByOps`（🆕 v0.4）

**为什么现在必须补**：`SPEC-recommendation-ranking §5.3` 已裁定内容来源分 `user`（普通用户）与 `official`（官方运营账号，有真人运营接留言），并据此定了一系列隔离规则——🔴 **官方号内容不计入北极星分子分母、不计入分类统计与配比反算、不占冷启动保底位**。但 `originType` **本规格 §1.5 的字段表里没有、`schema.sql` 里也没有**，排序侧与后台侧那一整套隔离规则**目前全部落不了地**。

*为什么不能"先不管，反正官方号内容不多"*：种子期恰恰相反——官方号有 43 条稳定高质量内容，而真人卡还很少。混进同一个口径里，**北极星会被官方号系统性拉高，正好掩盖住"真人发的卡没人理"这件唯一值得看的事**。种子期是这个字段最不能缺的时候。

```sql
-- 内容来源。🔴 无默认值：新增发布路径必须显式声明来源，漏写则报错
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "originType"    varchar(16);
-- 运营协助但署名用户的共创内容（GTM5）。它仍算 user，只是可拆分观测
ALTER TABLE "t_memory_card" ADD COLUMN IF NOT EXISTS "assistedByOps" boolean NOT NULL DEFAULT false;

-- 存量数据回填完成后再置 NOT NULL（分两步，避免锁表期间写入失败）
-- UPDATE "t_memory_card" SET "originType" = 'user' WHERE "originType" IS NULL;
-- ALTER TABLE "t_memory_card" ALTER COLUMN "originType" SET NOT NULL;

ALTER TABLE "t_memory_card" ADD CONSTRAINT "t_memory_card_ck_origin_type"
    CHECK ("originType" IN ('user','official'));

-- 支撑"按来源拆分"的全部口径：北极星分母、官方号零回应率、运营响应率
CREATE INDEX IF NOT EXISTS "t_memory_card_idx_origin_reviewed"
    ON "t_memory_card" ("originType", "reviewedAt") WHERE "reviewedAt" IS NOT NULL;
```

| 值 | 含义 | 计入北极星 | 计入分类统计 / 配比反算 | 产生 R 系列统计 |
|---|---|---|---|---|
| `user` | 普通用户发布（含 `assistedByOps=true` 的运营共创，内容是用户的、运营只是帮了忙）| ✅ | ✅ | ✅ |
| `official` | 官方运营账号发布（**有真人运营在接留言**）| 🔴 **不计入**（分子分母都不进）| 🔴 不计入 | ✅ **要统计，但必须可单独拆分**（回声是真实的，丢掉等于让运营看不见自己做得好不好）|

🔴 **`originType` 一经写入不应改判**——把一张官方号的卡改成 `user`，历史北极星会被追溯性抬高。它没有像 `reviewedAt`/`actorType` 那样加禁改触发器，**原因是运营共创的归属确实可能在发布后被纠正**（`assistedByOps` 的判定会返工）。作为替代：**每次 `originType` 变更必须在 §1.8.5 `t_card_visibility_log` 留一行**（🔄 **`changedRole` 记为 `moderator`**；~~`changeRole` 记为 `ops`~~ ——🔴 **2026-08-25 按 `DECISIONS §G⁗⁗⁗⁗ MOD4` 回改**，两处都错：字段名是 `changedRole` 不是 `changeRole`，取值只能是 `author`/`moderator`/`system`），且**该卡当期指标须走 §2.7 约定 9 的重算流程**——🔴 若该卡的 7 天窗口已在 7 天之外闭合，**历史数字冻结、不得重算**，只在当期修正。
> ⚠️ **这是本节唯一一个"允许改判但要留痕"的字段**，与 `reviewedAt`/`actorType`/`countsToAcceptance` 三个硬禁改字段区别对待。差别在于：那三个的改判**没有任何正当业务场景**，而这一个有。

> 🔴 **2026-08-25 回改说明（`DECISIONS §G⁗⁗⁗⁗ MOD4`）**：上段原写「`changeRole` 记为 `ops`」，🔴 **`ops` 不予采用，改用 `moderator`**。
> **裁定依据**：`t_memory_card.assistedByOps` **已经能区分「运营代发」**这件事。再加一个 `ops` 角色，流水里就会同时存在**两个都表示运营操作的值**（`moderator` 与 `ops`），🔴 **事后分不开**——查一条卡为什么变了，得先猜当时的人按的是哪套语义。
> ⚠️ 🔴 **这条不只是口径分歧，是照原文写就跑不起来**：§1.8.5 的 CHECK 约束为 `CHECK ("changedRole" IN ('author','moderator','system'))`，`ops` **根本写不进去**；而这条 INSERT 与 `originType` 变更**在同一事务里**，结果是**整个改判动作失败**。
> ⚠️ 🔴 **不要用放宽 CHECK 约束的方式"修好"它** —— 那正好制造出上面那个「两套运营语义并存、追溯能力永久损失」的结果。

---

#### 1.8.4 `t_account` 补字段：`accountType`（R-16）

**为什么必须有**：`SPEC-admin-console §2.1.1 ③` 裁定「**平台兜底回应不计入北极星分子**」。没有这个字段，**平台代答与真实用户回应在数据上不可区分**，北极星就成了一个**我们自己就能刷满的数字**——那比没有北极星更危险，因为它会让所有人以为产品在变好。

```sql
ALTER TABLE "t_account" ADD COLUMN IF NOT EXISTS
    "accountType" varchar(8) NOT NULL DEFAULT 'user';

ALTER TABLE "t_account" DROP CONSTRAINT IF EXISTS "t_account_ck_account_type";
ALTER TABLE "t_account" ADD  CONSTRAINT "t_account_ck_account_type"
    CHECK ("accountType" IN ('user','ops','system'));

-- 后台需能一键列出全部非真实用户账号供核查（应当是很短的一张表）
CREATE INDEX IF NOT EXISTS "t_account_idx_account_type"
    ON "t_account" ("accountType") WHERE "accountType" <> 'user';
```

| 取值 | 含义 | 约束 |
|---|---|---|
| `user` | 真实用户（**默认值**，绝大多数）| 计入北极星 |
| `ops` | 运营持有的对外账号 | 🔴 **不计入北极星**，计入「兜底回应触发率」 |
| `system` | 系统生成的虚拟主体 | 同上 |

🔴 **配套治理要求**：
- **默认值方向是刻意的**：`t_account.accountType` 给 `DEFAULT 'user'`（绝大多数账号是真人），而 `t_resonance.actorType` **不给默认值、必须显式写**（让每条新增的回声写入路径都必须声明它是谁产生的，漏写则数据库报错，而不是悄悄落成 `user`）。
- **运营用于对外表达的账号必须标为 `ops`**。用私人账号（`user`）做运营兜底属**违规操作**，记一次违规并进月度稽核报告（`SPEC-admin-console §10.1b R-16`）。
- `accountType` 的变更**属高危操作**：需 `super_admin` 二次审批并写审计。⚠️ 但注意——**改它不会改写历史**，因为 `t_resonance.actorType` 是当时的快照（§1.8.1 触发器保证）。

---

#### 1.8.5 `t_card_visibility_log` —— 可见性变更流水（R-17）

**为什么需要**：北极星要判定「**7 天窗口内**作者是否撤回了可见性」。只看 `t_memory_card` 的**当前**状态无法区分两件事——「窗口内就撤回了」（该整条剔除）和「窗口结束后才撤回」（🔴 **不得影响已闭合的历史数字**）。没有流水表，只能用当前状态近似，结果是**历史北极星被追溯性改写**。

```sql
-- ------------------------ 卡片可见性变更流水 --------------------------------
CREATE TABLE IF NOT EXISTS "t_card_visibility_log" (
    "id"             bigint      NOT NULL,
    "cardId"         bigint      NOT NULL,
    "fromVisibility" varchar(16) NOT NULL,      -- private | friends | public
    "toVisibility"   varchar(16) NOT NULL,
    "fromStatus"     varchar(16),               -- 同时记状态迁移，便于区分"作者撤回"与"运营下架"
    "toStatus"       varchar(16),
    "changedBy"      bigint      NOT NULL,
    "changedRole"    varchar(16) NOT NULL,      -- author | moderator | system
    "reasonCode"     varchar(32),
    "changedAt"      bigint      NOT NULL DEFAULT 0,
    PRIMARY KEY ("id"),
    CONSTRAINT "t_card_visibility_log_ck_role"
        CHECK ("changedRole" IN ('author','moderator','system')),
    CONSTRAINT "t_card_visibility_log_fk_card" FOREIGN KEY ("cardId")
        REFERENCES "t_memory_card" ("id") ON DELETE RESTRICT,
    CONSTRAINT "t_card_visibility_log_fk_actor" FOREIGN KEY ("changedBy")
        REFERENCES "t_account" ("id")     ON DELETE RESTRICT
);

-- 支撑 eligible_cards 里的 NOT EXISTS 子查询（判"窗口内是否降级过"）
CREATE INDEX IF NOT EXISTS "t_card_visibility_log_idx_card_time"
    ON "t_card_visibility_log" ("cardId", "changedAt");

-- 支撑撤回率统计
CREATE INDEX IF NOT EXISTS "t_card_visibility_log_idx_time_to"
    ON "t_card_visibility_log" ("changedAt", "toVisibility");
```

🔴 **只追加、不修改、不删除**（与审计账本同性质）。每一次可见性或状态迁移**都要写一行**，包括系统自动迁移。
> **同时记 `status` 迁移的用处**：`SPEC-admin-console §2.1.1` 要求区分三种情形——① 窗口内撤回可见性（整条剔除）② 窗口内关闭互动（保留分母）③ 运营下架（整条剔除）。只记 `visibility` 分不出 ① 和 ③，而这两者的运营含义完全不同（一个是用户不想要了，一个是我们判它违规）。

---

#### 1.8.6 四项与北极星查询的对应关系（给实现者的速查）

| `SPEC-admin-console §2.1.1` 的 SQL 片段 | 依赖本节的哪一项 |
|---|---|
| `WHERE c."reviewedAt" >= :periodStart AND < :periodEnd` | §1.8.3 `reviewedAt` + 索引 `t_memory_card_idx_reviewed_at` |
| `AND c."deletedAt" IS NULL` | §1.8.3 软删三列 |
| `NOT EXISTS (SELECT 1 FROM t_card_visibility_log ...)` | §1.8.5 整表 + 索引 `..._idx_card_time` |
| `JOIN "t_resonance" r ON r."cardId" = e.card_id` | §1.8.1 整表 + 索引 `t_resonance_idx_card_actor_time` |
| `AND r."type" IN (SELECT code FROM t_resonance_type WHERE "countsToAcceptance")` | §1.8.2 字典表 `countsToAcceptance` 列 + 禁改触发器 |
| `AND r."actorType" = 'user'` | §1.8.1 `actorType` + 触发器 + §1.8.4 `accountType` |
| `AND c."originType" = 'user'` 🆕 | §1.8.3b `originType` + 索引 `t_memory_card_idx_origin_reviewed` |
| `AND r."abnormal" = false AND r."moderationStatus" = 'passed'` | §1.8.1 两列（已下沉进 partial 索引）|
| （无）🔴 **关注不出现在北极星的任何 SQL 里** | §1.8.1 的归因三列**只服务** `SPEC-admin-console §2.5 ④-b` 的关注转化率，见上方防回流红线 |

#### 1.8.7 验收补充（TC-CARD-xx）

- **TC-CARD-07** 公开卡过审瞬间写入 `reviewedAt`；**编辑后复审、下架再上架，`reviewedAt` 都不变**；直接改它会被数据库拒绝。
- **TC-CARD-08** 走"先发后审"放行的卡，`reviewedAt` = **进入 public 的时刻**，不等后补的人工复核。
- **TC-CARD-09** 用 `ops` 账号写一条回声，`t_resonance.actorType` 落为 `ops`；随后把该账号的 `accountType` 改成 `user`，**这条历史回声仍是 `ops`**。
- **TC-CARD-10** 试着 `UPDATE t_resonance SET "actorType"='user'` → **数据库报错拒绝**；试着写一条 `actorType` 与账号类型不符的回声 → **同样被拒**。
- **TC-CARD-11** 同一人对同一张卡重复"记得" → 只有一行；取消后再"记得" → 新增一行（旧行软删），且人数统计**仍只算一个人**。
- **TC-CARD-12** 每次可见性/状态迁移都在 `t_card_visibility_log` 留一行；作者撤回与运营下架**可区分**。
- **TC-CARD-13** 删除一张有回声的卡 → **数据库不允许物理删除**（外键 RESTRICT），只能软删；软删后卡与其回声一并转为不可见，**一行都没被删掉**。
- 🆕 **TC-CARD-14 「什么算被接住」改不动**（§1.8.2 · 本轮重点）
  - 【怎么操作】① `UPDATE t_resonance_type SET "countsToAcceptance"=true WHERE code='R7'`；② 换个花样：`UPDATE ... SET "countsToAcceptance"=true WHERE code IN ('R6','R7')`；③ 试着改 `slug`、改 `targetScope`；④ 试着改 `name`（把「记得」改成「记住」）与 `status`（置 `off`）。
  - 【预期】①②③ **全部被数据库拒绝并报错**，报错信息里说清"改它等于改指标定义、请新增类型 + 停用旧类型"；④ **允许**，但 `t_resonance_type_log` 里各留一行，含变更前后整行与 `current_user`。
- 🆕 **TC-CARD-15 删了再插这条后门也被堵住**（§1.8.2）
  - 【怎么操作】找一个**还没产生任何回声**的类型（外键 RESTRICT 挡不住它），`DELETE FROM t_resonance_type WHERE code='R7'`，再以 `countsToAcceptance=true` 重新 `INSERT` 同一个 `code`。
  - 【预期】**DELETE 这一步就被拒绝**。这条要单独测——只禁 UPDATE 的话，"删了再插"是一条完整的绕过路径，而且外键 RESTRICT 只保护已被引用的行，保护不了新类型。
- 🆕 **TC-CARD-16 种子数据的口径位是对的**（§1.8.2）
  - 【预期】`SELECT code FROM t_resonance_type WHERE "countsToAcceptance"` 返回**恰好 `R1`–`R5` 五行**；`R6`/`R7` 为 `false`；`R6.targetScope='topic'`、`R7.targetScope='author'`、其余为 `card`；`R6.slug='follow_topic'`、`R7.slug='follow_author'`。另：试着插一个不写 `countsToAcceptance` 的新类型 → **报错**（无默认值，必须表态）。
- 🆕 **TC-CARD-17 官方号内容不混进真人口径**（§1.8.3b）
  - 【怎么操作】用官方运营账号发一张卡并让它过审、被真实用户接住；同期另有一张真人卡也被接住。分别看北极星、深共鸣率、零回应卡占比、分类统计。
  - 【预期】官方号那张卡**分子分母都不出现**（不是只从分子剔掉）；真人那张正常计入；官方号的回声**仍然被统计**，但只出现在 `SPEC-admin-console §2.6` 的官方号专属指标里。再试着不写 `originType` 直接发布 → **报错**（无默认值）。
- 🆕 **TC-CARD-18 `originType` 改判要留痕且不追溯改历史**（§1.8.3b）
  - 【怎么操作】把一张已过审卡的 `originType` 从 `official` 改成 `user`，分两种情形：① 它的 7 天窗口**还在 7 天内**；② 窗口已在两个月前闭合。
  - 【预期】两种情形都在 `t_card_visibility_log` 留一行（`changeRole='ops'`）；情形 ① 当期指标重算、该卡进入分母；情形 ② 🔴 **两个月前的历史数字一动不动**（§2.7 约定 9：7 天以外冻结），只在当期体现修正。

---

## 2. 运营审核后台（Moderation Console）

### 2.1 为什么必需
公开共鸣厅内容面向陌生人（含游客），**上线前合规硬性要求**：AI 生成内容 + UGC 都要可审、可下架、可留痕。这是公开层不能省的基建。

### 2.2 审核队列 & 状态机
```
提交公开 → 自动预审(机器:内容安全K + 词表 + 未成年人/敏感物识别)
   ├─低风险→ 直接 public（可配置为"先发后审"或"先审后发"）
   ├─中风险→ 进人工队列 pending
   └─高风险→ 直接 blocked，进人工队列并标红
人工：通过(public) / 驳回(rejected，带理由回作者) / 下架(takendown) / 升级(标记复核)
作者：对驳回/下架可**申诉一次** → appeal 队列
```
> **先审后发 vs 先发后审**：默认**先审后发**（种子期量小、稳）；量起来后可对"低风险 + 老作者"放开"先发后审"，由后台开关配置，无需发版。

> 🔴 **API 路径见 `API-CONTRACT.md §17`（唯一真源）· v0.5 新增**
> **背景**：`SPEC-admin-console §0.2` 核实指出「审核队列 REST 路径：本规格**只定义了规则与表，没有定义任何 API 路径**（只有 §3.5 的 `/ops/topics`、`/ops/curations`）」，登记为 `PRODUCT-MINDMAP §6.2a` 台账 **B12**，判定为**规格缺口而非口径冲突**。缺口已补。
> **分工（不两处各写一套）**：端点契约（路径 / 方法 / 入参出参 / 错误码 / 鉴权 / 幂等）写在 `API-CONTRACT.md §17` —— 依据是该文档自身定位「**前后端并行的唯一真源**」；**本节只写流程、状态迁移合法性与落库时机**，并指向前者。后台版面与角色权限链见 `SPEC-admin-console §4.3` / `§6.4`。
> **端点清单速查**（详情一律看 `API-CONTRACT §17`，此处不重复参数）：
>
> | 侧 | 端点 | 对应本节的哪个动作 |
> |---|---|---|
> | 运营 | `GET /admin/moderation/queue` · `GET /admin/moderation/:id` | 队列与详情（四 tab：待处理 / 高风险 / 申诉 / 已处置）|
> | 运营 | `POST /admin/moderation/:id/handle` | 人工四动作：通过 / 驳回 / 下架 / 升级复核 |
> | 运营 | `POST /admin/appeals/:id/handle` | 申诉处置（🔴 仅审核主管，见 §2.5）|
> | 运营 | `GET /admin/reports` | 举报列表（支撑 §4 举报率）|
> | 运营 | `PATCH /admin/moderation/settings` | 先审后发 / 先发后审开关（🔴 `TC-MOD-05` 依赖它）|
> | **作者** | `GET /cards/:id/moderation` | 看驳回理由（🔴 `TC-MOD-03` 依赖它）|
> | **作者** | `POST /cards/:id/appeal` | 申诉，🔴 **一张卡一生只有一次** |
>
> ⚠️ **作者侧那两条是 `SPEC-admin-console §6.4` 清单里缺掉的一半**——它只列了运营侧四条。但本节状态机里明明有作者的两个动作，缺 C 端端点则 `TC-MOD-03`「驳回带理由码回作者；作者可申诉一次」无法实现。
> ⚠️ **未补的三项**（不代拟，留待派单）：C 端**举报提交**端点与举报表 / 理由码字典 / `/ops/*` → `/admin/*` 前缀迁移。原因逐条见 `API-CONTRACT §17.6`。

#### 2.2.1 🆕 状态迁移合法性（v0.5 · 服务端校验，不信任前端）

上面的流程图给的是"正常路径"，实现还需要一张**封闭**的迁移表——否则「已下架的卡再点通过」这类调用只能靠开发临场判断。

| 当前 `status` | 允许的动作 | 迁移到 | 不允许的（返回 `3412` `moderation_state_conflict`）|
|---|---|---|---|
| `pending` | 通过 / 驳回 / 升级复核 | `public` / `rejected` / `pending`（标记复核，状态不变）| 下架（还没公开过，无从下架）|
| `blocked` | 通过 / 驳回 / 升级复核 | 同上 | 同上 |
| `public` | 下架 / 升级复核 | `takendown` | 通过（已经是通过态）、驳回 |
| `rejected` | **作者申诉**（一次）| `appealing` | 运营再驳回 |
| `takendown` | **作者申诉**（一次）| `appealing` | 通过（🔴 下架卡不得由审核台直接放行，必须经申诉 `overturn` 回 `pending` 重走人工）|
| `appealing` | 维持原处置 / 撤销原处置 | 保持原状态 / 回 `pending` | 直接放行到 `public` |
| `deleted`（软删）| 🔴 **无任何审核动作** | — | 全部。软删后卡与其互动一并不可见（§1.4），审核台不应再看到它 |

🔴 **`overturn`（撤销原处置）只回 `pending`，不直接放行。** 撤销的含义是"原处置有问题，重新判一次"，不是"改判为通过"——直接放行会让申诉变成一条绕过人工审核的通道。

#### 2.2.2 🆕 落库时机（v0.5 · 三条与已有裁定直接相关，最容易踩）

| # | 约束 | 依据 |
|---|---|---|
| **1** 🔴 | **「通过」动作必须在同一事务内写 `t_memory_card.reviewedAt`**，且**只在 `reviewedAt IS NULL` 时写**。它是北极星「被接住的发布率」7 天窗口的**起点**（不是 `publishedAt`）。**编辑后复审、下架再上架一律不刷新**——否则作者靠反复微编辑就能给自己续窗口期；数据库触发器会直接拒绝改写。完整写入时机表见 §1.8.3 | §1.8.3 · `SPEC-admin-console §2.1.1 ①` · `DECISIONS RK-D` |
| **2** 🔴 | **审核动作一律不得写、不得改 `originType`。** 该字段在**发布时**由发布路径显式落库（无默认值 + `CHECK IN ('user','official')`）。官方号内容**整条不进北极星分母**（正向白名单 `originType='user'`，🔴 **不是"只从分子剔掉"**）。审核台改判来源 = 追溯性改写历史北极星。§1.8.3b 允许的那种改判走的是**运营纠正流程 + `t_card_visibility_log` 留痕 + §2.7 约定 9 重算**，**不是审核动作** | §1.8.3b · `SPEC-recommendation-ranking §11.1` / `RK35 ②` |
| **3** 🔴 | **每次审核状态变更落两处流水，同一事务**：① `t_card_visibility_log` 一行（`changedRole='moderator'`，**同时记 `visibility` 与 `status` 迁移**——只记 `visibility` 分不出「作者撤回」与「运营下架」，而这两者运营含义完全不同）；② `t_audit_log` 一行（`action` 取值见 `API-CONTRACT §17.5` 的六个增量）。这就是 §2.4「每个处置留痕」的可实现形态 | §1.8.5 · §2.4 · `API-CONTRACT §15.4` |

> **为什么强调"同一事务"**：这三件事分开写，会出现「卡已公开但北极星窗口没起算」或「公开了但没留痕」。这两种不一致**事后都修不回来**——`reviewedAt` 有禁改触发器，流水表只追加。

### 2.3 审核动作 & 分级
| 风险 | 触发 | 处置 |
|---|---|---|
| 自动·低 | 全项通过 | 放行（按开关先发/先审） |
| 自动·中 | 词表命中可替换 / 疑似敏感 | 入人工队列 |
| 自动·高 | 命中内容安全红线 / 涉政涉黄涉恐 / 疑似真人未授权肖像 | 拦截 + 人工 + 留痕 |
| 人工 | — | 通过 / 驳回(选理由码) / 下架 / 升级复核 |

### 2.4 SLA & 敏感内容 SOP
- 人工队列 **SLA ≤ 4h**（种子期）；高风险 **≤ 1h**。
- 敏感内容（涉逝者的人、疾病、事故等）走**额外情感安全审**：只判"是否被围观/被消费/违规"，不做情绪加工（对齐 COPY-GUIDE 情感安全清单）。
- 每个处置**留痕**：谁、何时、动作、理由码、快照。

### 2.5 权限角色
| 角色 | 权限 |
|---|---|
| 审核员 | 看队列、通过/驳回/下架、写理由 |
| 审核主管 | + 处理申诉、配置先发/先审开关、看留痕报表 |
| 只读运营 | 看队列与报表，不可处置 |

### 2.6 数据字段（新增表 `t_moderation`）
`{ id, cardId, submitBy, autoRiskLevel, autoSignals(jsonb), state(auto_pass/pending/blocked/approved/rejected/takendown/appealing), handledBy, reasonCode, note, snapshot(jsonb), createdAt, handledAt }`

#### 2.6.1 🆕 申诉相关字段（v0.5 · 补齐「申诉一次」的落点）

原字段表有 `state='appealing'` 这个取值，**但没有任何字段承载申诉本身**——申诉文本存哪、什么时候申诉的、"一次"这个上限靠什么判定，全都没有落点。补五列：

| 字段 | 类型 | 说明 |
|---|---|---|
| `appealText` | varchar(200) | 作者的申诉说明（≤200 字，入库前过《温柔词表》，同 `TC-CARD-06` 口径）|
| `appealAt` | bigint | 申诉提交时刻（UTC 毫秒）。🔴 **非空即视为"这张卡的申诉机会已用掉"** |
| `appealHandledBy` | bigint | 处置人（须为审核主管，§2.5）|
| `appealHandledAt` | bigint | 处置时刻 |
| `appealResult` | varchar(16) | `uphold`（维持原处置）/ `overturn`（撤销，回 `pending` 重走人工）|

🔴 **「一次」怎么保证**：以 `appealAt IS NOT NULL` 为唯一判据，**不用计数列**。计数列会诱导后人写 `appealCount < 3` 之类的放宽；一个时间戳只能从"空"变成"有值"，语义上就没有"再来一次"的位置。
🔴 **`appealAt` 一经写入不可变更**（与 `reviewedAt` 同性质，建议同样加禁改触发器）——允许改它等于允许把申诉机会退回给作者，那就不是"一次"了。
⚠️ **时间列一律 `bigint`（UTC 毫秒）**，沿 §1.8 实现约定，不用 `timestamptz`。

### 2.7 验收（TC-MOD-xx）
- **TC-MOD-01** 公开卡未过审时 `/plaza` 不可见。
- **TC-MOD-02** 高风险自动拦截并进人工队列、标红、留痕。
- **TC-MOD-03** 驳回带理由码回作者；作者可申诉一次。（🆕 v0.5：端点为 `GET /cards/:id/moderation` + `POST /cards/:id/appeal`，见 `API-CONTRACT §17.2`）
- **TC-MOD-04** 下架即时从共鸣厅消失；处置有留痕快照。
- **TC-MOD-05** "先发后审/先审后发"开关后台可切，无需发版。（🆕 v0.5：端点为 `PATCH /admin/moderation/settings`）
- 🆕 **TC-MOD-06 过审瞬间写 `reviewedAt`，且只写一次**（§2.2.2 第 1 条）
  - 【怎么操作】① 一张 `pending` 卡走「通过」→ 看 `reviewedAt`；② 作者编辑该卡使其回 `pending`，再次「通过」；③ 把它下架再重新走一遍上架。
  - 【预期】① 写入且等于过审时刻，接口出参回显同一个值；②③ **`reviewedAt` 一动不动**；直接 `UPDATE` 它 → **数据库报错拒绝**。
- 🆕 **TC-MOD-07 审核动作改不了内容来源**（§2.2.2 第 2 条）
  - 【怎么操作】拿一张 `originType='official'` 的官方号卡走完整审核流程（通过 / 下架 / 申诉 `overturn`）。
  - 【预期】全程 `originType` 不变；审核接口**不提供**修改入口（传了也不生效）；该卡在北极星里**分子分母都不出现**（不是只从分子剔掉）。
- 🆕 **TC-MOD-08 一张卡只能申诉一次**（§2.6.1）
  - 【怎么操作】对一张 `rejected` 卡申诉 → 主管处置 `uphold` → 作者再申诉一次；另换一张 `takendown` 卡申诉 → 主管 `overturn` → 卡回 `pending` → 作者再申诉。
  - 【预期】两种情形的**第二次申诉都被拒绝**（`3410` + 温柔文案，非裸错误码）；`appealable=false` 时前端不出现申诉入口；`overturn` 让卡回 `pending` 而**不是直接 `public`**。
- 🆕 **TC-MOD-09 每次处置都有双流水，且同一事务**（§2.2.2 第 3 条）
  - 【怎么操作】做一次「通过」、一次「下架」；然后人为让第二处流水写入失败（如临时约束冲突）。
  - 【预期】正常情形下 `t_card_visibility_log` 与 `t_audit_log` **各留一行**，前者 `changedRole='moderator'` 且 `status` 迁移可读、能与「作者撤回」区分开；失败情形下**整个处置回滚**——不允许出现"卡状态变了但没留痕"或"公开了但 `reviewedAt` 没写"。
- 🆕 **TC-MOD-10 非法状态迁移被服务端拒绝**（§2.2.1）
  - 【怎么操作】对 `takendown` 卡直接调「通过」；对 `pending` 卡调「下架」；对已软删的卡调任意审核动作。
  - 【预期】三者**全部返回 `3412`**（`moderation_state_conflict`），且**不产生任何流水行**。软删卡根本不应出现在队列里。

---

## 3. 精选 + 主题池（免发版运营配置）

### 3.1 目标
运营能**不发版**地配置：首页/共鸣厅的**精选位**、**主题池**（主题周、栏目），以及"今日一处"。对齐 GTM §5.2 栏目与 §10.7。

### 3.2 模型
- **主题池 `t_topic`**：`{ id, name, slug, desc, coverKey, status(on/off), sort, startAt, endAt }`。栏目如《它总会这样》《窗边的那一刻》即主题。
- **精选位 `t_curation`**：`{ id, slot(home_hero/plaza_top/topic_of_week/today_one), refType(card/topic), refId, sort, status, startAt, endAt, operator }`。运营手动挑卡/主题挂到某个位。

### 3.3 配置后台交互
- 主题池：增/改/上下线/排序/定档期（到期自动下线）。
- 精选位：从"已过审公开卡"里搜/挑 → 挂到指定 slot → 排序 → 定档期 → 预览 → 发布。**即时生效、无需发版**。
- 所有精选/主题变更**留操作人 + 时间**。

### 3.4 排序与"今日一处"
- 共鸣厅默认排序 = **以"被接住率/健康度"为优化目标的个性化**（CM1，见 `PRD-echo-social §2.14`），叠加运营精选置顶；**停留信号仅作弱信号/负向护栏，不作最大化目标**。
- "今日一处" = 每日给用户**一处**值得驻足的卡/主题（运营可指定 or 系统按共鸣相似度+健康度选），克制、不刷屏。

### 3.5 API
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/plaza/curated` | 前台读当前精选 + 主题（合并进共鸣厅顶部） |
| GET/POST/PATCH | `/ops/topics`、`/ops/curations` | 运营后台配置（鉴权：运营角色） |

### 3.6 验收（TC-CUR-xx）
- **TC-CUR-01** 运营挂精选/改主题 → 前台**即时**变化，无发版。
- **TC-CUR-02** 主题/精选到期自动下线。
- **TC-CUR-03** 精选只能挑**已过审公开卡**；被作者收回/下架的卡自动从精选移除。
- **TC-CUR-04** 前台精选/主题呈现**不含热度/排名/精确互动数**。

---

## 4. 后台运营指标（北极星 + 健康度）

> **⚠️ 2026-08-24 归口**：本节的内容健康度指标、`§2` 审核后台、`§3` 精选/主题配置，连同制作人新增的「新增/活跃/付费」看板，已统一归入 **`SPEC-admin-console.md`**（一个后台四模块，共用鉴权/角色/审计/数据基座）。
> 本节口径**不变、仍为真源**；`SPEC-admin-console` 只负责把它挂进同一个后台壳子并统一权限与审计，不重复定义。北极星「被接住的发布率」在概览页**独占首行，位于新增/活跃/付费之上**。

> **⚠️ v0.3 补充（v0.6 已据此回改下表原文）：北极星的口径真源已迁移。** 可实现的完整口径（窗口起点 = `reviewedAt`、计入哪几类回声、平台兜底不计入、撤回三种情形、可执行 SQL）**唯一定义在 `SPEC-admin-console §2.1.1`**（该节已定稿，无待定项）。两者若有分歧，**以 `§2.1.1` 为准**。
> 🔴 **v0.6 变更**：下表原写的 v0.1 概述（「公开卡**发布后** 7 天内获 ≥1 条合规回声（记得/心意/回响）」）**已就地改写为真源口径**，不再只靠本注记覆盖。作废的旧表述与作废原因见此处——**起点由「发布」改为「过审」**（`reviewedAt`），**范围由笼统的「记得/心意/回响」收敛为 `R1`–`R5` 且兜底回应不计入**。<br>理由：注记压不住正文。研发读到表格那一行就会照着实现，不会往下看注记。
> 🔴 **关注（`R6` 关注题材 / `R7` 关注 ta）不计入本指标**，它有自己的一组指标（`SPEC-admin-console §2.5 ④-b`）。承载字段见 §1.8。

| 指标 | 定义（完整口径以 `SPEC-admin-console §2.1.1` 为准） | 来源 |
|---|---|---|
| **被接住的发布率**（北极星） | 公开卡**自过审时刻 `reviewedAt` 起算** 7 天内获 ≥1 条合规回声，且作者未撤回/关互动 的占比。🔴 **起点是过审、不是发布**（压在审核队列里的时间对任何人都不可见，不可能被接住）；计入 **`R1`–`R5`**，🔴 **`R6`/`R7` 关注不计入**（是关系行为，不是对这张卡的回应），🔴 **平台兜底回应不计入**（自己给的，计入即自欺） | 卡状态（`reviewedAt`，§1.8.3）+ `t_resonance`（§1.8.1），白名单取自 `t_resonance_type.countsToAcceptance`（§1.8.2）|
| 撤回率 | 发布后被降级/删除的占比 | 状态机 |
| 举报率 | 被举报卡 / 公开卡 | 举报表 |
| 续发率 | "被接住"的作者 14 天内再次发布的占比 | 作者维度 |

- 埋点：发布、过审、首个回声到达、撤回、举报、再发布。**这些数据仅后台/运营可见，永不对 C 端公开**（=GTM §10.5 / D4）。

---

## 5. 红线复述（实现必须遵守）
1. 发布永远**可选、默认私密**；私域核心不发布也完全可用。
2. 对 C 端**不显精确互动数、不排名、不做热度榜**（记得=暖光+面孔）。
3. 公开内容**必过审**；AI 生成内容带**诚实标识**（CR2）。
4. **绝不把任一段纪念内容本体锁进付费墙**；共鸣厅内**零交易**（CR-M 护栏）。
5. 献花对外称**"留一束心意"**、不加宠物温度、不给作者分成（D3/D5/E4/CR4）。
6. 敏感内容走额外情感安全审；处置全程留痕。
