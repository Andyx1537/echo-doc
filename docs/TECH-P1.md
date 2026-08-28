# 回响 (Echo) · P1 社区基座 技术方案纲要

> 配套文档：[`PRD.md`](./PRD.md)（需求，v0.2 已锁定）。本文是 **P1 社区基座**的技术落地纲要，作为委派给引擎/前端 agent 的依据。
> 服务端 = **Aengine 引擎支援**（Java26 / Netty / 缓存仓储 / event / scheduler / protobuf），业务在独立工程 `Echo/echo-server`。客户端 = **Unity（先 H5/WebGL）**。
> **数据库 = 单库 PostgreSQL（含 pgvector）**：关系实体 + 向量同库。详见 §2 决策 DB'。

> ⚠️ **阅读须知（2026-08-25 加注 · 时间线错位）**：本文写于**「回声·往宠」战略转向之前**，其「P1/P2/P3」分期沿用的是**旧的意识空间/对赌养成路线**，🔴 **与现行分期不对应**。<br>**现行口径**：**宠物建档是 MVP / P0 核心**，不是 P2 —— 私域「我的它」为情绪价值本体与留存命根（`DECISIONS.md §G⁗ 两层和谐模型`「底 · 核心（私域）」），AI 宠物近况为 **P0 私域核心能力**（`DECISIONS.md CR1`、`CM2`），建档四步流程与 AI 识别均已定案（`B2`–`B4`）并已有实现契约（`API-CONTRACT.md §2`、`AI-CAPABILITIES.md`）。<br>**本文的处置**：**保留不删**，作为「意识空间 / 共鸣匹配 / 定势空间」这条远期蓝图的技术纲要（同 `PRD.md` 顶部横幅的处置方式，`DECISIONS.md §I-3`）。🔴 **读本文的分期编号时，一律以 `DECISIONS.md` 为准**；本文的技术选型（Aengine 依托、单库 PostgreSQL + pgvector、`com.echo.*` 包根、独立 Maven 工程）仍然有效，**错位的只是范围与排期**。

---

## 0. P1 范围回顾（已锁定）
账号/形象 + 意识档案(LLM 补全 + 个人向量) + 定势空间 + 共鸣匹配 + **异步回声** + 手势/留痕/好友 + 摊位占位。
**不含**：对赌结算(P3)、~~宠物(P2)~~、实时在场(后置)。

> 🔴 **2026-08-25 勘误**：「宠物(P2)」这一句**已失效**。宠物在现行路线里是 **MVP / P0 核心**（见文首阅读须知与 `DECISIONS.md §G⁗`、`CR1`、`B2`–`B4`），不是被排除在本阶段之外的后置项。原文划线保留以追溯这份纲要的历史范围假设。

---

## 1. 系统拆分（P1）

| 子系统 | 职责 | Aengine 依托 | 归属 agent |
|---|---|---|---|
| Gateway/会话 | 连接、登录、会话态、协议分发 | `WebSocketServer` + `PacketHandlerManager` + `PlayerSessionManager` 子类 | 引擎 |
| Account/Avatar | 账号、形象、资料卡 | `CachedPgRepository`(自写) + Aengine 实体注解 | 引擎 |
| MindProfile | 偏好录入、LLM 补全、向量生成/存储 | `util.Http`(调 LLM) + pgvector + repo | 引擎 |
| Space | 定势组合拼装、空间实例持久化、主控配置 | `template`(定势配置表) + repo | 引擎 |
| Resonance | 向量相似度检索、共鸣候选 | pgvector(同库) + `cache` | 引擎 |
| Echo | 回声快照生成/读取/留痕 | repo + `scheduler`(过期清理) | 引擎 |
| Social | 好友/关注/共鸣记录、摊位占位 | repo | 引擎 |
| LLM/Vector 适配 | LLM 调用与向量编码的抽象与实现 | 新增 `ILlmClient` / `IVectorStore` | 引擎 |
| Client | H5(WebGL) 渲染、视角、偏好录入 UI、回声呈现 | Unity | 前端 |

> 落地包根：服务端业务放 `com.echo.*`（独立于引擎 `com.aengine.*`），作为**独立 Maven 工程 `Echo/echo-server`** 依赖 Aengine（已 `mvn install` 到本地仓库）。不修改 Aengine 源码。

> **引擎接线实况（BE-1 实测，纠正纲要早期假设）**：
> - `WebSocketServer / PacketHandlerManager / PlayerSession` 三者通过 `IEventListener` 解耦：需子类化 `PlayerSessionManager<K>`（如 `EchoSessionManager extends PlayerSessionManager<Long>`，实现 `offline(K)`），用 `server.register(sessionManager)` 注册；它负责建 `PlayerSession` 并把包投递给 `PacketHandlerManager.forward(...)`。
> - `PacketHandlerManager` 构造需 `RedisLockSupport`；未接 Redis 期用占位实现（`NoOpRedisLockSupport`），接 Redis 后替换为引擎 Jedis 锁。
> - `WebSocketServer.start()` 为空实现，真正监听在 `bind(ip,port)`；仍按约定 bind 后调用 start。
> - 注意 `PlayerSession` 身份方法命名：getter `getIdentity()` 与覆写父类的 `getIdenty()`（少个 i）并存，调用时勿混淆。

---

## 2. 数据模型（Aengine 实体注解 + 单库 PostgreSQL）

> **决策 DB'（已拍板）：单库 PostgreSQL（含 pgvector），不用 MySQL。**
> 原因：Aengine 的 `JDBCRepository` 写死 MySQL 方言（反引号 / `SHOW TABLES` / `INSERT...VALUE` / `MODIFY COLUMN` / `COMMENT=`），在"不改引擎"前提下无法跑 Postgres。但 Aengine 的**注解元数据层与缓存层 `CachedRepository` 是方言无关、可原样复用**的。
> 落地方式：echo-server 内自写 `com.echo.infra.persistence`：
> - `PgDb`：HikariCP + postgresql 连接池（可"不连库也能启动"开关）。
> - `PgRepository<T> implements IRepository<T>`：PostgreSQL 方言 CRUD + 自动建表（双引号标识符、`information_schema` 探测、`VALUES`、TypeEnum→PG 类型映射；主键用应用层雪花 id、非自增）。
> - `CachedPgRepository<T> extends PgRepository<T>`：镜像 `CachedJDBCRepository`，组合复用 Aengine 的 `CachedRepository<T>` + `ReferenceCountedLockManager`。
> - 向量：`SelfVector` 的向量列用 pgvector `vector` 类型，由 `IVectorStore` 通道处理（与关系数据同库）。

> 全部 `implements AbstractEntity`，用 `@Table/@Column/@Pk/@Index/@Cache`；ID 用雪花 `IDGenerator`；仓储 `extends CachedPgRepository<T>`。

| 实体 | 关键字段（草案） | 缓存/索引 |
|---|---|---|
| `Account` | id(pk), openId, status, createTime | idx(openId) |
| `Avatar` | id(pk), accountId, parts(json), fashionSlots(json), updateTime | idx(accountId) |
| `MindProfile` | id(pk), accountId, rawPrefs(json), enrichedPrefs(json), vectorId, version | idx(accountId) |
| `SelfVector` | id(pk), accountId, dim, vectorRef(外部库key), normHash | idx(accountId) |
| `MindSpace` | id(pk), accountId, presetSetId, dynamicParams(json), hostConfig(json), updateTime | idx(accountId) |
| `ResonanceRecord` | id(pk), accountId, peerId, score, createTime | idx(accountId) |
| `Echo` | id(pk), ownerSpaceId, fromAccountId, payload(json), expireAt | idx(ownerSpaceId), idx(expireAt) |
| `Friendship` | id(pk), accountId, peerId, type(friend/follow), createTime | idx(accountId,peerId) |
| `Stall` | id(pk), accountId, spaceId, displayPayload(json), status(占位) | idx(accountId) |

> 向量本体存同库 PostgreSQL 的 pgvector 列（`vectorRef`/向量表关联）；关系元数据走 PgRepository。
> `hostConfig`（主控配置）：`{ broadcast:bool, asyncOnly:bool, resonanceThreshold:float, allowBattle:bool(P3) }`。

---

## 3. 协议（protobuf，消息类名 `_<id>` 后缀；走 WebSocket）

> 消息号段建议：账号 10xx、形象 11xx、意识档案 12xx、空间 13xx、共鸣 14xx、回声 15xx、社交 16xx、**系统/心跳 90xx**。具体 proto 由引擎 agent 定义。

### 3.0 线上封包格式（已由 FE 逆向 Aengine 源码确认，作为客户端/服务端契约）
WebSocket 二进制帧 = 一个完整 Packet，**大端/网络字节序**：
```
+---------+-------------------+----------------+--------------------+
| head:1  | length:2 (int16)  | cmd:4 (int32)  | body:(length-4)    |
+---------+-------------------+----------------+--------------------+
length = body.length + 4（含 cmd 4 字节）；整帧 = 7 + body.length；一帧一包，无需粘包处理
```
- `head` 位定义：bit7=TCP(0x80)、bit6=NEED_ACK、bit5=ACK、bit4=CLOSE、bit1-0=协议位(`0x03`，0=protobuf/1=JSON)。客户端发包 head=`0x81`(TCP|JSON)。
- **JSON 约定**（对齐 `ProtobufUtil`/proto3 JSON）：lowerCamelCase、默认值省略、未知字段忽略、**int64 序列化为字符串**（如 `accountId` 用 string 承载）。

### 3.1 协议对齐结论（PM 已拍板，FE 提出的 4 点）
| 点 | 结论 |
|---|---|
| 回包包头协议位 | Aengine `PlayerSession.send()` 回包包头协议位恒为 0、body 实际按请求时 `session.protocol` 编码。**P1 接受现状**：客户端按本端协议(JSON)解析下行，不依赖回包头协议位。未来需"请求 JSON / 回包 protobuf"混合时，由 BE 在回包头正确置位。 |
| 心跳/超时 | **已落地**：系统段 `Heartbeat_9001`/`HeartbeatAck_9002`（9001 入白名单、连接级保活）。Aengine 连接 idle **默认 30s**，已在 `EchoServer` bind 前 `setOpt("IDLE_SEC",40)` 上调到 **40s**；客户端心跳 **15s**。 |
| 共鸣分值口径 | 内部排序/阈值/落库用**余弦距离**（越小越近）；**对客户端暴露"共鸣度" = 1 − 距离（裁剪 0~1，越大越近）**，转换在 `ResonanceHandler` 响应边界完成。 |
| 新增 ack 响应 | 补 `UpdateHostConfigResp_1304`、`LeaveTraceResp_1504`（§3 表原未列），用于回执。 |
| 错误码 | 统一 `code`：0=成功；通用 1xxx（1001 参数错误 / 1002 未登录 / 1003 限流）；登录 2xxx（2001 openId 非法 / 2002 封号）。后续按模块扩展，维护一张错误码表。 |
| 鉴权 | **P1 简化**：openId 直登、不带 token（原型阶段）。上线前定 token 方案（建议首包鉴权或 WS URL query），属上线前待办。 |

| 方向 | 示例消息 | 说明 |
|---|---|---|
| C→S | `LoginReq_1001` / `LoginResp_1002` | 登录（`@IPacketHandler.noNeedCheckMessage` 放行） |
| C→S | `UpdateAvatarReq_1101` | 更新形象 |
| C→S | `SubmitPrefsReq_1201` → `MindProfileResp_1202` | 提交偏好，触发 LLM 补全 + 向量生成 |
| C→S | `EnterSpaceReq_1301` → `SpaceSnapshotResp_1302` | 进入意识空间，下发定势 + 动态参数 |
| C→S | `UpdateHostConfigReq_1303` | 主控配置共鸣细节 |
| C→S | `QueryResonanceReq_1401` → `ResonanceListResp_1402` | 拉取共鸣者候选 |
| C→S | `PullEchoesReq_1501` → `EchoListResp_1502` | 拉取我世界里的回声 |
| C→S | `LeaveTraceReq_1503` | 留痕/手势信物 |
| C→S | `AddFriendReq_1601` 等 | 社交 |

---

## 4. 关键服务逻辑（P1）

### 4.1 意识档案生成（F-MIND）
```
SubmitPrefsReq → 校验 rawPrefs
  → ILlmClient.enrich(rawPrefs) 得 enrichedPrefs   // LLM 补全，异步 + 超时兜底
  → IVectorStore.encode(enrichedPrefs) 得 vector    // 编码为 Self Vector
  → IVectorStore.upsert(accountId, vector)          // 落向量库
  → 落 MindProfile/SelfVector → 回 MindProfileResp
```
- LLM/向量为外部依赖，**统一抽象接口**，便于换供应商、便于 mock 测试。
- 补全失败要有兜底（用原始偏好直接编码），不阻塞主流程。

### 4.2 意识空间生成（F-SPACE）
```
EnterSpaceReq → 取 SelfVector → 选 presetSet(定势组合, 来自 template 配置表)
  → 叠加 dynamicParams(少量实时: 天气/光影/点缀, 受预算上限)
  → 持久化/复用 MindSpace → 下发 SpaceSnapshot(定势ID + 动态参数 + hostConfig)
```
- 定势组合走 `template`（Excel 配置 → 配置类），美术/策划维护（依赖 O9）。
- **客户端按"定势ID + 参数"本地渲染**，服务端不传大资源，省带宽。

### 4.3 共鸣匹配 + 回声（F-RES / F-SHOW，P1 异步）
```
QueryResonance → IVectorStore.topN(myVector, threshold) → 过滤(自己/黑名单)
  → 回 ResonanceList
PullEchoes → 取共鸣者的 Echo 快照(满足 hostConfig) → 合并下发
LeaveTrace → 生成 Echo(payload+expireAt) 落库, 对共鸣者世界可见
```
- P1 **全异步**：共鸣者以 Echo（快照/留痕）出现；实时在场是后续叠加层（接口预留，不实现）。
- Echo 过期由 `scheduler` Cron 清理。

---

## 5. 外部依赖与选型（交引擎 agent 调研落地）

| 依赖 | 抽象接口 | 建议起步 | 待办 |
|---|---|---|---|
| 向量库 | `IVectorStore`（upsert/topN/encode） | pgvector（与关系实体**同库 PostgreSQL**） | T-OPEN-2 |
| LLM | `ILlmClient`（enrich） | 接一家(HTTP)，控频次/超时/缓存 | T-OPEN-3 |

> 两者都**先定义接口 + 提供假实现(mock)**，保证 P1 主流程可独立联调、可单测（符合 Aengine "外部服务一律 mock" 的测试约定）。

---

## 6. 非功能 / 工程约束（沿用 Aengine 规范）
- 测试：JUnit5 + AssertJ + Mockito；外部服务(LLM/向量库)一律 mock。
- 工作流：理解→确认→执行；破坏性/选型类先确认。
- 依赖：最新稳定版；新增依赖在 `MIGRATION.md` 记录（若改动引擎）。
- 日志：SLF4J；Lombok 消样板。
- 协议：protobuf 优先，JSON 兼容（引擎已支持双协议）。
- 安全：登录前消息走 `noNeedCheckMessage` 白名单；其余校验 `session.getIdenty()`。

---

## 7. 委派任务清单（按 agent 分）

### 7.1 引擎/后端 agent（在 Aengine 之上建 `com.echo`）
- BE-1 工程脚手架：`com.echo` 模块、依赖 Aengine、启动类、WebSocket 接入、Handler 注册扫描。
- BE-2 实体 + 仓储：第 2 节全部实体 + 自写 PG 持久化层（`PgDb`/`PgRepository`/`CachedPgRepository`）+ PostgreSQL 建表 SQL。
- BE-3 协议：第 3 节 proto 定义 + Handler 骨架。
- BE-4 `ILlmClient` / `IVectorStore` 接口 + mock 实现 + 真实实现(选型后)。
- BE-5 意识档案/空间/共鸣/回声 四条服务逻辑（第 4 节）。
- BE-6 定势组合配置表（template）模板 + 读取。
- BE-7 单元测试（mock 外部依赖）。

### 7.2 前端/客户端 agent（Unity → H5/WebGL）
- FE-1 工程脚手架：Unity 工程 + WebGL 构建 + WebSocket 连接 + protobuf 编解码。
- FE-2 登录/形象录入/资料卡 UI。
- FE-3 偏好录入引导 UI（对接 SubmitPrefs）。
- FE-4 意识空间渲染：按"定势ID + 动态参数"本地组装场景；**写实空间 + 卡通角色/宠物**（美术基调见 PRD §1.4）；第一/三人称视角。
- FE-5 共鸣回声呈现：拉取并渲染 Echo（痕迹/幽灵）；留痕/手势交互。
- FE-6 好友/摊位占位 UI。

### 7.3 PM（我）
- 维护 PRD/技术纲要一致性、定义验收口径、协调前后端协议契约、把关里程碑 M1/M2。

---

## 8. 技术待办（需你/团队拍板）
| 编号 | 事项 | 建议 |
|---|---|---|
| T-OPEN-1 | 服务端业务包根 `com.echo` | ✅ 已采用 |
| T-OPEN-2 | 数据库架构 | ✅ 已定 DB'：单库 PostgreSQL + pgvector + 自写 `CachedPgRepository`（复用 Aengine 注解+缓存层） |
| T-OPEN-3 | LLM 供应商与预算 | 接口先行，先 mock；后续可"自养"模型 |
| T-OPEN-4 | 定势组合清单（美术基调已定：写实空间+卡通角色/宠物，见 PRD §1.4） | 待美术细化定势清单 |
| T-OPEN-5 | 接 Redis（分布式锁/pubsub）时机 | 当前用 `NoOpRedisLockSupport` 占位，规模化前替换 |

---

## 9. 里程碑（P1）
- **M1**：脚手架 + 账号/形象 + 偏好→LLM→向量→定势空间，单机可进入"专属世界"。
- **M2**：共鸣匹配 + 异步回声 + 留痕/好友，两账号能在彼此世界看到对方回声。
