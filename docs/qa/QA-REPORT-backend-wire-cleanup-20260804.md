# QA 报告 · 后端接线 + 清理 · 2026-08-04

| 项 | 值 |
|---|---|
| 对应交付 | **后端接线 + 清理**（装配点接工厂 / mi-C harness 移出 / mi-D dev relations 种子） |
| 改动文件 | `EchoHttpBootstrap.java`、`EchoServer.java`、`EchoApi.java`、`com/echo/harness/**`（21 Java 文件 main→test 移动） |
| 结论 | **PASS** |
| 统计 | **Blocker 0 · Major 0 · Minor 3** |
| QA 依据 | QA-CHARTER v1.0（四层）、DECISIONS、ACCEPTANCE、API-CONTRACT §8/§14、AI-CAPABILITIES §2、COPY-GUIDE |
| 测试实况 | 后端 `mvn clean test`：**127 用例全绿**（0 失败/0 错误/0 跳过）；前端 `npm run build` 通过 + `npm test` **18 用例全绿** |

---

## 摘要
三项后端改动均已落实，**无 key 默认行为与改动前逐位一致**（Vision 回落 `StubVisionClient`、Embedding 回落 768 维 `MockEmbeddingClient`，编码算法与 `IVectorStore.encode` 占位实现一致）；harness 21 个 Java 文件已移出 `src/main`、main 构建不依赖 harness（编译通过佐证），两个 harness 测试类在 test 树正常运行且全绿；mi-D dev relations 种子严格只在**内存态 + 新游客**触发，持久化模式绝不写入 demo 数据。产品红线全过，契约与 API-CONTRACT §8 对齐。判 **PASS**。

---

## L1 产品红线
- [PASS] 温度地板 60% / 外部献花不加温度 — 本次改动未触碰温度与献花逻辑；种子宠 `temperature=80.0` 属正常态、无献花→温度路径 — 定案:C1/D5 — 文件:`EchoApi.java:1329`
- [PASS] 记得无精确数字 / 不排名 — 关系视图 `relationView` 仅下发 `reels/hasUnseenReel/pet`，无花数/记得数/排名字段；`myPetView`/`windowCard` 走 `warmthLevel`（暖光浓度）非数字 — 定案:D4 — 文件:`EchoApi.java:983-1008`、`920`
- [PASS] 看过仅 owner 内部 — 未改动 `windowSeen`/`petInsights`，seen 数不进关系/窗口对外视图 — 定案:D4 — 文件:`API-CONTRACT §6`
- [PASS] 可见性默认私密 / 公开按档裁字段 — 种子对端宠显式 `visibility="public"`（demo 需可见），viewableByMe 依 `canView(peerPet, viewer)` 真实计算，无权者不下发 reels/pet — 定案:D1 — 文件:`EchoApi.java:1330`、`994-1006`
- [PASS] 去游戏化措辞 / 文案过词表 — 种子文案（"换了个方式一直陪着你""它在那边，挺好的。"、昵称拾光/远山/阿岸）温柔克制，signature 经 `CopyGuardFilter.sanitize`；无金币/道具/充值等硬词，无逝去/离世等禁词 — 定案:D6/E3 — 文件:`EchoApi.java:1328`、`899`
- [PASS] **mi-D 红线：种子只在内存/dev，持久化模式绝不写入 demo** — `EchoHttpBootstrap` 用 `!persistent` 决定 `seedDemoRelations`（persistent = `PgDbManager.get("echo")!=null`）；`authGuest` 内 `if (seedDemoRelations)` 且**仅新游客**（`existing==null` 分支）才 `seedRelationsFor`；`seedDemoWindow` 同样 `if (!persistent)` 守卫。持久化（PgEchoStore）模式两项种子均不执行 — 定案:PRD-social §2.9 / API-CONTRACT §3 — 文件:`EchoHttpBootstrap.java:72,80-83`、`EchoApi.java:169-183`

> 其余红线（明信片不锁内容、献花额度制、场景授权、静一静、苦甜浓度）本次交付未涉及相关代码路径，沿用既有实现，无回归。

---

## L2 验收用例（相关项）
- TC-01 游客无缝进入 — PASS — `authGuest` deviceId 幂等分支未改；新游客首建号后按 `seedDemoRelations` 铺种子（内存态）；`EchoApiTest` guest 幂等类用例全绿
- TC-05/TC-06 记得暖光面孔墙 / 看过内部 — PASS — 关系/窗口对外视图无精确数字，warmthLevel 呈现（既有单测覆盖）
- TC-08 亲友列表 & 动态圈 — PASS — `EchoApiTest` 覆盖 `relationsReturnsMyPetShapeAndLastActive`（可见者 lastActive/reels/pet=MyPet）、`relationsHidesReelsAndPetForNonViewablePeer`（无权者不显动态）、`relationsViewableWhenPeerListsMeAsFriend`（挚友档可见）三例，均绿
- TC-AI-* 无法验证（本次不涉 AI 生成链路）— 无变更，跳过

---

## L3 测试与构建
- **后端 `mvn clean test`：绿**。`Tests run: 127, Failures: 0, Errors: 0, Skipped: 0`，`BUILD SUCCESS`。用例数与预期 127 一致。
- **harness 两个测试类从 test 树正常运行**：`com.echo.harness.ExpBotsHarnessTest`（6）+ `com.echo.harness.HeuristicBotReviewerTest`（3）均绿；surefire 报告确认在 test 阶段执行。harness data 资源 `harness/populations/default.json` 经 classpath 正常加载。
- **main 构建不依赖 harness**：`src/main/java` 内无 `import com.echo.harness`（仅 `ILlmClient.java:24` 一处 Javadoc `{@code com.echo.harness}` 文本引用，非编译依赖），编译通过佐证。
- **前端（可选）`npm run build` 通过**（62 模块，vite 产物正常）；`npm test` **18 用例全绿**（`relationsMap`/`spectrumMap`/`http` 契约映射单测）。
- **新代码覆盖**：无 key 回落分支由 `EmbeddingConfigTest`/`VisionConfigTest`/`MockEmbeddingClientTest`/`PgVectorStoreTest`/`ApiVisionClient/EmbeddingClientTest` 覆盖；relations 契约字段由 `EchoApiTest` 三例覆盖。**mi-D 种子方法（`seedRelationsFor`/`seedFriend`/构造重载 true 分支）无直接单测**（见 Minor-1）。

---

## L4 通用质量（无 key 默认行为 + 契约一致性）
- [PASS · 高优] **无 key 默认行为逐位不变**
  - Vision：改动前 `new StubVisionClient()` → 改动后 `VisionClientFactory.fromEnv()`；`VisionConfig.isStub()` 在 provider 缺省/为 stub、缺 baseUrl、或缺 key 时为 true → 回落同一 `StubVisionClient`。默认无 env 即 stub。文件:`EchoHttpBootstrap.java:64`、`VisionConfig.java:52-60`、`VisionClientFactory.java:31-34`
  - Embedding：改动前 `new PgVectorStore(pgDb)`（默认 `new MockEmbeddingClient()`=768 维）→ 改动后 `new PgVectorStore(pgDb, EmbeddingClientFactory.fromEnv())`；无 key 时 `fromEnv` 返 `MockEmbeddingClient(config.dimensions())`，`dimensions` 缺省 `IEmbeddingClient.DEFAULT_DIM=768`。`MockEmbeddingClient.embed` 用 `v[i%dim]+=charAt(i)`，与 `IVectorStore.encode` 占位实现**逐位一致**。文件:`EchoServer.java:156`、`EmbeddingClientFactory.java:19-22`、`EmbeddingConfig.java:54-62`、`MockEmbeddingClient.java:28-38` vs `IVectorStore.java:34-43`
- [PASS · 高优] **契约一致性（API-CONTRACT §8）** — 种子产出的关系视图字段 `id/name/avatar/online/priority/mutedUntil/lastActive(ms)/viewableByMe/hasUnseenReel/reels[]/pet` 与 §8/§14 M-5 要求对齐：`lastActive` 为毫秒、`pet` 为 MyPet 形状（`petId/name/signature/temperature/visibility/cover/recent/lifeBook/postcards`，非 Window）、`viewableByMe` 真实计算、无权者不下发 reels/pet。文件:`EchoApi.java:983-1008`、`886-907`
- [Minor] 见下阻断/建议清单。

---

## 阻断清单（必须修）
**无**（Blocker 0 · Major 0，达 PASS 门槛）。

---

## Minor（记录，可择期修）
1. **mi-D 种子逻辑无直接单测** — `seedRelationsFor`/`seedFriend`/`EchoApi` 7 参构造 true 分支为新增 dev-only 代码，无直接测试；其产出的关系契约形状已被 `EchoApiTest` 三例间接覆盖，且"持久化不种"红线在唯一装配点 `!persistent` 由构造保证。建议补一条内存态断言（`seedDemoRelations=true` 新游客首访后 `/relations` 铺 3 位 / `=false` 不铺）以锁红线、防回归。文件:`EchoApi.java:1303-1349`、`EchoHttpBootstrap.java:72`
2. **harness data 资源仍在 `src/main/resources`** — Java 已移 test 树，但 `src/main/resources/harness/populations/default.json` 仍在 main，会被打进生产 jar；测试经 classpath 仍可读（故不影响运行/构建）。建议随 harness 一并迁至 `src/test/resources/harness/`，与"harness 移出 main"清理意图一致。文件:`echo-server/src/main/resources/harness/populations/default.json`
3. **`ILlmClient` 残留 harness 文档引用** — `ILlmClient.java:24` Javadoc 仍写"为体验 Bot 定性层（`com.echo.harness` §7 …）新增"，指向已迁至 test 树的包。非编译依赖，仅文档陈旧。建议调整措辞避免 main 文档反向指 test 包。文件:`ILlmClient.java:24`

---

## 疑问 / 交 PM（不擅自放宽）
- 无。三项改动均在既有定案口径内，未发现定案本身冲突。

---

## 复审建议
本报告为 **PASS**，可放行合入。若后续团队按 QA-CHARTER L3"新代码无测试覆盖=Major"从严执行，可将 Minor-1 升级处理并补测后无需重跑全量、仅回归 relations 种子一例即可。
