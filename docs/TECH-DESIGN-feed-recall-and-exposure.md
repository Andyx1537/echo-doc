# TECH-DESIGN · 共鸣厅信息流 · 相似度召回与曝光计数

| 项 | 值 |
|---|---|
| 文档版本 | **v0.5 · 2026-08-25**（第五轮：**按上游 `SPEC` v0.3 回改口径残留**，销掉 5 项已被上游回答的「未决项」） |
| v0.2 修订摘要 | ① **裁定落地**：候选集保留「热点在线」（§2.2 重写）· 曝光上报端点 P0 就做（§3.10 新增前后端契约）· AI 种子内容进生产 + 强制标识（§3.11 新增）<br>② **Redis 存向量重新论证**（§2.10 新增）：上一轮"两份数据必有窗口期"的论证**不成立**，本轮逐条给出失败模式、成熟解法与总账数字。结论仍是 P0 不做，但**改为"现在不需要"而非"永远不该"**，并给出可直接执行的完整加固设计与量化触发条件<br>③ **缓存容量盘点**（§1.13 新增）：9 个 repository 逐个核算。确认 `maxElements=100000` 是**无依据的注解模板默认值**；并**推翻上一轮的泄漏归因**——`maxElements` 即使生效也修不了那个问题，真正无界的是 `CacheIndex` 内部的 `HashMap`（§1.13.4） |
| v0.2.1 修订摘要 | 🔴 **通道分组修正**（`SPEC-recommendation-ranking §3.8`）：**保底组（`FRESH`+`REVIVE`）必须全库直查，禁止经热点在线圈定**，否则 15% 保底会隐性缩水成 5%。已落进 §2.2.1（三组定义）· §2.2.4（保底组直查）· §2.2.5（核实排序侧可行性论据，逐条给数字）· §2.2.6（两组时延预算隔离）· §2.2.7（保底组降级阶梯，**明确禁止从相关性组补位**）· §2.2.9（副作用表更新：原第 2、3 类已由修正解决）<br>➕ **主动补强**：§2.2.8 把「保底位履约率」的口径从"位置是否填满"改为"填充来源是否合法"，并加 `slotProvenance` 与重叠率指标——**否则这条修正落地了也无法验证**<br>➕ **措辞限定**：v0.2 那句「按内容侧可召回性圈定被否」范围过宽，已限定为"被否的是**全部通道**都改按内容侧圈定"，保底组本身仍是按内容侧条件直查（§2.2.1 末） |
| v0.3 修订摘要 | ① **四项裁定落地**：向量走 pgvector HNSW（§2.4 / §2.10.6 定稿）· 引擎缓存缺陷不修的**正式理由入档**（§1.14）· `LONGTAIL` 归保底组（§7 Q13 结案，🔴 **但触发一个上游冲突，见 §8.7.5**）· `og:image` 叠 AI 标识 + **派生物料/用户素材边界**（§7 Q15 结案 + §3.12 新增整节）<br>② 🆕 **§8 曝光预算「梯度 + 时间」模型**（新增整节）：预算单位选**曝光次数**并给出决定性理由（§8.1）· 预算总额**发布时定、只减不增**（§8.2）· 分段常量衰减 60/30/0（§8.3）· 只扣保底位曝光（§8.4）· 🔴 **互动只做减法的制动设计**（§8.5）· 二级活跃改为**布尔准入而非加成**（§8.6）· **与四套既有机制的共存结论**（§8.7）· 容量自洽算术（§8.8）· TC-BUDGET-01…13（§8.10）· **叠床架屋判断**（§8.11）<br>③ 🔴 **两个上游问题上报**：`LONGTAIL` 已被 `SPEC` v0.2 移除，裁定三在当前规格下是空操作（§8.7.5）；`SPEC:815`「先到为准」与 `SPEC:817`「至少 700 次」在供给不足时自相矛盾（§8.7.3）<br>④ **术语同步**：`SUB` → `FOL`，「订阅」不再指代关注关系（全文 4 处） |
| v0.4 修订摘要 | 🔴 **§8 整节按「权重衰减」重做**，v0.3 的曝光次数配额记账**整套作废**（作废清单见 §8.0）：`W = W0 × γⁿ × T_eff × brakeFactor`，`γ=0.97`、时间衰减分段指数（τ₁=72h / τ₂=36h）· **「被接住后权重往哪走」给出结论**（撤除扶持，**不施加惩罚**，§8.2）· **`REVIVE` 建议整个删除**，欠投补发收敛成**一个 clamp**（§8.4.3 / §8.7.3）· 🆕 **`SURGE` 热点召回通道**（§8.6，含反马太的双条件门槛、五道防刷、终身 2 次 + 冷却 30 天）· 旧内容**完整生命周期 S1–S5**（§8.3）· 「自然流掉 = 搜得到推不到」写死为可验证约束（§8.7.6）· 北极星如实下降的说明（§8.8.3）· `TC-WEIGHT-01…15` 取代 `TC-BUDGET-*`（§8.10）<br>**净变化**：删掉额度表 / 扣减 / 结转 / 超发算术 / 日配额 / `REVIVE` 池 / `B4` 受众耗尽处理，换来一个三参数公式——**删掉的比新增的多** |
| v0.5 修订摘要 | 🔴 **本轮不产生任何新设计，全部是「上游已有结论、本文档回改滞后」的对齐**（来源：`PRODUCT-MINDMAP.md §6.2a` B 类台账 `B1`–`B5`）。逐条：<br>① **`B2`（工程风险最高，优先处理）**：§8.1.2 `W0` 表删除 `seed_ai = 0.30`。**核实结论：该行已无任何存在依据** —— 它挂靠的 `RK22` 现行原文恰恰是取消 `seed_ai` 这个来源类别本身（`SPEC §5.3` / `§17.4d`：「AI 生成」是素材成分标记而非内容来源，平台不做自创发布）。连带把 §3.8 DDL 注释、§3.11.1、§3.11.3、§2.2.9 里所有把 `seed_ai`/`seed_ops` 当枚举值用的**谓词与权重**一并改为 `{user, official}`<br>② **`B1`**：`REVIVE` **整条删除**（用户裁定：零回应复活作为普惠机制取消，投过了没人接即视为吸引力不足），已落 §2.2.1 / §2.2.4 / §2.2.6 / §2.2.7 / §2.2.8 / §2.2.9 / §0.3 / `R10`。🔴 **并按要求更新了论证强度**：§3.8「保底组必须全库直查」原本论证「只让 `REVIVE` 独立会让 15% 缩水成 5%」，现在保底组只剩 `FRESH` 一路 → **它失效则 15% 归零**，该约束由"防缩水"升级为"防归零"（§2.2.1 新增论证强度表，对齐 `SPEC §3.8.2` v0.3 重写）。连带：§2.2.7 的 **D3 池内补位整级取消**（两个补位来源都不存在了）、`slotProvenance` 删两个枚举值<br>③ **`B3` / `B4`**：`SPEC` 侧已给结论，本文档**只回改标记、不重新论证** —— `Q2` = 🟢 A（曝光上报端点 P0 就做，`SPEC §6.6` 上游裁定）；`Q1` = 🔴 **我的建议 A 被否**，维持热点在线圈定但限定在相关性组内（`SPEC §3.8`）。连带 `Q3` 随 `Q2` 自动作废、`Q11` 由 `H12`+`C13` 正面回答、`Q18` 三处连带已被 `SPEC` v0.3 吸收完毕 → 五项全部移入 🆕 **§7.0a**<br>④ **`B5`**：S4 的表达**统一为 `poolTag='DRAINED'` 作过滤谓词 + `drainedAt` 作时刻记录**（同事务写，召回层只读前者），撤回 v0.4「枚举收敛为 `FRESH\|STEADY\|RESTRICTED`、自然流掉不是一个池」那句 —— 依据是 `SPEC §6.2` 池枚举含 `DRAINED`、`§8.1 H11` 的硬过滤原文即 `poolTag = DRAINED`，且本文档文首已把「不重定义 `SPEC` 已定的池位」列为不做的事（§8.7.4 新增对照表）<br>➕ §5 对齐清单补 4 行（`§3.8.5` / `§6.6` / `H11` / `H12`）；§2.2.8 的口径修正建议标注**已被上游 `SPEC §3.8.5` 采纳** |
| 角色 | **技术方案**（后端实现方案，给研发直接开工的目标态） |
| 定位 | 解两个具体工程问题：① 相似度召回的写副作用 ② 排序所需的曝光计数怎么存 |
| 上游规格 | `SPEC-recommendation-ranking.md`（**本文档是它的下游实现方案**，口径以它为准）· `SPEC-trust-and-compliance.md §G0-10 / CM-G3`（授权门控）· `SPEC-admin-console.md §3`（埋点规范） |
| 本文档不做的事 | 不改任何业务代码（本轮只出方案）· 不重定义 `SPEC-recommendation-ranking` 已定的排序逻辑/特征/池位 · 不修改 `SPEC-*` / `DECISIONS.md` / `mock.ts` |
| 勘察基准 | `echo-server` **与 `Aengine`** 工作区状态 2026-08-24；引用行号以该时点为准。Aengine 侧已全模块核对（cache / scheduler / persistence / redis / event / util），结论散见 §1.5 §1.6 §1.8 §1.10 §3.4.0 |

> **v0.2 给产品的一句话**：上一轮我否决的两条，**你的反驳都对在了点子上，我的论证有实质缺陷，已重写。**
> ① **Redis 删 key**：你说得对——撤回时删 key 是标准做法，五种失败模式**全部有成熟解法**，我上一轮用"总有窗口期"一笔带过是偷懒。重新论证后结论**不再是"永远不该"，而是"现在不需要"**，依据是一个具体数字：它能省 **2–8 ms**，而要付出约 **500 行新基础设施 + 1 个新服务 + 1 个新故障域**，并且**被优化的那条链路今天 QPS = 0**（`VEC` 通道 P0 关闭且无向量数据）。升级阶梯与量化触发条件见 §2.10.6，完整加固设计见 §2.10.7（随时可执行，不需要重新设计）。
> ⓿ **通道分组修正（v0.2.1）**：这条修正抓到的失效模式比我 v0.2 列的四条副作用都更要紧，**我完全接受**。要害不是"少召回了些内容"，而是**失效是隐性的**——保底位被"恰好在热点人群里的新卡"占满，报表显示履约率 100%，但那些卡本来就能靠相关性出头，真正需要保底的那张进不了候选集。我 v0.2 只看到"内容变少"，没看到"监控会失明"。核实完排序侧的可行性论据后：**论据成立，代价估算偏保守（实际更便宜）**，需补三处实现约束（§2.2.5）。另外我主动加了一条规格没要求的：**把「保底位履约率」的口径从"位置填满"改成"填充来源合法"**，否则这条修正落地了也没法验证（§2.2.8）。
> **v0.4 给产品的一句话（权重衰减模型）**：
> ③ **换成权重制之后，方案是净简化的。** 删掉了额度表、扣减、结转、超发算术、日配额、`REVIVE` 池，以及 v0.3 专门为"受众耗尽"设计的那条机制——**后者在权重制下根本不需要处理**：投不出去 → `n` 不增长 → 权重不衰减，自愈。换来的是一个三参数公式。你那句「哪有这么直接的」指出的正是配额制的根本别扭：**它在承诺一个我们无法保证兑现的绝对数字**。
> ④ 🟢 **确认你的判断成立**：`SPEC:815` 与 `SPEC:817` 的矛盾在权重制下自动消失，因为矛盾来源是**两个硬上限互相踩踏**，而权重制里没有硬上限。结转机制已删。但那个矛盾**指向的实质问题**没消失（卡可能根本没被投出去），它现在由**一个 `max()` 承担**——不是一套机制，就一行公式（§8.4.3）。
> ⑤ 🔴 **「被接住后权重往哪走」我的结论是：往下，但只到"撤除扶持"，不再往下压。** 你的方向是对的（本产品与抖音那套确实是反的），但"降权"有两种实现，其中一种会反噬北极星：把被接住过的内容压到未被接住的内容**之后**，会让信息流里未经验证的内容占主导 → 浏览者流失 → **能去接住新内容的人变少** → 北极星下降。这是一条绕一圈回来打自己的设计。所以我采纳"撤除扶持"，不设"被接住惩罚系数"（§8.2.1）。
> ⑥ **`REVIVE` 建议整个删除，连改名保留都不必。** 因为"欠投补发"已经收敛成 §8.4.3 的那个 clamp——欠投的卡**根本不需要离开扶持期**，它的权重被地板托住，本来就还在候选集里。留一个"只有一个成员条件、且与扶持期高度重叠"的池是纯粹的状态机开销。🔴 **连带影响 3 处需要你转给排序侧**，其中 `SPEC` 的 `TC-RANK-49` 会**必然失败**（它的过标准是"仍能拿到复活保底位"），需要改写（§8.7.3）。
> ⑦ 🟢 **`SURGE` 的信号来源核实结论：不是落地阻塞。** 互动是**服务端写操作**，无论用户从搜索、主页、题材页还是站外链接进来都会落库，所以判定口径完全建立在今天就可得的信号上。搜索功能本身尚未实现、被动入口曝光结构上收不到（§3.10 的端点绑定 `/plaza` 的 `reqId`），这两项是**增强项**——本模型刻意不依赖它们，正是为了不去动那道防刷校验（§8.6.2）。
> ② **10 万缓存**：你说得对，这个数**没有任何依据**——它是 Aengine `@CRepository` 的注解默认值（`CRepository.java:22`），echo-server 里**没有一个 repository 覆写过它**。逐个盘点后真实需求是**几千到 5 万**（§1.13.3）。而且盘点还推翻了我上一轮的归因：**`maxElements` 即使生效也修不了我报的那个泄漏**，因为无界增长发生在单个 `CacheIndex` 的 `HashMap` 内部，而 `maxElements` 只限制缓存条目数、不限制条目里那个值对象有多大（§1.13.4）。真正该盯的 repository 也不是 `ResonanceRecord`，是 **`Echo`（`payload` 上限 4096 字符）**。

---

## 0. 结论摘要（TL;DR）

### 0.1 五个必须先说的勘察事实

| # | 事实 | 代码位置 | 对方案的影响 |
|---|---|---|---|
| 1 | `t_resonance_record` **零消费者**：全仓库（含 `docs`/`echo-h5-proto`/`test`）除写入与测试 mock 断言外，无任何一处读取 | `ResonanceService.java:70,75-86`；反查见 §1.1 | 拆分写副作用**不会破坏任何业务**，影响面≈0 |
| 2 | 写副作用不止"写表"：`add()` 同时把实体塞进**无容量上界**的进程内缓存与 `accountId` 索引，且每条一次独立 JDBC 往返 | `CachedPgRepository.java:37-41`；`PgRepository.java:392-415`；`CachedRepository.java:31-45,73-93`；`SimpleCache.java:12` | 真实风险是**内存泄漏 + 连接池占用**，比表膨胀更早出事 |
| 3 | **共鸣厅走的 HTTP/REST 侧与向量域完全没有接线**：`com.echo.http` 包内 `vector`/`prefs`/`resonance`/`MindProfile` 命中数 = **0**；`submitPrefs` 只能经 WS 1201 到达，H5 无任何 WebSocket 代码 | `EchoServer.java:121` 只把 `idGenerator/llm/accountService` 传给 HTTP；`MindProfileHandler`；`echo-h5-proto` 无 `WebSocket` | **H5 用户 100% 没有个人向量** → `VEC` 通道在 P0 不是"门控没就绪"，是**没有数据** |
| 4 | **Redis 分两层**：`echo-server` 侧零使用（无服务、无配置、无 `docker-compose` 条目，只有一个恒返回 `true` 的 `NoOpRedisLockSupport`）；但 **Aengine 侧已有完整封装**——`jedis 6.0.0` 在 classpath，`com.aengine.persistence.redis.Redis` 已封装计数器/Set/ZSet/per-key TTL | `NoOpRedisLockSupport.java:16-24`；`deploy/docker-compose.yml` 只有 `db`；`Aengine/pom.xml:117-122`；`Aengine .../redis/Redis.java:157-197,620-908` | 引入 Redis 的成本**不在 pom 也不在客户端代码，100% 在运维**；且当前是**单进程**部署，Redis 的核心价值（跨进程共享）用不上（见 §1.8/§2.4） |
| 5 | pgvector 的近邻索引**是注释掉的**，`topN` 当前是全表精确扫描 | `schema.sql:67-69`（`ivfflat` 被注释） | 这恰好是我们想要的（见 §2.4：小 N 下 exact 优于 ANN），但要有行数告警 |

### 0.2 两个问题的结论

| 问题 | 结论 | 关键取舍 |
|---|---|---|
| **① 相似度召回不能写库** | 抽出无副作用的 `findSimilar`，`queryResonance` = `findSimilar` + `persistRecords`（WS 1401 行为零变化）。**向量继续留在 pgvector 做读查询**，不搬内存、不搬 Redis。 | 决定性理由不是性能，是**授权门控**：向量留在 PG，四条件校验就是同一条 SQL 的 JOIN，撤回**零失效延迟**；搬到内存/Redis 就多一处必须自己保证 ≤5 s 失效的地方（§2.6） |
| **② 曝光计数怎么存** | **正确性放在 DB 唯一键上，性能放在内存里**：`t_card_exposure` 以 `(cardId, viewerId, day)` 唯一键承担 24 h 去重的持久化真相，批量 `INSERT ... ON CONFLICT DO NOTHING`；内存去重集合退化为纯性能优化，**它丢了、误判了、被 LRU 驱逐了都不影响最终计数正确性**。 | 这个结构让"用不用 Bloom""重启丢不丢"从**正确性问题**降级为**性能问题**；也让 HLL 被明确排除（§3.2：HLL 不具备成员查询能力，是被误用的工具） |

### 0.3 对产品两个方向的逐条判决

| 产品原话 | 判决 | 理由 |
|---|---|---|
| 「不要写库，查询写什么库」 | ✅ **完全成立**，且实际问题比这句话更严重 | §1.1–§1.3 |
| 「以热点在线过的 5000 或者一个量级里的人」 | ⚖️ **已裁定保留，但限定在相关性组内**（v0.2.1） | 最终口径：**相关性组（`REL`/`FOL`/`VEC`/`TAG`）走热点圈定**（裁定在这一组内完全成立）；🔄 **保底组（v0.5：只有 `FRESH`）全库直查**（`SPEC §3.8.1`）。两组预算/线程池/熔断/降级全部隔离（§2.2.6、§2.2.7）。<br>🔴 **v0.5：`REVIVE` 删除后这条约束由"防缩水"升级为"防归零"**——`FRESH` 是保底组唯一来源，它被圈定则 15% 一条都兑现不了（§2.2.1 论证强度表）。<br>⚠️ 落地前两个硬问题：① **「在线」这个信号当前根本不存在**——WS 在线态未实现（`EchoSessionManager.java:17`），H5 零 WebSocket，HTTP 侧无账号级活跃度记录，集合需**先造出来**（§2.2.2）；② 排序侧那条索引的四个列**当前有三个不存在**（`t_pet` 只有 `visibility`），P0 需改查 `t_card_pool_state`（§2.2.5 ③） |
| 「通过向量扫描方式核对」 | ✅ **成立**，且是本项目正确的选择 | 5,000 × 768 维精确扫描 ≈ 3–10 ms，占召回层 120 ms 预算的 <10%；小 N 下 exact 召回率 100%，优于 ANN（有损 + 需调参）。见 §2.4 |
| 「从缓存 Redis 做也可以」 | 🟢 **已裁定：采纳四级阶梯，P0 走 pgvector HNSW**（v0.3） | 上一轮的否决理由（"多一份副本必有失效窗口"）**已被推翻**：撤回时删 key + 事务外发件箱 + 只由同步器写索引 + 关持久化，这套组合能**可靠达成**"撤回后不再被使用"，它是合规的（§2.10.3）。真正的否决理由换成了**总账数字**：省 2–8 ms，付出 ~500 行基础设施 + 1 服务 + 1 故障域，且**目标链路当前 QPS = 0**（§2.10.5）。升级阶梯：精确扫描 → pgvector HNSW → JVM 镜像 → Redis Stack，**Redis 排第 4 且应与多实例决策捆绑**（§2.10.6）。<br>🟢 **v0.3 裁定落地**：P0 = **一条 `CREATE INDEX ... USING hnsw` DDL，零新组件**；§2.10.7 的 Redis 完整加固设计**保留在文档里作为可执行预案**，触发条件按 §2.10.6 的三条数字（不再需要重新设计，直接照做即可） |
| 「缓存记实时（热点数据 + 用户自身数据）」 | ✅ 成立 | 但要指明：现状下"缓存"只能是 JVM 内存 → 必须回答"丢了会怎样"。答案在 §3.5（误差方向是安全的） |
| 「事件本身也记录曝光量」 | ✅ 成立，但**必须定权** | 排序判定只认 `t_card_exposure`；`t_event` 只用于分析与对账。不定权则「保底位履约率 = 100%」无法验证。见 §3.6 |
| 「异步定期批量写入降低更新频率」 | ✅ 成立 | 批次 500 行 / 间隔 10 s，幂等由唯一键保证。见 §3.4 |

---

## 1. 现状勘察结论

> 本节全部结论均已在代码中逐条核对。凡与 `SPEC-recommendation-ranking §12.1` 表述有差异之处，在 §1.9 单列。

### 1.1 `queryResonance` 的写副作用到底是什么

```45:72:echo/echo-server/src/main/java/com/echo/module/resonance/ResonanceService.java
    public List<ScoredId> queryResonance(long accountId, int topN, double threshold) {
        float[] myVector = vectorStore.get(accountId);
        // ... topN 检索 + 过滤自己/黑名单 ...
        persistRecords(accountId, candidates);
        return candidates;
    }
```

```74:86:echo/echo-server/src/main/java/com/echo/module/resonance/ResonanceService.java
    /** 落共鸣记录（可选；便于后续召回/统计）。 */
    private void persistRecords(long accountId, List<ScoredId> candidates) {
        long now = System.currentTimeMillis();
        for (ScoredId c : candidates) {
            ResonanceRecord record = new ResonanceRecord();
            // ... setId/setAccountId/setPeerId/setScore/setCreateTime ...
            resonanceRecordRepository.add(record);
        }
    }
```

**写入的内容**：每个候选一行 `t_resonance_record{id, accountId, peerId, score, createTime}`（`ResonanceRecord.java:24-46`；DDL `schema.sql:84-92`）。

**它是给谁用的**：代码注释自称「可选；便于后续召回/统计」。**实际消费者：零。**

反查证据（全仓库检索 `t_resonance_record` / `ResonanceRecord`，排除 `target/`）：

| 命中位置 | 性质 |
|---|---|
| `ResonanceService.java:78` | **写入** |
| `EchoServer.java:162` | 仅 `new ResonanceRecordRepository()` 并注入，无查询 |
| `ResonanceRecord.java` / `ResonanceRecordRepository.java` | 实体与仓储声明 |
| `schema.sql:84-92` | DDL |
| `ResonanceServiceTest.java:50,68` | `verify(...).add(...)` 的 mock 断言 |
| `EntityMetaSmokeTest.java:33` | 元数据冒烟（只检查注解可解析） |
| `docs/TECH-P1.md:58` / `docs/PRD.md:294` | 文档提及 |

**没有任何 `list(...)` / `get(...)` / `SELECT` 读取路径。** 另一个佐证：表上唯一索引是 `idx_account_id` 单列（`schema.sql:92`）。若它真要用于"历史留痕查询"，索引形态应是 `(accountId, createTime DESC)`；只有单列 `accountId` 意味着查询形态是"按账号取全部历史"，而那正是最不该做的查询——说明这张表**从未被设计过读取场景**。

> **结论**：拆分写副作用的影响面 ≈ 0。唯一需要改动的是 `ResonanceServiceTest` 的两条 `verify` 断言，而若保留 `queryResonance` 原方法（本方案的做法），连这两条都不用改。

### 1.2 写放大的量化（不只是表膨胀）

`persistRecords` 的每一行都走 `CachedPgRepository.add(T)`：

```36:41:echo/echo-server/src/main/java/com/echo/infra/persistence/CachedPgRepository.java
    @Override
    public void add(T entity) {
        super.add(entity);
        cachedRepository.addCache(entity);
        cachedRepository.markLastChangeableField(entity, null, true);
    }
```

`super.add(T)` 是**单行 INSERT**，且 `PgDb.update` 每次调用**独立获取一次连接**：

```392:415:echo/echo-server/src/main/java/com/echo/infra/persistence/PgRepository.java
    @Override
    public void add(T entity) {
        String sql = buildInsertSQL();
        try {
            db.update(sql, ps -> { /* 逐列绑定 */ });
        } catch (SQLException e) { throw new RuntimeException(e.getMessage(), e); }
    }

    @Override
    public void add(List<T> entities) {
        // ⚠️ 批量 = for 循环调单条，没有 JDBC batch
        for (T entity : entities) { add(entity); }
    }
```

```113:127:echo/echo-server/src/main/java/com/echo/infra/persistence/PgDb.java
    public int update(String sql, PgStatementBinder binder) throws SQLException {
        // ...
        try (Connection connection = dataSource.getConnection();
             PreparedStatement ps = connection.prepareStatement(sql)) {
```

**四层放大**（按严重度排序，注意第一条比"写爆表"更早出事）：

| # | 放大 | 量化 |
|---|---|---|
| **A. 进程内缓存无界增长** | `CachedRepository` 的实体缓存是 `SimpleCache(timeToIdle=1800, timeToLive=0)`，**没有传 `maxElements`**（`CachedRepository.java:32`；`CRepository.maxElements()` 默认 100000 被忽略），底层就是一个裸 `ConcurrentHashMap`（`SimpleCache.java:12`）。同时 `@Cache(columns={"accountId"})`（`ResonanceRecord.java:26`）让每次 `add` 往一个 **per-account 的 `CacheIndex` 里追加主键**（`CachedRepository.java:78-92`）。`SimpleCache.get` 会刷新 idle 时间（`SimpleCache.java:72`）→ **一个正在翻页的用户，其索引条目永远不会被 1800 s idle 清掉，主键集合单调增长**。 | 单用户连续翻 50 页 × 30 候选 = 1500 个主键 + 1500 个实体常驻堆内 |
| **B. 连接池挤占** | 30 个候选 = **30 次 `getConnection()` + 30 次 round trip**，全在请求线程上同步串行。池上限 `maximumPoolSize=8`（`deploy/echo-db.properties:14`），HTTP 线程池 core 4 / max 16（`EchoHttpBootstrap.java:86-89`） | 按每次 INSERT 0.5 ms 计，单请求额外 **15 ms** 纯等待；16 线程并发时 8 连接会成为硬瓶颈 |
| **C. 表行数膨胀** | 行数 = `feed 请求数 × 候选数` | 3 万 DAU × 20 请求/天 × 30 = **1,800 万行/天**；按 ~100 B/行（含索引条目）≈ **1.8 GB/天** |
| **D. 索引写放大** | 每行一次 B-tree 插入 + WAL | 与 C 同数量级 |

> ⚠️ **重要澄清**：以上是**接线后**的推算。当前 HTTP/REST 侧尚未调用 `queryResonance`（§1.4），因此写爆**尚未发生**。`SPEC §12.1` 把它列为现状事实、`§12.6` 列为"研发必读"，两者都是正确的**前瞻风险**判断。本方案要做的是在接线**之前**把它拆掉。

### 1.3 `IVectorStore` 的实现与实际后端

| 项 | 现状 | 位置 |
|---|---|---|
| 接口 | `encode` / `upsert` / `get` / `topN(query, k, threshold)`；`DIM = 768`；**`topN` 不支持任何元数据过滤** | `IVectorStore.java:17-73` |
| 实现 A（DB 开） | `PgVectorStore`：`SELECT accountId, (embedding <=> ?::vector) AS score FROM t_self_vector WHERE embedding IS NOT NULL AND (embedding <=> ?::vector) <= ? ORDER BY score ASC LIMIT ?` | `PgVectorStore.java:88-112` |
| 实现 B（DB 关） | `InMemoryVectorStore`：`ConcurrentHashMap<Long, float[]>` + stream 全量映射 + **全排序**后 `limit(k)` | `InMemoryVectorStore.java:55-64` |
| 实际装配 | DB 开 → `PgVectorStore`；DB 关 → 无（只注册心跳 Handler） | `EchoServer.java:147-156` |
| **ANN 索引** | 🔴 **被注释掉**，`topN` 当前是**顺序扫描 + 精确计算** | `schema.sql:67-69` |
| 嵌入通道 | 默认 `MockEmbeddingClient`（确定性哈希，**不是语义向量**）；配 `ECHO_EMBED_API_KEY` 才切真 | `EmbeddingConfig.java:54-62`；`EchoServer.java:156` |
| 向量来源 | `submitPrefs`：用户偏好 → LLM 补全 → `encode` → `upsert`（**只有 WS 1201 这一个入口**） | `MindProfileService.java:55-108` |

两个额外发现：
- `InMemoryVectorStore.topN` 做的是**全量排序**而非有界堆选择，且每条 entry 都 new 一个 `ScoredId`。5,000 条量级下无所谓（~1 ms），但若将来把它当生产级内存索引用，需换成 bounded min-heap。
- 🔴 **`t_self_vector` 缺 `materialRef` / `consentRef` 两列**（`schema.sql:57-65`），而 `SPEC-trust-and-compliance §G0-10 ①` 明确把「embedding / 向量库行（pgvector）」列入**本期必须补齐这两列**的清单，并写了「没有这两列的派生物表一律不合格，评审直接打回」。**这是一个现存合规缺口**，同时也是本方案 §2.6 的 L2 门控能不能实现的前提。

### 1.4 关键事实：REST 侧与向量域完全没有接线

| 检索 | 范围 | 结果 |
|---|---|---|
| `vector\|prefs\|MindProfile\|SelfVector\|resonance`（忽略大小写） | `com/echo/http/**` 全包 | **0 命中** |
| `WebSocket\|new WebSocket\|ws://\|wss://` | `echo-h5-proto/src/**` | **0 命中** |

`EchoServer.java:121` 传给 HTTP 网关的依赖只有 `idGenerator, llmClient, accountService`——**向量库句柄没有传进去**。

推论链：
1. 共鸣厅（`GET /plaza`）跑在 HTTP 网关上；
2. HTTP 网关拿不到 `IVectorStore` / `ResonanceService`；
3. 生成个人向量的唯一入口 `submitPrefs` 只能经 WS 协议 1201 到达（`MindProfileHandler`）；
4. H5 前端零 WebSocket 代码；
5. → **H5 用户 100% 没有个人向量**，`t_self_vector` 对 REST 用户是空的。

> **这条改变了 `VEC` 通道的排期理由。** `SPEC §3.3 规则 3` 说「`IConsentGate` 未就绪时 `VEC` 默认关闭」——这是对的，但理由不完整。真实理由更硬：**即使门控明天就绪，`VEC` 通道也会返回空**，因为没有向量数据；而且即使有数据，`MockEmbeddingClient` 产出的是确定性哈希、不是语义向量，"相似"是伪相似。因此 `VEC` 在 P0 应当**明确不做**，其 30 配额按 `SPEC §3.3 规则 1` 永久转 `TOPIC`(+15) / `FRESH`(+15)。这需要产品确认（§7 Q4）。

### 1.5 缓存设施现状

**Aengine 提供的（`com.aengine.cache`）**：

| 类 | 语义 | 容量上界 | TTL | 线程安全 | 位置 |
|---|---|---|---|---|---|
| `ICache<K,V>` | `containsKey/put/putIfAbsent/computeIfAbsent/get/remove/size/removeAllExpired/clear` | — | — | — | `Aengine .../cache/ICache.java` |
| `SimpleCache` | 裸 `ConcurrentHashMap` + Element TTL；`get` 刷新 idle | 🔴 **无** | `timeToIdle` / `timeToLive` | ✅ | `SimpleCache.java:11-97` |
| `LRUCache` | `ConcurrentLinkedHashMap` + Element TTL + **驱逐监听** | ✅ `maxElements` | 同上 | ✅ | `LRUCache.java:12-106` |
| `CacheManager` | 单例，1 个 daemon 线程，**每 60 s** 遍历所有 cache 调 `removeAllExpired()` | — | — | ✅ | `CacheManager.java:54-61` |

**能力缺口（对本方案很关键）**：`ICache` **没有原子自增、没有集合/有序集合原语**。计数只能存 `LongAdder`/`AtomicLong` 作为 value 再 `computeIfAbsent`。（对比 §1.8：Aengine 的 `Redis` 封装这三类原语全都有——这是"内存 cache vs Redis"在**能力**而非性能上的真实差别。）

**Aengine 还有一处与本方案直接相关的现成设施，必须先评估再决定自建**：

| 类 | 能力 | 位置 | 本方案的取用结论 |
|---|---|---|---|
| `DelaySaveRepository` | 写后缓冲：脏队列 + `scheduleWithFixedDelay` 定时批量 flush + 失败保留重试 + shutdown hook 强制 flush | `Aengine .../persistence/DelaySaveRepository.java:20-106`；接入见 `DelayedJDBCRepository.java:16-26` | **复用模式与接线细节，不复用类**——它落库走 `forceSave()`（UPDATE），而本方案的幂等性依赖 `INSERT ... ON CONFLICT DO NOTHING`。完整论证见 §3.4.0 |

⚠️ `CacheManager` **没有 public shutdown 方法**（清扫线程随 JVM 结束）。这对纯缓存无影响，但意味着"停机时把缓存里的东西落完"这件事不能挂在它身上。

**Echo 侧现状**：
- HTTP 域（`com.echo.http`）**完全不用** Aengine cache——`InMemoryEchoStore` 是裸 `Map`，`PgEchoStore` 是直连 JDBC。`SPEC §12.4` 的判断（"本规格是第一个在 HTTP 域引入缓存的模块"）**正确**。
- WS 域经 `CachedPgRepository` 间接用到 `SimpleCache`，就是 §1.2-A 的泄漏源。
- ⚠️ `LRUCache` 依赖 `concurrentlinkedhashmap-lru 1.4.2`（Aengine 传递依赖）。该库自 2013 年后停止维护。作为热路径主力缓存需评估换 Caffeine——**但那是 Aengine 侧改动，按工作区约定需先与引擎侧确认**（§7 R3）。

### 1.6 调度设施现状

```185:188:echo/echo-server/src/main/java/com/echo/bootstrap/EchoServer.java
        // 过期回声清理：Scheduler + Cron
        Scheduler.init("echo-scheduler", 1);
        Scheduler.getInstance().schedule(new EchoExpiryJob(echoService));
```

| 事实 | 影响 |
|---|---|
| `Scheduler` = `ScheduledThreadPoolExecutor`，`init(name, threads)` 幂等（已初始化则直接 return，`Scheduler.java:21-25`） | 只有第一次 `init` 的线程数生效 |
| 🔴 **当前线程数 = 1**，且已被 `EchoExpiryJob`（cron `0 * * * * *`，每分钟）占用 | **再加任何作业都会串行阻塞**。本方案要加 flush(10 s) + 池位迁移 + 对账 + 保留期清理 → **必须先把线程数提到 ≥4** |
| `Scheduler.init` 只在 `EchoDatabase.initIfEnabled()` 成功后调用（`EchoServer.java:147-151, 186`） | DB 关闭时**没有任何调度器**；曝光落库需在 DB 关闭时整体降级为纯内存 |
| Cron 为 **6 段制**（秒 分 时 日 月 周），见 `TriggerTask` / `CronSequenceGenerator` | 新作业 cron 表达式沿用 6 段 |
| `TriggerTask.doTask()` 里的异常需自行 try-catch（`EchoExpiryJob.java:31-37` 的写法） | 新作业照抄该模式。补充一条实测语义：`TriggerTask.execute()` 的 `finally` 里**无条件重新 `schedule()`**（`TriggerTask.java:44-55`），所以异常**不会**取消周期任务；但异常若逃出 `doTask()` 会被 `WrappedRunnable` 吞掉只留日志——**静默失败**，因此每个作业必须自己落埋点，不能只靠日志 |
| 🔴 `Scheduler.shutdown()` **只调 `pool.shutdown()`，无 `awaitTermination`**（`Scheduler.java:99-101`） | 在途任务会被 JVM 退出直接截断。**任何"停机前要落完"的承诺都不能依赖调度器**，必须自己在 `Runtime.addShutdownHook` 里同步做完并自带超时（§3.4.3） |
| HTTP 与 WS **同进程**（`EchoServer.main` 先起 WS 再调 `EchoHttpBootstrap.start`，`EchoServer.java:112-121`） | 内存态在两个网关之间天然共享，不需要额外通道 |

### 1.7 配置约定

两套并存，都要沿用：

| 用途 | 形式 | 现有实例 |
|---|---|---|
| **可插拔 infra 组件** | `ECHO_XXX_*` 环境变量 + `record XxxConfig` 的 `fromEnv()` / `from(Function<String,String>)` 双入口（后者供单测注入），默认值内联，值一律 `trim()`（防 CRLF 带 `\r`） | `EmbeddingConfig.java:23-47`（`ECHO_EMBED_*`）· `LlmConfig`（`ECHO_LLM_*`）· `VisionConfig`（`ECHO_VISION_*`）· `StorageConfig`（`ECHO_STORAGE_*`） |
| **进程/端口/DB 开关** | `-Decho.*` 系统属性 | `echo.db.enabled` / `echo.db.config`（`EchoDatabase.java:36-39`）· `echo.port` / `echo.host` / `echo.http.port` / `echo.workerId` / `echo.devRoutes` |

数据源配置走 properties 文件：`-Decho.db.config=<path>` → `Properties.load` → `new PgDb(properties)`（`EchoDatabase.java:59-74`）。**没有中央 Config 类**，各模块自持一个 record。

> 本方案的新配置**全部用 `ECHO_*` 环境变量 + record**，与 `SPEC §3.3` 已命名的 `ECHO_RANK_CHANNEL_VEC_ENABLED` 一致。

### 1.8 Redis 现状：不存在

**必须分成两层看**——「Redis 不存在」这句话对 `echo-server` 成立，对 `Aengine` 不成立：

| 层 | 检查项 | 结果 |
|---|---|---|
| **Aengine（有）** | Maven 依赖 | ✅ `redis.clients:jedis 6.0.0`（`Aengine/pom.xml:117-122`），未被 echo-server 排除 → **已在 classpath**（`deploy/.cp.txt`） |
| | 客户端封装 | ✅ **`com.aengine.persistence.redis.Redis`（约 1,245 行）**，已封装本方案会用到的全部原语：`incr`/`incBy`/`decBy`（:157-197）、`zIncrby`（:755）、`sAdd`/`sCard`/`sIsMember`/`sRem`（:620-687）、`zAdd`/`zRange`/`zRangeByScore`（:695-908）、**per-key TTL**（`setNX(key,value,expire)` :202、`ttl(key)` :1110） |
| | 仓储与配套 | ✅ `RedisRepository` / `CachedRedisRepository` / `DelayedRedisRepository`；`RedisConfig`（ip/port/index/password/threads）；`RedisLockSupport` 分布式锁；`RedisActiveMessenger` + `PubSubService`（pub/sub） |
| **echo-server（无）** | `echo-server/pom.xml` | 无 redis 直接依赖（只显式排除了 `mysql-connector-j`，`pom.xml:56-61`） |
| | 实际使用 | 🔴 **零使用**。唯一 Redis 相关代码是 `NoOpRedisLockSupport.java:16-24`——`tryLock` 恒返回 `true`、`removeLock` 空实现，注释写明「本期不接 Redis」「待接入 Redis 后替换」；仅在 `EchoServer.java:91-92` 注入给 `PacketHandlerManager` |
| | 配置 / 环境变量 | 🔴 全无（无 `ECHO_REDIS_*`，`deploy/*.sh` 与 `echo-db.properties` 均无 Redis 项） |
| | 服务 | 🔴 `deploy/docker-compose.yml` 只有一个 `db` 服务（pgvector/pgvector:pg16），**无 redis 服务** |
| | 部署形态 | `DEPLOY.md`：「echo-server（一台/一组）」；「**多实例部署下献花额度的跨进程超发控制为 TODO（单实例用进程内锁足够）**」；会话 token / onboarding / 光谱**在进程内维护** |

> **三条推论（第 1 条是对"Redis 成本"最常见误判的纠正）**：
> ① 引入 Redis 的成本**既不在 pom，也不在客户端代码**——jar 已在 classpath，且 Aengine 的 `Redis` 封装恰好已覆盖计数器 / Set / ZSet / per-key TTL 这四类本方案需要的原语。真实成本 100% 在**运维**：新服务、新配置、新健康检查、新故障域、新备份策略、新 `RUNBOOK.md`/`DEPLOY.md` 条目、以及"Redis 挂了共鸣厅怎么办"的降级链。
> ② 这条纠正**不改变 §2.4 对"向量存 Redis"的否决**——否决理由是**合规（多一份副本 = 多一处失效点）**与**单进程下拿不到跨进程增益**，两条都与"客户端好不好写"无关。但它确实降低了 P2-4（真要引入时一次性承载 session/snapshot/exposure/rate-limit）的实施成本：届时曝光计数从内存迁到 `Redis.incBy` + `sAdd` 几乎是平移。
> ③ 当前**多实例是被会话 token 的进程内存储卡着的，不是被缓存卡着的**。在会话没外置之前引入 Redis，拿不到它唯一的核心增益（跨进程共享状态）。

### 1.9 授权门控现状：`IConsentGate` 不存在

| 检索项 | 结果 |
|---|---|
| `IConsentGate` / `assertUsable` | **0 命中**（不存在） |
| `t_ai_consent` 表 | **不存在**（`schema.sql` 无此表） |
| 现有的"同意"机制 | 只有两个布尔列：`t_account_profile.trainConsent`、`t_pet.trainConsent`（`schema.sql:154, 180`），用于训练语料回流门控（`EchoApi.recordTrainSample`）。**不是按能力分项的账本** |
| 向量/embedding 使用前的授权校验 | **完全没有**。`ResonanceService.queryResonance` 与 `MindProfileService.submitPrefs` 都不做任何 consent 检查 |
| `t_self_vector` 的 `materialRef`/`consentRef` | **缺失**（`schema.sql:57-65`） |

规格要求（`SPEC-trust-and-compliance`，不可打折）：
- `IConsentGate.assertUsable(materialRef, capability)` 是**唯一合法入口**，五处校验点（识别/定妆生成/近况生成/**向量检索**/训练）必须全部经它（`CM-G3` 校验点清单）。
- 四条件同时成立才允许使用：`granted=true` ∧ `revokedAt IS NULL` ∧ 源素材 `deletedAt IS NULL` ∧ `capability` 匹配（`G0-10 ②`）。
- 任一不成立 → **该素材连同其全部派生物退出本次调用**，不是"跳过这一条继续"。
- ArchUnit 或等价：AI 能力模块**不得直接查 `t_ai_consent`**，违反即构建失败（`G0-10 ③`）。
- 「向量检索」是**单独一项、「我」页可单独关闭**的授权（`G0-7 B-2`）。

### 1.10 表结构与 DDL 生成方式

**两条路并存，两条都要懂**：

| 域 | 机制 | 位置 |
|---|---|---|
| WS 域实体（`com.echo.module.*`） | **注解驱动自动建表**。`PgRepository` 构造时若 `@Table(autoCreate)` 则调 `fixTable()`：表不存在 → `CREATE TABLE IF NOT EXISTS`；存在 → 对每个非主键列 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`；再对每个 `@Index` 建索引（索引名自动加表前缀） | `PgRepository.java:45-62, 131-179` |
| HTTP 域（`com.echo.http.store`） | `PgEchoStore` 构造时执行**内嵌手写 DDL**（幂等） | `PgEchoStore.java` |
| 离线/DBA 真源 | `src/main/resources/sql/schema.sql`（**手写**，与上两者对齐；docker-compose 首次初始化时自动执行） | `schema.sql:1-15`；`docker-compose.yml` volumes |

**没有迁移框架**（无 Flyway/Liquibase）。加新表的做法：
1. 写实体类，加 `@Table` / `@Column` / `@Pk(auto=false)` / `@Index` / `@Cache`；
2. 写 `XxxRepository extends CachedPgRepository<Xxx>` 并标 `@CRepository(source="echo")`；
3. 在 `EchoServer.registerHandlers` 里实例化（构造即建表）；
4. **同步把等价 DDL 补进 `schema.sql`**（DBA 真源，不能只靠自动建表）。

**能力边界（本方案受此约束）**：
- ✅ 支持复合列 UNIQUE 索引（`buildCreateIndexSQL` 处理 `IndexType.UNIQUE` 与多列，`PgRepository.java:141-159`）；
- 🔴 **不支持分区表**、不支持部分索引（`WHERE ...`）、不支持 `ON CONFLICT`；
- 🔴 `PgDb.batch(List<String>)` 只接受**拼好的 SQL 字符串**（`Statement.addBatch`），**没有 `PreparedStatement` 批量绑定**（`PgDb.java:129-140`）→ 本方案需要新增一个批量方法（§3.4）。
- `G0-9` 要求"含唯一键的业务表唯一索引一律改为部分索引 `WHERE deletedAt IS NULL`"——自动建表**做不到**，需要在 `schema.sql` 手写。

**相关表的现状**：

| 表 | 关键列 | 缺什么（对排序而言） |
|---|---|---|
| `t_resonance_record` | `id, accountId, peerId, score, createTime` + `idx(accountId)` | 无消费者、无保留期 |
| `t_self_vector` | `id, accountId, dim, vectorRef, normHash, embedding vector(768)` + `idx(accountId)` | 🔴 `materialRef`/`consentRef`（G0-10 ①）；ANN 索引被注释 |
| `t_pet`（当前的"窗口"） | `petId, ownerAccountId, ..., visibility, seenCount, flowersReceived, createTime` + `idx(owner)` `idx(visibility)` | 无 `category` / `publishedAt` / `status` / `deletedAt`（`SPEC §12.1` 已列） |
| `t_event` / 曝光/impression 相关表 | — | 🔴 **一张都不存在** |

### 1.11 现有"曝光"与埋点现状

| 现状 | 位置 | 问题 |
|---|---|---|
| "埋点" = 一行 logback 日志，无落库、无 `/collect` | `EchoApi.java:1387-1395` | 不可聚合、不可对账 |
| `GET /plaza` 触发的埋点事件名是 **`window_open`** | `EchoApi.java:554` | 🔴 **语义错误**：`window_open` 应表示"打开了某扇窗"，而 `/plaza` 是列表请求。`SPEC §4.1 F3` 的 `topicMatch` 依赖 `window_open` 聚合，口径污染会直接影响题材偏好 |
| `POST /windows/:id/seen` 做 `pet.seenCount += 1; store.putPet(pet)` | `EchoApi.java:573-579` | 🔴 三个问题：① 读-改-写整行，**丢更新竞态**；② 每次一次全行 UPDATE；③ **无 `(cardId, viewerId)` 去重**。这不能作为 `SPEC §6.3` 的曝光额度口径 |
| 前端 `seen` 只在**详情页打开时**上报，不是列表曝光 | `DetailScreen.tsx:104` | 现状没有任何"曝光"信号 |
| 前端 `track()` 有可选上报端点（`sendBeacon`），未配置则只 `console.info` | `echo-h5-proto/src/api/track.ts:51-71` | 后端无对应端点，默认哪儿也不去 |
| `GET /plaza` = `store.allPets()` 全表 + `visibility=='public'` 过滤 + offset 分页，无 `ORDER BY` | `EchoApi.java:546-556`；`PgEchoStore.java:307-313` | 与 `SPEC §12.1` 一致 |

### 1.12 与 `SPEC-recommendation-ranking §12.1` 的差异修订

`SPEC §12.1` 的现状核实**基本准确**。以下三条是本次勘察的**补充/修订**，建议 PM 在下一版并入（本文档不修改该规格）：

| # | 规格原文 | 本次勘察的修订 |
|---|---|---|
| 1 | 「`ResonanceService.queryResonance` **有副作用**…feed 每次翻页都调会把这张表写爆」 | ✅ 成立，但**首要风险不是表**。`CachedPgRepository` 的无界进程内缓存与 per-account 索引会先 OOM（§1.2-A）；连接池（8 连接）先成瓶颈（§1.2-B）。且 `t_resonance_record` **零消费者**（§1.1）——这让处置方案的选择空间比规格设想的更大（可直接废弃） |
| 2 | 「`IVectorStore` 是账号级向量（`t_self_vector`，768 维，cosine），`topN` 不支持任何元数据过滤」 | ✅ 成立。**补两条**：① pgvector 的 ANN 索引是**注释掉的**（`schema.sql:67-69`），当前为精确顺序扫描；② `t_self_vector` **缺 `materialRef`/`consentRef`**，这是 `G0-10 ①` 的现存缺口，也是 `VEC` 门控 L2 的前提 |
| 3 | 「`VEC` 通道 ⚠️ 门控前置」「`IConsentGate` 不存在 → P0 默认关闭」 | ✅ 成立，**但理由不完整**。更硬的理由是**没有数据**：HTTP/REST 侧与向量域零接线，`submitPrefs` 只能经 WS 1201 到达，H5 零 WebSocket 代码 → H5 用户 100% 无向量；且默认 `MockEmbeddingClient` 产出确定性哈希、非语义向量。建议 `VEC` 在 P0 **明确不做**而非"默认关闭"（§7 Q4） |

### 1.13 缓存容量盘点（v0.2 新增 · 回应「什么玩意要超过 10 万的缓存」）

> 这一节是实打实的逐个核算，不是估个数交差。结论先说：**10 万这个数是 Aengine 注解的模板默认值，echo-server 里没有一个 repository 覆写过它，它跟本项目的数据规模没有任何关系。** 而且核算过程还推翻了我 v0.1 的泄漏归因（§1.13.4）。

#### 1.13.1 全量清单：9 个 repository，声明完全一样

全仓检索 `CRepository` / `CachedPgRepository` 的结果——**echo-server 一共 9 个带缓存的 repository，全部只写了 `source`，一个参数都没调**：

```java
@CRepository(source = "echo")          // 9 个 repository 全部是这一行，无一例外
public class XxxRepository extends CachedPgRepository<Xxx> { }
```

所以生效的是注解默认值（`Aengine .../annotation/CRepository.java:22-32`）：

| 注解参数 | 默认值 | 在 echo-server 的实际命运 |
|---|---|---|
| `maxElements` | **100000** | 🔴 **从未被读取**。`CachedPgRepository.java:33` 只传了 `timeToIdle()` 与 `timeToLive()` 给 `CachedRepository`，`maxElements()` 这个方法在整个 echo-server 里没有任何调用点 |
| `timeToIdle` | **1800**（30 分钟） | ✅ 生效。`SimpleCache` 按它做 idle 过期 |
| `timeToLive` | **0**（不启用） | ✅ 生效（即：只有 idle 过期，没有绝对存活上限） |
| `async` / `batch` / `interval` / `delay` / `rolling` | false / 200 / 10 / 60 / none | 🔴 全部未读取（`CachedPgRepository` 没有接 `DelaySaveRepository`，§3.4.0） |

> **所以「10 万」这个数字的来历，就是有人写 `@CRepository(source="echo")` 时注解默认值填了 100000。** 它不是估算结果，不是压测结论，也没有对应任何业务对象的规模。用户的质疑完全正确。

#### 1.13.2 逐个 repository 核算

**先说清缓存的两级结构**（决定容量该怎么算，`CachedRepository.java:19-21`）：

| 级 | 结构 | key | 容量由什么决定 |
|---|---|---|---|
| **实体缓存** | `SimpleCache<String, T>` | 主键字符串 | **在 30 分钟 idle 窗口内被访问过的行数** |
| **索引缓存** | 每个 `@Cache` 一个 `SimpleCache<String, CacheIndex>` | `表名_列名_值`（如 `t_echo_ownerSpaceId_123`） | **窗口内被访问过的不同索引值个数**；每个值里挂一个装主键的 `HashMap` |

关键推论：**8 / 9 个 repository 的 `@Cache` 列是 `accountId`（或 `openId` / `ownerSpaceId`），也就是"每个账号一行或少数几行"。** 这类缓存的天然上界是**并发活跃账号数**，跟表总行数无关——表里有 100 万个账号，只要同时活跃的是 300 个，缓存里就只有 300 条。

| # | Repository | 实体 / 表 | `@Cache` 索引列 | 每个索引值几行 | 数据总量级 | 访问模式 | **实际需要缓存多少条** |
|---|---|---|---|---|---|---|---|
| 1 | `AccountRepository` | `Account` / `t_account` | `openId`（UNIQUE） | **1** | = 注册账号数 | 登录时读，之后几乎不动。读多写极少 | = 活跃账号数 |
| 2 | `AvatarRepository` | `Avatar` / `t_avatar` | `accountId` | 1～少数 | ≈ 账号数 | 进空间时读一次，改形象时写。读多写少 | = 活跃账号数 |
| 3 | `MindProfileRepository` | `MindProfile` / `t_mind_profile` | `accountId` | **1** | ≈ 账号数 | 建档时写，之后读。读多写少 | = 活跃账号数 |
| 4 | `SelfVectorRepository` | `SelfVector` / `t_self_vector` | `accountId` | **1** | ≈ 提交过偏好的账号数（**当前 = 0**，§1.4） | `submitPrefs` 写、召回读。**注意实体里不含 768 维向量本体**（`SelfVector.java:27-46` 只有 `dim`/`vectorRef`/`normHash`），向量在 pgvector 列里 | = 活跃账号数 |
| 5 | `MindSpaceRepository` | `MindSpace` / `t_mind_space` | `accountId` | 1～少数 | ≈ 账号数 | 高频读（每次进空间） | = 活跃账号数 |
| 6 | `FriendshipRepository` | `Friendship` / `t_friendship` | `accountId` | **N（好友数）** ⚠️ | 账号数 × 好友数 | `list(accountId)` 会把该账号**全部**关系行灌进实体缓存 | = 活跃账号数 × 人均好友数 |
| 7 | `EchoRepository` | `Echo` / `t_echo` | `ownerSpaceId` | **N（该空间的回声数）** ⚠️ | 空间数 × 回声数 | 高频读；`payload` 字段**上限 4096 字符**（`Echo.java:46`）→ 单实体可达 **~8 KB**，是全部实体里最重的 | = 活跃空间数 × 空间内回声数 |
| 8 | `StallRepository` | `Stall` / `t_stall` | `accountId` | 1～少数 | **≈ 0**（`@Table` 注释自称「P1占位」） | 当前无业务 | ~0 |
| 9 | `ResonanceRecordRepository` | `ResonanceRecord` / `t_resonance_record` | `accountId` | **N（每次查询 topN 条，单调增）** 🔴 | 请求数 × 候选数 | **只写不读**（§1.1 零消费者）。删掉 `persistRecords` 后 → **0** | **0（本方案废弃）** |

#### 1.13.3 校核用户给的两个量级，并给出建议容量

**「最大热点超不过 30」** —— 这个数对应的是**内容维度的热点对象数**，不是 repository 实体缓存：

| 对得上的地方 | 数字来源 |
|---|---|
| 首屏卡片数 | `SPEC` 首屏 20 条 |
| `VEC` 通道 topN | 30（`ECHO_VEC_TOPN`） |
| 每 20 条里的保底位 | ≥5 条 |
| 正在被反复曝光的保底池热卡 | 几十量级 |

→ **在「热卡/热对象」这类缓存上，30 这个量级完全成立**（`poolIndex` 热卡集合、种子卡集合、`VEC` 候选 topN）。
→ 但它**不适用于 9 个 repository 的实体缓存**，因为那里的 key 基数由**并发活跃账号数**决定，而不是由"有多少个热点"决定。1000 个人同时在线各看自己的空间，就是 1000 条缓存，其中没有任何"热点"。

**「3 天内局部短期热点不超过 1 万」** —— 这个数对应的是**一段时间内出现过的不同对象数**，正是实体缓存工作集的正确度量。核算（30 分钟 idle 窗口 → 取峰值集中度 3×）：

| 阶段 | DAU | 30 分钟窗口内活跃账号（均摊） | 峰值 3× | 3 天累计不同账号 |
|---|---|---|---|---|
| 种子期（`GTM` 100–300 人） | 300 | ~20 | ~60 | ~300 |
| 早期 | 3,000 | ~190 | ~570 | ~5,000 |
| 中期 | 30,000 | ~1,900 | ~5,700 | ~50,000 |
| 目标期 | 300,000 | ~19,000 | ~57,000 | ~500,000 |

→ **用户给的「3 天内 1 万」这个量级，对应到 DAU 3 千～3 万之间，正是本项目未来 1–2 年的现实区间**，判断准确。
→ 注意：缓存真正要装的是**30 分钟窗口**（因为 `timeToIdle=1800`），比"3 天累计"小一个数量级还多。所以按 30 分钟窗口算，中期只要 **~6,000 条**。

**建议容量与内存估算**（按中期 DAU 3 万的峰值窗口定，留 2× 余量）：

单条缓存的固定开销（`Element` 48 B + `ConcurrentHashMap.Node` 32 B + 表槽位 ~11 B + 主键 String ~75 B）≈ **165 B**，再加实体本身：

| # | Repository | 建议 `maxElements` | 依据 | 单实体估算 | 内存估算 |
|---|---|---|---|---|---|
| 1 | `AccountRepository` | **10,000** | 活跃账号峰值 6k × 2 | ~250 B | **4.2 MB** |
| 2 | `AvatarRepository` | **10,000** | 同上 | ~250 B | 4.2 MB |
| 3 | `MindProfileRepository` | **10,000** | 同上 | ~600 B | 7.7 MB |
| 4 | `SelfVectorRepository` | **10,000** | 同上（实体不含向量本体） | ~350 B | 5.2 MB |
| 5 | `MindSpaceRepository` | **10,000** | 同上 | ~400 B | 5.7 MB |
| 6 | `FriendshipRepository` | **50,000** ⚠️ | 6k 活跃账号 × 人均 ~4 关系 × 2。Echo 是情感陪伴/回忆产品不是社交图谱，人均关系数应是**个位数**；若产品侧预期人均 >50，此项需重算 | ~200 B | 18 MB |
| 7 | `EchoRepository` | **20,000** ⚠️ | 6k 活跃空间 × 空间内 ~2 条常读回声 × 2。**这是内存最敏感的一项**：`payload` 上限 4096 字符，最坏单实体 ~8 KB | ~1 KB 均值 / ~8 KB 最坏 | **23 MB 均值 / 163 MB 最坏** |
| 8 | `StallRepository` | **1,000** | P1 占位，无业务 | ~250 B | 0.4 MB |
| 9 | `ResonanceRecordRepository` | **废弃** | 本方案删除写入路径（§2.5.3） | — | **0** |
| | **合计** | | | | **~68 MB 均值 / ~208 MB 最坏** |

> **结论：全部 9 个 repository 加起来，合理容量的总内存是几十 MB 量级。** 没有任何一个需要 10 万条。唯一需要盯的是 `EchoRepository`——不是因为条数多，而是因为 `payload` 4096 字符让**单条**很重。它的容量上界应该按**字节**而不是按**条数**来想。

#### 1.13.4 🔴 重要更正：我 v0.1 报的泄漏归因是错的

v0.1 我把内存风险归到「`maxElements` 被忽略」，并给了"分钟级 GB"的估算。**逐行读完引擎代码后，这个归因不成立，必须更正。** 三条：

**更正一：`maxElements` 即使生效，也修不了那个问题。**

`ResonanceRecord` 的无界增长有两个部分，第二个部分才是要害：

```java
// CachedRepository.addCache(entity) —— Aengine .../CachedRepository.java:73-93
T old = cache.putIfAbsent(pk.toString(), entity);   // ① 实体缓存：每条一个新条目
for (CacheMeta n : meta.getCache()) {
    CacheIndex cacheIndex = cache.get(key);          // ② key = "t_resonance_record_accountId_<id>"
    ...                                              //    每个账号只有 1 个条目
    cacheIndex.add(pk);                              // 🔴 但条目里那个 HashMap 无限长大
}
```

`CacheIndex.identities` 是一个**普通 `HashMap`**（`CacheIndex.java:16`），`add()` 只往里 put、**没有任何上界，也没有淘汰**。而 `maxElements` 限制的是**缓存里有多少个条目**——它管不到"某一个条目里的那个 `HashMap` 装了多少主键"。单账号翻 50 页 × 30 条 = 一个 `HashMap` 里 1500 个 key，`maxElements` 对此**完全无效**。

更糟的一条：索引处于 `NOT_COMPLETE` 状态时，`remove()` **不删 key，而是标记成 `REMOVED` 继续留着**（`CacheIndex.java:29-34`）——**删除操作也会让这个 map 变大**。只有 `complete()` 才会清理（`:47`）。

**更正二：实体缓存其实是自愈的，不是无限增长。**

`SimpleCache` 的 `putIfAbsent` 对新 key 会新建一个 `Element` 并带上自己的时间戳（`SimpleCache.java:46`），`CacheManager` 每 60 秒扫一遍调 `removeAllExpired()`。`ResonanceRecord` 从来没有人按主键读过 → 每个条目在创建 30 分钟后必然被清掉。所以实体缓存的上界是**「30 分钟的写入量」而不是「无限」**。v0.1 说"永远不会被 idle 清掉"只对**索引条目**成立（每次 `addCache` 都 `cache.get(key)` 刷新了它的 idle，`:83`），对实体条目不成立。

**更正三：真正该盯的 repository 不是 `ResonanceRecord`。**

`ResonanceRecord` 的写入路径本方案要删掉（§2.5.3），删完这个风险归零。剩下 8 个里：

| Repository | 缺陷是否会咬到 | 为什么 |
|---|---|---|
| 1,2,3,4,5,8（6 个） | 🟢 **不会** | `@Cache` 列是 `accountId`/`openId`，**每个索引值只挂 1 个主键**，`CacheIndex` 里那个 `HashMap` 永远只有 1 个元素；实体缓存条数由活跃账号数天然封顶（几千条）。`maxElements` 生不生效对它们毫无区别 |
| 6 `Friendship` | 🟡 **理论上会，实践上取决于关系数** | 每个 `accountId` 挂 N 个主键。若人均关系数是个位数 → 无风险；若某账号有 1 万个关系 → 该账号的 `CacheIndex` 里 1 万个 key。情感陪伴类产品不太可能，但**没有代码层上界** |
| 7 `Echo` | 🟠 **会，且是最实际的一个** | 每个 `ownerSpaceId` 挂 N 条回声主键，**且回声是持续产生的**（每次留痕一条）。一个长期活跃的热门空间，其 `CacheIndex` 会随留痕数单调增长且 idle 被不断刷新永不过期；叠加 `payload` 4096 字符 → 实体缓存也重。**这是全项目唯一一个"高频写 + 单 key 多行 + 大实体"三条同时成立的 repository** |

**所以准确的风险描述是**（替代 v0.1 的"分钟级 GB"）：

> 不是"必然 OOM"，而是：**只在"高频写入 + 单个 `@Cache` 值对应多行 + 该 key 持续活跃"三条同时成立的 repository 上才会出事。** 当前满足三条的只有两个——`ResonanceRecord`（本方案删除，归零）与 `Echo`（真实存在，但增速是"留痕频率"而非"feed 翻页频率"，慢好几个数量级）。删掉 `persistRecords` 之后，v0.1 那个"200 QPS × 30 条"的场景**不再存在**，"分钟级 GB"的估算随之作废。

#### 1.13.5 结论：引擎缺陷要不要单独排期修

**建议：不单独排期修 `maxElements`，因为修它是在修一个不解决问题的东西。** 分三步走：

| 优先级 | 动作 | 成本 | 理由 |
|---|---|---|---|
| **P0 · 做** | 删掉 `persistRecords` 的调用（§2.5.3 已列） | 已在 P0-4 | 这一步就把唯一一个高危路径去掉了。**性价比远高于改引擎** |
| **P0 · 做** | 给 9 个缓存加一个 size 观测埋点（日作业输出 `cache.size()` 与最大 `CacheIndex` 尺寸） | 很小 | `ICache` 有 `size()`（`ICache.java`）。**先能看见，再谈治理**——现在连"缓存里有多少条"都不知道，任何容量决策都是猜 |
| **P1 · 有条件做** | 若观测到 `Echo` 的 `CacheIndex` 尺寸持续增长，再动引擎 | 需与引擎侧确认 | 见下 |
| **不做** | 单独修 `maxElements` | — | 修完给人一种"容量已经受控"的错觉，而真正无界的 `CacheIndex` 还在那儿。**假的安全感比已知的缺陷更危险** |

**如果将来真要改 Aengine，正确的改动是这两条（不是 `maxElements`）**：
1. `CachedRepository` 构造时把 `SimpleCache` 换成 `LRUCache`，并**把 `maxElements` 真正传进去**（`LRUCache` 才有容量上界与驱逐监听，§1.5）；
2. 🔴 **给 `CacheIndex.identities` 加上界**，超限时把该索引整体降级为 `NOT_COMPLETE` 并清空（下次查询回源重建）。**这一条才是真正的修复**；只做第 1 条不做第 2 条，等于没修。

⚠️ 两条都在 `Aengine` 侧，按工作区协作约定**必须先与引擎侧确认再动**，本方案不自行决定（§7 Q10）。

---

### 1.14 引擎缓存缺陷「不修」的正式理由（v0.3 · 裁定二入档）

🟢 **裁定**：不单独排期修 Aengine 缓存缺陷。P0 只做两件事：① 删 `persistRecords`；② 给 9 个 repository 加 size 观测埋点。

**不修的正式理由（裁定原文采纳）**：

> **修完 `maxElements` 会给人「容量已受控」的错觉，而真正无界的 `CacheIndex` 还在那儿。假的安全感比已知缺陷更危险。**

这句话的技术依据在 §1.13.4：`maxElements` 限制的是**缓存条目数**，而观察到的无界增长发生在**单个条目内部**——`CacheIndex.identities` 这个 `HashMap` 装的是一个账号名下的全部 id 集合，它有多大取决于该账号的数据量，而 `SimpleCache` 只把整个 `CacheIndex` 当**一个**条目计数。所以：

| 只改 `maxElements` 的后果 | 说明 |
|---|---|
| 缓存条目数**看起来**受控了 | 监控上 `size` 曲线变平，容量告警不再触发 |
| 单条目内存**仍然无界** | `CacheIndex.identities` 的增长完全不受 `maxElements` 影响 |
| **观测手段被削弱** | 原本"条目数异常增长"这个信号会消失，而它是当前唯一能间接反映问题的信号 |

🔴 **将来若要改 Aengine，两条必须一起做，只做一条视为未修**：

| # | 改动 | 缺了它会怎样 |
|---|---|---|
| 1 | `SimpleCache` → `LRUCache`（让 `maxElements` 真正生效） | 条目数无上界 |
| 2 | `CacheIndex.identities` 加上界（超限则整个索引降级为 `NOT_COMPLETE`，回退查库） | 单条目内存无上界，且这是**主要**风险源 |

> **为什么必须捆绑**：只做 1 = 上面那张表的三个后果全中（假安全感）；只做 2 = `maxElements` 依然是死配置，注解上写着 100000 而运行时无效，这本身是一个会持续误导人的不一致。两条的实现都在 `Aengine` 侧，按工作区约定需先与引擎侧确认（见 §7 Q10）。

**P0 的 size 观测埋点口径**（这是替代方案，不是妥协）：

| 指标 | 口径 | 阈值 |
|---|---|---|
| `cache_entry_count{repository}` | `SimpleCache` 条目数 | 各 repository 按 §1.13.3 的实际需求量 ×3 告警 |
| `cache_index_max_identities{repository, indexName}` | 🔴 **单个 `CacheIndex` 内 `identities` 的最大 size**——这是直指真实风险源的指标 | >100000 告警 |
| `cache_index_incomplete_ratio{repository}` | `NOT_COMPLETE` 状态的索引占比 | 观测（持续为 0 说明降级路径从未被走到） |

> 第二条指标是本节的重点：它让"真正无界的那个东西"第一次变得可见。**在没有修复的情况下，可见 > 不可见**——这也是为什么"只加观测不修"不是拖延，而是先把问题从盲区里拿出来。

---

## 2. 问题一 · 相似度召回不写库

### 2.1 先把两件事分开：写副作用 ≠ 读查询

产品原话「不要写库，查询写什么库」里其实有两个诉求，工程上必须分开处理：

| 诉求 | 判决 | 说明 |
|---|---|---|
| **不要在查询路径上产生写入** | ✅ **完全采纳** | 这是本节 §2.7 的全部内容。查询就是查询，不该留痕 |
| **不要用数据库做查询** | 🔴 **不采纳** | pgvector 的 `SELECT ... ORDER BY embedding <=> ?` 是**纯读**：不写表、不写 WAL、不产生任何持久化变更。它是本项目**唯一已经落地**的向量检索能力（`PgVectorStore.java:88-112`，已有单测 `PgVectorStoreTest`）。放弃它去自建一套内存索引，是净损失：多一套要维护的代码、多一处授权失效点、少一个已验证的实现 |

> **给产品的说明**：「查询写什么库」这个直觉是对的——它指的是"查询不该产生写入"。但"读数据库"和"写数据库"在成本与风险上完全不是一回事：一次 `SELECT` 只占用连接和 CPU（毫秒级、无状态、可随时中断）；一次 `INSERT` 会产生 WAL、索引写、表膨胀、真空压力、备份体积（永久成本）。我们要砍掉的是后者。前者恰恰是 pgvector 存在的意义。

### 2.2 候选集怎么圈定（v0.2.1：相关性组走热点圈定 + 保底组全库直查）

#### 2.2.1 裁定（含 v0.2.1 修正）与本节改动

**最终口径 —— 通道按候选集来源分三组**（`SPEC-recommendation-ranking §3.8.1`，🔄 **v0.5 按 `SPEC` v0.3 对齐**）：

| 组 | 通道 | 候选集来源 | 判决 |
|---|---|---|---|
| **相关性组** | `REL` / `FOL` / `VEC` / `TAG` | ✅ **按热点在线圈定** | 裁定在这一组内**完全成立**，是合理的性能优化 |
| **保底组** | 🔄 **`FRESH`（本组只剩一路）** | 🔴 **全库直查，禁止经热点在线圈定** | v0.2.1 修正新增；🔴 **v0.5：`REVIVE` 已整条删除**，见下方 |
| **兜底组** | `FALLBACK` 热门层 | ✅ 可走热点圈定 | — |
| | 🔄 `FALLBACK` 随机层 · `CURATED` · 🆕 `SURGE` | 🔴 **禁止**（全库 / 运营指定 / 日聚合作业产出） | v0.5 补齐 `SPEC §3.8.1` 第 4 行 |

> 🔴 **v0.5 回改（B 类台账 B1）· `REVIVE` 整条删除**
> **依据**：用户裁定——**零回应复活作为普惠机制取消，投过了没人接即视为吸引力不足**。该裁定已被上游全面吸收：`SPEC §3.8.1`（保底组「v0.3：`REVIVE` 已删，本组只剩一路」）· `§6.2` 池枚举收敛为 `FRESH`/`STEADY`/`DRAINED`/`RESTRICTED` · `§7.1 C3`（冷启动保底位 **3 位全部由 `FRESH` 提供**）· `RK18` · `TC-RANK-49` 判据已改写。本文档 §8.7.3 的删除建议与 §7.1 `Q18` 的三处连带影响**均已被 `SPEC` v0.3 吸收完毕**，`Q18` 随之结案（§7.0a）。
> **配额不缩水**：保底位仍是每 20 条 **3 个位 = 15%**，只是 3 个位现在全给 `FRESH`。

🔴 **论证强度随之变化（这一条是本次回改的要点，不是文字调整）**：

| | v0.2.1 原论证 | 🔄 **v0.5 现论证**（对齐 `SPEC §3.8.2` v0.3 重写） |
|---|---|---|
| 前提 | 保底组有两路（`FRESH` + `REVIVE`） | **只剩 `FRESH` 一路** |
| `FRESH` 被热点圈定的后果 | 还有 1 个 `REVIVE` 位走独立通道能兑现 → **15% 缩水成 5%** | 🔴 **15% 缩水成 0**。唯一的保底来源就是这一路 |
| 结论的性质 | "别让保底缩水" | 🔴 **"它失效则整个保底机制失效"** —— 从"打折"变成"归零" |

→ 所以 §2.2.4「保底组全库直查」不再是一条优化约束，而是**15% 保底位能否兑现的唯一支点**。§2.2.6 的三条规则、§2.2.7 的降级阶梯、§2.2.8 的 `slotProvenance` 断言，全部因此**升级为不可让渡项**。

**我完全接受这个分组，并且认为修正抓住的那个失效模式比我 v0.2 写的那四条副作用都更要紧。** 它的要害不在"少召回了一些内容"，而在**失效是隐性的**：

> 保底位履约率报表会显示 **100%**（位置确实填满了），但北极星不动。因为填进去的是"恰好在热点人群内的新卡"——那些卡本来就有关系链和相关性召回能出头，**根本不需要保底位**。真正需要保底的那张卡（新注册、没亲友、没人关注、自己也不活跃）连候选集都进不去。

这条我 v0.2 没看出来。§2.2.5 里我列的"一次性发布者被排除"只说到了"内容少了"，没意识到**保底位会被无害地占满、从而让监控失明**。这是本轮最有价值的一条修正。

→ 因此本方案额外补一件排序规格没要求的事：**把「保底位履约率」的定义从"位置是否填满"改成"填充来源是否合法"，并加一个重叠率指标专门抓这种无用功**（§2.2.9）。否则修正落地了，我们也没有办法验证它真的生效了。

**分组的合理性（为什么这不是打补丁）**：`VEC` 与保底组解决的是两件方向相反的事——`VEC` 回答"跟我像的人留下了什么"（相关性，越准越好），保底组回答"谁的回忆还没被接住"（公平性，越是没人看见的越要给）。**用同一个候选集同时服务这两个目标，在定义上就是矛盾的**：热点在线是一个相关性/性能信号，它天然与"没被看见"负相关。拆开之后两组各自的候选集定义都变干净了。

**同时修正我 v0.2 的一处措辞**：v0.2 我写「按内容侧可召回性圈定被否」，这个表述现在**范围过宽、且与本节自相矛盾**，予以限定——

| 被否的 | 未被否的 |
|---|---|
| 🔴 "**全部通道**都改按内容侧可召回性圈定"（我 v0.1 的主张） | ✅ **保底组**仍然是按内容侧条件直查的：授权有效 ∧ 未下架 ∧ 可见 ∧ 池标签匹配 |

也就是说 v0.1 的做法并非整体被否，而是**被限定到了它真正适用的那一组**。相关性组用热点圈定、保底组用内容侧条件，两者各归其位，不存在冲突。

落地前仍有一个硬问题（§2.2.2）和四类副作用（§2.2.5）需要处理。

#### 2.2.2 🔴 硬问题：「在线」这个信号当前根本不存在

> **适用范围（v0.2.1 限定）**：本节的 `ActiveAccountSet` **只服务相关性组**（`REL`/`FOL`/`VEC`/`TAG`）与兜底热门层。**保底组不读它**（§2.2.7）。这个范围限定很重要——它意味着即使 `ActiveAccountSet` 完全没建好、或者恒为空，**15% 冷启动保底也照样能工作**。

这不是设计选择问题，是**前置工程量**问题。勘察结果：

| 想用的信号 | 现状 | 证据 |
|---|---|---|
| WS 在线态 | 🔴 **未实现** | `EchoSessionManager.java:17` 类注释原文：「BE-1 仅打通会话接入；登录鉴权、**在线态**、踢人等在后续里程碑补充」；`offline()` 覆写里只有一行 `log.info`（`:26-29`） |
| H5 用户的 WS 连接 | 🔴 **不存在** | `echo-h5-proto/src/**` 检索 `WebSocket`/`ws://` = 0 命中（§1.4） |
| HTTP 侧账号级活跃度 | 🔴 **不存在** | 全 `com.echo` 检索 `lastActive` 无命中；唯一相关的 `lastVisitAt` 只有一处（`EchoApi.java:388`），语义是**主人探访自己的宠物**，不是账号活跃度 |
| 会话存储 | 进程内 | `DEPLOY.md`：会话 token / onboarding / 光谱在进程内维护 |

→ **结论：照字面实现"热点在线人群"，得到的集合在当前架构下恒为空**（H5 用户永远不"在线"，因为他们不连 WS）。所以这个集合必须**先造出来**。

**建议的实现（最小可行，不引入新组件）**：

```
ActiveAccountSet（进程内，Aengine LRUCache）
  写入方：HTTP 网关的鉴权成功钩子（HttpGateway.java:207-214 之后）
          —— 每个通过 Bearer 校验的请求，把 accountId 记一次
          —— 只记 accountId + 时间戳，不记路径、不记内容
  结构  ：LRUCache<Long, Long>(maxElements=ECHO_VEC_ACTIVE_MAX, timeToIdle=ECHO_VEC_ACTIVE_TTL_SEC, 0, null)
          默认 maxElements = 5000（= 用户给的量级）
                timeToIdle  = 1800（30 分钟无请求即淘汰）
  淘汰  ：双重——LRU 满则淘汰最久未活跃；idle 超时自然过期
  读取  ：VEC 通道取 keySet() 作为候选账号 id 集合，下推成 SQL 的 accountId IN (...)
```

四个问题的明确答案：

| 问题 | 答案 |
|---|---|
| **谁写入** | HTTP 鉴权钩子（单点，一行代码）。**不用登录事件**——登录是低频的，会漏掉"长期不登出一直在用"的用户 |
| **何时淘汰** | LRU（容量 5000 满）+ idle 30 分钟，两者取先到 |
| **5000 是否合理** | ✅ 合理。它同时是"扫描成本上界"和"活跃人群规模上界"。DAU 3 万时 30 分钟窗口峰值约 5,700（§1.13.3）——**恰好落在 5000 附近，用户这个量级判断是准的**。性能侧的验算见 §2.3 |
| **冷启动集合为空** | 进程刚启动时集合为空 → `VEC` 通道返回空，配额按 `SPEC §3.3 规则 1` 转 `TOPIC`/`FRESH`。**不做预热**：预热要从 DB 捞"最近活跃账号"，而这个数据本身就不存在（见上表）。集合会在启动后几分钟内自然填充 |

⚠️ **多实例下这个集合是每进程独立的**，各实例看到的"活跃人群"不同 → 同一用户在不同实例上拿到的 `VEC` 结果不一致。P0 单进程无此问题；这是 §6 R2 的一个新增面。

#### 2.2.3 SQL 侧的候选集定义

候选账号 id 来自 `ActiveAccountSet`，但**能不能用**仍然全部由 SQL 谓词决定（门控不下放到内存，理由见 §2.7 L2）：

| # | 条件 | 落点 |
|---|---|---|
| 1 | `accountId IN (:activeSet)` | ⬅️ **本轮裁定新增**：热点在线圈定 |
| 2 | `t_self_vector.embedding IS NOT NULL` | SQL 谓词 |
| 3 | 授权四条件（`granted` ∧ `revokedAt IS NULL` ∧ 源素材未软删 ∧ `capability='向量检索'`） | **SQL JOIN**（§2.7 L2） |
| 4 | 账号状态正常（`t_account.status`） | SQL 谓词 |
| 5 | 排除 viewer 自己 / 双向拉黑 / `mutedUntil > now` | SQL 谓词（**下推，不超量拉取后再过滤**） |

`IN` 列表长度 = 活跃集大小（≤5000）。⚠️ 实现注意：5000 个参数的 `IN` 会让 PG 的执行计划劣化，**应改用 `= ANY(?::bigint[])` 传数组**（单参数绑定，计划稳定），而不是拼 5000 个 `?`。

保留 `ECHO_VEC_SCAN_MAX`（默认 20000）作为**第二道成本上界**：活跃集本身已被 5000 封顶，但若将来把活跃集调大，这道闸仍在。

#### 2.2.4 保底组（🔄 只有 `FRESH`）全库直查

本方案只定候选集获取与降级契约；池位规则本体属 `SPEC §6.2/§6.3`。

| 项 | 定义 |
|---|---|
| 候选来源 | **不查向量、不查活跃度、不读 `ActiveAccountSet`**。按池标签直查全库：`poolTag='FRESH'` + `n < D_min`（`SPEC §3.8.3`） |
| `FRESH` 排序键 | 🔄 **按 `W` 降序取 3 条**（`SPEC §3.8.3` v0.3；`W` 在快照作业里内存计算，§8.4.2），`approvedAt DESC` 仅作同权次级键 |
| ~~`REVIVE` 排序键~~ | 🔴 **v0.5 删除**（`REVIVE` 已整条取消，§2.2.1） |
| 配额 | 每 20 条 🔄 **3 个位全部由 `FRESH` 提供** = 15%（`SPEC §7.1 C3`）。**比例不变，构成变了**。本方案不自定 |
| 与相关性组的关系 | **完全解耦**：独立执行、独立超时、独立熔断。`VEC` 关掉/超时/熔断都不影响保底组；反之亦然 |
| 门控 | 保底组产出的是**卡**不是"相似账号"，不消费向量 → 不需要 L2 向量门控，但仍需卡本身的授权/可见性校验（与其他非向量通道同一套） |
| 🔴 排除项 | `originType='official'` 的卡命中本组时**从该路剔除**（`RK22` / `SPEC §8.1 H12`）——保底位只给真人新作者 |

> 🔴 **v0.5：本节的重要性已升级。** `REVIVE` 删除后 `FRESH` 是保底组的**唯一**来源，本节一旦被实现成"从相关性组候选里筛新卡"，15% 保底位**不是缩水而是归零**（推导见 §2.2.1 的论证强度表）。

> **一个额外好处**：保底组不依赖 `VEC`，意味着 `VEC` 在 P0 明确不做（§7 Q4）**完全不影响** 15% 冷启动保底。v0.1 我把两者绑在一起论证，反而放大了 `VEC` 的重要性。

#### 2.2.5 核实排序侧给的可行性论据

排序侧的论据是：「保底组不是全表扫描，而是按 `poolTag` 索引定位的小集合；池索引已在缓存里（TTL 60 s）、池位迁移由定时作业维护、不在请求路径上。实际成本约等于一次缓存读 + 60 秒一次的小范围索引查询。」

**逐条核实结论：论据基本属实，且比它自己说的更便宜。但有三处需要修正或补强。**

**① 索引查询代价 —— 属实，可以给出数字。**

目标查询形态：

```sql
SELECT "cardId" FROM "t_memory_card"
WHERE "poolTag" = ? AND "status" = ? AND "visibility" = ?
ORDER BY "approvedAt" DESC LIMIT 500;
```

前三列是**等值谓词**，第四列是排序键 → 在 `(poolTag, status, visibility, approvedAt)` 上是一次**连续区间的索引扫描**，代价 = B-tree 下降 + 取 limit 行：

| 项 | 估算 |
|---|---|
| 索引元组宽度 | poolTag/status/visibility 三个短 varchar + `approvedAt` bigint + ctid ≈ **50–60 B** |
| 单个 8 KB 索引页容纳 | ≈ 140 个元组 |
| 取 500 行需读 | ≈ 4 个叶子页 + 3–4 层 B-tree 下降 ≈ **7–8 次页读** |
| 命中 shared_buffers 时耗时 | **0.1–0.5 ms** |
| 100 万张卡时的变化 | B-tree 下降只多 1 层 → **仍是亚毫秒**（对数级，与总量几乎无关） |

→ **"小范围索引查询"这个描述准确。** 而且因为它是对数级的，不存在"卡多了就变慢"的风险。

🔴 **但有一个必须写死的实现约束**：这条查询**只能 select 索引里已有的列**（`cardId` + 排序键），才能走 **index-only scan**。一旦顺手多 select 几列（比如 `ownerAccountId`、`category` 给打散用），就要回表取 500 行随机堆页 → **0.5 ms 劣化到 5–50 ms**，慢 10–100 倍。
→ 做法：**保底组查询只取 id 列表**，卡的详情走既有的卡缓存批量取。注解建表也不支持 `INCLUDE`（§1.10），所以这条约束没有别的绕法。

**② `approvedAt DESC` 这个索引能不能自动建 —— 不能带 `DESC`，但不影响功能。**

`PgRepository.buildCreateIndexSQL` 拼列时只输出 `"列名"`，**没有排序方向**（`PgRepository.java:150-156`）：

```150:156:echo/echo-server/src/main/java/com/echo/infra/persistence/PgRepository.java
        List<String> cols = index.getColumns();
        for (int i = 0; i < cols.size(); i++) {
            sb.append('"').append(cols.get(i)).append('"');   // ← 只有列名，无 ASC/DESC
            if (i < cols.size() - 1) {
                sb.append(", ");
            }
        }
```

所以 `@Index` 建出来的是全 ASC 的 `(poolTag, status, visibility, approvedAt)`。

**好消息：这不影响功能。** 前三列是等值约束时，PostgreSQL 可以对该索引做**反向扫描（backward index scan）**来满足 `ORDER BY approvedAt DESC`，代价与正向相同。**`DESC` 关键字在这个形态下是可省的。**

→ 所以排序侧提的这条索引**可以走注解自动建表**，不需要手写 DDL。（仍需按 §1.10 把等价 DDL 同步进 `schema.sql` 作为 DBA 真源。）

**③ 🔴 索引的四个列里，当前有三个不存在。**

排序侧提的索引落在 `t_memory_card` 上，而那张表属 `SPEC-publish-and-ops`，**尚未落地**。当前充当"卡"的是 `t_pet`：

| 索引需要的列 | `t_pet` 有吗 |
|---|---|
| `visibility` | ✅ 有（`schema.sql:172`） |
| `poolTag` | 🔴 无 |
| `status` | 🔴 无 |
| `approvedAt` | 🔴 无 |

→ **P0 不能照抄这条索引。** 分两期落地：

| 期 | 保底组候选怎么取 | 说明 |
|---|---|---|
| **P0**（`t_memory_card` 未落地） | 直查**本方案自己的** `t_card_pool_state`：`WHERE pool=? ORDER BY lastBoostAt ASC / boostExposure` —— 走 §3.8 已定的 `idx(pool, lastBoostAt)` 与 `idx(pool, boostExposure)`；可见性/状态过滤在**快照构建时** join `t_pet` 完成 | ✅ 不依赖上游。join 的成本落在后台作业里（见 ④），不在请求路径 |
| **P1**（`t_memory_card` 落地后） | 迁到单表索引 `(poolTag, status, visibility, approvedAt)`，去掉 join | 需要上游把 `poolTag` 反规范化到卡表上，并由池位迁移作业维护一致性 |

**④ 「不在请求路径上」—— 属实，而且这是整个论据里最关键的一条，值得说透。**

因为候选集由**后台作业构建成内存快照**、请求只读快照，所以"全库直查"这件听起来很贵的事，其**请求期成本与库有多大完全无关**：

```
[后台] GuaranteePoolRefreshJob   每 60 s
         → 查 t_card_pool_state（索引扫描，0.1–0.5 ms）
         → join 卡表过滤可见性/状态（后台，慢一点也无所谓）
         → 构建 GuaranteePoolSnapshot{ freshIds[], reviveIds[], builtAt }
         → 原子替换引用（volatile 赋值，无锁）

[请求] 读 snapshot 的 id 列表 → 加权随机采样 → 取卡详情
         → 纯内存，无 IO，微秒级
```

→ 请求期代价 = **一次 volatile 读 + 一次采样**，比排序侧说的"一次缓存读"还便宜（连缓存查找的哈希都省了）。**"全库直查"与"热点在线圈定"在架构上确实正交**——这条论据成立。

🔴 **但要修正一处术语混淆**：排序侧说的"池索引已在缓存里（TTL 60 s）"里，有**两个不同的东西**必须分开，否则实现会做错：

| | `t_card_pool_state` | `GuaranteePoolSnapshot` |
|---|---|---|
| 是什么 | **持久池位状态**（哪张卡在哪个池、额度用了多少） | **内存候选 id 列表**（这一分钟保底位从这些 id 里选） |
| 谁维护 | `CardPoolTransitionJob`（每分钟，§3.4.4） | `GuaranteePoolRefreshJob`（每 60 s，本节新增） |
| 失效方式 | 无 TTL，是真相 | 60 s 重建 |
| 挂掉的后果 | 池位冻结（见 ⑥） | 快照陈旧（见 §2.2.8） |

**两个作业、两种失效模式、需要两个看门狗。** 把它们当成一个东西是本设计最容易出的实现错误。

**⑤ 缓存 TTL 60 s 对保底位新鲜度的影响 —— 可接受，但有一个反直觉的点要注意。**

| 影响 | 评估 |
|---|---|
| 新发布的卡最多晚 **60 s** 才进 `FRESH` 候选 | 🟢 **完全可接受**。卡在 `FRESH` 池里会待几天（~~额度 300 次曝光~~ 🔴 v0.6：配额说法作废，改为「直到 `n ≥ D_min` 或首个回声」，见 §8.4.3），晚 60 s 进池对它拿到的总曝光量影响 < 0.1%。结论不变 |
| 60 s 内快照是**固定的** | 🟡 需注意：同一分钟内所有请求从同一个 id 列表采样。**必须靠加权随机采样打散**（`SPEC §3.4`），不能按固定顺序取前 N 个——否则这 60 s 内所有用户的保底位看到的是同一批卡 |
| 额度已耗尽的卡在快照里继续待最多 60 s | 🟢 安全方向。多给几次曝光与北极星同向（§3.5 已论证）。叠加 §3.5 表 #6 的落库滞后，总滞后 ≤70 s，与既有承诺一致 |

**⑥ 定时作业维护池位的可靠性 —— 这是论据里最薄弱的一环，需要补三件事。**

`CardPoolTransitionJob` 一旦静默停摆，后果是**池位冻结**。🔄 **v0.5 修正后果评估**：`REVIVE` 删除后，原本"新的 `REVIVE` 不入池 = 该救的救不到"这一半**不存在了**——剩下的只有「`FRESH` 卡不毕业，继续占保底位」，方向是**多给曝光，安全**。
🔴 **但不能因此放松监控**，因为换来了一个新的不安全方向：新过审的卡**入不了 `FRESH` 池**（`poolEnteredAt` / `approvedAt` 反规范化列不刷新），而 `FRESH` 现在是保底组的唯一来源 → **新作者的第一张卡拿不到保底位**。这个方向比原来那个更要紧。而现有设施让"静默"这件事非常容易发生：

| 现存风险 | 证据 | 处置 |
|---|---|---|
| 调度器只有 **1 个线程**，已被 `EchoExpiryJob` 占用 | `EchoServer.java:186` `Scheduler.init("echo-scheduler", 1)` | 🔴 **必须提到 ≥4**（已列 P0-2）。否则池位迁移会被别的作业阻塞 |
| 作业异常被 `WrappedRunnable` 吞掉、**只留日志** | §1.6 已核实 | 每次成功运行必须落埋点并推进水位，**不能只靠日志** |
| 无人监控作业是否还活着 | — | 加**看门狗**：`now - lastSuccessfulRunAt > ECHO_POOL_TRANSITION_WATCHDOG_MS`（默认 **300000** = 5 分钟，容 5 次连续失败）即告警 |

新增两个埋点（并入 §3.7）：`rank_pool_transition_run{scanned, transitioned, durationMs, result}` 与 `rank_pool_snapshot_refresh{freshCount, reviveCount, buildMs, ageMs}`。

> **一句话总结核实结果**：排序侧的可行性论据**成立**，架构正交性判断正确，代价估算偏保守（实际更便宜）。需要补的是：只 select id 保持 index-only（①）、P0 先查 `t_card_pool_state` 因为上游三列还不存在（③）、把"持久状态"与"内存快照"分成两个东西两个看门狗（④⑥）。

#### 2.2.6 两组的时延预算分配

`SPEC §2.2` 给召回层整体 **≤120 ms**。两组**不共享预算、不共享线程池、不共享熔断器**：

| 组 | 预算 | 执行方式 | 失败影响 |
|---|---|---|---|
| **保底组** | **≤2 ms**（快照命中）<br>**≤15 ms**（快照缺失时同步兜一次查询） | 请求线程内**同步**读内存快照。**不进并行池** | 只影响保底位 |
| **相关性组** | **≤120 ms**（含 `VEC` 单路 ≤78 ms，§2.6.1） | `echo-recall` 并行池，各路 `Future.get(timeout)` | 只影响相关性位 |

🔴 **三条必须写死的规则**：

1. **保底组先算、且同步算。** 它只是一次 volatile 读 + 采样，把它丢进并行池反而更慢（线程调度开销 > 计算本身）。**更重要的是：它必须不能被相关性组的排队拖慢**——若两者共用线程池，`VEC` 打满池子时保底组会排队，15% 保底就变成了"看 `VEC` 心情"。
2. **保底组不设熔断。** 熔断的意义是"保护下游"，而保底组的下游是进程内存，没有需要保护的东西。给它加熔断只会引入一条把保底位关掉的路径。
3. **相关性组超时不得挤占保底位。** 编排层必须先把 3 个保底位（🔄 **v0.5：3 位全为 `FRESH`**）留出来，再用相关性组的结果填剩下 17 个。**顺序不能反**——先填满 20 条再"挤出"保底位，实现上一定会退化成"相关性组结果不够时才给保底"。

#### 2.2.7 保底组的降级阶梯（🔴 不得退化成从相关性组补位）

用户明确指出：保底组降级不能退化成"从相关性组补位，那等于取消保底"。**完全同意，这是本节的第一原则。** 阶梯如下：

| 级 | 触发条件 | 行为 | 埋点 |
|---|---|---|---|
| **D0** | 快照新鲜（`ageMs ≤ 120000`） | 正常采样 | — |
| **D1** | 快照陈旧（`120000 < ageMs ≤ ECHO_POOL_SNAPSHOT_MAX_AGE_MS`，默认 **600000** = 10 分钟） | ✅ **照常使用陈旧快照** + 告警。理由：陈旧快照的误差方向是"可能给已达额度的卡多几次曝光"，**与北极星同向**（§3.5 已论证）。为了新鲜度而放弃保底是本末倒置 | `rank_pool_snapshot_stale{ageMs}` |
| **D2** | 快照缺失/超龄/为空 | 同步兜一次索引查询（硬超时 **15 ms**） | `rank_pool_snapshot_miss` |
| ~~**D3**~~ | ~~D2 也失败或返回空 → 池内降级补位~~ | 🔴 **v0.5：本级整条取消，直接进 D4。**<br>原设计的池内补位链是「`FRESH` 缺 → `REVIVE` 补 → `LONGTAIL` 补」。现在**两个补位来源都不存在了**：`REVIVE` 已整条删除（§2.2.1）、`LONGTAIL` 已由 `SPEC` v0.2 移除且 `§7 Q17` 已结案维持移除（§8.7.5）。保底语义内**没有第二个池可退**，所以这一级失去了对象。<br>🔴 **绝不允许**把这一级改成"从相关性组补位"来填补它消失后的空档——那正是 §2.2.1 论证强度表所说"15% 归零"的具体实现方式 | — |
| **D4** | D2 失败或返回空（`FRESH` 池真的没有可投的卡，种子期会真实发生） | 🔴 **保底位留空**，这一屏输出 17 条而不是 20 条。**绝不用相关性组填** | `rank_pool_shortfall{pool:FRESH, wanted, got, action:leave_empty}` |

**为什么 D4 宁可少给 3 条也不补位**：保底位的全部意义在于"这个位置只给还没被看见的内容"。一旦允许相关性组补位，这个位置就失去了定义——而且**它会以"履约率 100%"的形式呈现在报表上**，正是修正要消灭的那种隐性失效。少 3 条是可见的、可解释的、会被追查的；补位是不可见的。

⚠️ **D4 在种子期是可能真实发生的**（`GTM` 目标 100–300 人，`SPEC §14 D21` 裁定已允许 feed 出现终点）。所以 `rank_pool_shortfall` 在种子期会有正常的非零值，**告警阈值需要按阶段设置**，不能一上线就按 0 报警（§7 Q12）。

#### 2.2.8 关键补充：把「保底位履约率」的定义改掉（否则修正无法验证）

这是本方案对修正的**主动补强**——排序规格没要求，但不做这一条，修正落地了也没人知道它有没有生效。

| | 现定义（会失明） | **建议定义** |
|---|---|---|
| 口径 | 每 20 条里保底位**是否被填满** | 保底位中**来自保底组候选集**的条数 / 应有保底位条数 |
| 用户描述的失效下的表现 | **100%**（位置确实满了） | **真实值**（被相关性组填的不计入分子） |

落地做法：给每个下发位打来源标签，随请求埋点上报。

```
slotProvenance ∈ {
    GUARANTEE_FRESH,     // 来自保底组 FRESH 快照（🔄 v0.5：保底位的唯一合法来源）
                         // 🔴 v0.5 删除 GUARANTEE_REVIVE（REVIVE 已取消）
                         // 🔴 v0.5 删除 GUARANTEE_FALLBACK（D3 池内补位已取消，无第二个池可退）
    RELEVANCE,           // 相关性组（🔴 出现在保底位上即违规）
    FALLBACK_HOT,        // 兜底热门层
    FALLBACK_RANDOM,     // 兜底随机层
    EMPTY                // D4 留空
}
```

🔴 **硬断言**：保底位上出现 `RELEVANCE` 即为**实现缺陷**，应当告警并在测试中断言为 0（建议加进 `TC-RANK-09` 的检查项）。

**再加一个专门抓"无用功"的指标**——用户举的例子里，保底位被"恰好在热点人群内的新卡"占满，这些卡**本来就能靠相关性出头**：

| 指标 | 口径 | 说明 |
|---|---|---|
| `rank_boost_slot_overlap` | 保底位命中的卡中，**同时也出现在本次请求相关性组候选里**的比例 | 这个比例越高，说明保底位越是在给"本来就能出头的卡"做无用功。健康值应当**很低**；若持续 > 50%，说明保底组的候选集事实上仍被相关性信号污染了 |

> 这两个指标合起来，才能把用户描述的那种"报表 100% 但北极星不动"的隐性失效变成**可观测**的。
> 🟢 **v0.5 更新：这条主动补强已被上游采纳。** `SPEC §3.8.5` 监控侧已写入「**保底位真实性**——保底位上的卡中同时能被相关性组召回的占比，🔴 持续 >50% 即告警」，与本节 `rank_boost_slot_overlap` 同一口径同一阈值。本节不再是"仅提出"，而是该指标的实现说明。

#### 2.2.9 ⚠️ 保留热点圈定后，还有哪些内容会被系统性排除

> **v0.2.1 更新**：下表原有 4 类，修正落地后**第 2、3 类已被保底组直查解决**（这正是修正的价值）。
> 🔄 **v0.5 更新**：第 1 类已关闭（前提被纠正，见 §3.11.3）、第 3 类整条移除（`LONGTAIL` 池不存在了）。**本表现在只剩第 2 类的一处收窄与第 4 类需要留意，两者都只影响相关性组、不影响保底位。**

裁定 + 修正共同覆盖了保底路径。但"相关性组按作者活跃度圈候选集"这个动作仍会排除以下内容：

| # | 被排除的内容 | 为什么被排除 | 修正后状态 |
|---|---|---|---|
| **1** | 🔄 **v0.5 改写**：**官方运营账号内容**（`originType='official'`，即种子内容的实际发布身份。原文写的 `seed_ai` / `seed_ops` 两个枚举值已被 `SPEC §5.3` 取消） | 运营真人的登录活跃度不稳定 → 其账号不一定在 `ActiveAccountSet` 内 → **相关性组（`TAG`/`VEC`/`FOL`）召回率不稳定**。而 `RK22`/`H12` 又规定 `official` 不占保底位 | ✅ **v0.5 关闭**。不再是"两头落空"：`SPEC §8.1 H12` 允许官方号经 `CURATED` 与 `FALLBACK` 随机层进入，而这两路按 `SPEC §3.8.1` **禁止**热点在线圈定、候选来源是全库——存在确定性通路。详见 §3.11.3 |
| **2** | **一次性发布者**：发完一条回忆就长期不回来的用户（情感陪伴类产品的主流画像之一——悼念宠物的人往往发一次、偶尔回看） | 不活跃 → 不进相关性组候选集 | ✅ **已由修正解决**（🔄 v0.5 收窄表述）。新卡由 `FRESH` 全库直查捞到（这正是修正针对的核心场景）。**相关性组召不到它不再是问题，因为保底组不看活跃度**。<br>⚠️ **但只覆盖扶持期（S1）内的卡**：原文"旧卡没被接住则进 `REVIVE`"这一半**已随 `REVIVE` 删除而失效**——投够了仍零回应的旧卡不再有池子接，它按 `SPEC §6.4` 自然流掉（搜得到推不到，§8.7.6）。这与 `SPEC §3.8.4` v0.3 对契约 C-7 的收窄同源，是裁定的直接后果，不是缺口 |
| ~~**3**~~ | ~~**`LONGTAIL` 池的作者**~~ | — | 🔴 **v0.5 整条移除**：该池已由 `SPEC` v0.2 删除，`§7 Q17` 已结案维持移除（§8.7.5），`§2.2.7` 的 D3 补位路径也已随之取消。**没有 `LONGTAIL` 池，就没有"`LONGTAIL` 池的作者"这一类** |
| **4** | **作息/时区错位的用户** | `ActiveAccountSet` 是"最近 30 分钟活跃"的滑动窗口。夜间用户在白天查询时不在集合里 → 相关性组结果带**时段偏置**，"相似"的口径掺入了"作息相似" | 🟡 **仅影响相关性组，不影响保底位**。严重度由"中低"降为"低"，建议只观测 |

**处置建议**：

| 建议 | 做法 | 覆盖 |
|---|---|---|
| ~~**A · 种子内容走独立通道**~~ | 🔴 **v0.5 撤回，不做**。依据 `SPEC §8.1 H12`（官方号可经 `CURATED` / `FALLBACK` / `SURGE` 进入，这些路不受热点圈定约束）+ `§7.1 C13`（官方号首屏 ≤2 条、独立计数）——通路已有、上限已封，再加一条固定配额的独立通道会与 C13 打架。原文的谓词 `originType IN ('seed_ai','seed_ops')` 本身也已失效（两个枚举值均被取消） | 1（已由规格覆盖） |
| **B · 活跃集加一条"发布即活跃"** | 发布回忆时也写一次 `ActiveAccountSet`，给一个更长的 idle 档（`ECHO_VEC_ACTIVE_PUBLISH_TTL_SEC`，默认 7 天）。**优先级由"必要"降为"可选"**——修正之后一次性发布者的内容已有保底组兜住，这条只是让它们**额外**有机会进相关性组 | 2（增强，非必需） |
| **C · 时段偏置只观测不处理** | 日作业统计相关性组召回结果的发布时段分布，偏斜超阈值再处理。**P0 不为它做设计** | 4 |

> 🔴 **v0.5 更新**：原文这里写「需要产品确认的是 A（§7 Q11）」。**该问题已由 `SPEC §8.1 H12` + `§7.1 C13` 正面回答，不需要产品再确认**（结案记录见 §7.0a）。剩下 B、C 两条维持原优先级不变。

#### 2.2.10 相关性组集合为空 / 降级怎么办

> **范围**：本节只讲**相关性组**（尤其 `VEC`）。保底组的降级另有阶梯，见 §2.2.7——两者不共用降级逻辑。

这不是假设，是**当前的默认状态**（§1.4，且叠加 §2.2.2 的冷启动）：

| 情形 | 处置 |
|---|---|
| viewer 自己没有向量 | `VEC` 通道对该 viewer 返回空；落 `rank_channel_empty{channel=VEC, reason=no_data}` |
| viewer 未授权「向量检索」 | 通道关闭；落 `rank_channel_empty{channel=VEC, reason=no_consent}` |
| 候选集为空 | 同上 `no_data` |
| **`ActiveAccountSet` 为空（进程冷启动，v0.2 新增）** | 同上 `no_data`。**不预热**（§2.2.2）；启动后几分钟自然填充。建议单独加一个 `reason=cold_start` 以便与"真的没数据"区分 |
| 通道被开关关闭 | `rank_channel_empty{channel=VEC, reason=disabled}` |
| 超时/异常/熔断 | `rank_channel_empty{channel=VEC, reason=error}` |

以上五种情形**统一处置：返回空列表**，配额按 `SPEC §3.3 规则 1` 转 `TOPIC`(+15) / `FRESH`(+15)。

🔴 **明确禁止的兜底**：不允许在 `VEC` 空/超时时"退化为随机取几张公开卡"。理由两条：① 会把一个坏掉的通道伪装成正常通道，掩盖问题；② 会让 `SPEC §10.2` 的「`VEC` 通道门控关闭占比」这个指标失真，而那个指标的用途正是"判断 `VEC` 是否值得投入"。

### 2.3 「5000 这个量级」是否合理 —— 定量估算

> ⚠️ **以下为估算，未实测。** 上线前必须在 pgvector 上跑基准（造 5k / 20k / 100k 行 × 768 维），把真实数字回填本节。估算方法与假设全部列出，便于校验。

**基础参数**：`d = 768`，`float4`（pgvector `vector` 类型），余弦距离算子 `<=>`。

**单向量体积**：768 × 4 B = 3,072 B ≈ **3 KB**。

| N（候选数） | 数据体积 | JVM 堆内驻留（含 `float[]` 对象头 16 B/条） |
|---|---|---|
| 500 | 1.5 MB | 1.5 MB |
| **5,000** | **15.4 MB** | **15.4 MB** |
| 20,000 | 61.4 MB | 61.4 MB |
| 100,000 | 307 MB | 307 MB ← 堆内驻留在这个量级需要单独规划 |

**单次距离计算量**：pgvector 的 `<=>` 不预归一化，每次算点积 + 两个模长 ≈ 3 × 768 ≈ **2,304 次浮点运算**。

**5,000 次距离 = 1.15 × 10⁷ 次浮点运算**：

| 路径 | 吞吐假设 | 纯计算耗时 | 内存带宽约束 | 含引擎开销的估计 |
|---|---|---|---|---|
| pgvector 精确扫描 | SIMD，但叠加元组解构 + 行外存储读取（768 维 = 3,076 B > 2 KB，`vector` 类型走 EXTERNAL 存储，多一次 TOAST 表读） | 0.6–1.2 ms | 读 15.4 MB @ 5–10 GB/s ≈ 1.5–3 ms | **3–10 ms** |
| JVM 堆内标量循环 | 1–2 GFLOP/s | 6–12 ms | 同上 1.5–3 ms | **6–12 ms** |
| JVM 堆内 + Vector API（SIMD） | 10–20 GFLOP/s | 0.6–1.2 ms | 同上 | **0.5–2 ms** |

**汇总预算表**：

| N | pgvector 精确扫描（估） | 堆内 SIMD 扫描（估） | 堆内内存 |
|---|---|---|---|
| 500 | < 1 ms | < 0.1 ms | 1.5 MB |
| **5,000** | **3–10 ms** | **0.5–2 ms** | **15 MB** |
| 20,000 | 12–40 ms | 2–8 ms | 61 MB |
| 100,000 | 60–200 ms | 10–40 ms | 307 MB |

**QPS 维度**（峰值集中度按 6× 日均估）：

| 场景 | DAU | feed 请求/人/天 | 峰值 QPS | 5,000 扫描的 CPU 占用（按 5 ms/次） |
|---|---|---|---|---|
| 种子期（`GTM` 目标 100–300 人） | 300 | 10 | **0.2** | 0.1% of 1 core |
| 早期 | 3,000 | 20 | 4.2 | 2% of 1 core |
| 中期 | 30,000 | 20 | 42 | 21% of 1 core |
| 目标期 | 300,000 | 20 | 417 | **2.1 cores** |

**结论（三条，都要说给产品）**：

1. ✅ **5,000 这个量级是合理的，且非常宽松。** 在 `SPEC §2.2` 给召回层的 **120 ms** 预算里，5,000 量级精确扫描占 3–10 ms（< 10%）。即便到 30 万 DAU，也只吃约 2 核。产品"向量扫描就够，不需要复杂索引"的直觉在这个数据规模下是**正确的**。
   > 补一条 v0.2 的交叉验证：5,000 这个数**同时**是两件事的合理上界——扫描成本上界（本节）和 DAU 3 万时 30 分钟活跃窗口的峰值规模（§1.13.3 算出 ~5,700）。两条独立推导落在同一个数量级，说明这个数不是拍的。
2. ⚠️ **但作为"性能优化"它在种子期是 no-op；它的正当性来自裁定而非性能。** 种子期目标 100–300 人（`SPEC §5.1`），而**实际有向量的账号数当前是 0**（§1.4）。全站账号 < 5,000 时，"限制到 5,000"不裁掉任何一行。
   → 所以要说清楚：`ActiveAccountSet` 这套维护逻辑（§2.2.2）**不是为了省这几毫秒**，而是为了实现裁定要求的"候选集 = 热点在线人群"这个**产品语义**。用性能理由论证它是站不住的；用"这是已裁定的召回语义"论证它是成立的。两者不要混。
3. 🔴 **扫描不是瓶颈，把工程精力花在这个数字上是错的。** `VEC` 单路的真实耗时构成（§2.7）里，向量扫描只占 40 ms 预算中的一部分；更贵的是**二段召回**（相似账号 → 其公开卡）与**连接池排队**（`maximumPoolSize=8` vs HTTP max 16 线程）。要设的上界是 `ECHO_VEC_SCAN_MAX`（默认 20000 ≈ 61 MB / 40 ms 量级），并把扫描耗时做成分项埋点（`rank_vec_scan.scanMs`），**用实测替代估算**。

**行数告警**：`t_self_vector` 行数 > `ECHO_VEC_SCAN_MAX` 时，日作业告警提示"考虑建 HNSW 索引"。注意 `schema.sql:67-69` 注释的是 `ivfflat`；若届时要建，建议改用 **HNSW**（`vector_cosine_ops`）——查询期召回率更稳、不需要按数据量调 `lists`。

> **反常识但正确的一条**：`N < 1 万` 时**不建 ANN 索引更好**。精确扫描召回率 100%；HNSW/IVFFlat 在小 N 下召回率有损（需要调 `ef_search`/`probes`），换来的时延收益又被"本来就只有几毫秒"抹平。当前 `schema.sql` 把索引注释掉，**恰好是对的**——只是需要把这个"对"变成一个有告警阈值的显式决定，而不是一个偶然。

### 2.4 向量放哪、怎么扫 —— 三条路的取舍

| | **A. pgvector 读查询**（去掉写副作用） | **B. 全量驻留 JVM 内存扫描** | **C. Redis 存向量** |
|---|---|---|---|
| 做法 | `SELECT accountId, embedding <=> ? FROM t_self_vector JOIN t_ai_consent ... ORDER BY ... LIMIT k` | 启动装载 `float[][]`，增量刷新，SIMD/堆内扫描，bounded min-heap 取 top-K | 向量存 Redis，客户端拉取后扫描；或引 RediSearch 向量索引 |
| 时延（5k） | 3–10 ms | 0.5–2 ms | 拉 15.4 MB 网络 → **不可行**；RediSearch 侧算 → 需新模块 |
| 内存 | 0（走 PG shared buffers） | 15 MB（5k）/ 307 MB（100k） | Redis 侧 15 MB + 客户端副本 |
| **授权门控** | ✅ **同一条 SQL 内 JOIN，强一致** | ⚠️ 内存里没有 consent 表 → 只能应用层过滤 + 额外失效通道 | ⚠️ 同 B，且**多一份副本要保证失效** |
| **撤回失效延迟** | **0**（同一查询快照） | 0（同步驱逐）/ 60 s（兜底对账） | 同 B |
| 与 `G0-10 ④` 核查 SQL 的一致性 | ✅ 线上过滤逻辑与核查 SQL 是**同一份逻辑** | ⚠️ 两份逻辑，可能漂移 | ⚠️ 同 B |
| 新增运维组件 | 0 | 0 | **1 个（Redis）** |
| 新增故障域 | 0 | 0（堆内） | 1（网络 + 内存淘汰 + 持久化配置） |
| 代码改动量 | 小（改 `topN` 加过滤重载） | 中（新建镜像 + 刷新 + 失效通道 + 对账） | 大（客户端封装 + 序列化 + 失效 + 运维） |
| **判决** | ✅ **P0 推荐** | ⚠️ **可选加速层（L2）**，触发条件见下 | ⏸ **P0 不做**（v0.2 措辞修正：**不是"永远不该"**，触发条件与完整加固设计见 §2.10） |

> 🆕 **v0.2 重要修正**：本表 C 列原本只评估了"Redis 当 KV / 当持久副本"这两种形态，**漏了 `Redis Stack + RediSearch 向量索引` 这一种**——而那才是"删 key 就完事了"真正成立的形态。**§2.10 是对 C 列的完整重做，以 §2.10 为准；本表 C 列仅保留作对照。**

#### 推荐：A（P0）→ 需要时先建 pgvector HNSW 索引（免费）→ B 作为进程内加速层 → Redis 排在最后且与多实例决策捆绑（升级阶梯见 §2.10.6）

**为什么 A 而不是 B——决定性理由是合规，不是性能。**

`G0-10 ②` 要求授权四条件校验，任一不成立则"该素材连同其派生出的一切退出本次调用"；`TC-CARD-03` 类要求撤回/移除 **≤5 s** 生效。

- 走 **A**：四条件过滤就是同一条 SQL 的 JOIN。用户点"关闭向量检索"的那一刻，下一次查询就读不到他的向量了——**零失效延迟，无需任何失效通道**。而且线上实际执行的过滤条件与 `G0-10 ④` 的日核查 SQL 是同一份逻辑，不会漂移。
- 走 **B**：内存里只有向量数值，没有 consent 表。要保证 ≤5 s 失效，必须额外建一条失效通道（撤回时同步驱逐 + 定时对账兜底）。**每多一处这样的地方，就多一处可能漏的合规缺口**，而合规缺口的代价是法律风险，向量扫描慢 5 ms 的代价是 5 ms。

**B 启用的触发条件（两条都满足才做）**：
1. `t_self_vector` 有效行数 > `ECHO_VEC_SCAN_MAX`（默认 20000）；**且**
2. `rank_vec_scan.scanMs` 的 P95 实测 > 40 ms（即真的吃掉了 `VEC` 单路预算的一半以上）。

**B 的关键结构（如果启用）—— 缓存"贵且可缓存的"，实时"必须实时的"**：

```
镜像只缓存"向量数值"（贵，可缓存，变化极慢）
门控判定永远回源  （便宜，必须实时）

流程：
  1. 内存镜像扫描 N 个候选 → top-K（K ≤ 30，不是 5000）
  2. 对这 K 个做一次 SQL 门控复核：
     SELECT "accountId" FROM t_self_vector v JOIN t_ai_consent c ...
     WHERE v."accountId" = ANY(?)   -- K 个，一次查询
  3. 复核未通过的剔除
```

这个结构让"内存加速"与"授权强一致"可以共存：昂贵的距离计算（5,000 次）走缓存，必须实时的授权判定（30 次）走 SQL。**这是 B 方案唯一可接受的形态**；任何"内存里自己判 granted"的写法，按 `G0-10 ③` 应当 CR 打回。

镜像的失效机制（三层）：
1. 撤回是低频写事件（用户在「我」页点关闭）→ 在 `POST /consents/:id/revoke` 同一次请求里**同步驱逐**镜像条目（进程内 remove，微秒级）。
2. 兜底对账：每 `ECHO_VEC_MIRROR_REFRESH_MS`（默认 60 s）拉 `accountId, normHash, consentValid` 三列（**不拉向量本体**，成本极低）对账，`consentValid=false` 即驱逐。最坏失效延迟 60 s。
3. 🔴 因为第 2 层的 60 s **超过了 5 s 要求**，所以镜像**不得作为门控依据**——这正是上面 top-K 复核存在的原因。

**为什么 C 在 P0 不做（四条，按重要度）** —— ⚠️ 以下四条写于 v0.1，其中**第 1 条已被 §2.10.3 推翻**（删 key + 完整加固能可靠达成合规诉求），保留在此仅为记录论证演进；**当前有效的论证是 §2.10.5 的成本收益账**：

1. ~~**合规成本 > 性能收益。** 多一份向量副本 = 多一处必须保证 ≤5 s 失效的地方，且 Redis 里没有 consent 表，判定只能在应用层做。~~ 🔴 **此条已作废（v0.2）**：`RediSearch` 形态下扫描发生在 Redis 内部，删 hash key 即从索引移除；配合事务外发件箱 + 陈旧度熔断，**失效延迟 ≤1 s 且 Redis 故障时 fail-closed**，合规诉求可被可靠达成。见 §2.10.3 逐条分析。
2. **Redis 的核心增益在当前架构下拿不到。** Redis 相对 JVM 内存的本质优势是**跨进程共享状态**。当前是单进程部署（`DEPLOY.md`「一台/一组」；会话 token/onboarding/光谱都在进程内；"多实例…为 TODO"）。单进程下 Redis 相对堆内 Map 的唯一增益是"重启不丢"，而**向量是可从 PG 秒级重建的派生数据**（一次全量 `SELECT`），这个增益价值接近 0。
3. **技术上走不通或代价过高。** 向量存 Redis 后：若在应用层扫描，每次请求要拉 15.4 MB（不可行）；若常驻本地副本，Redis 退化成"一个持久化备份"，而 PG 已经是这个角色；若在 Redis 侧算距离，需引入 RediSearch/Redis Stack 向量索引——那是一个比 pgvector 更重的新组件，而 pgvector **已经在库里、已有实现、已有单测**。
4. **运维成本被低估了（但要说清好消息在哪）。** 好消息比想象中多：不仅 `jedis 6.0.0` 已在 classpath，Aengine 还有一套 1,245 行的 `Redis` 封装，计数器/Set/ZSet/per-key TTL 全都现成（§1.8）——**写代码这一步几乎是免费的**。坏消息：真实成本 100% 在**服务、配置、健康检查、故障域、备份、`RUNBOOK.md`/`DEPLOY.md` 条目、以及"Redis 挂了共鸣厅怎么办"的降级链**。这些成本与"少 3 ms"不成比例。
   > ⚠️ **不要用"客户端已经写好了"来论证应该引入 Redis。** 前三条否决理由（合规副本数、单进程拿不到增益、技术上走不通）与客户端成熟度完全无关；封装现成只意味着**将来真该引入时会很快**，不意味着现在就该引入。

**引入 Redis 的明确触发条件（写下来，避免以后再争）**：当**同时**满足
① 部署形态变为 ≥2 个 `echo-server` 实例；**且**
② 会话 token / feed 快照 / 曝光计数 需要跨实例一致
时，应当**一次性**引入 Redis 并同时承载 session / snapshot / exposure / rate-limit 四类状态，而**不是**为一个向量缓存单独引入。
注意前置依赖：多实例当前是被**会话 token 的进程内存储**卡着的（§1.8），不是被缓存卡着的。

### 2.5 写副作用怎么处理 —— 接口拆分方案

采纳 `SPEC §12.6 / §15 Q8` 的**方案 A**，并在其之上加两条。

#### 2.5.1 拆分（`ResonanceService`）

```java
/** 无副作用只读查询：给 feed / 任何高频路径用。不写库、不进缓存、不留痕。 */
public List<ScoredId> findSimilar(SimilarQuery query);

/** 原语义保留：= findSimilar + persistRecords。WS 1401 继续调它，签名与行为零变化。 */
public List<ScoredId> queryResonance(long accountId, int topN, double threshold);
```

```java
/**
 * 相似账号检索入参。
 * 注意：不提供"跳过门控"的开关 —— 门控是 G0-10 的硬约束，不是可配置项。
 * 「关掉门控」这件事必须是"改代码 + 过 CR"，不能是"传个 false"。
 */
public record SimilarQuery(
        long viewerId,
        int topN,
        double maxDistance,
        Set<Long> excludeAccountIds  // 自己/双向拉黑/mute 生效中；下推到 SQL，不在应用层过滤
) {}
```

- WS `ResonanceHandler.onQueryResonance`（`ResonanceHandler.java:33`）**不动**，继续调 `queryResonance` → WS 侧行为零变化，`ResonanceServiceTest.java:50,68` 的两条 `verify` 断言**不需要改**。
- feed 侧只调 `findSimilar`。
- 符合 `QA6`「HTTP 真正复用 WS 侧领域服务，非平行自建域」。
  ⚠️ **这是本设计这一处的局部符合，不代表 `QA6` 已整体达成**——全局仍是两套平行域
  （`SPEC-admin-console §0.2`、`PRODUCT-MINDMAP B10`、`TECH-DB-INVENTORY §6` 均已核实）。
  🔴 事实上，`ResonanceService` 是目前**唯一**被两侧共用的领域服务，值得作为迁移的样板。

#### 2.5.2 加的第一条：`persistRecords` 本身也是缺陷，要一并改

即使只有 WS 1401 调用它，现在的实现也是"循环单条 INSERT + 每条一次连接获取"（§1.2）。10 个候选 = 10 次连接获取 + 10 次往返，在 8 连接的池上。

**改法**：给 `PgDb` 加一个真正的 `PreparedStatement` 批量方法（现有 `batch(List<String>)` 只接受 SQL 字符串，`PgDb.java:129-140`）：

```java
/** PreparedStatement 批量绑定执行；单连接、单事务、一次往返。 */
public int[] batchUpdate(String sql, List<PgStatementBinder> binders) throws SQLException;
```

并让 `PgRepository.add(List<T>)` 走它（当前是 for 循环，`PgRepository.java:407-415`）。**这个改动对全工程所有仓储都有收益**，也是 §3.4 曝光批量落库的前提。

> 这是一个独立于本次拆分的既有缺陷。建议单独一个 PR，先合它。

#### 2.5.3 加的第二条：`t_resonance_record` 要么给保留期，要么废弃

留着一张**没人读、无保留期、单调增长**的表，只是把同一个问题的增速放慢，不是解决它。两个选项（需拍板，🔄 **v0.5 更正引用：是 §7 `Q8`，原文误写 `Q1`**——`Q1` 讲的是候选集圈定依据，与本表无关，且已结案）：

| 选项 | 做法 | 评价 |
|---|---|---|
| **A（我倾向）· 废弃** | 删掉 `persistRecords` 调用，`ResonanceRecord`/`Repository` 标 `@Deprecated`，表在下个版本 drop | 零消费者（§1.1 已逐条反查）。"以后可能有用"不是保留**写入**的理由——真需要时，`SPEC §5.4 P0` 的**影子日志**（每次精排落 `(reqId, cardId, 各特征值, poolTag, score, 最终位次)`，保留 30 天）能提供比这张表完整得多的数据 |
| **B · 保留 + TTL** | 保留 `queryResonance` 的写入；加日作业删 `createTime < now - ECHO_RESONANCE_RECORD_TTL_DAYS`（默认 30）；索引改 `(accountId, createTime DESC)` | 保守。代价是永久保留一条无人消费的写路径与一个要维护的清理作业 |

无论选哪个，**feed 侧走 `findSimilar`（无写入）这一点不变**。

### 2.6 时延预算与降级

`SPEC §2.2` 给召回层整体 **≤120 ms**（7 路并行），`VEC` 配额 30。

#### 2.6.1 `VEC` 单路预算分解

| 步骤 | 预算 | 超时/失败处置 |
|---|---|---|
| L1 门控：viewer 的「向量检索」授权 | ≤3 ms（缓存命中 ≤0.1 ms） | 取不到 → **视为未授权** → 通道关闭 |
| 取 viewer 自己的向量 | ≤5 ms | 取不到 → 通道空（`no_data`） |
| 相似账号扫描（含 L2 门控 JOIN，topN=30） | ≤40 ms | 超时 → 通道空（`error`） |
| 二段召回：相似账号 → 其公开卡 | ≤25 ms | 超时 → 用已拿到的部分 |
| L3 出口复核 | ≤5 ms | 未通过项剔除 |
| **`VEC` 单路合计** | **≤78 ms** | **硬超时 `ECHO_VEC_TIMEOUT_MS` = 80 ms** |

#### 2.6.2 三条必须写死的规则

**① `VEC` 必须并行执行，不能占用请求线程串行等待。**
当前 HTTP 池是 core 4 / max 16 / queue 256（`EchoHttpBootstrap.java:86-89`）。若 7 路召回都在请求线程上串行跑，总时延会退化成各路耗时之和，`SPEC §2.2` 的 120 ms 预算必然破。
→ 需要一个独立的召回并行池：`NamedThreadFactory("echo-recall")`，size = 2 × CPU，**有界队列 + `CallerRunsPolicy`**（队列满时退化为调用方执行，保证不丢请求、只慢不错）。各路 `Future.get(timeout)`，超时即取该路为空。

**② fail-closed，不是 fail-open。**
门控查询失败/超时时，按**未授权**处理（关闭通道），不是"查不到就放行"。这与常规的降级直觉相反，但它是 `G0-10` 的硬约束语义（"任一不成立 → 退出本次调用"）。要在代码注释与 CR 清单里写明，否则一定会有人为了"提高可用性"把它改成 fail-open。

**③ 降级返回空，不返回兜底数据。**
见 §2.2.3。配额转移由编排层处理。🔴 禁止退化为"随机取几张公开卡"。

**④ 熔断。** 连续 `ECHO_VEC_BREAKER_THRESHOLD`（默认 20）次超时/异常 → 该通道熔断 `ECHO_VEC_BREAKER_COOLDOWN_MS`（默认 60 s），期间直接返回空 + 落 `rank_channel_empty{reason=error}`。避免一个慢向量查询把整个 feed 拖垮（连接池只有 8 个）。

#### 2.6.3 与 `SPEC §12.7` 降级链的对应

本节的降级完全落在 `SPEC §12.7` 的 **L1**（"向量库不可用 / 门控拒绝 → 关闭 VEC，配额转 TOPIC + FRESH"）。本方案不新增降级层级，也**不改变末端不得按热度排**这条红线。

### 2.7 授权门控卡在哪一层

**三层，缺一不可。** 对应 `G0-10 ②` 的"该素材及其全部派生物退出本次调用"语义。

| 层 | 卡什么 | 怎么卡 | 失效延迟 |
|---|---|---|---|
| **L1 · 通道入口（viewer 侧）** | viewer 自己是否授权「向量检索」 | `IConsentGate.assertUsable(viewerMaterialRef, "向量检索")`；不通过 → 整个 `VEC` 通道对该 viewer 关闭（没有合法的 query 向量）。= `SPEC §3.3 规则 1` | ≤5 s（门控缓存 TTL 上限，见下） |
| **L2 · 检索谓词（被召回侧，同一条 SQL 内）** | 候选账号的向量能否被参考 | 向量检索 SQL **直接 JOIN `t_ai_consent`** 做四条件过滤。🔴 **不在应用层过滤**。= `SPEC §3.3 规则 2` / `H9` | **0**（同一查询快照，强一致） |
| **L3 · 结果出口** | 二段召回出来的卡是否携带来自已撤回向量的派生特征 | 若某卡的 `resonanceAffinity`（`SPEC §4.1 F2`）源自已撤回的向量 → 该特征置 0 且从 `VEC` 归属剔除（该卡仍可经其他通道进来——其他通道不消费向量） | ≤5 s |

**L2 必须在 SQL 里，这是本方案对"向量放哪"的决定性论据**（已在 §2.4 展开）：向量留在 pgvector → 四条件是 JOIN → 撤回零失效延迟，且线上过滤逻辑与 `G0-10 ④` 的核查 SQL 同源。

**门控结果可以缓存吗**——可以，但 TTL 必须 ≤5 s：

| 缓存 | 内容 | TTL | 理由 |
|---|---|---|---|
| `consentGate:{accountId}:向量检索` | 布尔 | **5 s** | L1 每请求都要查；5 s 是 `TC-CARD-03` 类要求的上限，不能再长 |
| — | L2 的过滤结果 | 🔴 **不缓存** | 它是 SQL 谓词，缓存它就等于把强一致降级成最终一致 |

外加：撤回接口（`POST /consents/:id/revoke`）应在同一次请求里**主动失效** L1 缓存条目，让实际失效延迟接近 0，5 s TTL 只是兜底。

**缓存的向量在授权撤回后如何失效**：见 §2.4 的三层机制（同步驱逐 / 60 s 对账兜底 / top-K SQL 复核）。核心结论重复一次，因为它是这个问题的答案：**镜像只缓存向量数值，"能不能用"这个判断永远回源**。

**前置依赖（必须先做，否则 L2 无法实现）**：

| # | 前置项 | 现状 |
|---|---|---|
| 1 | `IConsentGate` 接口 + `t_ai_consent` 表 | 🔴 都不存在（§1.9） |
| 2 | `t_self_vector` 补 `materialRef` / `consentRef` 两列 | 🔴 缺失（`schema.sql:57-65`），`G0-10 ①` 已明确要求本期补齐 |
| 3 | ArchUnit（或等价）规则：`com.echo.module.rank` / `com.echo.module.resonance` **不得 import 或查询 `t_ai_consent`**，只能经 `IConsentGate` | 🔴 无 ArchUnit 依赖 |

→ 这三条是 `VEC` 通道的**硬前置**。在它们齐备之前，`ECHO_RANK_CHANNEL_VEC_ENABLED` 保持 `false`。

### 2.8 接口定义汇总

```java
// ── com.echo.module.resonance.ResonanceService（改造）
public List<ScoredId> findSimilar(SimilarQuery query);                              // 新增：无副作用
public List<ScoredId> queryResonance(long accountId, int topN, double threshold);   // 保留：签名/行为不变
public record SimilarQuery(long viewerId, int topN, double maxDistance,
                          Set<Long> excludeAccountIds) {}

// ── com.echo.infra.vector.IVectorStore（新增重载，对齐 SPEC §11 P1-8）
/**
 * 带门控与排除集的 Top-K 检索。
 * 实现约定（PgVectorStore）：门控四条件与 excludeAccountIds 一律作为 SQL 谓词下推，
 * 禁止"超量拉取后在应用层过滤"（那会让 LIMIT k 语义失真，且门控可被绕过）。
 */
List<ScoredId> topN(VectorQuery query);

public record VectorQuery(
        float[] embedding,
        int k,
        double maxDistance,
        Set<Long> excludeAccountIds,
        String capability,   // 恒 "向量检索"；显式传入以便 CR/审计能搜到调用点
        int scanMax          // ECHO_VEC_SCAN_MAX；> 0 时启用 id 取模轮转采样
) {}

// 既有 topN(float[], int, double) 保留（WS 1401 与既有单测在用），
// 但标注：新调用点一律用 VectorQuery 重载。

// ── 待建（合规前置，不属本方案交付范围，但本方案依赖它）
public interface IConsentGate {
    void assertUsable(long materialRef, String capability);      // 不通过即抛出
    boolean isUsable(long materialRef, String capability);        // 供 L1 通道开关判定
    Set<Long> filterUsable(Set<Long> materialRefs, String capability); // 供 L3 批量复核
}
```

### 2.9 配置项（问题一）

| 环境变量 | 默认 | 含义 |
|---|---|---|
| `ECHO_RANK_CHANNEL_VEC_ENABLED` | **`false`** | `VEC` 通道总开关（`SPEC §3.3 规则 3` 已定默认 false，本方案沿用不改） |
| `ECHO_VEC_TOPN` | `30` | 单次相似账号召回数（= `SPEC §3.1` 的 `VEC` 配额） |
| `ECHO_VEC_MAX_DISTANCE` | `0.75` | 余弦距离上限（对应 `toAffinity` ≥ 0.25，口径同 `ResonanceHandler.java:47-53`） |
| **`ECHO_VEC_ACTIVE_MAX`** | **`5000`** | 🆕 v0.2 · `ActiveAccountSet` 容量上界（= 裁定的「热点在线约 5000」，§2.2.2） |
| **`ECHO_VEC_ACTIVE_TTL_SEC`** | **`1800`** | 🆕 v0.2 · 活跃集 idle 淘汰时长（30 分钟无请求即移出） |
| **`ECHO_VEC_ACTIVE_PUBLISH_TTL_SEC`** | **`604800`** | 🆕 v0.2 · 「发布即活跃」的独立档位（7 天），兜住一次性发布者（§2.2.5 建议 B）。`0` = 关闭该档 |
| `ECHO_VEC_SCAN_MAX` | `20000` | 第二道成本上界（活跃集已被 5000 封顶，此项为将来调大活跃集时的兜底） |
| **`ECHO_POOL_SNAPSHOT_REFRESH_MS`** | **`60000`** | 🆕 v0.2.1 · 保底组内存快照重建间隔（§2.2.5 ④） |
| **`ECHO_POOL_SNAPSHOT_SIZE`** | **`500`** | 🆕 v0.2.1 · 每个池快照保留的候选 id 数上界。🔴 查询只取 id 以保持 index-only（§2.2.5 ①） |
| **`ECHO_POOL_SNAPSHOT_MAX_AGE_MS`** | **`600000`** | 🆕 v0.2.1 · 快照可用龄上限（10 分钟）。超过转 D2 同步兜查（§2.2.7） |
| **`ECHO_POOL_SNAPSHOT_SYNC_TIMEOUT_MS`** | **`15`** | 🆕 v0.2.1 · D2 同步兜查硬超时 |
| **`ECHO_POOL_TRANSITION_WATCHDOG_MS`** | **`300000`** | 🆕 v0.2.1 · 池位迁移作业看门狗（5 分钟无成功运行即告警，§2.2.5 ⑥） |
| `ECHO_VEC_TIMEOUT_MS` | `80` | `VEC` 单路硬超时 |
| `ECHO_VEC_BREAKER_THRESHOLD` | `20` | 连续失败触发熔断的次数 |
| `ECHO_VEC_BREAKER_COOLDOWN_MS` | `60000` | 熔断冷却时长 |
| `ECHO_VEC_CONSENT_CACHE_TTL_MS` | `5000` | L1 门控结果缓存 TTL（🔴 **上限 5000，不得调大**） |
| `ECHO_VEC_MIRROR_ENABLED` | **`false`** | L2 进程内向量镜像开关（§2.10.6 阶梯） |
| `ECHO_VEC_MIRROR_REFRESH_MS` | `60000` | 镜像兜底对账间隔 |
| `ECHO_RESONANCE_RECORD_TTL_DAYS` | `30` | `t_resonance_record` 保留期（`0` = 不清理；若 §7 Q8 判废弃则此项作废） |

装配形态：新增 `record RecallConfig(...)`，`fromEnv()` / `from(Function<String,String>)` 双入口，与 `EmbeddingConfig.java:23-47` 完全同构。

> 🆕 v0.2 · **`ECHO_VEC_*` 若将来走 §2.10.7 的 Redis 形态**，需再加：`ECHO_VEC_STALENESS_MAX_MS`（默认 5000，陈旧度熔断阈值）· `ECHO_VEC_SYNC_INTERVAL_MS`（默认 1000）· `ECHO_VEC_SYNC_FULL_CRON`（默认 `0 0 3 * * *`）。**P0 不引入**，列在这里是为了让 §2.10.7 的设计完整可执行。

### 2.10 重新论证：Redis 存向量 + 撤回时删 key（v0.2 新增）

> 用户的反驳：**「redis 存向量怎么了，用户说了取消授权，就先移除 redis 里面的 key 不就完事了吗」**
>
> 这个反驳是对的，我 v0.1 的论证有实质缺陷。本节重新论证，并且**不用合规当挡箭牌**——只讨论"能不能可靠达成'撤回后不再被使用'这个结果"，能达成就是合规的。

#### 2.10.1 先承认：我 v0.1 的论证错在哪

v0.1 我写的是「多一份副本 = 多一处必须保证 ≤5 s 失效的地方，而任何失效机制都有窗口期」。这句话的问题：

| 缺陷 | 说明 |
|---|---|
| **它是一个通用反对句式，不是分析** | 按同样的逻辑，任何缓存都不该存在——但我自己在 §2.7 就设计了 5 s TTL 的门控缓存、在 §3.2 用了内存去重集合。**标准前后不一致。** |
| **"有窗口期"没有量化** | 窗口期 5 ms 和 5 小时是完全不同的结论。不给数字就等于没论证 |
| **没有区分"可修复的窗口"与"不可修复的污染"** | 真正值得担心的不是"延迟几秒生效"，而是"某个失败路径会让旧向量**永久**留在缓存里且没人发现"。这才是该逐条排查的东西 |
| **把"结构上不可能出错"当成了论据** | 用户批评得对：这是一种偏好，不是论证。**能被可靠保证的正确性，和结构上不可能出错的正确性，在合规上是等价的** |

#### 2.10.2 关键澄清：Redis 存向量有三种形态，只有一种能让「删 key」真正成立

讨论"删 key 就完事了"之前，必须先确定向量到底在哪里被扫描——**因为这决定了删 key 有没有用**：

| 形态 | 做法 | 删 key 管不管用 | 判决 |
|---|---|---|---|
| **C1 · Redis 当纯 KV，客户端拉回来扫** | `MGET` 5000 个向量 → JVM 里算距离 | ✅ 管用（拉不到就是拉不到） | 🔴 **不可行**：每次请求要传 **15.4 MB**。千兆网 ≈ 123 ms 纯传输；即便走 loopback，也要每请求反序列化 5000 个 `float[768]` = **15 MB 垃圾/请求**，GC 压力直接压死。这条路在时延上比 pgvector 差一个数量级 |
| **C2 · Redis 当持久副本，JVM 本地镜像扫** | 启动/定时从 Redis 灌进本地 `float[][]`，扫本地 | 🔴 **不管用** | ⚠️ **这是关键点**：读路径根本不碰 Redis，删 Redis 的 key **不会**让本地镜像里那份消失。仍然需要一套镜像失效机制——也就是说，"删 key"并没有解决问题，只是把问题从 Redis 挪到了本地镜像。这等于 §2.4 的 B 方案外加一个 Redis |
| **C3 · Redis Stack / RediSearch 向量索引，扫描在 Redis 内部** | `FT.CREATE` 建 HNSW 索引，`FT.SEARCH` 带 KNN 查询 | ✅ **真正管用** | ✅ **这才是用户设想成立的那个形态**：删掉 hash key，RediSearch 会把它从索引里一并移除，下一次 `FT.SEARCH` 就搜不到了。**下面全部按 C3 论证** |

> **给用户的一句话**：你的方案在 **C3** 下是完全成立的，我上一轮没有把这个形态单独拎出来评估，直接按 C2 的口径否掉了，这是论证不完整。C3 值得认真算账。
>
> ⚠️ 顺带一个成本提示：C3 需要的是 **Redis Stack（带 RediSearch 模块）**，不是普通 Redis。而 Aengine 那套 `Redis` 封装（§1.8）包的是普通命令，**没有 `FT.*` 系列**——这部分要绕过 Aengine 直接用 Jedis 的 search API，属于新代码。

#### 2.10.3 五种失败模式逐条分析（按用户列的清单）

> 结论先给：**五条全部有成熟解法，其中四条能做到"零残余风险"，一条（Redis 宕机期间）需要用熔断把风险转成可用性损失。** 所以 C3 + 完整加固**能可靠达成合规诉求**。

| # | 失败模式 | 触发条件与概率 | 不加固的后果 | 成熟解法（具体做法） | 残余风险 |
|---|---|---|---|---|---|
| **F1** | **撤回事务提交了，但删 key 失败**（Redis 宕机 / 网络分区 / 进程在两步之间崩溃） | Redis 单机可用性按 99.9% 计 ≈ **8.8 小时/年**。撤回是低频用户动作，但只要撞上就中招 | 🔴 **最严重**：旧向量**永久**留在索引里，且用户界面已显示"已关闭"。没有任何人会发现 | **事务外发件箱（transactional outbox）**：撤回时在**同一个 DB 事务**里写一行 `t_consent_revoke_outbox{materialRef, capability, createdAt, doneAt}`；一个 1 秒间隔的 worker 扫 `doneAt IS NULL`，执行 `DEL` + `FT` 索引删除，成功才回写 `doneAt`。失败就下一轮重试，**永不放弃** | ⚠️ Redis 宕机期间积压。**必须叠加 F1-b** |
| **F1-b** | 上面那个积压期间，`VEC` 仍在照常返回结果 | Redis 宕机 / worker 挂掉 | 撤回未生效但通道仍在用旧数据 | **陈旧度熔断**：worker 每次成功后写一个 `lastSyncAt` 水位；`VEC` 通道每次查询前检查 `now - lastSyncAt > ECHO_VEC_STALENESS_MAX_MS`（建议 **5000**，= `TC-CARD-03` 上限），超了就**直接关闭 `VEC` 通道**（fail-closed，§2.6.2 已定的原则） | ✅ **零合规残余**。代价转成可用性：Redis 一挂，`VEC` 就降级为空（配额转 `TOPIC`/`FRESH`），这本来就是既定降级链 |
| **F2** | **删 key 成功，但一个 in-flight 读请求把旧向量回填了**（cache-aside 经典竞态） | 读请求在撤回提交**前**读到 DB 旧值，在删 key **后**才写回 Redis。窗口 = 一次 DB 读耗时（~5 ms） | 🔴 旧向量**永久**复活，且此后所有查询都命中它 | **最干净的解法是消灭回填本身**：规定 **Redis 索引只由同步器（syncer）写，读路径永远不写**。`VEC` 查询只做 `FT.SEARCH`，miss 就是 miss（回落 pgvector 或返回空），**不做 read-through 回填** | ✅ **零残余**。竞态的前提是"读路径会写缓存"，去掉这个前提，竞态从根上不存在 |
| **F3** | **主从复制延迟**：删 key 打在 master，读打在 replica，replica 还没收到 | 仅在启用读写分离时存在 | 短窗口内仍能搜到已撤回向量 | 两条任选：① **单节点部署，不做读写分离**（本项目规模完全够，5000 向量 QPS 几十）；② 若将来必须分离，删除后用 `WAIT numreplicas timeout` 等确认 | ✅ **零残余**（选 ①）。代价：放弃读扩展能力——而我们不需要 |
| **F4** | **持久化恢复后旧 key 复活**：RDB 快照在撤回之前生成，Redis 重启后从快照恢复 | 重启 + 快照时点早于撤回。AOF 被截断时同理 | 🔴 已撤回的向量**复活**，且看起来一切正常 | **关掉持久化，把 Redis 当纯缓存**：`save ""` + `appendonly no`。重启后索引是空的，由 syncer 从 PG 全量重建——**重建时读的是当前的授权状态，天然不含已撤回项**。5000 个向量的重建是秒级 | ✅ **零残余**，而且这个解法顺手把"冷启动一致性"也解决了。代价：重启后有一段索引为空的窗口（由 F1-b 的熔断兜住 → `VEC` 返回空） |
| **F5** | **多实例下的本地缓存副本**：每个实例还留了 JVM 镜像 | 仅在 C2 形态或"C3 + 本地二级缓存"下存在 | 删 Redis key 不影响各实例的本地副本；pub/sub 失效通知是 fire-and-forget，GC 停顿或重连期间会漏消息 → **永久陈旧** | **在 C3 下直接不要本地镜像**（扫描在 Redis 内部完成，本地不留向量）。若坚持要本地二级缓存，则必须改成**版本轮询**：全局 `consentEpoch` 计数器，各实例每秒拉一次，一变就整体丢弃镜像 | ✅ **零残余**（不要本地镜像）。这也是 C3 优于 C2 的一个额外理由 |

**小结：加固后的 C3 设计能不能达成"撤回后不再被使用"？——能。** 完整设计见 §2.10.7。所以**否决它的理由不能是合规**，只能是成本收益。

#### 2.10.4 收益到底有多少毫秒（这是决定性的一节）

| 路径 | 5,000 × 768 维一次 top-K 的耗时 | 依据 |
|---|---|---|
| pgvector 精确顺序扫描（当前，ANN 索引注释掉） | **3–10 ms** | §2.3 推导；含 TOAST 行外读放大 |
| pgvector + HNSW 索引（`vector_cosine_ops`） | **0.5–2 ms** | 索引查询，不扫全表 |
| Redis Stack HNSW（`FT.SEARCH` KNN） | **0.5–2 ms** | 同为 HNSW 算法，加一次本地网络往返（~0.2 ms） |
| JVM 堆内 + Vector API SIMD | **0.5–2 ms** | §2.3 |

**关键发现：Redis Stack 相对 pgvector 的收益是 2–8 ms；但相对 pgvector 加个 HNSW 索引，收益 ≈ 0。**

这一条把整个讨论的性质改变了：

> **如果嫌 pgvector 的 3–10 ms 慢，正确的第一步是在 `t_self_vector` 上建一个 HNSW 索引**（`schema.sql:67-69` 现在是注释掉的），一条 DDL、零新组件、零新故障域，就能拿到和 Redis Stack **同一档**的时延。为这 2–8 ms 引入一个新中间件，是先跳过了免费的那一步。

放到全链路里看这 2–8 ms 的分量：

| 分母 | 数值 | 2–8 ms 占比 |
|---|---|---|
| `VEC` 单路预算（§2.6.1） | 78 ms | 3–10% |
| 召回层预算（`SPEC §2.2`，7 路并行） | 120 ms | 2–7% |
| feed 单请求端到端（召回+粗排+精排+打散） | 300–500 ms | **0.4–2.7%** |

而 `VEC` 单路里真正的大头是**二段召回**（相似账号 → 其公开卡，25 ms）和**连接池排队**（`maximumPoolSize=8` 对 HTTP max 16 线程，§1.2-B）。把向量扫描从 5 ms 优化到 1 ms，优化掉的是 `VEC` 路径的 **~5%**。

#### 2.10.5 算总账

| | **A · pgvector 直接 JOIN 授权条件**（本方案 P0） | **C3 · Redis Stack + 删 key + 完整加固** |
|---|---|---|
| **新增基础设施代码** | 0（改一个 `topN` 重载，加 SQL 谓词） | **~500 行**：`FT.*` 客户端封装（Aengine 没包，~100）+ syncer 全量/增量（~150）+ outbox 表与 worker（~120）+ 陈旧度熔断与水位（~60）+ 冷启动重建（~50） |
| **新增数据库对象** | 0 | 1 张 `t_consent_revoke_outbox` |
| **新增运维组件** | 0 | **1 个 Redis Stack 服务**（注意：不是普通 Redis） |
| **新增故障域** | 0 | 1 个（网络、内存淘汰、模块版本、索引重建） |
| **新增部署/文档工作** | 0 | `docker-compose` 服务 + 内存上限 + 健康检查 + 监控项 + `RUNBOOK.md` 降级流程 + `DEPLOY.md` 条目 |
| **授权撤回的失效延迟** | **0**（同一条 SQL 的 JOIN，同一查询快照） | **≤1 s**（outbox worker 间隔），Redis 宕机时由熔断转为"`VEC` 不可用" |
| **失败后果严重程度** | 无此路径 | 加固后：**可用性下降**（`VEC` 返回空）。不加固：**静默合规违规** |
| **与 `G0-10 ④` 日核查 SQL 的一致性** | ✅ 线上过滤与核查 SQL 是同一份逻辑 | ⚠️ 两份逻辑（SQL 核查 vs Redis 索引内容），需要额外的一致性对账作业 |
| **性能收益** | 基准 | **快 2–8 ms**（相对 pgvector+HNSW：**≈ 0**） |
| **当前受益的 QPS** | — | 🔴 **0**。`VEC` 通道 P0 关闭（`SPEC §3.3 规则 3`），且 H5 用户 100% 无向量数据（§1.4） |

**判决：P0 不做。理由不是"不安全"，是这三条数字：**

1. **收益 2–8 ms，且有一条免费替代品能拿到同样的收益**（pgvector HNSW 索引，一条 DDL）。
2. **成本约 500 行新基础设施 + 1 个新服务 + 1 个新故障域**，其中大部分（outbox、熔断、syncer、不许回填的纪律）是**纯粹为了把合规风险压回零**才存在的——它们不产生任何业务价值。
3. 🔴 **被优化的这条链路现在 QPS = 0。** `VEC` 通道 P0 关闭，且 H5 用户没有向量。**这不是"以后再说"的托辞，这是"现在没有任何东西在慢"的事实陈述**——优化对象不存在。

#### 2.10.6 是「现在不需要」还是「永远不该」——明确回答

**是「现在不需要」。不是「永远不该」。** 这是本轮相对 v0.1 最实质的修改：v0.1 我把它写成了 `P0/P1/P2 均不为此引入`，那个措辞过强，撤回。

**升级阶梯（必须按顺序走，不许跳级）**：

| 级 | 手段 | 成本 | 预期时延（5k–50k 向量） | 升到下一级的触发条件 |
|---|---|---|---|---|
| **L0**（当前） | pgvector 精确顺序扫描 | 0 | 3–10 ms / 30–100 ms | 有效向量行数 > **20,000**（`ECHO_VEC_SCAN_MAX`） **或** `rank_vec_scan.scanMs` P95 > **40 ms** |
| **L1** | **pgvector 建 HNSW 索引**（`vector_cosine_ops`） | **一条 DDL**，零新组件 | 0.5–2 ms | 索引建好后 P95 **仍** > 40 ms |
| **L2** | JVM 堆内镜像 + SIMD + top-K SQL 门控复核（§2.4-B 已设计） | ~200 行 | 0.5–2 ms | 部署形态变为 **≥2 实例**（此时每实例一份镜像开始浪费内存，且实例间不一致） |
| **L3** | **Redis Stack 向量索引 + §2.10.7 完整加固** | ~500 行 + 1 服务 | 0.5–2 ms | — |

🔴 **L1 是关键的一级，也是最容易被跳过的一级。** 现在 `schema.sql:67-69` 的 ANN 索引是注释掉的，这在 N < 1 万时是**正确**的（精确扫描召回率 100%，优于 ANN）。但一旦触发 L0→L1，只要一条 DDL 就能拿到和 Redis 同档的时延。**任何"要不要上 Redis 存向量"的讨论，都必须先回答"HNSW 索引建了吗、建了还慢吗"。**

**L3 的具体触发条件（三条同时满足）**：
1. 已完成 L1（HNSW 索引已建）且 `rank_vec_scan.scanMs` P95 **仍** > 40 ms；**且**
2. 部署形态为 **≥2 个 `echo-server` 实例**（此时 L2 的每实例镜像方案不再经济）；**且**
3. 已经或同期决定引入 Redis 承载 **session / feed 快照 / 曝光计数 / 限流** 中的至少两类——即 Redis **不是为向量单独引入的**（§2.4 已定的原则，本轮保留）。

> **写下这三条的目的**：避免半年后再从"结构上不安全"开始重新吵一遍。到那时争论的应该只是"三条触发条件满足了没有"，而不是"删 key 靠不靠得住"——那个问题本节已经回答了：**靠得住，前提是按 §2.10.7 做全套**。

#### 2.10.7 如果要做：完整加固设计（可直接执行，不需重新设计）

放在这里是为了让这个决定**可逆**：将来触发条件满足时，照着做即可。

```
【存储形态】Redis Stack（RediSearch 模块），单节点，关持久化
  redis.conf:  save ""            # 不做 RDB
               appendonly no      # 不做 AOF
               maxmemory-policy noeviction   # 🔴 不许淘汰向量，宁可写失败也不能静默丢
  索引：FT.CREATE idx:selfvec ON HASH PREFIX 1 "sv:"
          SCHEMA embedding VECTOR HNSW 6 TYPE FLOAT32 DIM 768 DISTANCE_METRIC COSINE
  条目：HSET sv:{accountId} embedding <binary> consentEpoch <n>

【写入纪律】🔴 索引只由 syncer 写，读路径永远不写（消灭 F2 回填竞态）
  - VEC 查询只做 FT.SEARCH；miss 就是 miss，不做 read-through 回填
  - 建议用 ArchUnit 或 CR 清单固化：VEC 查询代码不得出现 HSET/FT.ADD

【同步器 syncer】
  全量：进程启动时 + 每 ECHO_VEC_SYNC_FULL_CRON（建议每日 03:00）
        SELECT accountId, embedding FROM t_self_vector v
          JOIN t_ai_consent c ON ...   -- 🔴 授权四条件在这里过滤
        WHERE v.embedding IS NOT NULL
        → 只灌授权有效的；已撤回的天然不进索引
  增量：每 ECHO_VEC_SYNC_INTERVAL_MS（建议 1000）扫 outbox

【撤回链路（F1）】事务外发件箱
  1. POST /consents/:id/revoke 的同一个 DB 事务里：
       UPDATE t_ai_consent SET revokedAt = now WHERE ...
       INSERT INTO t_consent_revoke_outbox(materialRef, capability, createdAt)   -- 同事务
     → 事务提交即"撤回已受理"，此时 DB 已是真相（pgvector 侧立刻生效）
  2. worker（1 s 间隔）：
       SELECT * FROM t_consent_revoke_outbox WHERE doneAt IS NULL ORDER BY createdAt LIMIT 500
       → DEL sv:{accountId}（RediSearch 自动从索引移除）
       → UPDATE ... SET doneAt = now
       → 成功后推进 lastSyncAt 水位
     失败不回写 doneAt，下一轮重试，永不放弃

【陈旧度熔断（F1-b）】🔴 这是零合规残余的关键
  VEC 每次查询前： if (now - lastSyncAt > ECHO_VEC_STALENESS_MAX_MS)  → 关闭 VEC 通道，返回空
                    落 rank_channel_empty{channel=VEC, reason=stale}
  ECHO_VEC_STALENESS_MAX_MS 默认 5000（= TC-CARD-03 的 ≤5 s 要求）
  语义：Redis 一挂 → 水位停止推进 → 5 s 后 VEC 自动下线。
        宁可 VEC 不可用，也不用可能过期的数据（fail-closed，与 §2.6.2 一致）

【冷启动（F4）】关持久化 → 重启后索引为空 → 水位为 0 → 熔断立刻生效 → VEC 返回空
                → syncer 全量重建（5000 条秒级）→ 水位推进 → VEC 自动恢复
                🔴 全程不会出现"用旧数据服务"的窗口

【多实例（F5）】不留本地镜像，扫描全在 Redis 内部 → 无副本一致性问题

【对账（补 G0-10 ④ 的一致性）】
  日作业：比对 FT.SEARCH 可见的 accountId 集合 vs SQL 授权有效集合
          差异 > 0 即告警（正常应恒为 0）
          落 rank_vec_index_reconcile{indexCount, sqlCount, diffCount}
```

**这套设计的合规结论（正面回答，不打太极）**：F1–F5 五种失败模式，F2/F3/F4/F5 做到零残余风险，F1 的残余风险被 F1-b 的熔断转换成可用性损失。**所以它能可靠达成"撤回后不得再被使用"。它是合规的。** 不做它的唯一理由是 §2.10.5 的成本收益账。

#### 2.10.8 顺带修正一个措辞

v0.1 §2.4 的 C 列判决写的是 `🔴 否决（P0/P1/P2 均不为此引入）`。**这个措辞过强，本轮改为：`P0 不做；触发条件见 §2.10.6`。** §2.4 表格与 §4 分期表已同步更新。

---

## 3. 问题二 · 曝光计数怎么存

### 3.1 对产品口径的判决与两点收紧

产品口径：「缓存记实时（热点数据 + 用户自身数据）+ 事件本身也记录曝光量 + 异步定期批量写入降低更新频率。」

**三条全部成立**——这是标准的 write-behind + 双通道设计，方向正确。两点必须收紧：

**收紧一：「缓存」在现状下只能是 JVM 内存，因此必须回答"丢了会怎样"。**
无 Redis（§1.8）、单进程（`DEPLOY.md`）。JVM 内存 = 进程重启即丢。本方案的处置见 §3.3：**把正确性放在 DB 唯一键上，让内存层的丢失退化为纯性能问题**。

**收紧二：「两份数据」必须定权，否则 `SPEC §10.2` 的硬阈值无法验证。**
产品要"缓存记实时 + 事件也记曝光量"，这天然是两份数据。必须明确谁是排序判定的依据：

> **定权：排序判定只认 `t_card_exposure`；`t_event` 只用于分析与对账。**

理由：池位迁移（`SPEC §6.3`）是一个**有状态判定**，必须有单一、可事务化、有唯一键的真相源。若两份数据打架，「保底位履约率 = 100%」（`SPEC §10.2` P0 即设的硬阈值）就无法验证——因为"不达标"和"两份数据不一致"会混在一起，无法区分。

### 3.2 实时层数据结构

#### 3.2.1 先算基数（这是选数据结构的唯一依据）

`SPEC §6.3` 要求：曝光按 `(cardId, viewerAccountId)` **24 h 去重**；单卡单日保底上限 ≤100 次；单卡保底额度 P-新 ≤300 / P-复活 每轮 ≤200 / ~~P-长尾 每 7 天 ≤50~~（🔴 **v0.3 修正**：长尾额度引的是 `SPEC` **v0.1** 口径，v0.2 已随长尾轮播一并移除，见 §8.7.5）。

假设：首屏 20 条/页，人均翻 3 页 ≈ 60 次曝光/天，去重后约 **50 张不同卡/人/天**。

| 场景 | DAU | 去重后 `(cardId, viewerId)` 对/天 |
|---|---|---|
| 种子期 | 300 | **1.5 万** |
| 早期 | 3,000 | 15 万 |
| 中期 | 30,000 | 150 万 |
| 目标期 | 300,000 | 1,500 万 |

内存占用（精确集合）：

| 实现 | 每条开销 | 1.5 万 | 15 万 | 150 万 | 1,500 万 |
|---|---|---|---|---|---|
| `Set<Long>`（装箱 16 B + Node 32 B + 槽 8 B） | ~56 B | 0.84 MB | 8.4 MB | 84 MB | 840 MB 🔴 |
| `long[]` 开放地址哈希（无装箱，负载因子 0.6） | ~13 B | 0.2 MB | 2 MB | 20 MB | 200 MB ⚠️ |

#### 3.2.2 HLL / Bloom / 精确集合的取舍

| 方案 | 内存（1,500 万对） | 误差 | 判决 |
|---|---|---|---|
| **HyperLogLog** | 12 KB/卡 × 卡数 | 基数估计 ±0.8% | 🔴 **能力不匹配，直接排除** |
| **Bloom filter** | ~18 MB（10 bit/条，fp 1%） | 假阳性 1%，**不能删除** | ⚠️ 可用但 P0 不用 |
| **分片 Bloom + 按小时轮转** | ~18 MB | 假阳性 ~0.5%，天然 24 h 滚动 | ⚠️ P1 备选 |
| **精确集合（`long[]` 开放地址 + LRU 上界）** | ~200 MB（或 P0 规模下 ≤84 MB） | 0 | ✅ **P0/P1 推荐** |

🔴 **HLL 是这里被误用的工具，必须讲清楚。** HLL 解决的是**去重计数**（cardinality：这张卡被多少个不同人看过），它**没有成员查询能力**（membership：这个人看过没有）。而 `SPEC §6.3` 的 24 h 去重需要的正是后者——"这个 `(cardId, viewerId)` 对今天出现过吗"。HLL 从原理上答不了这个问题。"去重"这个词在讨论里容易把两者混在一起，实现时会选错。

**为什么 P0 用精确集合而不用 Bloom——真正的理由不是内存，是可验收性。**
`SPEC §10.2` 把「保底位履约率」定成 **P0 即设的硬阈值 100%**，`§9 红线一` 说"低于 100% 即告警"，`TC-RANK-09` 要"连续看 100 个请求的首屏，每一屏都至少 5 条保底位"。**在一个"必须是 100%"的验收项上引入概率性数据结构，会让"真的不达标"和"数据结构的假阳性"无法区分**——QA 收到告警后无法定位。这个代价远大于省下的 180 MB。

（顺带记录 Bloom 的误差方向，供 P1 决策参考：假阳性 = 误判"这个人已经看过" → **少计一次曝光** → 额度消耗更慢 → 卡在保底池待得更久 → **偏向多给曝光**，与北极星同向。所以 P1 若换 Bloom，误差方向是安全的。）

#### 3.2.3 P0 实现

**去重集合**：Aengine `LRUCache`（`LRUCache.java:12-106`，有容量上界 + TTL + 驱逐监听）

```
key   : cardId + ":" + viewerId + ":" + day        // day = yyyyMMdd，口径同 EchoApi.today()
value : Boolean.TRUE（占位）
cache : new LRUCache<>(ECHO_EXPOSURE_DEDUP_MAX, ECHO_EXPOSURE_DEDUP_TTL_SEC, 0, evictListener)
        默认 maxElements = 2,000,000 / timeToIdle = 86400 s
```

选 `LRUCache` 而不是 `SimpleCache` 的理由：`SimpleCache` **没有容量上界**（§1.5），那正是 §1.2-A 泄漏的成因；这里必须有硬上界。

**驱逐监听的作用（不是可选的）**：容量满时 LRU 驱逐最老的去重记录 → 同一对可能被重复计数一次 → **额度消耗偏快 → 偏向少给曝光**。这个方向与北极星相反，所以驱逐必须**可见**：在 `evictListener` 里累计并落 `rank_exposure_dedup_evict{evictedCount, cacheSize, capacity}`，把"容量不够"变成一个可运维的告警信号，而不是一个静默的排序偏差。

**单卡单日计数**：
```
Map<String /* cardId:day */, LongAdder>   // ConcurrentHashMap
```
用 `LongAdder` 而非 `AtomicLong`：分段累加，避免高并发 CAS 争用。
规模：10 万张公开卡 × (~100 B LongAdder + ~60 B key + 32 B Node) ≈ **20 MB**。可接受。
判定：`dailyCount(cardId, today) >= 100` → 该卡本日不再占保底位（`SPEC §6.3`）。

**跨天累计额度**（P-新 ≤300 等）用 write-behind 的标准形态：
```
有效额度用量 = 落库基数（SQL count，进 poolIndex 缓存 60 s）+ 内存增量（自上次 flush 起）
```

**P1 演进**：DAU > 3 万时把去重集合换成 `long[]` 开放地址 + 按小时分 24 片（每小时丢弃最老一片），内存降到 ~13 B/条。因为正确性不依赖它（§3.3），这个替换是纯性能改动，零正确性风险。

### 3.3 关键设计：正确性放在 DB 唯一键上，性能放在内存里

这是本节最重要的一个决定。

```sql
-- 唯一键承担 24h 去重的"持久化真相"
CREATE UNIQUE INDEX "t_card_exposure_uk_card_viewer_day"
    ON "t_card_exposure" ("cardId", "viewerId", "day");
```

落库用 **`INSERT ... ON CONFLICT (cardId, viewerId, day) DO NOTHING`**（多值批量）。

由此得到四个性质：

| 性质 | 为什么 |
|---|---|
| **幂等天生成立** | `ON CONFLICT DO NOTHING` 重放安全。重试同一批次不会重复计数 → **不需要 flush 日志表、不需要 batchId 去重表** |
| **重启不重复计数** | 唯一键挡住。内存去重集合清空后重新计数，DB 侧照样只留一行 |
| **真实增量可直接读出** | `executeUpdate()` 返回的是**实际插入行数** = 真正新增的去重曝光数。不需要内存集合是完美的 |
| **内存层降级为纯性能优化** | 内存集合的作用只是"减少无效 INSERT 尝试"。它丢了、被 LRU 驱逐了、甚至换成概率性结构，都**不影响最终计数的正确性**——只影响无效 INSERT 的数量 |

> **这个结构把"用不用 Bloom""重启丢不丢""LRU 驱逐怎么办"从正确性问题降级为性能问题。** §3.2 里那些取舍因此变成了纯粹的成本权衡，而不是正确性赌注。

**代价与处置**：明细行数 = 去重后的对数（目标期 1,500 万行/天）。

| 项 | 处置 |
|---|---|
| 保留期 | `ECHO_EXPOSURE_RETENTION_DAYS` = **35 天**（覆盖 `SPEC` 用到的 30 天口径 + 缓冲），日作业按 `day` 批量删 |
| 分区 | P0 **不分区**（注解自动建表不支持分区，§1.10）。P1 当日增行数 > 100 万时，手写 DDL 迁到按 `day` 的 range 分区 |
| 索引 | `uk(cardId, viewerId, day)` · `idx(cardId, day)`（额度 count 用）· `idx(day)`（保留期清理与对账用） |

**`viaBoost` 的一个已知精度损失（要写明，因为它影响额度口径）**：
同一天同一 viewer 同一卡若先经普通位曝光、后经保底位曝光，`ON CONFLICT DO NOTHING` 会保留第一次的 `viaBoost=0`，**少记一次保底额度消耗**。
- 概率很低：`SPEC §4.2 G2`（同会话已曝光 ×0.40）与 `§7.1 C10`（已看过 ≤2 条）会压制同日重复出现。
- 误差方向：少记额度消耗 → 卡在保底池待得更久 → **偏向多给曝光**，与北极星同向。
- → **接受这个损失**，不为它引入 `DO UPDATE SET viaBoost = GREATEST(...)`（那会让"实际插入行数"这个免费的增量信号失效）。

### 3.4 异步落库

#### 3.4.0 先回答：能不能直接复用 Aengine 的 `DelaySaveRepository`

Aengine **已经有一套写后缓冲设施**，不先评估就自建是不负责任的：

```
com.aengine.persistence.DelaySaveRepository（Aengine .../DelaySaveRepository.java:20-106）
  构造：(IRepository<T> repo, ScheduledExecutorService ses, int batchSize, int interval, int delay)
  脏队列：ConcurrentMap<T, Long>  ——  key 是实体对象，value 是首次置脏时间戳（:26,55-57）
  定时：scheduleWithFixedDelay(interval, interval, SECONDS)（:48）
  落库条件：firstDirtyAt + delay*1000 < now  或  force=true（:60-68）
  批量：按 batchSize 分批调 repository.forceSave(save)（:82-95）
  失败：保留脏标记下次重试（:96-99）；成功才条件删除（:101-104）
  接入：DelayedJDBCRepository（:16-26）+ shutdown hook delaySave(true)（:25）
  配置：@CRepository(batch=200, interval=10, delay=60)
```

**结论：复用它的"模式"与两处接线细节，但不复用这个类。** 四条不匹配，前两条是**正确性级别**的：

| # | 不匹配点 | 后果 |
|---|---|---|
| 1 🔴 | 它落库调的是 **`repository.forceSave()` = UPDATE**（`IRepository.save` 直接委托 `forceSave`），而 Aengine **全项目没有任何 upsert / `ON CONFLICT` / `ON DUPLICATE KEY` 支持**（已全仓检索确认） | 我们的幂等性完全建立在 `INSERT ... ON CONFLICT DO NOTHING` 上（§3.3）。用 `forceSave` 对一条不存在的行做 UPDATE 会**静默影响 0 行** → 曝光**直接丢失且无任何报错**。这条单独就足以否决直接复用 |
| 2 🔴 | 脏队列是 `ConcurrentMap<T, Long>`，**key 是实体对象**，去重依赖 `T` 的 `equals`/`hashCode` | 我们的去重键是业务三元组 `(cardId, viewerId, day)`。同一次逻辑曝光若被 new 成两个对象，会入队两次；而实体类默认是对象同一性语义 → 去重失效 |
| 3 | `delay` 语义是"置脏后至少等 `delay` 秒才落"，Aengine 默认 `delay=60` | 我们承诺的最大滞后是 **10 s**（§3.5）。要用它必须 `delay=0`，此时 `delay` 这个参数退化成无意义 |
| 4 | 它的形态是"**可变实体的写后回写**"（一个聚合被反复改，攒够了再整体 UPDATE） | 曝光的形态是"**不可变去重事实的追加**"。两者数据形状不同，硬套会一直别扭 |

**要复用的是这两处接线细节（照抄，不重新发明）**：
1. `scheduleWithFixedDelay(interval, interval, SECONDS)` 的循环形态（`DelaySaveRepository.java:48`）——注意是 **fixed-delay 而非 fixed-rate**，避免上一轮 flush 慢时任务堆积。
2. **shutdown hook 里 `force=true` 强制全量 flush**（`DelayedJDBCRepository.java:25`）——这正是 §3.4.3「优雅停机丢失 0」的实现手法。

**要有意做得不一样的一处**：Aengine 失败后**无限保留脏标记重试**（`:96-99`）。本方案改为**重试 3 次后丢弃并告警**（§3.4.1）。理由：无限重试在 DB 长时间不可用时会让缓冲区无界增长直至 OOM，而曝光丢失的误差方向是安全的（§3.4.3）——**宁可丢计数，不可拖垮进程**。

> 顺带记录一个将来的收敛机会：若 P2-4 引入 Redis，Aengine 的 `DelayedRedisRepository` + `Redis.incBy`/`sAdd`（§1.8）可以承接实时层，届时这套自建缓冲可以退役。

#### 3.4.1 批次与频率

| 参数 | 值 | 依据 |
|---|---|---|
| 批次大小 `ECHO_EXPOSURE_FLUSH_BATCH` | **500 行** | PG 多值 INSERT 在 500 行附近达到吞吐拐点（再大收益递减、事务时长与锁持有变长）；500 × ~50 B = 25 KB，远低于任何包大小限制 |
| flush 间隔 `ECHO_EXPOSURE_FLUSH_INTERVAL_MS` | **10,000 ms** | 见 §3.5 一致性边界的推导。相对 `SPEC` 的 72 h 观察窗，10 s 滞后 = 0.004% |
| 触发条件 | `间隔到期` **OR** `缓冲区 ≥ batch` **OR** `shutdown 信号` | 三者任一 |
| 失败重试 `ECHO_EXPOSURE_FLUSH_MAX_RETRY` | **3 次**，指数退避 2 s / 4 s / 8 s | 三次都失败 → 该批次丢弃 + 落 `rank_exposure_flush{result=fail}` 告警。丢弃是安全方向（§3.5） |
| 缓冲上界 `ECHO_EXPOSURE_BUFFER_MAX` | **100,000 行** | 背压：满时**丢弃最新并告警**。不阻塞请求线程（拖慢 feed 不可接受），不丢最老（最老的更接近已确认状态） |

#### 3.4.2 落库实现

```sql
INSERT INTO "t_card_exposure" ("id","cardId","viewerId","day","viaBoost","channel","pool","createdAt")
VALUES (?,?,?,?,?,?,?,?), (?,?,?,?,?,?,?,?), ...   -- 至多 500 组
ON CONFLICT ("cardId","viewerId","day") DO NOTHING;
```

依赖 §2.5.2 新增的 `PgDb.batchUpdate(sql, binders)`。⚠️ 注意 `ON CONFLICT` 是 `PgRepository` 的自动 SQL 生成**不支持**的（§1.10），所以这条 SQL 由 `ExposureRepository` **手写**，不走 `PgRepository.add`。

`executeUpdate()` 的返回值 = 实际插入行数 → 落 `rank_exposure_flush{rows, insertedRows}`，`rows - insertedRows` 就是去重命中数（内存集合的漏检率，可用于调 `DEDUP_MAX`）。

#### 3.4.3 幂等 · 重启 · 崩溃

| 场景 | 行为 |
|---|---|
| **重试同一批次** | 幂等（`ON CONFLICT DO NOTHING`）。不需要 batchId / flush 日志表 |
| **优雅停机**（SIGTERM / `Runtime.addShutdownHook`，模式同 `EchoServer.java:123-126`） | shutdown hook 强制 flush 全部缓冲 → **丢失 0**。⚠️ 见下方实现约束，这个 0 不是免费的 |
| **崩溃**（`kill -9` / OOM / 断电） | 丢失 = 内存中未 flush 的增量，**上界 = 一个 flush 间隔 = 10 s** |
| **重启后去重集合为空** | 不回填、不预热。DB 唯一键兜住正确性（§3.3）；短期内会有一些无效 INSERT 尝试（纯性能损耗，随集合回暖消失） |

🔴 **「优雅停机丢失 0」的实现约束（不满足则这个 0 不成立）**：

`Scheduler.shutdown()` 只调了 `pool.shutdown()`，**没有 `awaitTermination`**（`Aengine .../scheduler/Scheduler.java:99-101`）；`CacheManager` 更是**完全没有 public shutdown 方法**。因此：

| 约束 | 说明 |
|---|---|
| 最终 flush **必须**在 `Runtime.addShutdownHook` 里**同步执行完** | 不能只依赖"调度器里那个 10 s 的周期任务恰好跑一次"。`pool.shutdown()` 不等待在途任务，正在执行的 flush 可能被 JVM 退出直接截断 |
| hook 内要**串行**做完"停止接收新增量 → 全量 flush → 关连接池" | 顺序错了会边 flush 边进新数据，或连接池先关导致 flush 全失败 |
| hook 要有**自己的超时上界**（建议 `ECHO_EXPOSURE_SHUTDOWN_FLUSH_MS` = 5000） | 容器 SIGTERM 到 SIGKILL 通常只有 10–30 s。flush 卡住时必须能放弃，否则会被 `SIGKILL` 打断成"部分落库"（幂等键保证这仍是安全的，只是丢一部分） |

→ 落地要求：`ExposureFlushJob` 的 flush 逻辑抽成一个**可被 hook 直接同步调用**的方法（形态同 Aengine `DelaySaveRepository.delaySave(force=true)`），**不要**把逻辑写在 `TriggerTask.doTask()` 里面。

🔴 **明确不做：本地磁盘 WAL / 落盘缓冲。**
理由：曝光计数丢 10 s 的后果是"某些卡的额度少消耗了几次" → 它们在保底池里多待一会儿 → **偏向多给曝光**。这个误差方向与北极星（`GTM4` 被接住的发布率）**同向**。为一个方向安全、量级微小（§3.5 算出 <1%）的误差引入一个本地持久化组件，不划算。

> "丢数据"听起来很严重，但要看**丢了往哪个方向偏**。这个判断标准建议写进后续所有涉及排序状态的设计。

#### 3.4.4 调度装配（有一个必须先改的现存约束）

```
ExposureFlushJob        每 10 s      write-behind 落库
CardPoolTransitionJob   每 1 min     池位迁移扫描（SPEC §12.5 已列）
ExposureRetentionJob    每日 03:00   删 35 天前明细
ExposureReconcileJob    每日 03:30   与 t_event 日对账（P1 起有意义）
```

🔴 **前置：`Scheduler.init("echo-scheduler", 1)`（`EchoServer.java:186`）的线程数必须从 1 提到 ≥4。**
`Scheduler.init` 幂等（`Scheduler.java:21-25`），只有第一次生效；当前 1 个线程已被 `EchoExpiryJob`（每分钟）占用。`ScheduledThreadPoolExecutor` 单线程时任务**串行**——再加 4 个作业会互相阻塞，10 s 的 flush 会被日作业拖成分钟级。

🔴 **DB 关闭时的降级**：`Scheduler.init` 只在 `EchoDatabase.initIfEnabled()` 成功后调用（`EchoServer.java:147-151, 186`）。DB 关闭时**没有调度器**，也没有 `t_card_exposure`。此时曝光记账整体降级为**纯内存、不落库、进程生命周期内有效**（仅联调态），并在启动日志明确告知。

### 3.5 一致性边界（明确数字）

> 🔴 **v0.6 标注：本节第 7、8 项与 §3.5.1 整段属于 v0.3 配额制残留，已随 §8.0 作废。**
> 权重制下没有「单卡保底额度 300」「日配额 100」这类总量上限，因此也不存在「额度超发」这个问题——
> 超发算术、≤1% 的推导、容量自洽结论**全部不适用**。
> ⚠️ 第 1–6 项（flush 滞后、崩溃丢失、池位迁移滞后）**仍然有效**，它们讲的是曝光落库的一致性，
> 与配额无关；`n` 的准确性依赖它们。**不要把整节一起划掉。**

| # | 项 | 数字 |
|---|---|---|
| 1 | 实时层 → 明细表最大滞后 | **10 s**（= flush 间隔） |
| 2 | P99 滞后 | **≤ 12 s**（含一次 2 s 退避重试） |
| 3 | 优雅停机丢失 | **0** |
| 4 | 崩溃（`kill -9`）最大丢失 | **10 s 内的曝光增量**。目标期 1,500 万/天 ≈ 174 条/s → 约 **1,740 条** |
| 5 | 崩溃丢失对全站分析指标的影响 | 1,740 / 1,500 万 = **0.012%**（可忽略） |
| 6 | 池位迁移判定的滞后 | **≤ 70 s** = 10 s（flush）+ 60 s（`poolIndex` 缓存 TTL，`SPEC §12.4` 已定） |
| 7 | 单卡单日上限（≤100）的超发 | **单进程内 0 次**（内存 `LongAdder` 实时判定，不经落库） |
| 8 | **单卡保底额度（≤300）的超发上界** | **≤ 3 次（≤1%）** ← 推导见下 |

#### 3.5.1 为什么单卡额度超发只有 ≤1%（这是关键推导）

直觉会认为"10 s 滞后 + 174 条/s = 可能超发 1,740 次"。**这是错的**，因为约束是**单卡**的曝光速率，不是全站的：

```
单卡单日保底上限 = 100 次/日        （SPEC §6.3，且由内存实时判定、不受滞后影响）
→ 单卡 10 s 内的保底曝光期望：
    均匀分布：100 × 10/86400  = 0.012 次
    流量集中在 2 h 高峰：100 × 10/7200 = 0.14 次
→ 取悲观上界（极端并发下同一卡在 10 s 内被反复选中）：≤ 3 次
→ 相对 300 的额度配额：≤ 1%
```

**「单卡单日上限 ≤100」这条规则顺带把额度误差压到了 1% 以内**——这是 `SPEC §6.3` 那条防刷规则的一个意外但真实的收益。崩溃场景下同样是 ≤3 次，因为约束仍是单卡速率。

#### 3.5.2 最终一致会不会影响保底位判定的正确性

**不会。这里有一个必须讲清的区分：**

| 判定 | 是否受最终一致影响 | 为什么 |
|---|---|---|
| **保底位履约**（每 20 条 ≥5 条保底位；`SPEC §10.2` 硬阈值 100%） | 🟢 **完全不受影响** | 履约判定的是"这一屏有没有输出 ≥5 条保底池卡"，由编排层在**单次请求内同步**完成（`SPEC §7.3` 的贪心滑窗），**不读曝光计数** |
| **池成员资格**（某张卡属于 P-新 还是 P-复活） | 🟡 受影响 | 依赖累计 `boostExposure` 是否达 300 → 最坏滞后 70 s（表 #6） |
| 曝光基尼系数 / 零回应窗口占比等分析指标 | 🟡 受影响 | 误差 0.012%（表 #5） |

> **一句话**：最终一致性影响的是「**哪些卡在保底池里**」，不影响「**有没有给保底位**」。前者的误差是 ≤1% 的额度超发（方向偏向多给曝光），后者是 100% 硬阈值且不依赖曝光数据。

#### 3.5.3 产品侧需要接受的误差（三条，都是具体数字）

| # | 误差 | 数值 | 方向 |
|---|---|---|---|
| 1 | 单卡保底曝光额度可能超出配额 | **≤3 次 / ≤1%**（P-新 300 的配额实际可能执行到 303） | 偏向多给曝光（与北极星同向）✅ |
| 2 | 池位迁移（P-新 → P-复活）的时间点滞后 | **≤70 s**（相对 72 h 观察窗 = 0.03%） | 中性 |
| 3 | 崩溃时曝光记录丢失 | **≤10 s / ≈1,740 条 / 全站 0.012%** | 偏向多给曝光 ✅ |

三条都不影响 `SPEC §13` 的任何 `TC-RANK-xx` 验收项（`TC-RANK-07`/`09` 只依赖池成员与保底位，容差远大于以上误差）。

### 3.6 与事件数仓的关系

#### 3.6.1 定权与分工（回答"会不会变成两份真相"）

| | `t_card_exposure`（本方案自建） | `t_event`（数仓，待建） |
|---|---|---|
| 定位 | **排序引擎的内部状态** | **分析事件流** |
| 回答的问题 | "这张卡的额度还剩多少" | "发生了什么" |
| 形态 | 有状态、唯一键去重、按 `(cardId,viewerId,day)` 聚合 | append-only、可重放、全维度（`pos`/`channel`/`pool`/`reqId`/设备） |
| 延迟要求 | ≤10 s | T+1 可接受 |
| 允许丢失 | ≤10 s 窗口 | 允许少量（`sendBeacon` 不保证到达） |
| **排序判定** | ✅ **唯一依据** | 🔴 不作为判定依据 |
| 分析/看板 | ⚠️ 仅作对账参照 | ✅ 唯一依据 |

**为什么不合并**（这是"两份真相"担忧的正面回答）：
- 用 `t_event` 做额度判定，要求每次请求扫事件流做聚合 → 不可行。
- 用 `t_card_exposure` 做分析，缺失位次/通道/池/设备维度，且 24 h 去重后无法还原原始曝光序列。
- 它们不是同一份数据的两份拷贝，是**两个不同粒度、不同一致性要求的派生物**。

**"两份真相"的真正解法是对账，不是合并**：
`ExposureReconcileJob`（每日 03:30）比对
```
count(distinct (cardId, viewerId)) from t_event where event='window_impression' and day=D
   vs
count(*) from t_card_exposure where day=D
```
差异率 > **2%** 即告警（`rank_exposure_reconcile{day, detailCount, eventCount, diffRate}`）。
2% 这个阈值的来源：客户端上报丢失（`sendBeacon` 无投递保证）+ 服务端 10 s flush 丢失（0.012%）+ 下发与渲染的差异。上线后按实测分布收紧。

#### 3.6.2 迁移路径（三阶段，终态是单一真相源）

| 阶段 | 曝光额度口径 | `t_card_exposure` 的写入方 | 说明 |
|---|---|---|---|
| **P0** | 客户端上报（推荐）/ 服务端下发（备选） | 排序引擎直写 | 见 §3.6.3 的口径选择 |
| **P1** | 客户端 `window_impression` | 排序引擎直写；`/collect` + `t_event` 并行上线，开始日对账 | 若 P0 走的是服务端下发口径，此处切换需**双口径并行跑 2 周**对比后再切 |
| **P2** | 客户端 `window_impression` | **改由 `t_event` 流式聚合回灌** | `t_card_exposure` 退化为一张由 `t_event` 派生的物化表。此时**单一真相源 = `t_event`**，真正收敛 |

#### 3.6.3 P0 的曝光口径：一个需要拍板的取舍

`SPEC §15 Q10` 建议"排序侧自建轻量 `t_card_exposure` 过渡"，本方案采纳。但还有一个规格没展开的问题：**P0 没有 `/collect`，曝光信号从哪来？**

两个选项：

| | **推荐 · 自建最小曝光上报端点** | **备选 · 服务端下发即记账** |
|---|---|---|
| 做法 | 新增 `POST /api/v1/plaza/impressions {reqId, items:[{cardId, viaBoost}]}`，前端在卡片进入视口时批量上报（500 ms 合批） | `/plaza` 返回的 20 条**下发即记一次曝光** |
| 口径准确性 | ✅ 贴近"真的被看见" | ⚠️ 下发 ≠ 看见。用户只滑到第 5 条，后 15 条也记了账 |
| 误差方向 | 客户端丢报 → 少记 → **偏向多给曝光** ✅ | 多记 → 额度消耗快 → 卡更早退出保底池 → **偏向少给曝光** 🔴 与北极星反向 |
| 需要前端改动 | ✅ 需要（`PlazaScreen` 加视口观察 + 批量上报） | ❌ 不需要 |
| 与 `/collect` 的关系 | 不冲突（`/collect` 是通用事件通道，这个是排序专用的额度记账通道）；P2 迁移时只换写入源 | — |
| 成本 | 一个路由 + 一次写内存缓冲；比等 `/collect` 全套事件基座轻得多 | 0 |

**推荐自建上报端点。** 理由：备选方案的误差方向是"系统性少给曝光"，而这正是北极星最敏感的方向。若排期上前端确实来不及，则走备选并**加额度补偿系数** `ECHO_EXPOSURE_DELIVERY_FACTOR`（默认 1.5，即 300 的额度按下发口径执行到 450），待 P1 拿到真实渲染率后校准——但**补偿系数本身是个需要产品接受的猜测**（§7 Q3）。

### 3.7 埋点上报（`rank` 前缀）

> **对齐声明**：`SPEC-recommendation-ranking §10.1` 已定义 `rank_request` / `rank_pool_shortfall` / `rank_diversity_relax` / `rank_channel_empty` / `rank_feature_reject` / `card_pool_transition` / `window_impression`。本方案**不重定义、不改名**，只新增本方案两个机制自诊断所需的事件。
> 命名与字段规范沿用 `SPEC-admin-console §3.1/§3.2`：`<域>_<动作>`、`snake_case`、动词原形；公共信封（`eventId/ts/accountId/isGuest/bound/deviceId/sessionId/...`）全部沿用；**`props` 只允许标量与枚举（零原文）**。

#### 3.7.1 建议新增的事件

| 事件 | 端 | `props` | 支撑什么 |
|---|---|---|---|
| `rank_vec_scan` | 服务端 | `reqId` · `candidateCount`(实际扫描候选数) · `hitCount` · `scanMs` · `source`(枚举 `pgvector`/`mirror`) · `truncated`(bool，是否触发 `SCAN_MAX` 轮转采样) | `VEC` 单路时延与扫描规模；**用实测校验 §2.3 的估算**；判断是否该启用镜像 |
| `rank_vec_consent_reject` | 服务端 | `stage`(枚举 `viewer`/`candidate`/`result`) · `rejectedCount` | 🛡 三层门控各拦了多少（`G0-10` 的运行时证据） |
| `rank_exposure_flush` | 服务端 | `rows` · `insertedRows` · `latencyMs` · `retryCount` · `result`(枚举 `ok`/`retry`/`fail`) | 落库健康；`rows − insertedRows` = 去重命中数 |
| `rank_exposure_dedup_evict` | 服务端 | `evictedCount` · `cacheSize` · `capacity` | 🛡 去重缓存容量不足（会导致额度多消耗 → 少给曝光） |
| `rank_exposure_lag` | 服务端 | `lagMs`(最老未落库增量的滞后) · `bufferRows` | 🛡 §3.5 的 10 s 承诺的实测值 |
| `rank_exposure_reconcile` | 服务端 | `day` · `detailCount` · `eventCount` · `diffRate` | 🛡 与 `t_event` 的日对账（阈值 2%） |
| ~~`rank_quota_exhausted`~~ | ~~服务端~~ | ~~`cardId` · `pool` · `quotaType` · `actual` · `cap`~~ | 🔴 **v0.6 作废**（v0.3 配额制残留，随 §8.0 一起）。权重制下没有额度，也就没有「额度耗尽」这个事件；池位迁移的触发点改为 `W < W_MIN`，对账走 `card_pool_transition` |
| **`rank_pool_snapshot_refresh`** 🆕 | 服务端 | `freshCount` · `reviveCount` · `buildMs` · `ageMs` | v0.2.1 · 保底组快照健康（§2.2.5 ④） |
| **`rank_pool_snapshot_stale`** 🆕 | 服务端 | `ageMs` · `pool` | 🛡 v0.2.1 · D1 降级发生（§2.2.7） |
| **`rank_pool_snapshot_miss`** 🆕 | 服务端 | `pool` · `syncQueryMs` · `result`(枚举 `ok`/`timeout`/`empty`) | 🛡 v0.2.1 · D2 同步兜查 |
| **`rank_pool_transition_run`** 🆕 | 服务端 | `scanned` · `transitioned` · `durationMs` · `result` | 🛡 v0.2.1 · 池位迁移作业心跳。**看门狗依赖它**——作业静默停摆是隐性故障（§2.2.5 ⑥） |
| **`rank_boost_slot_provenance`** 🆕 🔴 | 服务端 | `reqId` · `pos` · `slotProvenance`(见 §2.2.8 枚举) · `pool` | v0.2.1 · **修正能否验证的关键埋点**。保底位上出现 `RELEVANCE` 即为实现缺陷 |
| **`rank_boost_slot_overlap`** 🆕 | 服务端 | `reqId` · `boostCount` · `overlapCount` · `overlapRate` | v0.2.1 · 抓"保底位给了本来就能出头的卡"这种无用功（§2.2.8） |

#### 3.7.2 建议新增的指标（需并入 `SPEC-admin-console §2.6`）

| 指标 | 口径 | 来源 | 刷新 | 阈值 |
|---|---|---|---|---|
| `VEC` 扫描时延 P95 | `rank_vec_scan.scanMs` 的 P95 | 服务端 | 实时 | ≤40 ms（超过则评估启用镜像，§2.4） |
| 有效向量账号数 | `t_self_vector` 中 embedding 非空且门控通过的行数 | 日作业 | T+1 | > `ECHO_VEC_SCAN_MAX` 时告警（提示建 HNSW 索引） |
| 曝光落库滞后 P99 | `rank_exposure_lag.lagMs` 的 P99 | 服务端 | 实时 | **≤12 s**（= §3.5 承诺） |
| 去重缓存驱逐率 | `evictedCount / 曝光总数` | 服务端 | 小时 | **恒 0**；非 0 即调大 `DEDUP_MAX` |
| 曝光对账差异率 | `rank_exposure_reconcile.diffRate` | 日作业 | 每日 | **≤2%** |
| 额度超发次数 | `rank_quota_exhausted.actual − cap` 的正值之和 | 日作业 | 每日 | 单卡 **≤3 次**（= §3.5 承诺） |
| **保底位履约率（修正口径）** 🆕 🔴 | `slotProvenance ∈ {GUARANTEE_*}` 的保底位数 / 应有保底位数。**分母是应有位数，不是已填位数** | 服务端 | 实时 | 100%（`SPEC §10.2` 硬阈值）。⚠️ 种子期 `EMPTY` 会有正常非零值，阈值需分阶段（§7 Q12） |
| **保底位被相关性组占用次数** 🆕 🔴 | `slotProvenance == RELEVANCE` 且位置属保底位 | 服务端 | 实时 | **恒 0**。非 0 即实现缺陷，立即告警 |
| **保底位重叠率** 🆕 | `rank_boost_slot_overlap.overlapRate` 的均值 | 服务端 | 小时 | 建议 **< 50%**；持续超过说明保底候选集仍被相关性信号污染 |
| **池位迁移作业存活** 🆕 | `now − rank_pool_transition_run` 最近成功时间 | 服务端 | 实时 | **≤5 分钟**（= `ECHO_POOL_TRANSITION_WATCHDOG_MS`） |

🔴 **`SPEC §2.7 约定 11 / §10.2` 的「C 端零暴露」对以上全部适用**：一个都不得出现在 C 端，也不得作为 C 端展示依据。

#### 3.7.3 一条必须处理的红线冲突

`rank_quota_exhausted` 带 `actual` / `cap`，这是**曝光计数的数值**。而 `SPEC §4.3 X6` 禁止「精确记得数 / 心意数 / **看过数**的数值」进排序，`§4.5 保证 2` 要求 ArchUnit 规则让"排序模块 import 互动计数相关的类与列名常量"**构建失败**。

按字面执行，本方案的曝光计数会被这条规则误伤。必须做一个**显式区分**（建议并入 `SPEC §4.5`，本文档不改该规格）：

| 类别 | 例子 | 排序模块可否读取 |
|---|---|---|
| **互动计数**（X6 禁止） | `t_remember` 的记得数、`t_flower_log` 的心意数、`t_pet.seenCount` / `flowersReceived` | 🔴 **禁读**（只允许布尔化的 `acceptedFlag`） |
| **曝光计数**（本方案，属排序引擎内部状态） | `t_card_exposure` 的 `uniqueViewers` / `boostExposure` | ✅ **允许读**，且**必须**读——`SPEC §6.3` 的额度与池位迁移完全依赖它 |

区分的实质理由：**互动计数度量"多少人喜欢它"（马太效应的燃料）；曝光计数度量"它已经拿到多少机会"（马太效应的刹车）**。二者在排序里的作用方向相反。`X6` 禁的是前者，本方案用的是后者。

→ 具体落地建议：ArchUnit 规则的表达式从"禁 import 计数相关类"改为**显式黑名单 + 显式白名单**：
- 黑名单（禁读）：`t_remember` · `t_flower_log` · `t_pet.seenCount` · `t_pet.flowersReceived` 的列名常量与访问方法；
- 白名单（可读）：`t_card_exposure` · `t_card_pool_state`。
黑白名单都必须显式枚举——"没在名单里"默认拒绝，新增需按 `SPEC §4.5 保证 3` 走三签。

> 🔴 顺带指出一个既有风险：`t_pet.seenCount`（`schema.sql:177`）当前由 `POST /windows/:id/seen` 累加（`EchoApi.java:575`），它**既是 X6 禁读的"看过数"，又长得像曝光计数**。极易被后来的实现误当作曝光口径接进排序。建议：本方案的曝光计数**绝不复用 `seenCount`**，且把 `seenCount` 明确列入 ArchUnit 黑名单。

### 3.8 表结构定义

```sql
-- =============================================================================
-- 排序引擎内部状态（TECH-DESIGN-feed-recall-and-exposure §3）
--
-- 定位：这两张表是"排序引擎的内部状态"，不是分析表。
--   - 分析口径以 t_event（数仓，待建）为准；本表仅供排序判定与对账。
--   - P2 数仓建成后，t_card_exposure 改由 t_event 流式聚合回灌（§3.6.2）。
--
-- 合规说明（供 CR 核对，避免被 G0-9/G0-10 误判打回）：
--   - 无 deletedAt：本表不是用户内容，是引擎派生状态，按保留期硬删除，故不适用
--     G0-9 的"唯一索引改部分索引"。
--   - 无 materialRef/consentRef：本表不是"素材派生物"（不由用户素材派生），是行为记账，
--     故不适用 G0-10 ① 的双外键要求。（对比：t_self_vector 是素材派生物，必须补这两列。）
--   - 但 (cardId, viewerId) 属 PIPL 下的行为个人信息：需保留期（35 天）+ 挂账号注销清理链路。
-- =============================================================================

-- 曝光明细：24h 去重的持久化真相（§3.3）
CREATE TABLE IF NOT EXISTS "t_card_exposure" (
    "id"        bigint      NOT NULL,                 -- 雪花（@Pk auto=false，工程约定）
    "cardId"    bigint      NOT NULL DEFAULT 0,
    "viewerId"  bigint      NOT NULL DEFAULT 0,
    "day"       integer     NOT NULL DEFAULT 0,       -- yyyyMMdd，口径同 EchoApi.today()
    "viaBoost"  smallint    NOT NULL DEFAULT 0,       -- 1 = 本次曝光占用了冷启动保底位
    "channel"   varchar(16) NOT NULL DEFAULT '',      -- 召回通道枚举（SPEC §3.1）
    "pool"      varchar(16) NOT NULL DEFAULT '',      -- 池枚举（SPEC §6.2）
    "createdAt" bigint      NOT NULL DEFAULT 0,
    PRIMARY KEY ("id")
);
-- 🔴 这条唯一索引是整个曝光方案的正确性基石（§3.3）：24h 去重与幂等都靠它
CREATE UNIQUE INDEX IF NOT EXISTS "t_card_exposure_uk_card_viewer_day"
    ON "t_card_exposure" ("cardId", "viewerId", "day");
CREATE INDEX IF NOT EXISTS "t_card_exposure_idx_card_day"
    ON "t_card_exposure" ("cardId", "day");           -- 额度 count
CREATE INDEX IF NOT EXISTS "t_card_exposure_idx_day"
    ON "t_card_exposure" ("day");                     -- 保留期清理 + 日对账

-- 池位状态机：SPEC §6.2/§6.3 的四池状态与额度进度（排序层只读，由作业维护）
-- 🔴 v0.4 注意：本段是 v0.2.1 的目标态。§8 换成权重制后，其中「额度进度」相关的三列
--    （reviveRound / boostExposure / lastBoostAt）与 REVIVE / LONGTAIL 两个池均已废弃，
--    以 §8.9.1 的增量为准。此处保留原文以便对照，勿直接照此建表。
CREATE TABLE IF NOT EXISTS "t_card_pool_state" (
    "id"                bigint      NOT NULL,
    "cardId"            bigint      NOT NULL DEFAULT 0,
    -- 🔴 v0.4：REVIVE 已删除（§8.7.3）、LONGTAIL 已被 SPEC v0.2 移除（§8.7.5）。
    -- 🔴 v0.5 回改（B5）：v0.4 这里写「枚举收敛为 FRESH|STEADY|RESTRICTED，自然流掉由 drainedAt
    --    表达、不是一个池」——与上游不一致，已改。SPEC §6.2 的池枚举含 P-流掉 `DRAINED`
    --    （原 ARCHIVED_FROM_FEED 改名），且 §8.1 H11 的硬过滤条件原文就是 `poolTag = DRAINED`。
    --    统一口径见 §8.7.4：`DRAINED` 是过滤谓词，`drainedAt` 只是时刻记录，两者不是两套表达。
    "pool"              varchar(16) NOT NULL DEFAULT 'FRESH',  -- 🔄 FRESH|STEADY|DRAINED|RESTRICTED（对齐 SPEC §6.2）
    "poolEnteredAt"     bigint      NOT NULL DEFAULT 0,
    "reviveRound"       integer     NOT NULL DEFAULT 0,        -- [v0.4 废] REVIVE 删除，不再实现
    "boostExposure"     bigint      NOT NULL DEFAULT 0,        -- [v0.4 废] 额度口径已废，改用 deliveredCount（§8.9.1）
    "observeRerunCount" integer     NOT NULL DEFAULT 0,        -- 观察窗重跑次数（≤2，防刷）—— 仍有效
    "lastBoostAt"       bigint      NOT NULL DEFAULT 0,        -- [v0.4 废] 长尾轮播已移除
    "graduatedAt"       bigint      NOT NULL DEFAULT 0,        -- 获首条合规回声、毕业到 STEADY 的时刻
    -- 🆕 v0.2.1：以下两列为保底组「全库直查」的 index-only 支撑（§2.2.5 ①③）
    -- 反规范化自卡表，由 CardPoolTransitionJob 维护。目的：让保底组查询无需 join 卡表即可完成
    -- 排序与可见性过滤，从而保持 index-only scan（回表会让 0.5 ms 劣化到 5–50 ms）
    "approvedAt"        bigint      NOT NULL DEFAULT 0,        -- FRESH 排序键（过审时间）
    "eligible"          smallint    NOT NULL DEFAULT 0,        -- 1 = 授权有效 ∧ 未下架 ∧ 可见 ∧ 状态正常
    "originType"        varchar(16) NOT NULL DEFAULT 'user',   -- 🔴 v0.5：枚举只有 user|official（RK22 取消 seed_ai，原 seed_ops 归入 user）
    "updatedAt"         bigint      NOT NULL DEFAULT 0,
    PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX IF NOT EXISTS "t_card_pool_state_uk_card" ON "t_card_pool_state" ("cardId");
CREATE INDEX IF NOT EXISTS "t_card_pool_state_idx_pool_boost"
    ON "t_card_pool_state" ("pool", "boostExposure");          -- 🔴 v0.4 废弃：权重制下取卡按 W 降序，
                                                               --    而 W 在快照作业里内存计算（§8.4.2），不需要索引
CREATE INDEX IF NOT EXISTS "t_card_pool_state_idx_pool_lastboost"
    ON "t_card_pool_state" ("pool", "lastBoostAt");            -- 🔴 v0.4 废弃（REVIVE/LONGTAIL 两池均已删除）
-- 🆕 v0.2.1：保底组快照构建用。列序对应 (等值, 等值, 排序)，可被反向扫描满足 approvedAt DESC
CREATE INDEX IF NOT EXISTS "t_card_pool_state_idx_pool_eligible_approved"
    ON "t_card_pool_state" ("pool", "eligible", "approvedAt");
```

> **🆕 v0.2.1 · 关于反规范化的取舍**：`approvedAt` / `eligible` / `originType` 三列是**卡表数据的副本**，正常应当避免。这里之所以接受，是因为保底组要求 index-only scan（§2.2.5 ①），而注解建表既不支持 `INCLUDE` 也不支持部分索引（§1.10）——没有别的办法在一次索引扫描里同时完成过滤与排序。
> 一致性由 `CardPoolTransitionJob` 维护（每分钟），**最坏滞后 60 s**：一张刚被下架的卡最多 60 s 后才从 `eligible` 掉出。⚠️ 这个滞后**不能用于授权门控**——`eligible` 只是"快照构建时的预筛"，卡下发前仍必须走一次实时的授权/可见性校验（与其他通道同一套出口复核）。**把 `eligible` 当门控依据是本设计最危险的误用方式**，需在 CR 清单里写明。
> P1 `t_memory_card` 落地后，这三列应改为直接查卡表上的 `(poolTag, status, visibility, approvedAt)` 索引，本表退回纯状态表（§2.2.5 ③）。

**为什么没有日聚合表（`t_card_exposure_daily`）**：不需要。额度判定是 `SELECT count(*) FROM t_card_exposure WHERE cardId=? AND viaBoost=1 AND day>=?`，走 `idx(cardId, day)`，单卡最多 300 行（额度上限），毫秒级；且这个查询由 `poolIndex` 缓存（TTL 60 s，`SPEC §12.4`）挡住，**不是每请求一次**。加一张日聚合表是过早优化。P1 若分析侧需要，再加。

**建表方式**：走注解自动建表（§1.10 路径 1），复合唯一索引用 `@Index(name=..., type=UNIQUE, columns={...})`（`PgRepository.java:141-159` 支持）。同步把上面的 DDL 补进 `schema.sql`（DBA 真源）。

### 3.9 配置项（问题二）

| 环境变量 | 默认 | 含义 |
|---|---|---|
| `ECHO_EXPOSURE_ENABLED` | `true` | 曝光记账总开关（关 → 排序层按"额度无限"运行，仅联调） |
| `ECHO_EXPOSURE_SOURCE` | `impression` | 额度口径：`impression`（客户端上报，推荐）/ `delivery`（服务端下发，备选） |
| `ECHO_EXPOSURE_DELIVERY_FACTOR` | `1.5` | 仅 `source=delivery` 时生效的额度补偿系数（§3.6.3） |
| `ECHO_EXPOSURE_DEDUP_MAX` | `2000000` | 内存去重集合容量上界（LRU 驱逐） |
| `ECHO_EXPOSURE_DEDUP_TTL_SEC` | `86400` | 去重条目 TTL（= 24 h 口径，`SPEC §6.3`） |
| `ECHO_EXPOSURE_FLUSH_BATCH` | `500` | 单批落库行数 |
| `ECHO_EXPOSURE_FLUSH_INTERVAL_MS` | `10000` | flush 间隔（= §3.5 的一致性承诺） |
| `ECHO_EXPOSURE_FLUSH_MAX_RETRY` | `3` | 失败重试次数（指数退避 2 s / 4 s / 8 s）；**有意不同于** Aengine `DelaySaveRepository` 的无限重试（§3.4.0） |
| `ECHO_EXPOSURE_SHUTDOWN_FLUSH_MS` | `5000` | 停机 hook 内最终 flush 的超时上界（§3.4.3）。`Scheduler.shutdown()` 无 `awaitTermination`，必须自己兜 |
| `ECHO_EXPOSURE_BUFFER_MAX` | `100000` | 内存缓冲上界；满则**丢弃最新 + 告警**（不阻塞请求线程） |
| `ECHO_EXPOSURE_RETENTION_DAYS` | `35` | 明细保留期 |
| `ECHO_EXPOSURE_RETENTION_CRON` | `0 0 3 * * *` | 保留期清理 cron（**6 段制**，Aengine `CronSequenceGenerator`） |
| `ECHO_EXPOSURE_RECONCILE_CRON` | `0 30 3 * * *` | 日对账 cron |
| `ECHO_EXPOSURE_RECONCILE_DIFF_THRESHOLD` | `0.02` | 对账差异率告警阈值（2%） |
| `ECHO_POOL_TRANSITION_CRON` | `0 * * * * *` | 池位迁移扫描 cron（每分钟） |

装配形态同 §2.9：`record ExposureConfig(...)` + `fromEnv()` / `from(Function<String,String>)`。

### 3.10 曝光上报端点：前后端契约（v0.2 · 裁定「P0 就做」）

> 裁定：**曝光上报端点 P0 就做，前端排期配合。** 本节是可直接交给前端开工的契约。
> 口径选择的论证见 §3.6.3（`ECHO_EXPOSURE_SOURCE=impression`，`delivery` 与补偿系数 §7 Q3 作废）。

#### 3.10.1 曝光的定义（前端判定标准）

一次曝光 = **卡片在视口中"有效停留"**，三个条件同时满足：

| 条件 | 阈值 | 理由 |
|---|---|---|
| 面积可见比例 | **≥ 50%** | 与主流 `IntersectionObserver` 实践一致；50% 以下用户基本读不到卡面信息 |
| 连续停留时长 | **≥ 1000 ms** | 快速滑过不算"看见"。1 s 是"眼睛落到卡上"的下限 |
| 同一卡同一会话 | **只报一次** | 前端本地去重，减少无效请求（服务端仍会去重，见 §3.10.5） |

```js
// 判定要点（不是最终代码，是契约要求）
new IntersectionObserver(cb, { threshold: [0.5] })
// 进入 ≥0.5 时起计时；退出 <0.5 时清除计时；计时满 1000ms 即入队
```

🔴 **明确不算曝光的情形**：页面处于后台标签（`document.hidden === true`）时不计时；`prefers-reduced-motion` 或无障碍模式下规则不变（不能因为无障碍而少给作者曝光）。

#### 3.10.2 批量策略

| 项 | 规则 |
|---|---|
| 攒批触发 | **满 10 条** 或 **距上次上报 5000 ms**，先到者触发 |
| 单请求上限 | **50 条**（超出拆多请求） |
| 页面隐藏 / 关闭 | `visibilitychange → hidden` 与 `pagehide` 时**立即 flush**，用 `navigator.sendBeacon`（唯一能在卸载期可靠送出的方式） |
| 路由切换（SPA） | 视为一次 flush 时机 |
| `sendBeacon` 不可用 | 回落 `fetch(..., { keepalive: true })` |
| 🔴 不得阻塞渲染 | 上报全程异步，失败静默（与既有 `track.ts:79-81` 的原则一致） |

#### 3.10.3 接口定义

```
POST /api/v1/plaza/impressions
Authorization: Bearer <token>        # 与既有 REST 一致（HttpGateway.java:207-214）
Content-Type: application/json
```

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `reqId` | string | ✅ | 该批曝光所属的 feed 请求 id（由 `GET /plaza` 响应下发）。**用于服务端校验，见 §3.10.4** |
| `items[].cardId` | string(int64) | ✅ | 卡 id |
| `items[].pos` | int | ✅ | 该卡在本次 feed 里的位次（0-based） |
| `items[].dwellMs` | int | ✅ | 实际停留时长（≥1000）。用于服务端抽样校验合理性 |
| `items[].ts` | int64 | ✅ | 客户端判定曝光的时刻（epoch ms） |

🔴 **前端不传的字段**（服务端自己定，防伪造）：`viaBoost` · `channel` · `pool` · `slotProvenance` · `viewerId`。
理由：这些是**排序侧的归属信息**，前端既不知道也不该知道。前端若传了，服务端**忽略**。

**响应**：`200 {"accepted": <int>, "rejected": <int>}`。**不返回错误细节**（避免给刷量者反馈信号）。

#### 3.10.4 防刷：服务端校验（客户端上报天然可伪造）

这是本节最关键的一部分。五道校验，全部在服务端：

| # | 校验 | 做法 | 不通过的处置 |
|---|---|---|---|
| 1 | **`reqId` 必须是服务端真实下发过的** | `GET /plaza` 时把 `reqId → {viewerId, 下发的 cardId 集合, 位次, 通道/池归属, 下发时刻}` 写入内存 LRU（TTL **30 分钟**，容量 `ECHO_IMPRESSION_REQ_TTL_SEC` / `_MAX`）。上报时按 `reqId` 反查 | 整批丢弃 + `rank_impression_reject{reason=unknown_req}` |
| 2 | **`viewerId` 必须与 `reqId` 的下发对象一致** | 从 token 解出的 accountId 与快照里的 `viewerId` 比对 | 整批丢弃 + `reason=viewer_mismatch`。**这是越权信号，应告警** |
| 3 | 🔴 **`cardId` 必须在该 `reqId` 实际下发的集合里** | 集合成员检查 | 该条丢弃 + `reason=card_not_delivered`。**这一道最重要**——它让"伪造任意卡的曝光"变得不可能：攻击者只能给"服务端确实发给他的卡"报曝光，而那本来就是要算的 |
| 4 | **时间窗合理性** | `下发时刻 ≤ ts ≤ 下发时刻 + 30 分钟`，且 `dwellMs ∈ [1000, 300000]` | 该条丢弃 + `reason=out_of_window` / `implausible_dwell` |
| 5 | **频率限制** | 单 `viewerId` 每分钟 ≤ `ECHO_IMPRESSION_RATE_LIMIT`（默认 **200** 条曝光）。进程内计数器 | 超出部分丢弃 + `reason=rate_limited` |

> **校验 3 是整个防刷设计的支点**：因为 `viaBoost` / `pool` / `channel` 全部由服务端从 `reqId` 快照里取（不信前端），而 `cardId` 又必须在下发集合内，所以攻击者**能做到的上限**就是"把服务端本来就发给他的卡多报几次曝光"——而那会被 24 h 去重（§3.3）吃掉。**攻击的收益被压到了 0。**
>
> ⚠️ 反过来的攻击面：攻击者**少报**曝光（不上报），让自己的卡少消耗额度、在保底池里待更久。这个方向**无法通过上报校验防御**（不上报是沉默的）。处置：`rank_impression_coverage` 指标监控"下发数 vs 上报数"的比例，单作者显著偏低即告警（§3.10.6）。这个残余风险需产品知情（§7 Q14）。

#### 3.10.5 去重责任在哪端

**两端都做，但责任不同——这一点必须写清，否则会出现"两边都以为对方在做"**：

| 端 | 做什么 | 是否可信 |
|---|---|---|
| **前端** | 同一卡同一会话只报一次 | 🔴 **不可信**，仅作为**减少无效请求**的优化 |
| **服务端** | `(cardId, viewerId, day)` 24 h 去重 | ✅ **唯一权威**。内存集合做性能优化，**DB 唯一键做正确性**（§3.3） |

→ 结论：**服务端不假设前端做过任何去重**。前端的去重纯属省流量，去掉也不影响正确性。

#### 3.10.6 失败重试与丢弃

| 场景 | 前端行为 |
|---|---|
| HTTP 5xx / 网络失败 | 本地队列保留，**最多重试 2 次**，间隔 2 s / 5 s |
| HTTP 4xx | **不重试**（契约问题，重试也不会好），丢弃并 `console.warn` |
| 重试仍失败 | 🔴 **丢弃，不做本地持久化**（不写 localStorage）。理由与 §3.4.3 服务端侧一致：丢失曝光的误差方向是"少记额度消耗 → 卡在保底池待更久 → 偏向多给曝光"，与北极星同向 |
| 队列上限 | 本地队列 **≤200 条**，超出丢弃最旧 |
| `sendBeacon` 无回执 | 卸载期上报**无法确认送达**，接受该损失（这是 `sendBeacon` 的固有特性，也是 §3.6.1 里 `t_event` "允许少量丢失"的同一个原因） |

新增埋点（并入 §3.7）：

| 事件 | 端 | `props` |
|---|---|---|
| `rank_impression_report` | 客户端 | `count` · `retryCount` · `result`(枚举 `ok`/`retry`/`drop`) |
| `rank_impression_reject` | 服务端 | `reason`(见 §3.10.4 五类枚举) · `count` |
| `rank_impression_coverage` | 日作业 | `deliveredCount` · `reportedCount` · `coverageRate` —— 🛡 抓"少报"型作弊与端上 bug |

配置项（并入 §3.9）：`ECHO_IMPRESSION_REQ_TTL_SEC`（1800）· `ECHO_IMPRESSION_REQ_MAX`（50000）· `ECHO_IMPRESSION_RATE_LIMIT`（200）· `ECHO_IMPRESSION_BATCH_MAX`（50）。

> ⚠️ **`reqId` 快照是一笔新的内存开销，且它不在 §1.13 的盘点里**：50,000 个 `reqId` × (20 个 cardId + 位次/归属) ≈ 50,000 × ~600 B ≈ **30 MB**。按 §1.13 的口径这是可接受的，但**它是本方案新增的最大一块内存**，需要 size 埋点。多实例部署下 `reqId` 快照必须能被处理该请求的任意实例读到 → **这是 §6 R2 的又一个面**（也是将来引入 Redis 时该一并承载的第 5 类状态）。

### 3.11 AI 种子内容与 AI 生成标识（v0.2 · 裁定三项）

> 裁定：① **AI 种子内容生产环境也出**；② **必须带 AI 生成标识**（前端角标「该内容由 AI 生成」，**左下角，不烧进图片**）；③ **用户主动分享出去的内容，若含 AI 生成成分，也要带 tag**。
> ⚠️ 这三条裁定改变了 `SPEC §16 Q13` 的原建议（原建议 A：只在 dev/演示环境出现）。本文档**不修改那份规格**，仅记录本方案受此影响的部分。

#### 3.11.1 召回/曝光链路对种子内容不需要特殊排除 —— 确认

> 🔴 **v0.5 前提纠正（B2 连带）**：本节 v0.2 写的是「种子内容 = `originType ∈ {seed_ai, seed_ops}`」。依据 `SPEC-recommendation-ranking §5.3` / `§17.4d` / `RK22`，**这两个枚举值都不存在了**：种子内容实际以**官方运营账号**身份发布（`originType='official'`，有真人运营），运营共创且署名用户的卡归入 `user` + `assistedByOps`。下表按新枚举重述，**四条结论本身未变**。

| 环节 | 种子内容（🔄 `originType='official'`）如何处理 | 需要特殊排除吗 |
|---|---|---|
| **召回** | 正常参与（这是"生产环境铺量"的前提），通道范围由 `SPEC §8.1 H12` 明确列出 | ❌ 不需要 |
| **曝光计数**（§3.3） | **正常记录**。`t_card_exposure` 照常写 `(cardId, viewerId, day)` | ❌ 不需要——而且**必须记**，否则同一张种子卡会在同一用户面前反复出现（去重与频次控制都依赖它） |
| **保底位** | 🔴 **不占**（`RK22` + `H12`：`official` 命中保底组 `FRESH` 时从该路剔除） | ✅ **需要**：`t_card_pool_state.originType`（§3.8 已加该列）在快照构建时过滤掉 `official` |
| **统计 / 北极星 / 配比反算** | 🔴 **不计入**（`RK22`）。🔄 **但计入共鸣厅内容供给量、且产生 R 系列统计**（`§17.4d 第 5 项`，与上一版**相反**） | ✅ **需要**：见下 |

🔴 **一个必须处理的口径污染点（本方案发现，规格未展开）**：

`t_card_exposure` 会包含种子卡的曝光行。而 `RK22` 要求 `official` 不计入分类统计、配比反算与北极星分子分母。**如果对账与看板直接对 `t_card_exposure` 做 `count(*)`，种子卡的曝光就混进了真人内容的统计口径里。**

→ 处置：**曝光明细表本身不加 `originType` 列**（避免又一处反规范化与不一致源），但 §3.6.1 的日对账与所有分析查询**必须 join `t_card_pool_state.originType` 并按 `originType='user'` 过滤**。这条约束需写进对账作业的实现说明与 CR 清单，否则一定会有人写出污染口径的 SQL。

→ `rank_exposure_reconcile` 埋点增加 `userOriginCount` 字段（只统计 `originType='user'` 的部分），与 `detailCount` 并列。**北极星只看前者。**

#### 3.11.2 AI 标识如何携带（含分享物料）

标识是**前端角标形式，不烧进图片**，因此标识信息必须**随数据下发**，不能靠前端猜。

| 场景 | 标识来源 | 携带方式 |
|---|---|---|
| **共鸣厅 feed / 卡详情** | 卡的 `originType` + `aiGenerated` 标记 | feed / 详情响应里下发一个布尔字段（建议 `aiGenerated: true`），前端据此渲染左下角角标 |
| **用户主动分享出去的内容**（裁定 ③） | 同上 | 见下方三种分享形态 |

**分享物料的三种形态，处理方式不同**：

| 形态 | 做法 | 说明 |
|---|---|---|
| **A · 分享链接（H5 落地页）** | 落地页读同一个 `aiGenerated` 字段，渲染同样的左下角角标 | ✅ 与站内一致，零额外成本。**推荐主路径** |
| **B · 分享卡片的社交预览**（`og:image` / 微信卡片缩略图） | ⚠️ 这是唯一一个"角标不可能不烧图"的场景——`og:image` 是一张静态图片，平台不会渲染我们的 HTML | 🔴 **需要产品决策**（§7 Q15）：要么这张预览图在**生成时**叠加标识（等于烧图，与"不烧进图片"的裁定冲突），要么预览图不带标识（合规风险）。**技术上没有第三条路** |
| **C · 用户自行截图** | 无法控制 | 不在系统可控范围内。角标在截图里天然会被一起截到（因为它是页面元素），这反而是"不烧图"方案的一个优点 |

> 🔴 **形态 B 是本节唯一的真实冲突**，必须提请产品裁定，不能默认。它同时触及 `CM-G2`（AI 生成内容必须显式标识，2025-09-01 已施行的硬合规）。我的建议：**`og:image` 预览图在生成时叠加一行小字标识**——理由是"不烧进图片"这条裁定的意图是"不破坏站内视觉与用户自有素材"，而社交预览图是**我方生成的派生物料**、不是用户素材，在它上面叠标识不违背裁定意图，且是唯一能满足 `CM-G2` 的做法。

#### 3.11.3 与召回链路的交互（承接 §2.2.9 第 1 类）

> 🔴 **v0.5 重写（B2 连带）· 我 v0.2 报的「两头都落空」前提已不成立，此项关闭。**
> 那个论证建立在「种子卡背后没有会登录的真人账号」上。而 `SPEC §5.3` / `§17.4d 第 1 项`已明确：种子内容由**官方运营账号**发布，**有真人运营**（会读留言、会持续产出——这正是 `SPEC-admin-console §2.6b-2` 要考核「运营响应率 / 响应时延」的前提）。前提一变，结论就变了。

`SPEC §8.1 H12` 已把官方号的通道范围逐条列清，**不需要再加独立种子通道**：

| 通道组 | 官方号卡能否被召回 | 依据 |
|---|---|---|
| `TAG` / `VEC` / `FOL` | ✅ **能**（`H12` 明确不过滤） | 但这三路属相关性组、受热点在线圈定约束（§2.2.1），实际召回率取决于运营真人的登录活跃度 |
| `CURATED` / `FALLBACK`（热门层 + 随机层） | ✅ **能，且不受热点圈定约束** | `SPEC §3.8.1`：`CURATED` 与 `FALLBACK` 随机层**禁止**按热点在线圈定，候选来源是全库 / 运营指定。**这是官方号内容在召回上的确定性通路** |
| 🆕 `SURGE` | ✅ **能**（`H12` 明确允许） | 全库级日聚合作业产出，同样不受热点圈定约束 |
| `REL` | ❌ 不适用 | 官方号无亲友关系链 |
| 保底组 `FRESH` | 🔴 **不能** | `RK22` + `H12`：命中即从该路剔除。**这一条不变**——保底位是给真人新作者的 |

**输出上限另有约束**：`SPEC §7.1 C13` 定官方号内容首屏 **≤2 条**且独立计数（不复用 C7 的"同一作者 ≤2"额度）。所以「铺量」的天花板本来就由规格封住了，加独立通道反而会与 C13 打架。

→ **结论：`§7 Q11`（是否加独立种子通道）已由 `SPEC H12` + `C13` 正面回答 = 不加，已结案（§7.0a）。** 实现上唯一要做的事是保底组快照按 `originType='official'` 剔除，这条 §3.11.1 已写。

---

### 3.12 「我方派生物料」与「用户原始素材」的边界（v0.3 · 裁定四）

🟢 **裁定**：在 `og:image`（我方生成的分享预览图）上叠一行 AI 标识小字。**站内原图与用户素材一律不动。**

裁定同时要求把边界写清楚，**避免将来被扩大解释成"给用户的照片打水印"**。这个担心是对的——"派生物料"是个可以无限扩张的词，所以下面用**可判定的规则**而不是形容词来划线。

#### 3.12.1 判定规则（三条全部满足才算「可叠标识的我方派生物料」）

| # | 条件 | 为什么这条不可省 |
|---|---|---|
| **C1** | 这张图**由我方代码在服务端生成**，不是用户上传的任何字节的直接呈现 | 划掉一切用户上传物。用户上传的原图、经过无损/有损压缩的原图、裁剪后的原图，都是"用户上传字节的呈现"，**全部不可叠** |
| **C2** | 它的**唯一用途是平台外的元数据展示**（`og:image` / `twitter:card` 这类给第三方平台抓取的静态图），站内不使用这张图 | 划掉一切站内展示物。站内有 HTML 可渲染，标识用前端角标即可，**没有任何理由烧进图片** |
| **C3** | 用户**没有把它当作自己的作品**——它是分发过程的副产品，不出现在作者的内容库里，作者删不了也不拥有它 | 这是最关键的一条。它把"物料"和"作品"分开：作者的作品是他上传/生成的那张，`og:image` 是我们为了让链接在微信里有个缩略图而临时合成的一张卡片 |

🔴 **三条是 AND 关系。任何一条不满足，一律归入"用户原始素材"，不可叠加任何标识。**

#### 3.12.2 逐项落到具体物料上

| 物料 | C1 | C2 | C3 | 判定 |
|---|---|---|---|---|
| 分享预览图 `og:image`（我方按模板合成的卡片） | ✅ | ✅ | ✅ | 🟢 **可叠**（本次裁定的对象，也是**唯一**一项） |
| 站内信息流卡片图 | ✅ 合成 | ❌ 站内使用 | ❌ | 🔴 不可叠 → 用前端角标（§3.11.2 形态 A） |
| 站内详情页大图 | ❌ 用户上传 | ❌ | ❌ | 🔴 不可叠 |
| 用户上传的照片（原图 / 压缩图 / 缩略图 / 裁剪图） | ❌ | ❌ | ❌ | 🔴 **绝对不可叠**。这正是裁定要防的那件事 |
| AI 生成的图片本体（用户在站内生成并保留为作品） | ✅ 我方生成 | ❌ 站内使用 | ❌ **是用户的作品** | 🔴 不可叠 → 角标 + `aiGenerated` 元数据 |
| 导出 / 下载功能产出的文件 | ✅ | ❌ 用户自己持有 | ❌ | 🔴 不可叠。**导出物属于用户**，见下条红线 |
| 官方号 / 种子内容的 `og:image` | ✅ | ✅ | ✅ | 🟢 可叠（同第一项） |

#### 3.12.3 三条防扩大解释的红线

| # | 红线 |
|---|---|
| **L1** | 🔴 **本裁定的适用范围仅限 `og:image` 一处，不得类推到任何其它物料。** 新增物料要叠标识，必须重新走一次 C1–C3 判定并留档，不能引用"§3.12 已经批准过派生物料叠标识"作为依据 |
| **L2** | 🔴 **「导出 / 下载」永远不叠。** 用户点下载拿到的东西属于用户，无论其中有多少 AI 成分。AI 成分的告知义务由**站内标识 + 元数据**承担，不由在用户的文件上打印字来承担 |
| **L3** | 🔴 **叠加的内容限定为「AI 标识」这一个语义，不得夹带任何其它元素**（不得加 logo、水印、二维码、作者 ID、追踪码）。一旦允许"顺便加点别的"，这条通道半年内一定会变成水印通道 |

#### 3.12.4 实现约束

| 项 | 约定 |
|---|---|
| 触发条件 | 仅当该卡 `aiGenerated = true` 时叠加；`false` 的卡预览图**不叠**，两种预览图走同一套模板、只差这一行 |
| 视觉规格 | 固定位置（右下角）、固定字号、半透明底衬保证可读性。🔴 **不得覆盖用户内容的主体区域** |
| 文案 | 与前端角标**同一份文案常量**，不另起一套（否则两处措辞漂移，合规核查会发现两个口径） |
| 缓存与失效 | 预览图按 `(cardId, aiGenerated, 模板版本)` 缓存；`aiGenerated` 被修正时必须失效重生成——🔴 **这是一个真实的失效路径**：审核把一张卡改判为含 AI 成分后，旧预览图仍在第三方平台的缓存里，我方只能保证自己不再返回旧图，无法回收已被抓取的 |
| 残留风险 | 上一条的第三方缓存无法回收，属**已知不可控残留**。合规上的处置是：站内标识与元数据即时生效，预览图尽最大努力。需合规知情（并入 §7 Q15 的结案说明） |

---

## 4. 分期落地建议

> 排期上位约束：`SPEC §14 RK13` 已定「推荐排序是 `SPEC-publish-and-ops`（`t_memory_card` + `category`）与 `SPEC-admin-console`（`t_event` + `/collect`）的下游」。本方案的 P0 项**刻意选成不依赖 `t_memory_card`** 的部分，可与上游并行开工；依赖 `t_memory_card` 的部分（曝光的 `cardId` 语义）在上游落地时只需换主键来源。

### P0 · 与 `SPEC-recommendation-ranking` P0 同批

| # | 交付项 | 依赖 | 备注 |
|---|---|---|---|
| P0-1 | `PgDb.batchUpdate(sql, binders)` + `PgRepository.add(List)` 改多值 INSERT | — | **建议单独 PR 先合**；全工程受益，且是 P0-5 的前提（§2.5.2） |
| P0-2 | `Scheduler.init` 线程数 1 → 4 | — | 🔴 **硬前置**，否则新作业互相阻塞（§3.4.4） |
| P0-3 | `ResonanceService.findSimilar` 抽出（无副作用）；`queryResonance` 保留 | — | WS 1401 与既有单测零改动（§2.5.1） |
| P0-4 | `t_resonance_record` 处置（废弃 或 保留期作业） | 🔄 §7 **`Q8`** 拍板（v0.5 更正：原写 `Q1`，误引） | — |
| P0-5 | `t_card_exposure` + `t_card_pool_state` 建表（注解 + `schema.sql`） | P0-1 | — |
| P0-6 | `ExposureCounter`（LRU 去重 + `LongAdder` 计数 + 驱逐告警） | — | §3.2.3 |
| P0-7 | `ExposureFlushJob`（10 s，`ON CONFLICT DO NOTHING` 批量） | P0-1/2/5 | §3.4 |
| P0-8 | `CardPoolTransitionJob`（每分钟，池位迁移 + 额度判定）+ **看门狗与心跳埋点** | P0-2/5/7 | `SPEC §6.3` 的规则本体。🆕 v0.2.1：作业静默停摆是隐性故障，心跳埋点与看门狗**同批交付**（§2.2.5 ⑥） |
| **P0-8b** 🆕 | **`GuaranteePoolRefreshJob`**（每 60 s 构建保底组内存快照）+ 请求侧只读快照 | P0-2/5 | v0.2.1 · 保底组全库直查的落地形态（§2.2.5 ④）。P0 查 `t_card_pool_state`，P1 迁到 `t_memory_card` 单表索引 |
| **P0-8c** 🆕 🔴 | **`slotProvenance` 全链路打标 + 保底位履约率改口径** | P0-8b | v0.2.1 · **不做这条，通道分组修正无法验证**（§2.2.8）。含"保底位出现 `RELEVANCE` 即告警"的断言 |
| **P0-8d** 🆕 | 保底组降级阶梯 D0–D4（🔴 含"绝不从相关性组补位"的实现约束与单测） | P0-8b | v0.2.1 · §2.2.7。建议单测直接断言 D4 时输出条数 < 20 且无 `RELEVANCE` 占保底位 |
| P0-9 | `POST /api/v1/plaza/impressions` 曝光上报端点 + 前端视口上报 + **五道防刷校验** | ✅ **已裁定 P0 做** | 完整前后端契约见 §3.10，可直接交前端开工。`ECHO_EXPOSURE_SOURCE=impression`；`delivery` 口径与补偿系数（原 §7 Q3）**作废** |
| **P0-9b** 🆕 | `reqId → 下发快照` 内存 LRU（防刷校验 1–4 的依据） | P0-9 | §3.10.4。⚠️ 约 30 MB，是本方案新增的最大一块内存，需 size 埋点 |
| **P0-9c** 🆕 | AI 生成标识：feed/详情/分享落地页下发 `aiGenerated` + 前端左下角角标 | 裁定 | §3.11.2 形态 A。形态 B（`og:image`）待 §7 Q15 裁定 |
| **P0-9d** 🆕 🔴 | 对账与分析查询强制按 `originType='user'` 过滤 | P0-5 | §3.11.1。不做这条，种子卡曝光会污染北极星分子分母（`RK22`） |
| P0-10 | `ExposureRetentionJob`（每日，35 天） | P0-5 | — |
| P0-11 | 埋点：`rank_exposure_*` / `rank_quota_exhausted`（先落日志，格式对齐 `SPEC-admin-console §3`） | §7 Q6 拍板域前缀 | — |
| P0-12 | ArchUnit 依赖规则（黑白名单显式枚举，§3.7.3） | — | 需与 `SPEC §4.5` 作者对齐 |

**P0 明确不做**：`VEC` 通道（`ECHO_RANK_CHANNEL_VEC_ENABLED=false`）· 向量内存镜像 · 日聚合表 · Redis · `IConsentGate`（属合规专项，不在本方案交付范围）

### P1

| # | 交付项 | 依赖 |
|---|---|---|
| P1-1 | `IConsentGate` + `t_ai_consent` 落地；`t_self_vector` 补 `materialRef`/`consentRef` | 合规专项（§2.7 前置） |
| P1-2 | `IVectorStore.topN(VectorQuery)` 重载：门控 JOIN + 排除集下推 + `scanMax` 轮转采样 | P1-1 |
| P1-3 | `VEC` 通道启用（三层门控齐备 + 真实 embedding provider 已配 + REST 侧有 prefs 入口） | P1-1/2、§7 Q4 |
| P1-4 | `/collect` + `t_event`；额度口径切 `impression`（若 P0 走的是 `delivery`，需双跑 2 周对比） | `SPEC-admin-console` P0-1 |
| P1-5 | `ExposureReconcileJob` 日对账（2% 阈值）实装 | P1-4 |
| P1-6 | 去重集合换 `long[]` 开放地址 + 小时分片（DAU > 3 万时） | — |
| P1-7 | `t_card_exposure` 按 `day` range 分区（日增 > 100 万行时；手写 DDL 迁移） | — |
| P1-8 | 曝光日聚合表（仅当分析侧有性能需求） | — |

### P2

| # | 交付项 | 触发条件 |
|---|---|---|
| P2-1 | `VectorMirror` 进程内向量镜像（含 top-K SQL 复核结构，§2.4） | `t_self_vector` 有效行数 > 20000 **且** `rank_vec_scan.scanMs` P95 > 40 ms |
| P2-2 | pgvector HNSW 索引（`vector_cosine_ops`） | 有效向量行数 > `ECHO_VEC_SCAN_MAX` |
| P2-3 | `t_card_exposure` 改由 `t_event` 流式聚合回灌（单一真相源收敛） | 数仓建成 |
| P2-4 | 引入 Redis，一次性承载 session / snapshot / exposure / rate-limit | ≥2 实例部署 **且** 会话 token 已外置（§2.4） |

---

### P0/P1 增量 · 权重衰减模型（§8）

| 期 | 项 | 依赖 | 备注 |
|---|---|---|---|
| **P0** | `t_card_pool_state` **4 列**（`deliveredCount` / `initialWeight` / `brakeFactor` / `drainedAt`，§8.9.1） | — | 与 §3.8 同批。🔴 **不加 `weight` 列**（§8.4.2） |
| **P0** | 权重函数 + 快照作业内存计算排序（§8.1 / §8.4.2） | 曝光上报端点（§3.10）**硬前置**（`n` 的唯一来源） | `ECHO_WEIGHT_ENABLED` 默认 `false`，灰度打开。**不需要新索引** |
| **P0** | 欠投补发 clamp（§8.4.3） | `D_min` 的队列分位统计 | 🔴 修 `SPEC:815`/`817` 指向的实质问题，**不是可选项**。一行公式 |
| **P0** | 启动期配置校验（§8.9.3 五条） | — | 🔴 `MIN_RATIO < FAIR_FLOOR` 与 `COOLDOWN > DRAIN_AGE` 两条挡的是**静默失效** |
| **P0** | 权重单调性巡检指标（§8.9.4） | — | §8.5.3 红线的运行时探针 |
| **P1** | 制动 B1（§8.5.2） | 「不看」事件就位 | B2/B3 复用 `SPEC` 既有机制。**B4 不需要实现**（自愈） |
| **P1** | `CardActivityRollupJob` + `CardDrainJob`（S4 自然流掉，§8.9.2） | — | 30 天聚合表 |
| **P1** | `SURGE` 通道：`SurgeDetectJob` + `SurgeExpireJob` + 五道防刷（§8.6） | 互动信号（**今天已可得**，§8.6.2） | 🔴 `surge_window_overdue` 指标必须与功能同批 |
| **P2** | `SURGE` 接入搜索命中信号（§8.6.2 增强项） | 搜索功能本身尚未实现 | 缺了它通道照样能跑 |

---

## 5. 与上游规格的对齐清单

| `SPEC-recommendation-ranking` 条目 | 本方案的承接 |
|---|---|
| `§3.1` `VEC` 通道（配额 30、输出 ≤8） | §2.8 `ECHO_VEC_TOPN=30`；配额转移按 `§3.3 规则 1` |
| `§3.3` 三条 `VEC` 合规硬规则 | §2.7 的 L1/L2/L3 三层门控逐条对应；规则 3 的默认 `false` 沿用不改 |
| `§4.1 F2` `resonanceAffinity = 1 − cosineDistance` | 沿用 `ResonanceHandler.toAffinity`（`ResonanceHandler.java:47-53`）口径，不另立 |
| `§6.3` 曝光计数按 `(cardId, viewerId)` 24 h 去重 | §3.3 由 `uk(cardId, viewerId, day)` 承担；`day` 口径同 `EchoApi.today()` |
| `§6.3` 单卡单日 ≤100 / 池额度 300/200/50 | §3.2.3 内存实时判定 + §3.8 `t_card_pool_state.boostExposure` |
| **`§3.8.1` 通道按候选集来源分三组**（v0.2.1 修正）<br>🔄 **v0.5：保底组只剩 `FRESH`** | §2.2.1 三组定义（含论证强度表：15% 由"缩水成 5%"变为"归零"）· §2.2.4 保底组直查 · §2.2.5 可行性核实（论据成立，补三处实现约束）· §2.2.6 预算隔离 · §2.2.7 降级阶梯（D3 取消，禁止相关性组补位） |
| 🆕 **`§3.8.5` 保底位真实性监控（>50% 告警）** | §2.2.8 `slotProvenance` + `rank_boost_slot_overlap`，同口径同阈值。**本文档 v0.2.1 主动提出的口径修正已被上游采纳** |
| 🆕 **`§6.6` 曝光上报端点 P0 就做**（上游裁定） | §3.10 前后端契约；`§7.1 Q2` 已据此结案（§7.0a）。`SPEC` 同节删除的两条埋点缺位退路，本文档不再保留任何等价降级口径 |
| 🆕 **`§8.1 H11` 自然流掉硬过滤 `poolTag='DRAINED'`** | §8.7.4（v0.5 回改）：`DRAINED` 是过滤谓词、`drainedAt` 是时刻记录，同事务写、召回层只读前者。§3.8 的 `pool` 枚举已补回 `DRAINED` |
| 🆕 **`§8.1 H12` 官方号通道范围** | §3.11.3：官方号经 `CURATED`/`FALLBACK` 随机层/`SURGE` 进入（不受热点圈定约束）；保底组 `FRESH` 命中即剔除。`§7.1 Q11` 据此结案 |
| `§10.2` 保底位履约率硬阈值 100% | §3.5.2 论证：**不受最终一致影响**（履约由编排层同步判定，不读曝光）。🆕 v0.2.1 **另提口径修正**：现定义只统计"位置是否填满"，在通道分组失效时会显示 100% 假象 → 建议改为按 `slotProvenance` 统计（§2.2.8）。🟢 **v0.5：已被 `SPEC §3.8.5` 采纳** |
| `§11 P1-8` `PgVectorStore.topN` 支持 SQL 侧过滤谓词 | §2.8 `VectorQuery` 重载（本方案把它从 P1 提为 `VEC` 启用的**硬前置**） |
| `§12.4` 缓存表（`poolIndex` TTL 60 s 等） | §3.5 表 #6 的 70 s 滞后正是 10 s + 该 60 s |
| `§12.5` Aengine `scheduler` 承载日作业 | §3.4.4，并指出**必须先把线程数从 1 提到 ≥4** |
| `§12.6` / `§15 Q8` `ResonanceService` 副作用处置 | §2.5 采纳方案 A，并加两条（`persistRecords` 批量化、表保留期/废弃） |
| `§12.7` 降级链 L1 | §2.6.3，不新增层级、不改"末端不得按热度排"红线 |
| `§15 Q10` 排序侧自建轻量 `t_card_exposure` | §3.3 采纳，并补规格未展开的 P0 曝光信号来源问题（§3.6.3） |

---

## 6. 风险

| # | 风险 | 影响 | 处置 |
|---|---|---|---|
| R1 | **§2.3 的时延/内存数字全是估算，未实测** | 若 pgvector 实际比估算慢 5–10 倍（TOAST 读放大可能被低估），`VEC` 单路 78 ms 预算会破 | 上线前必须跑基准（5k/20k/100k × 768 维），把真实数字**回填 §2.3**；`rank_vec_scan.scanMs` 埋点作为长期实测 |
| R2 | **单进程假设一旦破，曝光计数会失真** | 多实例时内存去重集合与 `LongAdder` 各进程独立 → 单卡单日上限变成 `N × 100`；`t_card_exposure` 的唯一键仍能保证明细正确，但**上限判定会超发** | 这是引入 Redis 的**硬触发条件**（P2-4）。在此之前，部署文档必须写明"echo-server 单实例"是排序正确性的前提 |
| R3 | **`LRUCache` 依赖 `concurrentlinkedhashmap-lru 1.4.2`（2013 年后停止维护）** | 作为热路径主力缓存有长期维护风险 | 建议评估换 Caffeine。⚠️ 这是 **Aengine 侧改动**，按工作区约定需先与引擎侧确认，不在本方案自行决定 |
| R4 | **`t_self_vector` 缺 `materialRef`/`consentRef`（`G0-10 ①` 现存缺口）** | `VEC` 门控 L2 无法实现；且按 `G0-10 ④` 的日核查 SQL，现有向量行会被判为合规缺口 | 列为 `VEC` 硬前置（P1-1）。**这是既有缺口，不是本方案引入的**，但本方案是第一个被它阻塞的下游 |
| R5 | **`t_pet.seenCount` 极易被误当作曝光口径** | 它既是 `X6` 禁读的"看过数"，又长得像曝光计数；且现有实现有丢更新竞态（§1.11） | §3.7.3 把它明确列入 ArchUnit 黑名单；曝光计数**绝不复用**它 |
| R6 | **`GET /plaza` 现在打的埋点事件名是 `window_open`（语义错误）** | `SPEC §4.1 F3` 的 `topicMatch` 依赖 `window_open` 聚合，口径污染会直接影响题材偏好个性化 | 建议在接入排序时一并修正（列表请求不应打 `window_open`）。但 `SPEC §10.1` 已定「既有事件名一律不改、只允许新增」→ 需与 `SPEC-admin-console` 作者确认这算"改名"还是"修 bug"（§7 Q7） |
| R7 | **`ON CONFLICT` 与注解自动建表机制不兼容** | 曝光落库 SQL 必须手写，绕过 `PgRepository.add`；未来若有人"顺手"改回用 `add()`，幂等性会静默丢失 | 在 `ExposureRepository` 里覆写并让 `add()` 抛 `UnsupportedOperationException`，强制走批量方法；配单测断言 |
| R8 | **曝光数据的 PIPL 定位需合规确认** | `(cardId, viewerId)` 是行为个人信息；账号注销时是否需清理、35 天保留期是否足够，本方案是技术判断而非合规判断 | §7 Q5 交合规裁定 |
| **R9** 🆕 🔴 | **保底位被相关性组静默占用**（v0.2.1 修正针对的失效模式） | 报表显示履约率 100%、北极星不动，**现有监控发现不了**。这是本方案里唯一一个"失败时看起来像成功"的风险 | 三道：① `slotProvenance` 打标 + 保底位出现 `RELEVANCE` 即告警（§2.2.8）；② 履约率口径改为按来源统计；③ 编排层**先留位再填充**的顺序约束进单测（P0-8c/8d） |
| **R10** 🆕 | **`GuaranteePoolRefreshJob` / `CardPoolTransitionJob` 静默停摆** | 池位冻结。🔄 **v0.5 重估**：`REVIVE` 删除后原来那半（新 `REVIVE` 不入池）消失，但换了一个**更要紧**的不安全方向——**新过审的卡入不了 `FRESH` 池**，而 `FRESH` 现在是保底组唯一来源，新作者的第一张卡直接拿不到保底位 | 心跳埋点 + 5 分钟看门狗（§2.2.5 ⑥）。**前置**：调度器线程数必须先从 1 提到 ≥4（P0-2），否则作业会被别的作业阻塞而"看起来像挂了" |
| **R11** 🆕 | **保底组查询顺手多 select 几列导致回表** | 0.5 ms 劣化到 5–50 ms，慢 10–100 倍；且劣化是渐进的（卡越多越明显），容易被当成"数据量大了自然变慢" | §2.2.5 ① 的约束写进 CR 清单：**保底组查询只取 id**。建议加单测断言 SQL 文本不含除 id/排序键外的列 |

---

## 7. 未决项（需产品 / 制作人 / 合规拍板）

> 前 4 项**不定则相应模块不建议开工**。

### 7.0 v0.3 已结案项

| # | 裁定 | 落点 |
|---|---|---|
| **Q10** | 🟢 **A**（P0 只加 size 观测埋点，不动引擎）。不修的正式理由已入档，且约定**将来必须两条一起改，只做一条视为未修** | §1.14 |
| **Q13** | 🟢 **A**（`LONGTAIL` 归保底组）。🔴 **但落地时发现上游冲突**：`SPEC` v0.2 已移除长尾轮播，本裁定在当前规格下是空操作 → 转为新问题 **Q17** | §8.7.5 |
| **Q15** | 🟢 **A**（`og:image` 叠一行 AI 标识小字）。并按要求补齐**「我方派生物料」vs「用户原始素材」的可判定边界**（C1–C3 三条 AND 条件 + 逐项判定表 + 三条防扩大解释红线） | §3.12 |
| **向量路线** | 🟢 采纳四级阶梯，P0 = **一条 `CREATE INDEX ... USING hnsw` DDL，零新组件**；Redis 加固设计保留为可执行预案 | §2.4 · §2.10.6 · §2.10.7 |
| **Q17** | 🟢 **A**（维持 `SPEC` v0.2 对 `LONGTAIL` 的移除）。我报的那条「残留缺口」**已被后续两条裁定正面关闭**：无人问津的内容自然流掉是**有意为之**；且新增了 `SURGE` 这条由**真实需求**驱动的回归出口。不需要任何补偿机制 | §8.7.5 |
| **分发机制** | 🟢 **配额记账 → 权重衰减**（v0.4 换代）。作废清单见 §8.0；`REVIVE` 建议整个删除 → 遗留接口变更转 **Q18** | §8 整节 |

### 7.0a v0.5 已结案项（🔴 全部为「上游已给结论、本文档只需回改标记」，非本文档自行裁定）

> **本节的性质要说清楚**：下列五项在 v0.4 里仍标着「未决」，但上游 `SPEC-recommendation-ranking` v0.3 与用户裁定**早已给出结论**。它们不是新的判断，是**回改滞后**——本文档文首已写「上游规格口径以它为准」，这些标记继续挂着只会让研发误以为还能选。**依据全部落在 `SPEC` 或用户裁定原文，无一条由本文档自行拍板。**

| # | 原状态 | 🟢 结案结论 | 依据出处 | 落点 |
|---|---|---|---|---|
| **Q1** 🔴 | 「热点在线圈定是否接受否决」标**未决**，本文档建议 **A（改按向量全集）** | 🔴 **我的建议 A 被否，维持热点在线圈定，但限定在相关性组内。** 保底组 + `CURATED` + `FALLBACK` 随机层 + `SURGE` 全部**禁止**热点圈定 | `SPEC §3.8` 开头：「**上游裁定**：候选集**保留「热点在线」作为圈定依据**（技术侧"改为按内容侧可召回性圈定"的建议被否）」+ `§3.8.1` 分组表 | §2.2.1（v0.2.1 已按此实现，本轮只销掉 §7.1 的残留标记）<br>⚠️ Q1 原背景里「与 `SPEC §6.2` `REVIVE` 池（`poolBoost` 1.50）冲突」这条论据**已失效**（`REVIVE` 已删，`poolBoost` 随额度概念作废） |
| **Q2** 🔴 | 「P0 是否自建曝光上报端点」标**未决**，本文档建议 **A（做）** | 🟢 **A，P0 就做。** 前端排期配合 | `SPEC §6.6` 「🟢 P0 可运转性结论（**上游已裁定「曝光上报端点 P0 就做，前端排期配合」**）」；同节并已**删除**原先两条埋点缺位退路 | §3.10 前后端契约（v0.2 已按裁定写完，`Q2` 标记是遗留） |
| **Q3** | 「若 Q2 选 B，补偿系数 1.5 是否接受」 | ⚪ **随 Q2 结案自动作废**。Q2 = A 意味着不存在"服务端下发即记账"的补偿口径，1.5 这个数没有适用场景 | 同上。且 `SPEC §6.6` 已明确删除「P0 先用请求数近似曝光数」这条退路，理由是 `n` 被高估会让 `γⁿ` 提前衰减 | §7.1 整条划除 |
| **Q11** 🔴 | 「AI 种子内容要不要独立召回通道」 | 🟢 **不加独立通道。** 官方号内容经 `CURATED` / `FALLBACK` 随机层 / `SURGE` 进入（这三路按 `§3.8.1` 禁止热点圈定，是确定性通路），首屏 ≤2 条封顶 | `SPEC §8.1 H12`（官方号通道范围逐条列出）+ `§7.1 C13`（≤2 条、独立计数）+ `§5.3`（官方号**有真人运营**——原「两头落空」论证的前提由此消失） | §3.11.3 重写 · §2.2.9 第 1 类关闭 · §2.2.9 建议 A 撤回 |
| **Q18** | 「`REVIVE` 删除的三处连带影响需排序侧吸收」 | 🟢 **三处已全部被 `SPEC` v0.3 吸收，无遗留。** ① 池枚举已收敛（`REVIVE` 删、`ARCHIVED_FROM_FEED` 改名 `DRAINED`）；② 15% 构成已改「3 位全给 `FRESH`」；③ `TC-RANK-49` 判据已改写为「仍可被搜索与作者主页访问，且够格时可经 `SURGE` 回来」 | 用户裁定（零回应复活取消，投过了没人接即视为吸引力不足）→ `SPEC §3.8.1` · `§6.2`（`P-流掉 DRAINED`）· `§7.1 C3` · `§3.8.5` / `RK18` | §2.2.1 论证强度表 · §2.2.4 · §8.7.3 |

### 7.1 未决项

> 🔄 **v0.5**：`Q1` / `Q2` / `Q3` / `Q11` / `Q18` 已结案，移入 §7.0a。下表保留原行但标注结案指针，**不删除**，以便追溯当初的选项与理由。

| # | 问题 | 背景与冲突 | 选项 | 我的建议 |
|---|---|---|---|---|
| ~~**Q1**~~ | 🟢 **已结案（v0.5）→ §7.0a：建议 A 被否，维持热点在线圈定但限定在相关性组内**（`SPEC §3.8`）。以下为原文留档 —— **「热点在线人群」作为向量候选集的圈定依据，是否接受否决？** | 这是产品给的核心方向之一，我否决它的依据：按活跃度圈定候选集会让**不活跃作者的卡永远不经 `VEC` 通道被召回**，与 `SPEC §6.2` `REVIVE` 池（`poolBoost` 1.50，全局最高）的存在目的直接冲突；且「热度」是 `SPEC §0.2` 明令废除的表述 | **A** 接受替代方案：候选集 = 授权有效的向量全集，超 `SCAN_MAX` 时按 `id` 取模轮转采样<br>**B** 维持"热点在线 5000 人"，接受该偏置<br>**C** 折中：全集 + 活跃度作为**排序打破平局**的次级键 | **A**。它同时更简单（不需要维护物化集合、无写入方、无淘汰逻辑、无冷启动预热，§2.2.3）、成本上界一致、且零活跃度偏置。C 看似温和，但"次级键"半年后极可能被提成主键 |
| ~~**Q2**~~ | 🟢 **已结案（v0.5）→ §7.0a：A，P0 就做**（`SPEC §6.6` 上游裁定，契约见 §3.10）。以下为原文留档 —— **P0 是否自建最小曝光上报端点 `POST /plaza/impressions`（需前端改动）？** | 不做则只能用"服务端下发即记账"，其误差方向是**系统性少给曝光**——与北极星（`GTM4`）反向 | **A** 做（前端加视口观察 + 500 ms 合批上报）<br>**B** 不做，走 `source=delivery` + 补偿系数 1.5<br>**C** 等 `/collect`（`SPEC-admin-console` P0-1）一起做 | **A**。成本很小（一个路由 + 一次写内存缓冲），换来的是额度口径从一开始就贴近"真的被看见"。C 会让排序 P0 被数据基座卡住，而 `SPEC §15 Q10` 已判"曝光是排序的内部状态，不该等分析基座" |
| ~~**Q3**~~ | ⚪ **已随 Q2 结案自动作废（v0.5）→ §7.0a**。以下为原文留档 —— **若 Q2 选 B，补偿系数 1.5 是否接受？** | 1.5 是一个**没有实测支撑的猜测**（首屏 20 条的真实渲染率未知）。选它等于让 P-新 的 300 额度实际执行到 450 | **A** 接受 1.5，P1 拿到真实渲染率后校准<br>**B** 不补偿（接受系统性少给曝光）<br>**C** 更保守用 2.0 | **A**（前提是 Q2 选了 B）。**B 不可接受**——它会让「零回应窗口占比」这个 `SPEC §10.2` 的第一指标被一个纯技术原因系统性推高 |
| **Q4** 🔴 | **`VEC` 通道在 P0 是"默认关闭"还是"明确不做"？** | `SPEC §3.3 规则 3` 已定默认 `false`。但勘察发现更硬的事实（§1.4）：H5/REST 侧与向量域**零接线**，H5 用户 100% 无向量；且默认 `MockEmbeddingClient` 产出确定性哈希、非语义向量。即使门控明天就绪，通道也会返回空 | **A** 明确不做：P0 不写 `VEC` 代码，30 配额永久转 `TOPIC`(+15)/`FRESH`(+15)<br>**B** 写代码但默认关（规格现状）<br>**C** 补齐 REST 侧 prefs 入口，让 `VEC` 在 P0 可用 | **A**。B 会产出一段**永远跑不到、无法被测试覆盖**的代码路径，那比没有更糟。C 是一个独立的产品决策（要不要在 H5 上做偏好提交流程），不该由排序方案顺手带出 |
| **Q5** | **曝光数据的 PIPL 定位与保留期** | `(cardId, viewerId)` = "这个人看过这张卡"，属行为个人信息。本方案定 35 天保留期，并判断它**不需要** `materialRef`/`consentRef`（不是素材派生物）——这是技术判断，需合规确认 | **A** 确认 35 天 + 挂账号注销清理链路<br>**B** 缩短到 7 天（但会影响 `SPEC` 的 30 天口径）<br>**C** 需要双外键 | **A**。`SPEC §4.2 G5`（近 30 天无举报）、`§6.4`（长尾每 7 天）等口径都需要 ≥30 天窗口，35 天是最小可行值 |
| **Q6** | **`rank_` 域前缀（= `SPEC §15 Q11`）** | 本方案的 7 个新事件全部落在 `rank_` 域。该前缀本身是 `SPEC-admin-console §3.1` 固定集合外的新增，尚未裁定 | 同 `SPEC §15 Q11` 的 A/B/C | 跟随 `SPEC §15 Q11` 的裁定，**本方案不单独主张**。若判 B/C，本方案的事件名跟着改 |
| **Q7** | **`GET /plaza` 现有埋点事件名 `window_open` 语义错误要不要修？** | `EchoApi.java:554` 在列表请求上打 `window_open`。`SPEC §4.1 F3` 的 `topicMatch` 依赖它聚合，口径污染直接影响题材偏好。但 `SPEC §10.1` 已定「既有事件名一律不改、只允许新增」 | **A** 算修 bug，直接改（`/plaza` 不打 `window_open`）<br>**B** 算改名，保持不动，新增一个正确的事件<br>**C** 保持不动，在聚合侧过滤掉来自 `/plaza` 的记录 | **A**。这不是命名偏好问题，是**同一个事件名承载了两种语义**，任何下游聚合都是错的。需与 `SPEC-admin-console` 作者确认 |
| **Q8** | **`t_resonance_record` 保留还是废弃？** | 零消费者（§1.1 已逐条反查）；无保留期；索引形态说明它从未被设计过读取场景 | **A** 废弃（删 `persistRecords`，表下版本 drop）<br>**B** 保留 + 30 天 TTL 作业<br>**C** 保留，无 TTL（现状） | **A**。留一张没人读的表 + 一条无人消费的写路径 = 纯技术债。"以后可能有用"不是保留**写入**的理由——`SPEC §5.4 P0` 的影子日志能提供完整得多的数据。**C 不可接受**（无界增长） |
| **Q9** | **ArchUnit 黑白名单的"互动计数 vs 曝光计数"区分（§3.7.3）** | `SPEC §4.3 X6` 禁「看过数的数值」进排序，但 `§6.3` 的额度机制**必须**读曝光计数。按字面执行会互相矛盾 | **A** 采纳显式黑白名单（黑：`t_remember`/`t_flower_log`/`t_pet.seenCount`/`flowersReceived`；白：`t_card_exposure`/`t_card_pool_state`）<br>**B** 只写文档不做构建期规则 | **A**。区分的实质：**互动计数度量"多少人喜欢它"（马太效应的燃料），曝光计数度量"它已经拿到多少机会"（马太效应的刹车）**，作用方向相反。需与 `SPEC §4.5` 作者对齐后并入其保证 2 |
| **Q10** | **Aengine `CachedRepository` 要不要改** | §1.13.5 结论：**不建议单独修 `maxElements`**（修了也不解决问题，还给人假的安全感）。真正该修的是 `CacheIndex.identities` 无上界 + `SimpleCache` 换 `LRUCache` 两条一起做 | **A** P0 只加 size 观测埋点，不动引擎<br>**B** 现在就改引擎两条<br>**C** 只改 `maxElements` | **A**。两条引擎改动都在 `Aengine` 侧，按工作区约定需先与引擎侧确认；且删掉 `persistRecords` 之后已无高危路径（§1.13.4）。**C 明确不可取** |
| ~~**Q11**~~ | 🟢 **已结案（v0.5）→ §7.0a：不加，官方号有 `CURATED`/`FALLBACK` 随机层/`SURGE` 三条确定性通路**（`SPEC H12`+`C13`）。以下为原文留档 —— **AI 种子内容要不要独立召回通道** | 本轮裁定 3 决定种子内容进生产铺量。但 §2.2.9 第 1 类指出：种子卡**两头都落空**——相关性组召不到（作者永不在线）、保底组也不给（`RK22` 规定 `seed_ai` 不占保底位）。不补通道，"铺量"在召回链路上拿不到效果 | **A** 加独立种子通道（固定配额，复用保底组的快照机制，成本极低）<br>**B** 不加，靠兜底层偶然出现<br>**C** 改 `RK22`，允许 `seed_ai` 占保底位 | **A**。**C 不可取**——让 AI 生成内容占用"扶持真人新作者"的保底位，与保底位的存在理由直接冲突。B 等于裁定 3 的目的落空 |
| **Q12** | **`rank_pool_shortfall` 的告警阈值怎么分阶段** | §2.2.7 的 D4（保底池真空、保底位留空）在种子期是**会真实发生的**（`GTM` 100–300 人，且 `SPEC §14 D21` 已允许 feed 出现终点）。一上线就按 0 报警会淹掉告警通道 | **A** 分阶段：种子期阈值按"供给量的函数"设，早期起收紧到 0<br>**B** 固定 0，靠人工静默<br>**C** 种子期不报 | **A**。需产品给出种子期可接受的 shortfall 比例。**B 会导致告警疲劳，进而让真正的故障被忽略** |
| **Q14** | **「少报曝光」这个攻击方向的残余风险是否接受** | §3.10.4 的五道校验能把"伪造曝光"压到 0，但**不上报**（让自己的卡少消耗额度、在保底池待更久）无法通过上报校验防御——沉默是检测不到的。只能靠 `rank_impression_coverage` 事后监控 | **A** 接受残余风险 + 覆盖率监控告警<br>**B** 改用服务端下发即记账（无此攻击面，但误差方向变成系统性少给曝光）<br>**C** 双口径交叉校验 | **A**。B 的代价见 §3.6.3（与北极星反向）。C 成本高且 P0 没有第二个口径可交叉。**需产品知情这条残余风险的存在** |
| **Q15** 🔴 | **分享预览图（`og:image`）上的 AI 标识怎么处理** | 裁定"标识不烧进图片"，但 `og:image` 是静态图，社交平台不会渲染我方 HTML → **技术上没有第三条路**（§3.11.2 形态 B）。同时触及 `CM-G2`（AI 生成内容必须显式标识，硬合规） | **A** 预览图生成时叠加一行小字标识（等于对这一张图烧字）<br>**B** 预览图不带标识<br>**C** 含 AI 成分的内容不生成社交预览图 | **A**。"不烧进图片"的裁定意图是不破坏站内视觉与用户自有素材，而 `og:image` 是**我方生成的派生物料**，在它上面叠标识不违背该意图，且是唯一满足 `CM-G2` 的做法。**B 有合规风险，不建议** |
| **Q16** | **热词晋升出口是否计入作者的「重跑 ≤2 次」配额** | `SPEC §6.4` 给了三条重新激活出口，`SPEC §6.3` 定了「累计重跑 ≤2 次」防作者刷额度。但热词晋升（`SPEC:577`）是**平台侧事件、非作者可控**，把它计入作者配额等于让作者为平台行为付代价；不计入则一张命中多个热词的卡可能反复回归、反复获得新的 `W0` | **A** 不计入作者配额，但单独设上限（每卡因热词回归 ≤1 次）<br>**B** 计入，与编辑重过审共用 ≤2 次<br>**C** 不计入且不设上限 | **A**。B 会让作者因平台行为失去自己的重跑机会；**C 不可接受**——热词是会持续晋升的，不设上限等于开了一个无界的 `W0` 重新授予入口（§8.1.2）。需与 `SPEC` 作者确认 |
| ~~**Q18**~~ | 🟢 **已结案（v0.5）→ §7.0a：三处连带全部被 `SPEC` v0.3 吸收完毕**。以下为原文留档 —— **`REVIVE` 删除的三处连带影响需排序侧吸收** | §8.7.3 建议整个删除 `REVIVE`（"欠投补发"已由 §8.4.3 的 clamp 承担）。连带：① `SPEC §6.2` 四池 → 三池；② 15% 的构成由「2 新 + 1 复活」改为 **3 位全给新内容**（比例不变）；③ 🔴 `SPEC` 的 `TC-RANK-49` 过标准是「仍能拿到**复活**保底位」（`SPEC:1648`），删除后**必然失败** | **A** 按 §8.7.3 执行，`TC-RANK-49` 改写为「自然流掉后仍可被搜索/主页访问，且够格时可经 `SURGE` 回来」<br>**B** 保留 `REVIVE` 空壳以免动 `SPEC` | **A**。B 会留下一个永远为空的池和一条永远为真的迁移条件，比删掉更难理解。这不是待拍板项，是**需要转达给排序侧的接口变更**（本文档无权改 `SPEC`） |

---

## 8. 推荐权重衰减模型（v0.4 · 重做，取代 v0.3 的配额记账）

### 8.0 机制换代说明与作废清单

产品原话：

> 你这个投放节奏是按照次数直接投吗。你做个权重类的，然后获得一次投放机会就衰减一下不就好了吗。什么给 700 次，哪有这么直接的。

**v0.3 的「曝光次数配额记账」整套作废。** 明确列出被删掉的东西，防止在别处残留引用：

| 已删除 | v0.3 原位置 |
|---|---|
| `budgetTotal` / `budgetUsed` / `carriedOverBudget` / `dailyAllowance` 等 11 列 | §8.9.1 |
| 700 / 300 / 200 次这类硬计数上限 | §8.7.0 · §8.2.1 |
| 结转机制 | §8.7.3 |
| 分档日配额（T1 60/日、T2 30/日） | §8.3 |
| 超发算术与容量自洽推导 | §8.8.1 |
| `TC-BUDGET-01…13` | §8.10 → 本节重写为 `TC-WEIGHT-*` |
| `REVIVE` 零回应复活池 | §8.7.3（另见本节 §8.7.3 的删除结论） |

🟢 **确认产品的判断成立**：`SPEC:815`「7 天或 200 次先到为准」与 `SPEC:817`「至少 700 次曝光机会」的矛盾，**在权重制下自动消失**。矛盾的来源本身消失了——那两句话是**两个硬上限**（一个时间上限、一个次数上限）在供给不足时互相踩踏。权重制里没有任何硬上限，只有一条连续单调下降的曲线，**"两个上限谁先到"这个问题不存在**。所以结转机制是为了修一个不再存在的问题而设计的，已删除。

但要保留那个矛盾**指向的实质问题**：卡可能因为我们的供给不足或候选集圈定问题而**根本没被投出去**。这个问题在权重制下**不会自动消失**——时间衰减是照着墙上的钟走的，不管这张卡有没有真的被人看到。处置见 §8.4.3（一个 clamp，不是一套机制）。

---

### 8.1 权重函数

#### 8.1.1 形式

```
W(card) = W0 × γ^n × T_eff(a, n) × brakeFactor

W0          = 初始权重（发布时确定，§8.1.2）
n           = 累计主动分发投放次数（去重曝光数，口径见 §8.4.1）
γ           = 单次投放衰减因子 = 0.97
a           = 过审至今小时数
T_eff       = 时间衰减因子（§8.1.4），值域 (0, 1]
brakeFactor = 负反馈制动累积系数（§8.5.2），值域 (0, 1]，初值 1.0
```

🔴 **除 `W0` 之外的三个因子值域全部是 (0, 1] 且单调不增** —— 这一条是 §8.5.3「权重只减不增」结构性保证的全部依据，改动公式时不得破坏它。

#### 8.1.2 初始权重 `W0`（发布时一次性确定）

> 🔴 **v0.5 回改（B 类台账 B2）**：`originType` 枚举**只有两个值** —— `{user, official}`。依据 `SPEC-recommendation-ranking §5.3` 枚举重构表 + `§17.4d 第 1 项` + `RK22`：「AI 生成」是**素材成分标记**（`aiGenerated` 布尔）而非内容来源类别，**平台不做自创发布**，故 `seed_ai` 作为来源类别**已整条取消**；原 `seed_ops`（运营共创、署名用户）归入 `user` + `assistedByOps` 布尔。
> **核实结论：`seed_ai = 0.30` 已无任何存在依据，本轮删除。** 它在 v0.4 里的挂靠依据是「`RK22` 不占保底位」，而 `RK22` 现行原文恰恰是取消该类别本身；留着它会让实现按一个不存在的枚举值给权重（`W0` 是发布时一次性写入 `initialWeight` 列的、永不 UPDATE 的值，§8.9.1 —— 一旦写错就没有纠正入口）。

| `originType` | `W0` | 说明 |
|---|---|---|
| `user` | **1.0** | 🔴 **所有用户内容一律 1.0，无差别**（含 `assistedByOps=true` 的 `GTM5` 运营共创卡——它们署名用户，不降权） |
| `official` | 0.30 | `SPEC §5.3.1` 官方号限流，且不占保底位（`H12`） |
| ~~`seed_ai`~~ | ~~0.30~~ | 🔴 **v0.5 删除**：该来源类别已被 `SPEC §5.3` / `RK22` 取消，见上方说明。**枚举里没有这个值，不得为它保留权重** |

🔴 **禁止进入 `W0` 的因子**（沿用 v0.3 红线，未变）：任何互动数据 · 作者粉丝数（`X12`）· 作者历史表现（会造成**作者级**马太，比卡级更隐蔽且永久）· 题材/标签热度（会让冷门题材系统性吃亏，反北极星）· 内容质量分 / 审核评分。

> 结果：**同一时刻过审的两张用户内容，`W0` 完全相同**，无论作者是谁、内容是什么。

#### 8.1.3 为什么两个维度**相乘**而不是相加

| # | 理由 |
|---|---|
| **1** | 🔴 **「只减不增」成为结构性保证**。`γ^n ≤ 1` 且 `T_eff ≤ 1`，两者都是值域 (0,1] 的**单调不增**函数，所以 **`W ≤ W0` 恒成立**——这是**代数上的**保证，不需要任何运行时检查或纪律约束。加法做不到：它需要额外钉一个 clamp，而 clamp 是可以被人改掉的 |
| **2** | **语义正确**。两个维度是**互相独立的耗损来源**，相乘表达"两种耗损各自独立生效"。相加会出现"投了 500 次但内容还很新，时间项还撑着所以权重仍然不低"——与"投得多了自然沉下去"直接冲突 |
| **3** | **量纲干净**。`W0` 是权重，两个因子是无量纲衰减系数。相加需要两个同量纲的量，而"投放次数"与"小时数"量纲不同，必须各自先标定到权重量纲，多引入两个任意常数 |

#### 8.1.4 时间衰减 `T`：分段指数，3 天是曲率转折点

产品原意「新上作品优先级较高，3 天、7 天两档自然滑落」在权重制下体现为**曲线形状**，而不是分档配额：

```
T(a) = exp(−a / 72)                           a ≤ 72h    （τ₁ = 72h，慢衰段）
T(a) = exp(−1) × exp(−(a − 72) / 36)          a > 72h    （τ₂ = 36h，快衰段）
```

| 时刻 | `T(a)` | 说明 |
|---|---|---|
| 0 h | 1.000 | 刚过审 |
| 24 h | 0.717 | |
| **72 h（3 天）** | **0.368** | 🔴 **曲率转折点**：时间常数由 72h 缩短到 36h，衰减加速一倍 |
| 120 h（5 天） | 0.098 | |
| **144 h（6 天）** | **0.050** | 恰好触及退出阈值 `W_MIN`（§8.3）——零投放的卡靠时间衰减在**第 6 天**退出首页 |
| **168 h（7 天）** | **0.026** | 已明显低于阈值，「7 天见底」成立 |

**为什么是分段指数**：

- 「3 天、7 天两档」在权重制下的正确表达是**衰减速度换档**，不是额度换档。分段指数让「3 天」成为一个真实的物理拐点（一阶导数不连续），而不是一个记账边界。
- 纯单段指数无法同时满足两个要求：要 7 天见底就得 τ 很小，那前 24h 掉得太快；要前 24h 平缓就得 τ 大，那 7 天时还剩太多。
- τ₁ = 72h **刻意与 `SPEC §4.1 F4 freshness` 的 τ 对齐**（同一个 72h），让两处的"新鲜"是同一个概念。⚠️ 但两者会**相乘**（`F4` 在 `score` 里，本模型的 `T` 在分发权重里），新内容的实际衰减比任一单独曲线更陡。建议上线后只调其中一处，不要两边同时动。

---

### 8.2 被接住之后，权重往哪走

🔴 **结论：往下。但「往下」的含义是<u>撤除扶持</u>，不是<u>施加惩罚</u>。不设任何"被接住惩罚系数"。**

#### 8.2.1 推导

产品给的方向是对的，本产品与主流推荐产品在这一点上确实是反的：北极星是「被接住的发布率」，一条**已经被接住**的内容对北极星的贡献已经计入分子，再给它更多曝光**不会让北极星前进一步**。所以「点赞越多权重越高」那套在本产品里没有依据。

但"降权"有两种截然不同的实现，必须分清：

| 实现 | 做法 | 判决 |
|---|---|---|
| **A. 撤除扶持** | 被接住 → 退出扶持期，不再占保底位，不再有扶持系数（`poolBoost` 1.35 → 1.00），此后靠相关性存活 | 🟢 **采纳** |
| **B. 施加惩罚** | 在 A 之上，再把 `W` 乘一个 `λ_accept < 1`，让它排到未被接住的内容**之后** | 🔴 **不采纳** |

**为什么不采纳 B —— 它会绕一圈回来打自己**：

> 北极星是**发布侧**的目标（保护发布者），但信息流同时还有一个**消费侧**的前提——得有人愿意留在这里看。而被接住过的内容恰恰是"被验证过有人愿意回应"的那部分。把它们系统性地压到常规内容之后，信息流里剩下的就是**未经验证的内容占主导**：浏览者体验下降 → 活跃浏览者减少 → **能去接住新内容的人变少** → 新内容更难被接住 → **北极星下降**。
>
> 撤除扶持不会有这个问题：它只是不再额外推，没有把它按下去。

**「会不会让优质内容过早消失」**：不会，因为撤除的是**扶持**，不是**相关性**。降到基准后它在相关性主导区里继续按关系链、题材匹配、向量相似出现，而相关性是 **viewer 相关**的——一条真正好的内容会在对的人那里持续出现。它失去的是"平台主动推它"，保留的是"匹配的人能遇到它"。

这两件事在本设计里本来就是分开的（§8.1 的 `W` 是**内容侧、viewer 无关**的分发权重；`SPEC §4` 的 `score` 是 **viewer 相关**的相关性），所以可以只撤一个而不动另一个。

#### 8.2.2 「我们究竟在优先谁」——自洽性交代

这个问题必须回答，因为几轮裁定合起来同时否掉了两个方向的扶持：被接住的不再扶持、没被接住的也不再复活。

> **我们只优先一类内容：还没有被判定过的新内容。**
>
> 「判定」= 在扶持期内，这张卡究竟有没有人接住。判定完成后，**无论结果是哪一种**，扶持一律撤除：
>
> | 判定结果 | 归宿 |
> |---|---|
> | 被接住了 | 目的达成 → 撤除扶持 |
> | 投够了仍零回应 | 默认吸引力不足（裁定）→ 撤除扶持 |
>
> **两者的归宿是同一个**：退出扶持期，进入由相关性主导的常规池，随时间自然衰减、自然流掉。区别仅在于到达那里的原因，不在于待遇。
>
> 🔴 **我们不优先任何"老"内容，无论它成功还是失败。** 这就是「旧不如新」在权重机制上的完整表达，也是本模型唯一的价值取向。

这个交代同时解释了为什么不需要 `λ_accept`：既然两类内容的归宿本来就相同，那么给其中一类再加一层惩罚，就是在两个**都已经不被扶持**的东西之间再分高下——而我们没有任何依据说"没被接住的"应该排在"被接住的"前面（裁定恰恰说了前者吸引力不足）。

---

### 8.3 旧内容完整生命周期与各阶段阈值

```
S1 扶持期        W = W0·γⁿ·T_eff        在 FRESH 池，可占冷启动保底位
  │
  ├─ 被接住（≥1 条合规回声 R1–R5）─────┐
  └─ n ≥ D_min（投够了）──────────────┤
                                      ↓
S2 常规期        撤除扶持，靠相关性竞争，W 继续衰减
  │
  └─ W < W_MIN ────────────────────────┐
                                      ↓
S3 退出首页主动分发   不再进首页召回；仍可被分类/相似度在**其各自时间窗内**选中
  │
  └─ 龄 > 14 天 且 双低 ────────────────┐
                                      ↓
S4 自然流掉      🔴 退出全部召回池，但**不退出索引**：搜得到，推不到
  │
  └─ 热度突增（§8.6 SURGE 判定）────────┐
                                      ↓
S5 热点召回（24 h）  独立通道，不占保底位，权重不回升
  │
  ├─ 期内获 ≥1 条合规回声 → 回 S2
  └─ 24 h 期满且零回应 → 回 S4（计入终身触发次数）
```

| 阈值 | 取值 | 理由 |
|---|---|---|
| `γ` 单次投放衰减 | **0.97** | 半衰期 ≈ **23 次投放**（`0.97²³ = 0.50`）；100 次后剩 **0.048**、300 次后剩 **1.1×10⁻⁴**。与 `SPEC` 旧口径量级自洽（旧口径 300 次到顶，新口径 300 次时已彻底沉底），但是**软的、无硬上限** |
| `D_min` 公平曝光下限 | **`clamp(同期队列 P25 曝光数, 20, 100)`** | §8.4.3 |
| `W_MIN` 退出首页阈值 | **0.05 × W0** | 与 `T(144h) = 0.050` 配合：零投放的卡靠时间衰减在**第 6 天**触及该阈值，有投放的更早。取 5% 而非 1%，是为了不让一堆权重极低的卡长期挂在候选集里增加排序成本 |
| 自然流掉 · 龄 | **> 14 天** | 裁定「两周以上」 |
| 自然流掉 · 访问量低 | 近 7 天去重曝光 **< 10** | ⚠️ 见下方说明 |
| 自然流掉 · 关注度低 | 近 14 天独立互动者数 **= 0** | 取最严口径——**零**独立互动者。有 1 个人回应过就不算双低 |

⚠️ **一条如实的口径澄清**（不是待办）：已进入 S3 的卡按定义已退出首页主动分发，它的"访问量"几乎必然低于 10——**「访问量低」这个条件在实践中几乎恒为真**。因此双低判定的**实际有效条件是「关注度低」那一条**。这与裁定意图一致（两周还没人理就自然流掉），此处写明是为了避免后人误以为访问量这一条在做实际把关。

---

### 8.4 记账：只记一个数

权重制下需要持久化的只有 **`n`（累计投放次数）** 一个计数。其余全是纯函数——给定 `W0`、`n`、`a` 即可算出 `W`，**不需要存 `W`**。

#### 8.4.1 `n` 的口径

| 项 | 规则 |
|---|---|
| 定义 | 累计**主动分发**的去重曝光数 |
| 去重 | `(cardId, viewerId, 自然日)`，Asia/Shanghai（`SPEC E-1`，不变） |
| 计入 | 首页信息流曝光（含保底位与相关性位）· 分类/题材召回曝光 · 相似度召回曝光 · `SURGE` 通道曝光 |
| 🔴 不计入 | **被动入口**访问：搜索结果、作者主页、题材页直达、站外分享落地。理由：`n` 度量的是"**我们主动推了多少次**"，被动入口是用户自己找上来的，不该消耗内容的分发权重 |
| 数据来源 | §3.10 的 `window_impression` 上报（契约不变），落 `t_card_exposure`（表不变） |

> 与 v0.3 的一处**实质差异**：v0.3 规定"相关性位曝光不扣预算"（因为预算是一份保底承诺）。权重制下**相关性位曝光要计入 `n`**——因为 `n` 不是"额度消耗"而是"已获得的分发机会"，一次曝光就是一次机会，不管它来自哪个位置。这让 `n` 的语义变干净了：**它就是这张卡被主动推过多少次。**

#### 8.4.2 `W` 不落库

`W` 是派生量，**不设列、不落库**。在保底池快照作业（`GuaranteePoolRefreshJob`，TTL 60 s，§2.2.4）里内存计算并排序即可。

理由：① 它每秒都在变（`a` 在走），落库必然是陈旧值；② 🔴 落库会诱导后人写 `UPDATE ... SET weight = ?`，而那是「只减不增」被破坏的第一个入口。**没有这一列，就没有这个入口。**

#### 8.4.3 唯一保留的窄口子：欠投补发（一个 clamp，不是一套机制）

裁定：**实际曝光数远低于应得量的，把欠的投放补上；判定只看曝光数，🔴 不看互动量。**

权重制下这件事不需要任何补偿机制，只需要在时间衰减上加一个**条件地板**：

```
T_eff(a, n) = max( T(a),  n < D_min ? T_FLOOR : 0 )

T_FLOOR = 0.15
D_min   = clamp(同期队列 P25 曝光数, 20, 100)
```

**它做了什么**：一张投放次数还没达到 `D_min` 的卡，其时间衰减因子**不会低于 0.15**。于是 `W ≥ W0 × γⁿ × 0.15`；而 `n` 小的时候 `γⁿ ≈ 1`，所以 `W ≈ 0.15 W0 > W_MIN = 0.05 W0` —— **它留在候选集里，直到真的被投够 `D_min` 次**。一旦 `n ≥ D_min`，地板撤除，`T_eff` 回到真实的 `T(a)`，正常衰减、正常流掉。

| 裁定要求 | 本 clamp 如何满足 |
|---|---|
| 「投了 X 次零回应 → 吸引力不足，不补」 | `n ≥ D_min` 时地板撤除，按 `T(a)` 正常沉底。**不看互动量，只看 `n`** |
| 「7 天到期实际只投了远少于应得的量 → 欠账结清」 | `n < D_min` 时地板生效，卡继续留在候选集直到投够 |
| 🔴 「判定不得看互动量」 | 公式里只有 `n` 和 `a`，**没有任何互动项**。断言 `TC-WEIGHT-06` |
| 「不是二次机会」 | 它不给任何**额外**的量，只是**不让时间把还没投出去的机会抹掉** |

🔴 **概念上的关键区分（这一条要写清，否则会被误认为配额制复辟）**：

> v0.3 被否掉的是**上限**——预算总额 300/700、剩余额度、结转（产品原话「哪有这么直接的」）。
> `D_min` 是一个**下限**——公平曝光下限。
>
> 两者方向相反：上限规定"最多给多少"，下限规定"至少得真的投出去多少，才算这张卡被判定过"。
> **保留一个下限不等于把配额制搬回来**：整个方案里只剩这一个数，而且它不做记账、不做扣减、不做结转，它只是一个 `max()`。

**`D_min` 为什么用同期队列分位数而不是绝对数**：绝对数在种子期（100–300 人）与成熟期（30k DAU）会差两个数量级，写死任何一个数都会在另一个阶段错得离谱。P25 是自校准的——**按定义只有约 1/4 的卡会触发这个地板**，成本自动有界。上下 clamp 到 [20, 100] 兜住两个极端：种子期队列太小、分位数噪声大（下限 20）；成熟期避免地板过高变成事实上的配额（上限 100）。

> 分位数在这里是**布尔准入判定**（`n < D_min`），产物是一个布尔，不进 `score`、不做 `ORDER BY`。与 `SPEC §3.7` 兜底热门层的分位准入**同构**，套用 `SPEC:288` 已承认的 `X6`/`X7` 例外，**不新开例外**。且它算的是**曝光数**（§3.7.3 白名单：曝光是刹车不是燃料），不是互动数。

---

### 8.5 负反馈只做刹车（红线延续）

#### 8.5.1 🔴 零回应不是制动信号

沿用已定口径，未变：

| 信号形态 | 含义 | 是否制动 |
|---|---|---|
| 0 正反馈 **且** 0 负反馈 | 没人回应，也没人拒绝。冷门真诚内容就是这个形态 | 🔴 **不制动**，按 `γ` 与 `T` 正常衰减 |
| 有明确负反馈 | 人们看到了并**主动推开** | ✅ 制动 |

两类内容在信号空间里**可分**，分界是"有没有明确的拒绝"，不是"互动多少"。

#### 8.5.2 制动信号与效果（全部只减不增）

| # | 信号 | 口径 | 效果 |
|---|---|---|---|
| **B1** | 明确负反馈率 | （「不看」+ 拉黑 + 举报）÷ `n`，🔴 仅在 `n ≥ 50` 后评估 | 一档（≥8%）：`γ` 由 0.97 **加重**为 0.90（掉得更快）<br>二档（≥20%）：**直接终止**，退出全部主动分发（跳 S4） |
| **B2** | 作者关闭全部回应通道 | `SPEC §8.3` 三项全关 | `brakeFactor` 乘 0.30（沿用 `SPEC G7` 既有系数，不新造数字） |
| **B3** | 违规 / 收回 / 审核改判 | 转 `RESTRICTED`（`SPEC §6.2`） | 立即终止 |
| **B4** | 受众耗尽 | 连续 2 日实投远低于应投 | **不做任何事** —— 🔴 权重制下不需要处理：投不出去 → `n` 不增长 → `γⁿ` 不衰减 → §8.4.3 的地板还在。**自愈** |

> B4 从 v0.3 的一条机制变成了"什么都不用做"，这是换成权重制之后最直接的一处简化收益。

#### 8.5.3 🔴 「权重不得回升到高于初始值」的结构性保证

不靠纪律，靠三条结构：

| # | 保证 | 机制 |
|---|---|---|
| **1** | `W ≤ W0` 恒成立 | `W = W0 × γⁿ × T_eff × brakeFactor`，除 `W0` 外全部因子值域为 (0,1]（§8.1.3 理由 1）。这是**代数上的**保证 |
| **2** | 制动只能让因子变小 | 全部制动效果都是"乘一个 <1 的数"或"加重 `γ`"，**没有任何一条制动是乘 >1 的数**。可用单测枚举全部制动分支断言 |
| **3** | 没有任何写入路径能改 `W` | `W` **不落库**（§8.4.2）——没有 `weight` 列，就没有 `UPDATE ... SET weight`。而 `n` 只增不减、`a` 只增不减，两个输入都是单调的 |

断言 `TC-WEIGHT-03`；运行时探针见 §8.9.4 的「权重单调性巡检」。

---

### 8.6 热点召回通道 `SURGE`（产品新增）

产品原话：

> 你可以把一些热度忽然高起来的作品，重新拉回到推荐视野。但是有效期仅在 1 天以内。有可能是有些东西忽然火了。这些是热点类内容的一个召回。

#### 8.6.1 🔴 它与已取消的 `REVIVE` 的本质区别（必须留着）

| | 已取消的 `REVIVE` | `SURGE` 热点召回 |
|---|---|---|
| 谁发起 | **平台**按"这条没人看它"发配额 | **内容自己挣回来的**——外面真有人在找它 |
| 依据 | 缺少互动（一个**负**信号、一个匮乏状态） | 出现真实的独立账号互动增长（一个**正**信号、一个可验证的事实） |
| 正当性 | 平台的怜悯 | 需求的证据 |
| 判决 | 🔴 **已取消** | 🟢 采纳 |

🔴 **给后人的警告**：`SURGE` **不是 `REVIVE` 的替身**。任何"把 `SURGE` 的触发条件放宽一点，让那些没人理的内容也能进来"的改动，都是在恢复已被取消的复活池语义。`SURGE` 的门槛之所以是"相对自身基线的增速 + 绝对地板"，就是为了让**没有真实需求的内容永远触发不了它**。

#### 8.6.2 信号来源与可得性核实

`SURGE` 的信号只能来自被动入口（这类内容已不在任何主动分发通道里），这正是它的正当性所在。核实结果：

| 信号 | 现状 | 结论 |
|---|---|---|
| **互动**（记得 / 心意 / 关注） | 🟢 **可得**。互动是**服务端写操作**——无论用户从搜索、作者主页、题材页还是站外链接进来，写入都会落库，与页面来源无关 | ✅ **足以支撑本通道** |
| 搜索命中 | ⚠️ 搜索功能本身尚未实现（`EchoApi.java` 无 search 路由；`echo-h5-proto/src/api/track.ts:39-46` 只有前端事件桩） | 搜索上线时一并接入 |
| 被动入口**曝光** | ⚠️ 结构上收不到：§3.10 的端点绑定 `GET /plaza` 下发的 `reqId`（防刷校验 1、3），非 feed 页面没有 `reqId`，上报会被判 `unknown_req` | 见下 |
| 站外分享回流 | ⚠️ 无 referrer 落地追踪 | 同上 |

🟢 **结论：不构成落地阻塞。** `SURGE` 的判定口径（§8.6.3）**完全建立在互动信号上**，而互动信号今天就可得。后三项是**增强项**——它们能让判定更灵敏，但缺了它们通道照样能触发、能工作。

> 一处如实说明：把"被动入口曝光"纳入判定，需要给搜索/主页/题材页单独下发 `reqId`；否则就得放开防刷校验 3，而那是 §3.10.4 整个防刷设计的支点，不能动。本模型**刻意不依赖它**，正是为了不去动那道校验。

#### 8.6.3 触发判定

```
基线  base  = 该卡近 14 天的「日均独立互动者数」
当期  surge = 该卡近 24 h 的「独立互动者数」（去重、合规，§8.6.4）

触发 ⟺ surge ≥ 5           ① 绝对地板
   AND surge ≥ 3 × base    ② 相对增速
```

| 数 | 取值 | 理由 |
|---|---|---|
| 绝对地板 | **5 个独立账号** | 直接复用 `SPEC §5.2` 热词晋升的门槛（「≥5 位**不同作者**」）——同一个平台里"这不只是巧合、确实有人在关注"的最小可信人数**已经标定过一次，不新造数字**。且 5 个独立绑定账号是组织成本的实际拐点：2–3 个人太容易凑，10 个在种子期不现实 |
| 相对倍数 | **3 ×** | 2 倍在小基线上过于容易（基线 0.2/日 → 0.6，一个人就够）；4 倍以上在种子期几乎不可能达到。3 倍与地板 5 的**联合效果**才是关键 ↓ |

🔴 **两个条件联合起来的效果正好是反马太的**：

| 该卡的基线 | 触发所需的 24h 独立互动者数 |
|---|---|
| 0 /日（完全无人问津） | **5**（地板生效） |
| 1 /日 | 5（地板仍生效） |
| 2 /日 | **6** |
| 5 /日 | **15** |
| 10 /日 | **30** |

> **基线越高，门槛越高。** 本来就有人在看的内容需要**更多**绝对增量才能触发，而完全无人问津的内容只需要 5 个人真的找上来。这与"用绝对量做门槛会退回马太效应"的担心正好相反——**地板保护小内容，倍数约束大内容，两个数各管一头。** 断言 `TC-WEIGHT-11`。

#### 8.6.4 防刷

一旦"突然变热"成为旧内容重回分发的唯一入口，它就是被针对的入口。五道约束：

| # | 约束 | 规则 |
|---|---|---|
| **1** | 独立账号去重 | 按 `accountId` 去重，且要求 `bound=true`（`S1′`：写操作需可验证绑定，办号需真实手机号） |
| **2** | 排除作者自身 | 作者本人及其关联账号的互动不计入 `surge` |
| **3** | 🔴 **排除小圈子集中互动** | 触发窗口内的互动账号中，**与作者存在关注关系（双向任一方向）的占比 > 50%** → 本次触发**作废**。这一条直接打击"作者叫几个熟人来点一下" |
| **4** | 互刷环检测 | 复用 `SPEC §6.5` 已有的互刷环检测，命中即作废 |
| **5** | 🔴 **单作者触发频次** | 同一作者名下内容，**每 7 天最多 1 次** `SURGE` 触发。防止一个作者把全部旧作轮流刷回 |

#### 8.6.5 🔴 终身上限与冷却期

| 项 | 取值 | 理由 |
|---|---|---|
| **有效期** | **24 h** | 裁定 |
| **终身触发上限** | **2 次** | 1 次过于绝对——一条内容确实可能在不同时间被两波不相干的人发现（例如某题材因外部事件两次被提起）。3 次以上开始接近"常驻"；而且如果一条内容第 3 次还能真的热起来，说明它已被实质接住，那时它该走 S2 常规期，不该靠这条通道 |
| **冷却期** | **30 天** | 与 24 h 有效期的比例是 **1 : 30**。即一条内容通过这条通道能获得的主动分发时间上限是「**每 30 天 1 天，终身 2 天**」——这从算术上让"1 天有效期变成常驻"**不可能发生**（产品的担心）。同时 30 天 > 14 天的自然流掉窗口，保证它必须在 S4 稳定待过一整个周期才可能再次触发 |

> **合并起来的硬上限**：一条已自然流掉的内容，**终身最多再获得 2 天主动分发窗口，且两次之间至少隔 30 天**。这个数字直接写进断言 `TC-WEIGHT-09`。

#### 8.6.6 被拉回的 24 h 里用什么权重

🔴 **走独立召回通道，不做权重回升。** 产品的倾向是对的，理由：

| # | 理由 |
|---|---|
| **1** | 权重回升会直接破坏 §8.5.3 的结构性保证。那条保证之所以成立，是因为除 `W0` 外所有因子都是 (0,1] 单调不增——**让 `W` 回升就必须打破这个代数结构**，红线会从"代数上不可能"退化成"我们记得不要这么写" |
| **2** | 通道配额的量**可控且可观测**（固定 ≤1 条/20 条、可单独熔断、可单独埋点）；权重回升的实际曝光量**不可预测**（取决于大盘竞争强度），既无法承诺也无法验收 |
| **3** | 语义更准：它不是"这张卡又变重要了"（那是内容属性的改变），而是"外面有人在找它，顺手在信息流里也放一下"（那是一个临时的、有配额的窗口） |

| 项 | 规则 |
|---|---|
| 排序用的权重 | **就用它自然衰减后的真实 `W`，不做任何提升**。它靠**通道配额**进入候选集，不靠权重赢过别人。所以 `W ≤ W0` 完全不受影响 |
| 通道配额 | **≤1 条 / 20 条**（5%），从**兜底组**的份额里出 |
| 🔴 不占保底位 | **确认不占**。15% 的位置是给**新内容首次曝光**的，`SURGE` 是旧内容，两者存在理由完全不同。占用会直接侵蚀 §2.2.8 的保底位来源合法性校验 |
| 通道内排序 | 按 `surge / base` 降序（挣得越猛的越靠前）；通道间按 `SPEC §7` 既有编排 |
| 曝光计入 `n` | ✅ 计入（§8.4.1）。所以被拉回来的这一天里，它的 `W` 会**继续下降** |

#### 8.6.7 24 h 期满后的归属

| 期内情况 | 期满归属 | 理由 |
|---|---|---|
| 获得 **≥1 条合规回声**（R1–R5） | → **S2 常规期** | 它现在是"被接住过"的内容，与 S2 里其它内容同质。🔴 这**不违反只减不增**：`W` 一个字没改，变的只是**池归属** |
| 零回应 | → **回 S4**，计入终身触发次数 | 有人找到它但没人回应，判定不变 |
| 期内命中 B1 二档 / B3 | → 立即回 S4（或 `RESTRICTED`），并**计入**终身次数 | — |

---

### 8.7 与四套既有机制的关系（前提已换成权重制，重新给结论）

#### 8.7.1 「有限的第二次机会 ≠ 无限强推」的等价表述（保留，改写）

v0.3 那段用"终身上界 700 次"表述，配额概念已废，改为权重制下的等价说法。**这段的作用是防止后人拿"没人喜欢就不该强推"当依据把 15% 冷启动保底位砍掉，所以必须留着。**

> 🔴 **本文档对「不强推」的定义（权重制版）**：
>
> 不强推 = **权重只减不增、没有任何回升路径、没有任何形式的配额倾斜**。
>
> 它**不等于**取消 15% 冷启动保底位。
>
> **依据（三条，都可核对）**：
> 1. **权重只减不增是代数保证**（§8.5.3）：`W = W0 × γⁿ × T_eff × brakeFactor`，除 `W0` 外所有因子恒 ≤1。一张卡被推得越多，权重越低——**"越推越推"这个正反馈回路在数学上不存在。**
> 2. **保底位是零和且有界的**：每 20 条固定 3 个位置。一张卡多占一次就有另一张少占一次，**不存在"某张卡吃掉大盘"的路径**。而「强推」这个词描述的正是无上界的重复投放。
> 3. **保底位解决的不是权重问题，是候选集问题**（§8.7.2）。砍掉它并不能减少任何"强推"，只会让一类内容**连被看见一次的机会都没有**。
>
> 换句话说：**"强推"在本模型里不存在，所以削减保底位不能解决它，只会削减北极星。**

#### 8.7.2 15% 冷启动保底位 —— 🟢 核实产品判断：**仍然需要，判断成立**

产品的判断是「保底位解决的是候选集圈定问题，不是权重不够高的问题」。**核实结论：完全成立**，而且这一点在权重制下比在配额制下更清楚。

依据在 `SPEC §3.8.2`（`SPEC:320-328`）与本文档 §2.2.1：

> 相关性组（`REL`/`FOL`/`VEC`/`TAG`）的候选集**按热点在线人群圈定**。一个新注册、没有亲友关系、没有粉丝、自己也不在热点在线人群里的用户，发布的第一张卡——**它的作者不在那个集合里，所以这张卡进不了相关性组的候选集**。
>
> 🔴 **这与它的权重是多少完全无关。** 就算给它 `W = 1.0`（最高初始权重），它也**根本没有进入排序竞争的机会**——权重是在候选集内部比较的，**进不了候选集的东西，权重再高也是 0 次曝光。**

| | 保底位解决的 | 权重解决的 |
|---|---|---|
| 问题 | **进不进得了候选集**（准入） | **进了候选集之后排多前**（排序） |
| 机制 | 全库直查 + 硬预留位置 | `W0 × γⁿ × T_eff` |
| 能否互相替代 | 🔴 **不能**。权重再高，也不能把自己塞进一个按别的条件圈定的集合 |

**结论：保留，本模型对它不做任何改动。** 唯一的衔接点是保底位的**取卡排序键**：v0.3 用 `paceDeficit`（配额概念，已废），现改为**按 `W` 降序**。这更简单，且 `W` 已经天然包含了"投得少的权重高"（`γⁿ` 项）与"新的权重高"（`T` 项）两层含义，不需要额外的赤字概念。仍在快照作业里内存计算排序，**不需要新索引**。断言 `TC-WEIGHT-13`。

#### 8.7.3 `REVIVE` 零回应复活池 —— 🟢 **v0.5：已裁定整个删除，本节转为留档**

> 🟢 **v0.5 状态更新（B 类台账 B1）**：本节 v0.4 写的是"建议"。**该建议已被采纳并执行** —— 用户裁定「零回应复活作为普惠机制取消，投过了没人接即视为吸引力不足」，上游 `SPEC` v0.3 已把 `REVIVE` 整条删除（`§3.8.1` / `§6.2` / `§7.1 C3` / `RK18`），下方三处连带影响也**已全部被 `SPEC` 吸收完毕**（逐条核对见 §7.0a `Q18`）。本节保留原推导，作为"为什么删"的依据留档。

产品问：整个删掉、还是收窄成"欠投补发"并改名。

**建议：整个删除。连"欠投补发"也不需要它。**

理由：§8.4.3 已经把"欠投补发"实现成了**时间衰减上的一个条件地板**。那张欠投的卡**根本不需要离开扶持期**——它的权重被地板托住，本来就还在保底位的候选集里，会被继续投，直到投够 `D_min`。

| 方案 | 评价 |
|---|---|
| **整个删除**（建议） | 🟢 "欠投补发"由一个 `max()` 完成。**少一个池、少一条状态迁移、少一套额度、少一个迁移作业** |
| 收窄 + 改名（如 `UNDERSERVED`） | ⚠️ 会引入一个**只有一个成员条件、且与扶持期高度重叠**的池。一张欠投的卡本来就该在扶持期里（它还没被判定过），把它挪到另一个池再挪回来，是纯粹的状态机开销 |
| 保留原名 | 🔴 **明确反对**。名字带"复活"会诱导后人恢复原语义，这正是产品担心的 |

**连带影响（v0.4 时需上报排序侧，共 3 处 —— 🟢 v0.5 核对：三处已全部落地）**：

| # | 影响 | 说明 | 🟢 上游落地状态 |
|---|---|---|---|
| 1 | `SPEC §6.2` 的池划分少一个池 | 四池（新 / 复活 / 稳态 / 软退出）→ 三池（新 / 常规 / 流掉） | ✅ 已改。`SPEC §6.2` 现枚举 `FRESH` / `STEADY` / `DRAINED` / `RESTRICTED`（`REVIVE` 删、`ARCHIVED_FROM_FEED` 改名 `DRAINED`） |
| 2 | 15% 的构成要重新定 | 现为「2 新 + 1 复活」。`REVIVE` 删除后建议 **3 个位置全给 `FRESH`**——保底位的语义仍然完整（给新内容首次曝光）。🔴 **比例仍是 15%，不缩水** | ✅ 已改。`SPEC §7.1 C3`：「v0.3：3 位全部由 P-新（`FRESH`）提供」 |
| 3 | 🔴 `SPEC` 的 `TC-RANK-49` 必须重写 | 那条用例的过标准是「它仍然能拿到**复活**保底位」（`SPEC:1648`）。`REVIVE` 删除后这条**必然失败**。按裁定，正确的过标准应改为：「这张卡自然流掉后**仍可被搜索与作者主页访问到**，且若出现真实热度增长可经 `SURGE` 回到分发」——即从"平台会救它"改为"**它还在，且够格时能回来**" | ✅ 已按建议原文改写。`SPEC §3.8.5`：「🔄 **TC-RANK-49**（v0.3 改判据）：自然流掉的卡**仍可被搜索与作者主页访问到，且够格时可经 `SURGE` 回到分发**」 |

#### 8.7.4 软退出 —— **改为阈值判定，不另设状态位**

产品问：权重低到什么程度算软退出，是阈值还是另设状态位。

**结论：用阈值。** 但本模型里"软退出"这个概念被拆成了**两个不同的阈值**，它们不是一回事：

| 阶段 | 判定 | 含义 | 是否落状态位 |
|---|---|---|---|
| **S3 退出首页主动分发** | `W < W_MIN`（0.05 × W0） | 首页不再召回；分类/相似度在各自时间窗内仍可能选中 | ❌ **不落** |
| **S4 自然流掉** | 龄 > 14 天 **且** 双低（§8.3） | 退出**全部**召回池 | ✅ 落 `drainedAt` |

**为什么 S3 不落状态位**：`W` 是派生量（§8.4.2），`W < W_MIN` 是纯函数判定，每次快照刷新算一遍即可。而 `W` 会因 `a` 增长而单向下降——状态位只会从"未退出"翻到"已退出"，**信息量为零**，维护它纯属负担。

**为什么 S4 要落一个标记**：它的判定依赖 14 天窗口的聚合（近 7 天曝光、近 14 天独立互动者），不能在请求路径上算。所以落一个 `drainedAt` 时间戳，由日级作业写。🔴 **但它不是"归档"或"下架"**，见 §8.7.6。

🔴 **v0.5 回改（B 类台账 B5）· S4 的过滤条件统一为 `poolTag`，`drainedAt` 不作谓词**

v0.4 在 §3.8 的 DDL 注释里写过「枚举收敛为 `FRESH|STEADY|RESTRICTED`，自然流掉由 `drainedAt` 表达、**不是一个池**」。**这一句与上游不一致，已撤回。** `SPEC` v0.3 里两个东西是**并存且分工明确**的，不是两套竞争表达：

| | `poolTag = 'DRAINED'` | `drainedAt` |
|---|---|---|
| 定位 | 🔴 **硬过滤谓词**。`SPEC §8.1 H11` 原文即「`poolTag = DRAINED`（原 `ARCHIVED_FROM_FEED`）」；`SPEC §6.2` 池枚举含 `P-流掉 DRAINED` | **时刻记录**。`SPEC §17.6` 新增 `t_memory_card.drainedAt` |
| 谁读 | 召回层的硬过滤链（H11）。🔴 **唯一例外：有效期内的 `SURGE` 卡不被此条过滤**，否则 §8.6 整条通道无法工作 | `CardDrainJob` 写入；`SurgeDetectJob` 判基线用；审计与回溯用 |
| 读取限制 | 仅召回层（`SPEC §6.4.2`：搜索 / 作者主页 / 题材页 / 直链**一律不过滤**） | 同样只允许召回层读取（`SPEC` `P0-21` / `TC-RANK-49`；本文档 §8.7.6 的 ArchUnit 白名单） |

**为什么按 `SPEC` 对齐而不是反过来**：池位枚举属 `SPEC §6.2` 的口径，本文档文首已把「不重定义 `SPEC` 已定的排序逻辑/特征/池位」列为不做的事。而且**过滤条件必须只有一处**——一边过滤 `pool='DRAINED'`、另一边过滤 `drainedAt > 0`，只要 `CardDrainJob` 写这两处之间出任何偏差（如只更新了一列就崩了），就会出现"搜不到也推不到"或"推得到但已判流掉"的不一致，而这类不一致在报表上是看不见的。

→ **实现约束**：`CardDrainJob` 判定成立时**在同一事务内**写 `pool='DRAINED'` 与 `drainedAt=now`；召回层过滤**只读 `pool`**；`drainedAt` 只用于作业与审计。§8.7.6 的读取点白名单对两列同时生效。

`SPEC §6.4` 既有的「2 轮复活后软退出」整条作废（`REVIVE` 已删）。`SPEC §6.4` 的**三条重新激活出口**：编辑后重新过审 → 仍有效（授予新 `W0`，受累计 ≤2 次限制）；热词晋升 → 仍有效；站外被接住 → 由 `SURGE` 与 §8.6.7 承接。

#### 8.7.5 `LONGTAIL` 长尾轮播 —— 🟢 **确认删除，且残留缺口已被裁定关闭**

已确认 `SPEC` v0.2 移除该通道（`SPEC:219` / `SPEC:1703 RK18` / `SPEC:776`），产品采纳我的意见（支持移除）。

v0.3 我报的那条残留缺口（「三条出口全部依赖事件触发，一条无人问津的内容将永不回来」）——**产品已用后续裁定正面回答，缺口关闭**：

| 缺口的那一半 | 裁定的回答 |
|---|---|
| "一条无人问津的内容将永不回到主动分发" | 🟢 **这是有意为之**：两周以上双低即自然流掉，默认吸引力不足，**不做挽救** |
| "除非有事件触发" | 🟢 现在**多了一条非编辑类的事件出口**：`SURGE` 热点召回（§8.6）。而且它的触发依据是**真实需求**，比长尾轮播的"轮到它了"正当得多 |

所以**不需要任何补偿机制**，此项关闭。

#### 8.7.6 🔴 「自然流掉」的确切含义（写死，防止被理解成下架）

> **自然流掉 = 退出召回池，不退出索引。搜得到，推不到。**

| 自然流掉后**仍然**成立 | 自然流掉后**不再**成立 |
|---|---|
| ✅ 内容**永久保留**：不删除、不归档、不隐藏 | ❌ 不进首页信息流召回 |
| ✅ **搜索**可检索到（搜索索引不剔除） | ❌ 不进分类 / 题材召回 |
| ✅ **作者主页**正常展示 | ❌ 不进相似度召回 |
| ✅ **题材页 / 话题页**主动浏览可达 | ❌ 不占任何保底位或配额 |
| ✅ **直链 / 站外分享链接**正常打开 | ❌ 不获得任何形式的权重回升 |
| ✅ 作者可编辑（编辑后重过审 → 回 S1） | |
| ✅ 可经 `SURGE` 回到分发（§8.6） | |

🔴 **实现约束**：`drainedAt` 标记**只允许被召回层读取**。搜索索引、作者主页查询、题材页查询**一律不得引用这个字段**。ArchUnit 可钉死这一条（`drainedAt` 读取点白名单 = 召回模块）。这是把"搜得到推不到"从一句话变成一条可验证约束的方式。断言 `TC-WEIGHT-08`。

#### 8.7.7 一个已知张力的如实记录（已另立话题，本文档不处理）

本产品是**怀旧主题**，而本模型的分发规则是**旧不如新**——时间衰减、两周自然流掉、分类与相似度召回同样偏向新内容。这两者之间存在张力。

产品负责人已明确知晓，裁定为：**靠其他页签或主题页面找补，另开话题讨论。**

> 此处记录的唯一目的：让后来者看到「旧不如新」时知道**这是有意为之、且已被讨论过**，不要自作主张把长尾兜底或复活配额加回来。

---

### 8.8 曝光分布预期与降级

#### 8.8.1 分布预期

权重制下不再有"配额需求 vs 容量"的算术（配额概念已废），分布由**位置比例**决定：

| 部分 | 占全站曝光 | 归属 |
|---|---|---|
| **冷启动保底位** | **15%**（🔄 v0.5：`REVIVE` 已删，3 位全给 `FRESH`，`SPEC §7.1 C3` 已定） | 新内容首次曝光 + 欠投补发（§8.4.3） |
| **热点召回 `SURGE`** | **≤5%**（≤1 位 / 20 条，从兜底组份额出） | 已流掉但挣回热度的旧内容 |
| **相关性 + 兜底 + 精选** | **≈80%** | S1 / S2 内容按 `W × score` 竞争 |

#### 8.8.2 降级

| 级 | 触发 | 处置 | 误差方向 |
|---|---|---|---|
| **L1** | `SurgeDetectJob` 不可用 | 通道返回空，那 1 个位置由兜底组补。**其余一切不受影响** | 旧内容少一条出路，可接受 |
| **L2** | `n` 的计数不可用（曝光上报管道故障） | 🔴 **冻结 `n` 的增长**（宁可让权重多留一会儿），告警。🔴 **不得用请求数近似 `n`**（`SPEC:876` 已删这条退路） | 偏"多给"，安全 |
| **L3** | 快照作业不可用（`W` 算不出来） | 退回 `SPEC §3.5` 原口径（曝光加权随机），**保底位照填** | 保底位不空缺，只丢失权重排序 |

🔴 **统一原则不变：降级一律朝"多给保底"偏，不朝"少给"偏。** 少给的误差会系统性推高「零回应窗口占比」（`SPEC §10.2` 第一指标），制造一个纯技术原因造成的假信号。

#### 8.8.3 🔴 北极星会如实下降，这是预期内且正确的

裁定要求写明这一条：

> 取消零回应复活后，「被接住的发布率」**会如实下降**。
>
> 这是**正确的**：此前靠反复推同一批零回应内容把分子硬撑上去，是在**给自己刷指标**——那些额外曝光换来的回声是"推了十次终于有人回一次"，而不是"内容真的被需要"。
>
> 🔴 **给后人的话**：看到北极星走低时，**不要把复活池加回来**。北极星的正确提升方式是让**新内容的首次曝光更准**（这是 15% 保底位与 §8.4.3 欠投补发在做的事），而不是让旧内容被反复推。**如果一个指标可以靠重复投放同一批内容来提升，那它在那个维度上已经不是一个可信的指标了。**

---

### 8.9 存储、调度与配置

#### 8.9.1 表结构增量（相比 v0.3 大幅缩减）

`t_card_pool_state`（§3.8）新增 **4 列**（v0.3 是 11 列，配额相关的 7 列全部删除）：

```sql
ALTER TABLE "t_card_pool_state"
  ADD COLUMN "deliveredCount" integer NOT NULL DEFAULT 0,   -- n：累计主动分发去重曝光数
  ADD COLUMN "initialWeight"  real    NOT NULL DEFAULT 1.0, -- W0：🔴 只在 INSERT 时写，永不 UPDATE
  ADD COLUMN "brakeFactor"    real    NOT NULL DEFAULT 1.0, -- 制动累积系数：🔴 只减不增
  ADD COLUMN "drainedAt"      bigint  NOT NULL DEFAULT 0;   -- S4 自然流掉时刻：🔴 只允许召回层读
-- 🔴 v0.5（B5）：drainedAt 只是时刻记录，不是过滤谓词。召回层的 H11 硬过滤读 pool='DRAINED'，
--    两者由 CardDrainJob 在同一事务内写入。口径见 §8.7.4。
```

🔴 **`weight` 不设列**（§8.4.2）：没有这一列，就没有 `UPDATE ... SET weight`，就没有权重被写高的入口。

`SURGE` 状态（§8.6）：

```sql
ALTER TABLE "t_card_pool_state"
  ADD COLUMN "surgeCount"     smallint NOT NULL DEFAULT 0,  -- 终身触发次数，上限 2
  ADD COLUMN "surgeLastAt"    bigint   NOT NULL DEFAULT 0,  -- 上次触发时刻（冷却期判定）
  ADD COLUMN "surgeExpiresAt" bigint   NOT NULL DEFAULT 0;  -- 当前 24h 窗口到期时刻
```

活跃度日聚合表 `t_card_activity_daily` **保留**，用途改为 `SURGE` 基线计算与 S4 双低判定：

| 列 | 用途 |
|---|---|
| `cardId` · `statDay` | 唯一键 |
| `distinctInteractors` | 独立互动者数（去重、合规）→ `SURGE` 基线 + S4「关注度低」判定 |
| `dedupExposure` | 当日去重曝光数 → S4「访问量低」判定 |
| 保留期 | **30 天**（需支撑 14 天基线窗口 + 冗余） |
| 🔴 访问约束 | 只允许 `SurgeDetectJob` / `CardDrainJob` 读取；召回与排序模块一律不读计数（`X6`，沿用 §3.7.3 白名单口径） |

#### 8.9.2 任务调度

| 作业 | 频率 | 职责 | 失败后果 |
|---|---|---|---|
| `GuaranteePoolRefreshJob`（**已有**） | 60 s | 刷新保底池快照，**新增**：内存计算 `W` 并降序排序 | 降级 L3 |
| `CardPoolTransitionJob`（**已有**） | 60 s | S1 → S2 迁移（被接住 或 `n ≥ D_min`） | 卡滞留 S1；**方向安全** |
| `CardActivityRollupJob` | 每日 00:20 | 聚合 `t_card_activity_daily`（独立互动者 + 去重曝光） | `SURGE` 基线陈旧、S4 判定延迟；**方向安全**（少流掉） |
| `CardDrainJob` | 每日 01:00 | S4 双低判定，写 `drainedAt` | 内容多留在召回池；**方向安全** |
| `SurgeDetectJob` | **1 h** | `SURGE` 触发判定（§8.6.3）+ 五道防刷（§8.6.4）+ 上限冷却校验（§8.6.5） | 降级 L1 |
| `SurgeExpireJob` | 10 min | 24 h 到期处理 + §8.6.7 归属判定 | 🔴 **窗口不过期 =「1 天有效期」失效**。必须有心跳看门狗 + `surge_window_overdue` 指标 |

> `SurgeDetectJob` 用 1 h 而非分钟级：判定窗口是 24 h，1 小时的检测延迟相对 24 h 是 4%，可忽略；而 1 h 一次让"独立互动者去重 + 关注关系占比"这类聚合查询的成本可以忽略不计。

所有作业沿用 §3.4 已定的可靠性约定：心跳表 + 看门狗告警 + `ShutdownHook` 同步 flush。

#### 8.9.3 配置项

| 配置键 | 默认值 | 说明 |
|---|---|---|
| `ECHO_WEIGHT_ENABLED` | `false` | 总开关。关闭 = 退回 `SPEC §3.5` 原口径 |
| `ECHO_WEIGHT_GAMMA` | `0.97` | 单次投放衰减因子，🔴 必须 ∈ (0, 1) |
| `ECHO_WEIGHT_TAU1_HOURS` | `72` | 慢衰段时间常数 |
| `ECHO_WEIGHT_TAU2_HOURS` | `36` | 快衰段时间常数 |
| `ECHO_WEIGHT_SEGMENT_HOURS` | `72` | 换档时刻（3 天） |
| `ECHO_WEIGHT_MIN_RATIO` | `0.05` | `W_MIN / W0`，S3 退出首页阈值 |
| `ECHO_WEIGHT_FAIR_FLOOR` | `0.15` | `T_FLOOR`，欠投补发地板 |
| `ECHO_WEIGHT_DMIN_PCTL` | `25` | `D_min` 的队列分位 |
| `ECHO_WEIGHT_DMIN_CLAMP` | `20,100` | `D_min` 的上下 clamp |
| `ECHO_DRAIN_AGE_DAYS` | `14` | 自然流掉龄阈值 |
| `ECHO_DRAIN_EXPOSURE_MAX` | `10` | 「访问量低」阈值（近 7 天） |
| `ECHO_SURGE_ENABLED` | `false` | 热点召回开关 |
| `ECHO_SURGE_ABS_FLOOR` | `5` | 绝对地板（独立账号数） |
| `ECHO_SURGE_RATIO` | `3.0` | 相对增速倍数 |
| `ECHO_SURGE_TTL_HOURS` | `24` | 有效期 |
| `ECHO_SURGE_LIFETIME_MAX` | `2` | 终身触发上限 |
| `ECHO_SURGE_COOLDOWN_DAYS` | `30` | 冷却期 |
| `ECHO_SURGE_FOLLOW_RATIO_MAX` | `0.5` | 小圈子判定：互动账号中与作者有关注关系的占比上限 |
| `ECHO_SURGE_AUTHOR_INTERVAL_DAYS` | `7` | 单作者触发间隔 |
| `ECHO_SURGE_SLOT_PER_20` | `1` | 通道配额 |

**启动期校验**（不合法则拒绝启动，不静默纠正）：

`GAMMA ∈ (0,1)` · `TAU2 < TAU1`（快衰段必须更快）· 🔴 **`MIN_RATIO < FAIR_FLOOR`** · `SURGE_LIFETIME_MAX ≥ 1` · 🔴 **`SURGE_COOLDOWN_DAYS > DRAIN_AGE_DAYS`**。

> 第三条值得单独说：如果 `W_MIN > T_FLOOR`，欠投补发的地板就低于退出阈值，那个 clamp 会**完全失效且不报错**——这是一个静默失效点，所以用启动期校验钉死。
> 第五条同理：冷却期若短于自然流掉窗口，卡会在还没稳定流掉时就再次触发 `SURGE`，"1 天有效期"会被变相延长。

#### 8.9.4 埋点与指标（§3.7 增量）

| 事件 / 指标 | 口径 | 阈值 |
|---|---|---|
| `rank_weight_snapshot` | 快照刷新时的 `W` 分布（P10/P50/P90） | — |
| `rank_card_stage_change` | 生命周期迁移（`from` `to` ∈ S1–S5） | — |
| `rank_fair_floor_active` | 处于欠投补发地板保护中的卡数占比 | 🔴 **持续 >40% 告警**——说明供给严重不足（`D_min` 按 P25 定义，正常应 ≈25%） |
| `rank_card_drained` | S4 自然流掉（`cardId` `age` `exposure7d` `interactors14d`） | — |
| `rank_surge_trigger` | `SURGE` 触发（`cardId` `surge` `base` `ratio`） | — |
| `rank_surge_reject` | 触发被防刷拒绝（`reason` ∈ 五道约束） | `reason=follow_ratio` 占比升高 → 有人在试这条通道 |
| 📊 `surge_window_overdue` | 已过期但未被处理的 `SURGE` 窗口数 | 🔴 **>0 即告警**（`SurgeExpireJob` 静默失败的唯一探针） |
| 📊 **权重单调性巡检** | 抽样卡的 `W` 时序，检测是否出现上升 | 🔴 **出现即告警**。这是 §8.5.3 红线的运行时探针 |

---

### 8.10 可验收断言（`TC-WEIGHT-*`，取代已废的 `TC-BUDGET-*`）

| # | 断言 |
|---|---|
| **TC-WEIGHT-01** 🔴 | **高互动内容不会因互动而多拿曝光**。造一张卡：1000 次记得、500 次关注，持续 7 天。**过的标准**：其累计曝光数与另一张**互动全为 0、其余条件相同**的卡的曝光数之差 **≤5%**（残差只能来自相关性排序，不能来自权重）；且全程 `W ≤ W0` |
| **TC-WEIGHT-02** 🔴 | **零互动内容不被提前掐死**。造一张零互动、零负反馈的冷门卡。**过的标准**：`brakeFactor` 全程 = 1.0，`W` 严格按 `W0·γⁿ·T_eff` 下降，且在 `n < D_min` 期间**始终留在保底位候选集**（地板生效） |
| **TC-WEIGHT-03** 🔴 | **权重只减不增**。对一张卡回放任意事件序列（高互动、负反馈、关闭通道后重开、`SURGE` 触发与期满）。**过的标准**：`W` 的时序**单调不增**，且任一时刻 `W ≤ W0` |
| **TC-WEIGHT-04** 🔴 | **被接住后是"撤除扶持"而非"施加惩罚"**。造两张卡 A（被接住）与 B（投够 `D_min` 仍零回应），其余条件相同。**过的标准**：两者退出扶持期后的 `W` **相等**（都只由 `γⁿ·T` 决定，不存在 `λ_accept`），且 A 未被排到 B 之后 |
| **TC-WEIGHT-05** | **`W0` 无差别**。同一时刻过审的两张用户卡，一张作者有 10 万粉丝且历史毕业率 100%，一张是全新账号首发。**过的标准**：`W0` 完全相等 |
| **TC-WEIGHT-06** 🔴 | **欠投补发只看曝光不看互动**。造两张卡，均 `n = 5`（远低于 `D_min`），一张零互动、一张已有 20 次互动。**过的标准**：两者的 `T_eff` **相等**（地板都生效），证明判定未读互动 |
| **TC-WEIGHT-07** 🔴 | **投够了就不再托底**。一张卡的 `n` 达到 `D_min` 之后。**过的标准**：`T_eff` 立即回到真实 `T(a)`；且龄 >7 天时 `W < W_MIN`，退出首页主动分发 |
| **TC-WEIGHT-08** 🔴 | **自然流掉 = 搜得到推不到**。一张 S4 卡。**过的标准**：① 不出现在首页 / 分类 / 相似度**任何**召回结果中；② **搜索、作者主页、题材页、直链全部正常返回它**；③ 数据未删除、未归档、未隐藏 |
| **TC-WEIGHT-09** 🔴 | **`SURGE` 终身上限与冷却期**。对一张 S4 卡持续制造热度增长。**过的标准**：① 终身最多触发 **2 次**；② 两次间隔 **≥30 天**；③ 累计获得的主动分发窗口 **≤2 天** |
| **TC-WEIGHT-10** 🔴 | **`SURGE` 防刷**。作者组织 5 个与其**互相关注**的账号在 24 h 内集中互动。**过的标准**：触发**被拒绝**，`rank_surge_reject{reason=follow_ratio}` 上报 |
| **TC-WEIGHT-11** | **`SURGE` 的反马太性**。基线 10/日的卡与基线 0/日的卡。**过的标准**：前者需 **≥30** 个独立账号才触发，后者 **5** 个即可 |
| **TC-WEIGHT-12** 🔴 | **`SURGE` 不占保底位、不回升权重**。`SURGE` 期内。**过的标准**：① 它占的是兜底组配额，冷启动保底位仍全部由新内容填充；② 其 `W` 在这 24 h 内**继续下降**（曝光计入 `n`） |
| **TC-WEIGHT-13** 🔴 | **新人第一张卡能被看见**（`SPEC TC-RANK-50` 的权重制版）。新注册账号，无亲友、无粉丝、不在热点在线人群内，发布首卡。**过的标准**：它拿到冷启动保底位并出现在别人首屏。（这条测的是 §8.7.2：**保底位解决候选集准入，权重解决不了它**） |
| **TC-WEIGHT-14** | **配置静默失效防护**。把 `ECHO_WEIGHT_FAIR_FLOOR` 设为 `0.01`（低于 `MIN_RATIO` 0.05）。**过的标准**：服务**拒绝启动**并报错，不静默运行 |
| **TC-WEIGHT-15** | **`SurgeExpireJob` 失效可被发现**。停掉该作业 2 天。**过的标准**：`surge_window_overdue > 0` 告警触发，不依赖人工发现 |

---

### 8.11 这套模型解决了什么、以及它与既有机制的重叠

| 分类 | 内容 |
|---|---|
| 🟢 **真正新增** | **① 一条连续、无硬上限的分发衰减机制。** 此前 `SPEC` 只有"总额 300 / 单日 100"两个硬计数，中间是空的，且两个上限在供给不足时互相踩踏（`SPEC:815` vs `SPEC:817`）。权重制用一条曲线取代了两个上限，那个矛盾从"要修"变成"不存在" |
| | **② 公平曝光下限与"没人接住"的区分**（§8.4.3）。一个 clamp，把"我们没投出去"和"投了没人要"分开——这是唯一保留的窄口子，也是原矛盾指向的实质问题 |
| | **③ `SURGE` 热点召回。** 一条**由需求驱动、而非由怜悯驱动**的旧内容回归路径，并把 `LONGTAIL` 移除后的残留缺口正面关闭了（§8.7.5） |
| | **④ 「搜得到推不到」成为可验证约束**（§8.7.6 的 `drainedAt` 读取点白名单 + `TC-WEIGHT-08`），而不只是一句口头承诺 |
| 🟡 **与既有机制重叠** | **⑤ 时间衰减**与 `SPEC §4.1 F4 freshness`（τ=72h，权重 0.15）重叠。两者会**相乘**，实际衰减比任一单独曲线更陡。建议上线后只调一处 |
| | **⑥ 「被接住后撤除扶持」** 就是 `SPEC` 既有的 `poolBoost` 1.35 → 1.00。本模型**不新增机制，只是给出了它的理由**（§8.2），并挡掉了"再往下压一档"这个看起来符合北极星、实际会反噬北极星的做法 |
| 🔴 **明确不做** | **⑦ 任何形式的权重回升 / 配额倾斜 / 复活扶持**（`REVIVE` 已删，§8.7.3） |
| | **⑧ 为"旧内容被埋"设计的任何补偿机制。** 裁定明确：两周双低即自然流掉，分类与相似度召回同样旧不如新，此项**不是缺口**（§8.7.5、§8.7.7） |

**总判断**：相比 v0.3 的配额方案，权重制**删掉的比新增的多**——去掉了额度表、扣减、结转、超发算术、日配额、`REVIVE` 池、`B4` 受众耗尽处理，换来一个三参数公式（`γ`、`τ₁/τ₂`、一个 clamp）。这是一次**净简化**，不是等价替换。唯一新增的复杂度是 `SURGE` 通道，而它换来的是旧内容有一条**正当**的回归路径。

## 9. 完整度清单

| 交付要求 | 状态 |
|---|---|
| 现状勘察结论（附代码位置与行号） | ✅ §1（12 小节，含与 `SPEC §12.1` 的差异修订 §1.12） |
| 问题一：候选集怎么圈定 | ✅ §2.2（v0.2.1：相关性组热点圈定 + 保底组全库直查；含「在线」信号不存在的前置工程量） |
| v0.2.1：通道分组修正落地 | ✅ §2.2.1（三组）· §2.2.4（保底组）· §2.2.5（可行性论据逐条核实 + 数字）· §2.2.6（预算隔离）· §2.2.7（降级阶梯 D0–D4，禁止相关性组补位）· §2.2.9（副作用表更新） |
| v0.2.1：修正的可验证性 | ✅ §2.2.8（`slotProvenance` + 履约率口径改为按来源 + 重叠率指标）——**规格未要求，本方案主动补强** |
| v0.2.1：论述自相矛盾清理 | ✅ §2.2.1 末（限定"按内容侧圈定被否"的范围：被否的是"全部通道都改"，保底组本身仍按内容侧条件直查） |
| 问题一：5000 量级是否合理（维度/QPS/耗时/内存估算） | ✅ §2.3（含三条结论；⚠️ 数字未实测，处置见 R1） |
| 问题一：向量放哪、怎么扫（三条路取舍 + 推荐） | ✅ §2.4（A/B/C 逐项对比，决定性理由是合规不是性能） |
| 问题一：写副作用是什么、有无依赖、拆分方案 | ✅ §1.1（零消费者的逐条反查）+ §2.5（拆分 + 两条补充） |
| 问题一：时延预算与降级 | ✅ §2.6（单路 78 ms 分解 + 四条写死的规则） |
| 问题一：授权门控卡在哪层、缓存向量如何失效 | ✅ §2.7（三层门控 + 三层失效机制 + 三条硬前置） |
| 问题二：实时层数据结构（HLL/Bloom/精确集合取舍） | ✅ §3.2（含"HLL 是被误用的工具"的论证） |
| 问题二：异步落库（批次/频率/重试/幂等） | ✅ §3.4（幂等由唯一键保证，不需要 batchId 表） |
| 问题二：一致性边界（明确数字） | ✅ §3.5（8 项数字 + 单卡额度 ≤1% 的推导 + 保底位履约不受影响的论证） |
| 问题二：与事件数仓的关系与迁移路径 | ✅ §3.6（定权 + 三阶段收敛 + 对账阈值 2%） |
| 问题二：`rank` 前缀埋点事件与字段 | ✅ §3.7（v0.2.1 扩至 16 个事件 + 12 个指标 + 一条红线冲突的处置） |
| v0.2 裁定：曝光上报端点前后端契约 | ✅ §3.10（曝光定义 50%/1s · 批量 10 条/5 s · 字段 · **五道防刷校验** · 去重责任划分 · 重试与丢弃） |
| v0.2 裁定：AI 种子内容与 AI 标识 | ✅ §3.11（确认召回/曝光不需特殊排除 · 发现北极星口径污染点 · 分享物料三形态，其中 `og:image` 需裁定 §7 Q15） |
| v0.2：Redis 存向量重新论证 | ✅ §2.10（三形态辨析 · 五失败模式逐条解法 · 总账数字 · 升级阶梯 · 完整加固设计） |
| v0.2：缓存容量逐 repository 盘点 | ✅ §1.13（9 个 repository 核算 · 两个量级校核 · 建议容量与内存 · **推翻 v0.1 泄漏归因** · 引擎缺陷排期结论） |
| 接口 / 表结构 / 配置项定义 | ✅ §2.8 §2.9 §3.8 §3.9 §8.9 |
| 与上游规格的对齐 | ✅ §5 |
| 本轮不改业务代码 | ✅ 只改本文件 |
| **v0.3 裁定一**：向量走 pgvector HNSW | ✅ §0.3 · §2.4 · §2.10.6（Redis 加固设计保留为预案） |
| **v0.3 裁定二**：引擎缓存缺陷不修的正式理由入档 | ✅ §1.14（含"两条必须一起做"的约定与 P0 三项 size 观测指标） |
| **v0.3 裁定三**：`LONGTAIL` 归保底组 | ⚠️ §8.7.5（按裁定写入，🔴 **但发现上游已移除该通道，裁定为空操作** → §7 Q17） |
| **v0.3 裁定四**：`og:image` 叠 AI 标识 + 物料边界 | ✅ §3.12（C1–C3 可判定条件 · 7 项物料逐项判定 · 三条防扩大解释红线 · 第三方缓存残留风险） |
| **v0.3 术语同步**：`SUB` → `FOL`，「订阅」不指代关注 | ✅ 全文 4 处 |
| 🔴 **v0.4 换机制**：配额记账整套作废 | ✅ §8.0（7 项作废清单，逐项标注 v0.3 原位置，防止残留引用） |
| 🆕 **权重函数**：形式与推导 | ✅ §8.1（`W = W0·γⁿ·T_eff·brakeFactor` · `γ=0.97` 半衰期 23 次 · **相乘而非相加的三条理由**，其中第一条是"只减不增成为代数保证"） |
| 🆕 **权重函数**：时间衰减曲线 | ✅ §8.1.4（分段指数 τ₁=72h / τ₂=36h，**3 天是曲率转折点** · 数值表核到 `T(144h)=0.050` 与 `T(168h)=0.026` · 否决单段指数的理由） |
| 🔴 **被接住后权重往哪走** | ✅ §8.2（结论：**撤除扶持，不施加惩罚** · "施加惩罚会通过消费侧反噬北极星"的闭环论证 · §8.2.2 回答"我们究竟在优先谁"） |
| 🆕 **旧内容完整生命周期** | ✅ §8.3（S1–S5 状态图 + 六项阈值取值与理由 + 一条如实的口径澄清："访问量低"实践中几乎恒为真） |
| 🆕 **记账**：只记一个数 | ✅ §8.4（只持久化 `n`；🔴 `W` **不落库**——没有列就没有写高的入口） |
| 🔴 **欠投补发**（唯一保留的窄口子） | ✅ §8.4.3（**一个 `max()`，不是一套机制** · 公式里只有 `n` 和 `a`，无互动项 · 🔴 **「下限 ≠ 上限」的概念区分**，防止被误认为配额制复辟） |
| 🆕 **负反馈只做刹车** | ✅ §8.5（零回应不是制动信号 · B1–B3 · **B4 变成"什么都不用做"（自愈）** · §8.5.3 三条结构性保证） |
| 🆕 **`SURGE` 热点召回** | ✅ §8.6（🔴 与 `REVIVE` 的本质区别 + 给后人的警告 · **信号可得性核实：不是阻塞** · 双条件门槛 + **反马太性数值表** · 五道防刷 · 终身 2 次 / 冷却 30 天的比例推导 · 走独立通道而非权重回升的三条理由） |
| 🔴 **与四套既有机制的关系（重判）** | ✅ §8.7（15% 保底位**核实产品判断成立**：它解决候选集准入，权重解决不了 · `REVIVE` **建议整个删除** + 三处连带影响 · 软退出改阈值、S3 不落状态位的理由 · `LONGTAIL` 缺口关闭） |
| 「有限的第二次机会 ≠ 无限强推」 | ✅ §8.7.1（保留并改写为权重制版：**三条可核对依据**，核心是"正反馈回路在数学上不存在，所以削减保底位不能解决一个不存在的问题"） |
| 🔴 「自然流掉」的确切含义 | ✅ §8.7.6（**搜得到推不到** · 7 项仍成立 / 5 项不再成立 · `drainedAt` 读取点白名单 = 可验证约束 · `TC-WEIGHT-08`） |
| 怀旧主题与「旧不如新」的张力 | ✅ §8.7.7（如实记录 + 处置去向；**不写成待办、不写成风险、不提解决方案**，仅防后人自作主张加回长尾兜底） |
| 🆕 **分布预期与降级** | ✅ §8.8（15% / ≤5% / ≈80% · L1–L3 降级方向统一朝"多给" · 🔴 §8.8.3 **北极星会如实下降且这是正确的**，含"不要把复活池加回来"的明文警告） |
| 🆕 **存储 / 调度 / 配置 / 埋点** | ✅ §8.9（**4 + 3 列**（v0.3 是 11 列）· 6 作业 · 20 配置项 · 🔴 **五条启动期校验**，其中两条专挡静默失效） |
| 🆕 **可验收断言** | ✅ §8.10（`TC-WEIGHT-01…15`，含产品点名要求的三条：高互动不多拿、零互动不掐死、被接住方向正确） |
| 🆕 **净变化判断** | ✅ §8.11（四项真正新增 / 两项重叠 / 两项明确不做；**删掉的比新增的多**） |
| 🔴 **需转达排序侧的接口变更** | 🟢 **v0.5 已闭环**：`Q18` 的三处连带（池枚举 / 15% 构成 / `TC-RANK-49` 判据）经核对**已全部被 `SPEC` v0.3 吸收**，`Q18` 结案（§7.0a · §8.7.3 落地状态列） |
| 🆕 **v0.5 上游口径回改**（B 类台账 `B1`–`B5`） | ✅ `B2` `seed_ai=0.30` 删除并核实无依据（§8.1.2）· `B1` `REVIVE` 整条删除 + **15% 论证由"缩水成 5%"升级为"归零"**（§2.2.1）· `B3`/`B4` 五项未决项按 `SPEC` 结论销账（§7.0a）· `B5` S4 过滤条件统一为 `poolTag='DRAINED'`（§8.7.4） |
| 分期落地建议 | ✅ §4（P0 5 项 / P1 3 项 / P2 1 项，含硬前置标注） |
| 风险与未决项 | ✅ §6（**11 项风险**）+ §7.0（v0.3 · 6 项已结案）+ 🆕 **§7.0a（v0.5 · 5 项已结案：`Q1`/`Q2`/`Q3`/`Q11`/`Q18`，全部为上游已给结论的回改）** + §7.1（其余未决项；已结案的行保留原文并标结案指针，不删除）|
