# 回声·往宠 — 前后端 API 契约（H5 完整落地版 · v1）

| 项 | 值 |
|---|---|
| 文档版本 | **v1.6 · 2026-08-27**（在 v1.5 基础上，🔴 **不改任何既有出入参**）<br>🆕 📋 **§6.0.4 给前端线的移交清单 —— 本节可整节转发、自带全部上下文**：三处独立改动（`petIdOfCard()` 的修法 · `http.ts` 两个写错的路径前缀 · 新增出参 `echoGenerated`），每处都带**怎么验**；🔴 并写明**一处不要动的**（`/messages/arrivals` 的 `cardId` 键今天装 petId，改法未定，⚠️ **「以后会自动变对」这个说法已被 `RK-H` 撤销**）。<br>🆕 **§3 `POST /pet/me/visit` 近况节流成一天一条**，同一天再回访返回**今天那一条**（不是空列表），新增出参 `echoGenerated`；🔴 不下发回访次数计数（`DP2`）。<br>v1.5 · 2026-08-27 🔴 **含一处破坏性变更**（后端线 `C-2` / `C-5` / 置顶）<br>① 🔴 **`GET /plaza` 改发回忆卡**（`OM1` 落地）：`item.id` 含义从 **petId** 变成 **cardId**，⚠️ **前端五个 `/windows/:id/*` 端点会静默 404，逐条清单见 §6.0.3**（修法只有一处：`lib/ids.ts` 的 `petIdOfCard()` 改成从卡自带的 `petId` 取值）。顺带报出**两处与本次无关的既有 404**：前端把留言端点写成 `/windows/:id/messages`，后端提供的是 `/cards/:cardId/messages`。<br>② 🆕 **§6.0 `cards[]` 契约**（此前整块不存在）：**只有一个 card 形状**，广场与作者主页共用；🔴 `title` 可空、`cover` 可缺（手写 record 与生命之书多半没标题、常常没图）；🔴 **正文首句由服务端切**，列表响应**不含 `body` 键**——前端切等于把全文下发给不该看全文的人，这是下发面问题不是渲染问题。<br>③ 🆕 **§6.0 三个新端点**：`GET /pet/me/cards`、`GET /users/:id/cards`、`PATCH /cards/:id/visibility`（卡级可见性三档；🔴 卡宽于窗时**报错而不静默收窄**）、`PUT`/`DELETE /cards/:id/pin`（上限 3 后台可配、仅 public 且已过审、🔴 自动解除不留悬空、`pinnedAt DESC NULLS LAST, publishedAt DESC`）。<br>④ ⚠️ **`GET /plaza` 的曝光登记为 `surface=grid`，网格层整批不记 `n`**（`SPEC-feed-surfaces` 概述第 1 条）。<br>📌 **`GET /windows/:id` 保留且语义不变**，它收的仍是 petId；变的只有「广场下发的 `id` 是什么」。<br>v1.4 · 2026-08-25（同步 `DECISIONS.md` v1.7 `§G⁗⁗⁗′` `MOD1 ③` / `MOD2`，**只补三处、不改任何既有端点与出入参**：① **§17.0 `M-C` 补「与状态变更同一事务」**，并写明「每一次」= 全部动作而非只 `approve`（`reject`/`takedown`/`restore`/`escalate`/`uphold`/`overturn` 同样适用）；② **§17.2 写死 `appealUsed` 的唯一判据 = `t_moderation.appealAt IS NOT NULL`**，🔴 不得由计数列推导、不得新增此类字段；③ **`POST /cards/:id/appeal` 补 `overturn` 不重置 `appealAt`**——撤销原处置不等于退还申诉机会。<br>📋 **核实结论**：`M-A`（`reviewedAt` 同事务只写一次）与 `M-B`（审核不得写改 `originType`、审核接口不暴露该字段可写入口）**v1.3 已在，本轮未改**）<br>v1.3 · 2026-08-25（🆕 新增 **§17 审核 / 申诉 / 举报契约**：补 `PRODUCT-MINDMAP §6.2a` 台账 **B12** 判定的规格缺口 —— 审核 REST 路径此前**任何规格都没有定义**。运营侧六条（队列 / 详情 / 处置 / 申诉处置 / 举报列表 / 先审后发开关）+ 🔴 作者侧两条（看驳回理由 / **一生一次**的申诉，`SPEC-admin-console §6.4` 的清单缺了这一半，缺则 `TC-MOD-03` 无法实现）；三条既有裁定约束写死：**`approve` 同事务写 `reviewedAt`（只写一次）** · **审核一律不得改 `originType`** · **状态变更必落 `t_card_visibility_log` + `t_audit_log` 双流水**。分工：端点契约在本文档，流程与状态机在 `SPEC-publish-and-ops §2`）<br>v1.2 · 2026-08-25（🆕 新增 **§16 分享物料契约**：分享落地页 `GET /w/:windowId` 直出按窗 meta + `GET /share/meta/:windowId` + `POST /share/og-image` 合成预览图并叠 AI 标识，**入参含 `cover.aiGenerated`、缺省按 `true`**；🔴 边界写死「只有分享预览图叠标识，站内原图与用户素材一律不动」。产品规格 `SPEC-trust-and-compliance §CM-G0S S-11`）<br>v1.1 · 2026-08-24（新增 §15 合规 P0 契约；§3 `DELETE /pet/me` 按 QA 复签 A-4 下线，正式删除端点定死 `DELETE /pet/:id`） |
| 归属 | 后端 + 前端 · 接口契约（前后端并行的唯一真源） |
| 传输 | **HTTP/JSON REST**（H5 核心闭环）；WebSocket 保留给心跳/实时（沿用现有 9001） |
| 后端 | 给 echo-server **新增轻量 HTTP/JSON 网关**；**目标架构：WS 与 HTTP 在服务端并存、共享同一套领域服务**（`AccountService`/`EchoService`/`MindSpaceService`/`MindProfileService`/`ResonanceService` 及各 Repository）。**现状**：HTTP 层暂为独立自建域（`EchoStore`），正按此目标重构为真复用，详见 §14（2026-07-28 定案）。 |
| 关联 | `PRD-echo-social.md` v0.9（§0.6/§0.7 六项定案）、`PRD-echo-pet.md`（温度）、`COPY-GUIDE.md`、`RELEASE.md`、**`SPEC-trust-and-compliance.md`（§15 的产品规格来源）**、**`SPEC-security.md §2.1`（游客权限 S1′：写操作需可验证绑定）** |
| 原则 | **六项定案在服务端强制**（不信任前端）；游客账号=一等公民；私密默认、可见性逐项显式 |

---

## 0. 通用约定

- **Base URL**：`/api/v1`
- **编码**：请求/响应均 `application/json; charset=utf-8`
- **鉴权**：首次访问 `POST /auth/guest` 拿 `token`（游客态，设备匿名）；后续请求头 `Authorization: Bearer <token>`。绑定手机/微信后 token 不变、账号升级（`isGuest=false`）。
- **时间**：统一毫秒时间戳（`number`）。
- **ID**：字符串（后端 `IDGenerator` 生成，前端只透传）。
- **成功响应**：`{ "code": 0, "data": {...} }`
- **错误响应**：`{ "code": <非0>, "msg": "<面向用户的温柔文案，须过 COPY-GUIDE 词表>", "detail": "<给开发的英文原因，可选>" }`
- **错误码段**：`1xxx` 鉴权 / `2xxx` 参数 / `3xxx` 业务规则（如献花额度用尽） / `5xxx` 服务端。
- 🔴 **`1002 BINDING_REQUIRED` / HTTP `403`**（2026-08-27 补登，**已在代码中运行**）：**未完成可验证身份绑定的账号请求受限写操作时返回**（`S1′`）。
  - 🔴🔴 **判据只看 `code === 1002`。** ⚠️ **不要匹配 `msg` 文案**（文案会随 COPY-GUIDE 改），⚠️ 🔴 **也不要只看 HTTP `403`** —— **`403` 还表示归属越权（改别人的东西），两者的前端处置完全不同**：`1002` 该引导去绑定，归属越权该提示无权限。
- **分页**：`?cursor=<id>&limit=<n>`，响应含 `{ items, nextCursor }`；`nextCursor=null` 表示到底。

---

## 1. 鉴权 / 账号（复用 AccountService，游客一等公民）

### POST /auth/guest — 领取游客身份（免登录体验入口）
- 入参：`{ "deviceId": "<前端生成的稳定设备指纹>" }`
- 出参：`{ "token": "...", "accountId": "...", "isGuest": true, "hasPet": false }`
- 说明：同 `deviceId` 幂等返回同账号（守"免登录=游客态、逻辑同正式用户"，见 PRD §2.7）。

### POST /auth/bind — 游客升级为正式账号
- 入参：`{ "type": "phone|wechat", "credential": "..." }`
- 出参：`{ "isGuest": false }`

### GET /me — 当前账号概要
- 出参：`{ "accountId", "isGuest", "nickname", "hasPet", "visibilityDefault": "private|friends|public" }`

---

## 2. 建档 Onboarding（先肖像识别 → 命名 → 补充 → 写/说 → 三选一两轮 → 场景二次确认，PRD §往宠建档）

### POST /pet/onboarding/detect — 肖像识别（第 1 步：上传一张 → 顺路认出种类，支持多主体）
- 入参：`{ "resourceId": "<已上传肖像的资源id>" }`
- 出参：`{ "source": "model|fallback", "subjects": [ { "subjectType": "animal|person|other", "species": "狗", "confidence": 0.0~1.0, "box": { "x":0~1, "y":0~1, "w":0~1, "h":0~1 } } ] }`
  - `subjects` 为识别到的主体**列表**（按 confidence 降序）；`box` 为归一化位置框（相对肖像宽高），用于多主体时前端在图上叠加可点选框；单主体可省略 `box`。
  - **`source`（AI 诚实标识，必读）**：`model` = 视觉模型真实识别所得；`fallback` = **兜底默认，不是识别结果**（未配 key / 素材解析失败 / 供应商异常 / 模型输出为空）。
    - `source === "fallback"` 时前端**不得**把 `species` 当作「AI 认出来的」展示（不淡入、不预选），直接请用户自己选——兜底值恒为 `animal/狗/0.5`，照常展示等于让用户以为「AI 认错了」，违反「AI 诚实标识、绝不乱认」红线。
    - 🔄 🔴 **措辞更正（2026-08-26，依据 `DECISIONS SR-D13`）**：本行原写「兜底值恒为**中性默认** `animal/狗/0.5`」，~~「中性默认」~~ **这个说法已被推翻**。🔴 **`animal` 不是中性值，它是<u>能力最宽</u>的那一档** ——「中性」听起来不偏不倚因而安全，⚠️ **而在这个字段上偏向 `animal` 就是偏向放开生成能力，认不出的时候放开能力方向正好是反的**。<br>🟢 **本行的<u>要求</u>不变、且仍然正确**（fallback 时不得当作识别结果展示）；**改的只是那个标签。** ⚠️ 🔴 **`/detect` 出参的 `subjectType` 与素材侧门控用的 `assetSubjectType` 是两个不同字段**（`MOD5` 三处同名不同义），🔴 **但踩的是同一个坑** —— 该值经 `/start` 往下传，**不要拿一个用户可随手纠正的预填值当门控判据**。
    - `source === "model"` 时才走原有的淡入 + 用户确认交互。
    - 旧客户端未读该字段时行为不变（字段为新增，向后兼容）。
- 说明：走后端**视觉模型**（`IVisionClient` 插件化抽象，与 `ILlmClient`/`IVectorStore` 同一风格；`ECHO_VISION_*` 环境变量选供应商，缺 key 自动回落桩实现）。
  - `species` 尽量对齐前端长列表词表（狗/猫/兔/仓鼠/龙猫/…/其他）；无法归类返回 `"其他"`。
  - `subjectType` 为将来扩展「人 / 其他」预留（当前建档主要面向动物，默认 `animal`）。⚠️ 🔴 **「当前建档主要面向动物」是<u>解释</u>，不是把默认值定成 `animal` 的<u>授权</u>**（`SR-D13`）—— 🔴 **素材侧门控字段 `assetSubjectType` 的兜底已定为 `other`，不要照这一行去填它。**
  - **资源解析**：`resourceId` 是我们自己的存储键，供应商既不认识也拉不到，故服务端在调用前经 `IImageRefResolver` 解析——存储能给出公网 URL（OSS/CDN）就直传 URL；本地存储则读字节内联为 `data:<mime>;base64,...`。
  - **发送前压缩**：内联前用 JDK `javax.imageio`（不引第三方依赖）缩到最长边 **768px**（`ECHO_VISION_MAX_EDGE` 可调）、重编码 JPEG（质量 0.85），目标 base64 后 < 500KB。原图直发会让单次调用耗时一分钟以上而必然超时；实测同一张 1.7MB 猫照片：1024px 约 10~13s、768px 约 5s、512px 约 3.5s，识别结果均为「猫 / 0.98」，故取 768。压缩失败安全回退（原图发送），解析不出可用引用则不发请求、直接 `fallback`。
  - 视觉调用超时 30s（余量，正常路径几秒返回）；降级 warn 日志带 `step=resolve|compress|network|http-status|extract-content|parse-json|parse-empty` 标明失败环节。
  - **多主体护栏**：`subjects.length > 1` 时，前端要求用户**点选单一主体**后才能点「就是 ta」确认；未选定不允许进入下一步。`length === 1` 直接作为识别结果（仍需用户确认）；`length === 0` 视为未认出，前端转手动选择。
  - 前端行为：识别结果**淡入**呈现让用户注意到已识别，但**必须用户确认**才进入下一步；可点「不是 ta？」用滚轮手动纠正（错误兜底，不阻断流程）。
  - 无后端/离线：前端 mock **永远返回单主体**兜底值（🔄 **原写「中性默认」，措辞已按 `SR-D13` 更正**；mock 看不到图，绝不假装多主体），并应带 `source: "fallback"`；仅当显式设 `VITE_MOCK_MULTI=1` 时才返回两主体带 box，用于本地演示多主体选择交互。

### POST /pet/onboarding/start — 开始建档，提交原始素材/描述
- 入参：`{ "petName", "species", "subjectType"?, "rawDesc", "traits": ["温柔","粘人"], "photoRefs": ["<上传后返回的资源id>"] }`
  - `photoRefs[0]` 约定为第 1 步的肖像主图，其余为第 3 步补充素材。`subjectType` 由 `/detect` 或用户纠正得到，默认 `animal`。⚠️ 🔴 **这个 `animal` 只覆盖建档识别出参这一路**（`SR-D13`）；🔴 **服务端不得把它当成「用户主动填过」** —— 判「用户有没有主动填」看 `subjectSource`，不看 `subjectType` 有没有值。
- 出参：`{ "onboardingId", "candidates": [ {"id","cover":{gradient,emoji},"signature"} x3 ] }`
- 说明：`candidates` = 第一轮 AI 生成的三张推荐定妆（走 `ILlmClient`+基调层）。

> 🆕 🔴 **`subjectType` 辨异（2026-08-25 新增 · 🔴 不改字段，只防误接）**
>
> 本文件的 `subjectType`（`/detect` 出参与 `/start` 入参，取值 `animal` / `person` / `other`）🔴 **与 `SPEC-subject-recognition-and-degradation.md` 的 `assetSubjectType` 不是同一个字段，严禁互相赋值、严禁合并成一个字段。**
>
> | | 本文件的 `subjectType` | 规格的 `assetSubjectType` |
> |---|---|---|
> | 产生时机 | **建档第一步**的肖像识别 | **素材入模前**的主体判定 |
> | 用途 | 替用户**预填种类**，用户可当场纠正 | 🔴 **生成能力门控**（四级收缩阶梯 `L0`–`L3`）|
> | 取值 | `animal` / `person` / `other` | `pet` / `person` / `object` / `unknown` |
> | 判错的后果 | 预填错一个种类，用户改一下即可 | 🔴 **可能让一个真人拟真产物被生成出来** |
>
> 🔴 **为什么要专门写这一段**：两者名字曾经完全相同（该规格原也叫 `subjectType`，已于同日改名）。🔴 **同名不同义时，最省事的实现就是把 `/detect` 的结果直接当作门控判据** —— 而它是**用户可以随手纠正**的预填值，拿它当门控等于让用户自助关掉门控。
>
> ⚠️ **另有第三处同名**：`PRD-echo-pet §3.3` 的 `subjectType`（指用户声明的对象类别）。🔴 **那一处的建议改法是改用项目通用的 `objectKind`**，已登记 `DECISIONS §G⁗⁗⁗⁗″ MOD5`，因该文件在禁改清单上，**本轮只登记未改**。
>
> 📋 **本文件的字段本身不改名** —— 改名要动 `echo-server` 与 `echo-h5-proto`，不在文档线权限内，且该接口已有实现。

### POST /pet/onboarding/refine — 第二轮：选定一张再细化三选一
- 入参：`{ "onboardingId", "chosenCandidateId", "adjust": "更活泼一点" }`
- 出参：`{ "candidates": [ ...x3 ] }`

### POST /pet/onboarding/confirm — 定稿 + 纪念场景二次确认
- 入参：`{ "onboardingId", "finalCandidateId", "memoryScene": {"caption","allowUse": true} }`
- 出参：`{ "petId" }`（此后 `hasPet=true`）
- 护栏：`memoryScene.allowUse` 必须为 true 才落库（用户明示允许使用该场景，PRD 要求）。

### POST /upload — 素材上传（图片/音频/视频）
- `multipart/form-data`（字段名 `file`），需 Bearer；出参：`{ "resourceId", "url" }`。
- 大小上限 25MB；由 `HttpGateway` 直接处理（原始字节 + 二进制安全 multipart 解析，不走 JSON 路由）。
- 存储经 `IStorage` 抽象装配（默认本地磁盘 `LocalDiskStorage`，预留 OSS/COS/MinIO），见 §存储配置。
- 返回的 `url` 用于 `<img>/<audio>/<video>` 直接引用；本地存储由 `GET /api/v1/files/{key}` 公开下发。

### GET /api/v1/files/{key} — 素材下发（公开）
- 读本地存储对象并按 MIME 下发（带长缓存头）；云存储模式下 `url` 直接是云对象地址，不经此端点。

---

## 3. 我的它（主卡 + 温度 + 明信片墙）

### GET /pet/me — 我的宠物档案（MyPet）
- 出参（对齐 FE `MyPet`）：
```json
{ "petId","name","signature","temperature":72,"visibility":"private",
  "cover":{"gradient","emoji"}, "recent":"<最新一条温柔近况>",
  "lifeBook":[{"title","year","desc","placeholder":{}}],
  "postcards":[{"id","date","caption","placeholder":{},"locked":false}] }
```
- 🔄 温度规则（`PRD-echo-pet.md §3.11`，服务端权威）：**绝对硬下界 60%**（`C1`，不可编辑）、只由主人 1v1 陪伴驱动；**外部献花不改温度**（§0.7 #5）。
  - 🔴 **衰减（2026-08-25 制作人裁定改写，`DECISIONS TM1`）**：**免费 —— 无回访则按 `kDecay` 缓慢回落至 `TEMP_FLOOR_FREE`；订阅期 —— 保持当前刻度不回落。**
  - ⚠️ 🔴 **上面这条是<u>裁定</u>，不是线上现状 —— 回落至今没有实现**（2026-08-27 回代码核实）：`Temperature.java` **只有回暖没有回落**，`onOwnerVisit` 单向朝天花板走，**没有任何按时间衰减的入口**；该类文档自己标着「本类目前只有回暖没有回落…… 上面第 2 条是裁定，不是本类的现状描述」，`EchoApi.petVisit` 那行注释同样写着「⚠️ 回落尚未实现」。🔴 **唯一存在 `kDecay` 计算的地方是测试沙盘 `src/test/java/com/echo/harness/TemperatureModel.java`，那不是生产路径。**
    > 🔴 **为什么必须在契约里写这一句**：本节读起来像回落已经生效。⚠️ **温度只会往上走，而这件事不报错、也不会让任何请求失败** —— 报表上看起来就是「用户的宠物都挺暖的」。🔴 **照本节去验收的人会以为「长期不来会降温」这条已经能测**，而它一次都跑不出来。
    > 📌 **本行只登记状态，不含任何实现方案**（`kDecay` 取值、按什么周期跑、订阅态怎么读，均未定，见下方两条硬约束与 `WORKLOG` 待深化）。
  - `TEMP_FLOOR_FREE` **本期取值 60**，🔴 **写成配置项，不硬编码**（配置台须校验 `≥ 60`）。⚠️ 🔴 **它与那个 60 硬下界本期恰好重合，但不是同一个东西** —— 🔴 **不得实现成对硬下界常量的复用或别名**（`SPEC-admin-console §4.7` 验收清单）。
  - 🔄 🔴 **原文「不惩罚式衰减 …… 绝不下探」已删。** ⚠️ **裁定方向是以 `PRD` 为准改契约，不是改 `PRD`。** 推翻理由：原判断只看到「回落 = 加剧负面情绪」这一面，🔴 **漏了「回落 = 温度有条件 ⇒ 否定官方点名的『无条件陪伴』风险画像」这一面** —— **一个永不下探的温度实质上就是无条件的**，反而是那条抗辩的弱项。
  - ⚠️ 🔴 **另有一个与本裁定无关的独立文档质量 bug，一并记住**：**这一行原本自称「依据 `PRD §3.11`」，却写了与 `PRD §3.11` 相反的规则**（PRD 一直写「长期不来缓慢回落」）。🔴 **本次改完之后那句引用才第一次变成真的。** **不要把「有引用」当成「引用是对的」。**
  - 📌 **代码侧连带（🔴 归后端线，本文档不改代码）**：~~`Temperature.java` 类注释三条硬规则第 2 条仍写「无回访即保持不变，**绝不下探**」，🔴 **须一并改写**~~ 🔄 ✅ **已于 2026-08-27 改完并销账**（该类文档现写「会自然回落，回落到地板为止」，并单列一节记下推翻理由）。🔴 **仍未做的只剩一件**：它需从纯静态函数改为**可读付费状态**（订阅期豁免要读订阅域），且**回落本身尚未实现**（见上）。
    > ⚠️ 🔴 **这一行本身就是那类错误的一个实例**：它把「代码未改」写成了状态描述，而代码已经改了。**规格记的是它写下那一刻的事实，不是现在的事实** —— 引用这类状态句之前必须回代码查一次。
  - 🆕 🔴 **温度的<u>出口</u>只有一个：色调与性情表达**（`DECISIONS DP11`，2026-08-25）。🔴 **温度不得驱动回声频率** —— **本行以及全契约不存在任何「温度 → 频率」的字段或参数，这是有意为之，不是遗漏。**
    > ⚠️ 🔴 **写这一句是为了挡住一次「顺手补全」**：`PRD` 原本写着「温度分档驱动**回声频率**、色调与性情表达」，🔴 **实现的人若照旧版 PRD 写，会以为契约漏了一个字段并主动补上。**
    > 🔴 **反向断言**：**三档温度下，稳定期回声投递间隔相同。** 验收 `ACCEPTANCE TC-22`。
    > 🟢 **稳定期频率本身只降不升**：冷淡自动放缓保留，**活跃加频删除**（`B18` 已就地收窄）。
  - ✅ **本行引用已复核（2026-08-25 晚）**：`PRD-echo-pet §3.11`/`§3.12` 现行原文与本行**逐条一致**（地板 60 · 回落 · 订阅期豁免 · 温度只驱动色调与性情表达）。🔴 **上一轮那处「引用了却写反」已消除，且本轮新裁定没有再造出一处。**
  - ✅ **2026-08-27 再复核一次**：`PRD-echo-pet §3.11` 核心概念逐字「**欠维系→朝地板缓慢回落；盈余→朝 100 回暖；恰好维系→不变**」，与本节**方向一致**。🔴 **所以「§3 自称依据 `§3.11①` 却写了相反规则（『绝不下探』vs『自然回落』）」这条早先登记的缺陷，与本节是<u>同一处</u>，且已经关闭** —— ⚠️ **不要再当成待修项重开**；本轮唯一还成立的问题是「回落未实现」，见上。

### PATCH /pet/me — 更新档案（签名/可见性等）
- 入参：`{ "signature"?, "visibility"? "private|friends|public" }`（可见性直白三档，§0.7 #1）

### POST /pet/me/visit — 记一次"主人回访"（触发温度回暖 + 拉取今日近况）
- 出参：`{ "temperature", "newEchoes": [Echo...], "echoGenerated": bool }`
- 🔴 **近况一天一条**（2026-08-27）。同一天再回访 **返回今天那一条**，不生成第二条。
  阈值不是拍的：**「今日近况」这四个字本身就规定了一天只有一条**，节流前的行为
  （每次回访产一条，一天点 10 次 10 行雷同私密卡）与端点自己的措辞矛盾。
  ⚠️ 因此**没有引入可配参数** —— 可配的阈值会让「今日近况」变成一天可以有五条的东西。
- 🔴 **同一天再回访刻意<u>不</u>返回空列表**：「你来了，但今天没有近况」会被读成
  「它今天没有消息」，那是往缺席方向推（`CR2` 的反面）。屏幕上永远有内容。
- `echoGenerated` = 这一条是不是刚生成的，供前端决定要不要做「有新内容」的动效。
  🔴 **不下发「今天第几次来」的计数**，前端也不要自己数 —— 那是对回访行为的计量反馈（`DP2`）。
- ⚠️ **温度那一侧尚无节流**：每次回访都朝天花板走一档，一天点 10 次≈顶到 100。
  📋 **已报出待裁定**（改它会改变「回暖速度」这个产品可感知的数字，属裁定不属修复）。

### ~~DELETE /pet/me~~ — **已下线**（2026-08-24，见下方处置）

- **正式删除端点定死为 `DELETE /pet/:id`**（语义 = **软删置位**），契约见 **§15.1**。全项目**只此一条**删除回忆集的路径，生产可用。
- `DELETE /pet/me` **下线**：路由摘除、前端 `resetPet()` 改调 `DELETE /pet/:id`。
- 其现网实现 `PgEchoStore.deletePet`（连删 `t_pet_echo` / `t_postcard` / `t_remember` / `t_pet` **四张表**）**一并下线**。

> **⚠️ v1.1 处置留痕（2026-08-24 · QA 复签 A-4 / 不一致-4）**：原契约 `DELETE /pet/me — 删除当前宠物，回到未建档态（dev-only，非生产）` 与 `SPEC-trust-and-compliance CM-G1` 的 `DELETE /pet/:id` 在**路径**（`/pet/me` vs `/pet/:id`）、**语义**（重置 vs 软删）、**生产可用性**（dev-only vs 正式能力）三处对不上，且规格未说这个已存在端点怎么处置 → 开发必然自行发挥。
>
> **处置理由（不引入新例外）**：① 其实现是标准的四表级联清理，正是 `DECISIONS CM-D1` / `SPEC G0-1` 明令禁止的（QA §5.4 存量第 1 处，处置表见 `SPEC §CM-G0S S-10`）；② 保留它就得为它开一个 CR 红线白名单项，而白名单**以外一律禁止、新增需 PM 批**（`SPEC §CM-G0S S-9`）；③ 它原本的用途「方便重入建档流程」在软删 + `G0-9` 部分唯一索引（`WHERE "deletedAt" IS NULL`）之后已由 `DELETE /pet/:id` 天然满足——软删后 owner 本人亦不可见（`CM-D11`）、重新建档不再撞唯一键。故**保留第二条删除路径既无必要、又要付一个白名单例外的代价**。
>
> 📌 **交 PM 复核**：本条为按既有裁定（CM-D1 + G0-9 + S-9 白名单机制）**推导收敛**的结论，非新放宽。若 PM 希望保留一个测试专用重置端点，须**回批一个白名单项**并明确「仅非生产 profile 装配」；在此之前以「下线」为准。

---

## 4. 近况/来信（复用 EchoService，AI 生成 + 基调安全层）

### GET /pet/me/echoes — 我的它的近况流（回声周期产物）
- 分页；item：`{ "echoId","text","tone","createdAt","placeholder":{} }`
- 生成侧：`text` 由 `ILlmClient.complete` 产出，**必过 COPY-GUIDE §4 system prompt 约束 + 禁用词过滤**（服务端强制）。

### POST /pet/me/echoes/:echoId/reply — 给它回信（互动阶梯 L4，§2.14）
- 入参：`{ "text" }`；出参：`{ "echoId", "reply": {...可选它的回应...} }`

---

## 5. 献花 & 记得（**必须拆开** · §0.6/§0.7 #3#4）

> 关键：献花 ≠ 记得。此前原型把二者混在一起，本版服务端强制区分。

### GET /flowers/quota — 我的今日献花额度
- 出参：`{ "dailyFree": 5, "usedToday": 2, "remaining": 3, "purchasedBalance": 0 }`
- 规则（§0.7 #3）：每日免费 5 朵，可全给一人；用尽可购买；**不加宠物温度、不排名**。

### POST /windows/:windowId/flower — 献花（对"主人"的心意）
- 入参：`{ "count": 1, "type": "daily|limited|premium", "message"?: "…", "anonymous": false }`
- 出参：`{ "ok": true, "quota": {...更新后额度...}, "bondMark": "你为它献过 3 朵" }`
- 校验：`count<=remaining+purchasedBalance`，否则 `3001 额度不足`（温柔文案）。
- 落库：记 owner 可见的"私密羁绊名单"；**不写温度**。

### POST /windows/:windowId/remember — 记得（对"它"的静默誓约，开关状态）
- 入参：`{ "remembered": true }`（一人一次的**状态**，非可叠加计数）
- 出参：`{ "remembered": true }`
- 幂等：重复置 true 无副作用。

### GET /windows/:windowId/remember — 记得的"暖光面孔墙"（§0.7 #4）
- 出参：
```json
{ "warmthLevel": 0.0-1.0,               // 暖光浓度（前端据此渲染光晕强度）
  "faces": [ {"accountId","avatar"} ],   // 记得它的人的头像（聚成一片暖光；有上限、可分页）
  "meRemembered": true }
```
- **红线**：**不返回精确总数字段、不排名**（前端也不得展示数字）。看过数仅 owner 内部接口可见（§6）。
- ❄️ 🔴 **上面这行红线守不住，见 §18.3。** 它字面为真（确实没有整数总数字段），但 `warmthLevel` 就在上一行、
  `faces = round(warmthLevel × 20)` 一步反解出精确人数，且**每个能看到这扇窗的访客都拿得到**。
  **它描述的是实现，不是后果** —— 别看见这行就以为这一处已经检查过了。
- ❄️ `faces[]` 的下发范围另有一条冻结项 `C-8`，见 §18.1（前端已按阈值 5 停画，服务端仍整批下发）。

---

## 6. 窗口页 / 广场（一扇窗 · 游客可看，PRD §2.1-2.8）

> 🆕 🔴 **`OM1` 已落地：`GET /plaza` 改发回忆卡（2026-08-27 · 后端线 `C-2`）**
> 模型：**窗口是容器（一只宠物一个窗）· 回忆卡是窗里发出来的一条 · 🔴 共鸣厅流的是卡，不是窗。**
>
> 上一版这里写着「本节契约一字未改，也不得据此自行改动」，理由是 `OM1` 只登记模型、
> 改造「是另一条线的活」。🔴 **那条线就是本次这条**，所以 §6.0 与 `GET /plaza` 已按 `OM1` 改写。
> ⚠️ **这是破坏性契约变更**，前端会 404 的每一处逐条列在 §6.0.3，**不要自己猜**。
>
> 📌 `GET /windows/:id`（窗详情）**保留且语义不变** —— 它收的仍然是 petId。
> 变的只有「广场下发的 `id` 是什么」这一件事。

### 6.0 `cards[]` — 卡的唯一形状（契约 `C-2`）

🔴 **只有一个 card 形状。** `GET /plaza`、`GET /pet/me/cards`、`GET /users/:id/cards` 共用它。
两处差别只体现在**作者侧三个键给不给**，⚠️ **不是换一个形状** —— 两套形状会让前端写两个卡组件，
然后它们会缓慢分叉，而分叉那天没有任何报错，只是某个字段在某个页面上不见了。

> 🆕 🔴 **2026-08-27 裁定 · 卡面出作者（产品含义与后果见 `PRODUCT-MAINLINE.md §18.4`，此处只落契约面，不写第二份全文）**
>
> **卡面出现作者是有意的裁定，不是漏写。** 出**头像 + 昵称**，点了去**作者主页**（`GET /users/:id/cards`）。
> 🔴 **粉丝数不上卡面**，仍只在作者主页出现（`RK14`/`X12` 不变：不做榜单、不进排序）。
>
> ⚠️ 🔴 **本形状今天一个作者字段都没有**（见 §6.0.1），落地需要新增三个键：`authorId` · `authorName` · `authorAvatar`。
>
> 🔴 **落地口径：三个键无条件下发，作者块出不出<u>由使用面决定</u>，不由形状决定。**
> 广场与关注页签**渲染**；作者主页与「我的卡」列表**不渲染**（在他自己的页面上每张卡都挂着他自己的头像，是冗余）。
> **理由与本节开头那句同源** —— 按使用面拆形状，就是两套形状，然后缓慢分叉。
>
> ⚠️ 🔴 **本节开头「差别只体现在作者侧三个键」这句口径要跟着改**：现在有**两组**条件键，
> 而且方向相反 —— `pinnedAt`/`visibility`/`visibilityIntent` 是**只有作者自己看得到**，
> 新增的作者三键是**只有别人看才有意义**。🔴 **不改这句，下一个人会按「只有一处差别」去实现，
> 把作者块在三个面上全渲染出来**，而那在两个面上都是错的。
>
> 🔴🔴 **一条给将来的人的硬提示**：**卡面出作者之后，「陌生人走进那扇窗」从必然降为概率，**
> **第 12 步只剩 `RK-H` 一堵承重墙**（记得与献花是窗级、卡级那一列仅供归因且**永不下发**，见 §6.0.2）。
> ⚠️ **动 §6.0.2 那两行之前，先回去看 `PRODUCT-MAINLINE.md §18.4.2`** ——
> **把卡级归因列下发出去，看起来会像一次纯粹的技术优化。**

#### 6.0.1 字段表

| 键 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 否 | 🔴 **cardId**，不是 petId。int64 序列化成字符串 |
| `petId` | string | 否 | 所属窗。🔴 **要调 `/windows/:id/*` 那一组端点取这个键**，不是 `id` |
| `title` | string | 🔴 **可空（空串）** | 作者取的标题，≤30 字。⚠️ **手写 record 与生命之书多半没有**，空串是合法值 |
| `excerpt` | string | 可为空串 | 🔴 正文首句，**服务端切**。⚠️ 列表响应里**没有 `body` 这个键** |
| `cover` | string | 🔴 **可缺（空串）** | 封面素材 key。⚠️ 空串是合法值，不是数据缺陷 |
| `hasCover` | bool | 否 | 与 `cover` 非空等价，显式给出——让「没有图」是一个可判断的状态，不是一次字符串比较 |
| `sourceType` | string | 否 | `record｜book_page｜postcard｜echo` |
| `topicIds` | string[] | 否（可空数组） | 主题标签 id，0–3 个。⚠️ 不上卡封面（设计线已删 chip） |
| `publishedAt` | int64\|null | 是 | 作者点发布的时刻 |
| `pinnedAt` | int64\|null | 是 | 🔴 **仅作者视图下发**。置顶不进共鸣厅公开流 |
| `visibility` | string | 否 | 🔴 **仅作者视图**，且是**生效**档位（已与窗取过交集） |
| `visibilityIntent` | string | 否 | 🔴 **仅作者视图**。作者**设定**的那一档。与 `visibility` 不同即说明被窗收窄了 |

🔴 **`title` 与 `excerpt` 两个都可能为空，这是预期输入不是缺陷。** 前端取值链是
`title` 非空则用 `title`，否则用 `excerpt`；两个都空的卡靠封面撑，没封面就靠留白撑。
⚠️ **服务端刻意不做这一层合并** —— 合并之后前端就分不清这张卡到底有没有标题了。

#### 6.0.2 🔴 刻意**不**下发的字段

| 不发什么 | 为什么 |
| --- | --- |
| `body`（正文全文） | 列表面只给 `excerpt`。🔴 **前端切首句等于把全文发给了不该看全文的人** —— 前端的 fail-closed 渲染保护的是「页面上画什么」，保护不了「端点下发什么」，而抓一次包看的是后者。全文只在卡详情里给 |
| 卡级入口归因 | `RK-H` 护栏：🔴 一旦下发到任何用户能看见的地方，当场退化成点赞 |
| 任何互动计数 | `D4` 不显精确数字、不排名。暖意走窗级 `warmthLevel` |
| `status`（非作者视图） | 「审核中 / 被打回」是作者与平台之间的事，陌生人不该看到一张卡的审核状态 |

#### 6.0.3 🔴 前端会 404 的每一处（破坏性变更清单）

广场下发的 `item.id` 含义从 **petId** 变成 **cardId**。下面五个端点收的仍然是 **petId**，
拿新的 `id` 去调 🔴 **不是编译错、不是类型错，是运行时静默 404，只有点进去才会发现**。

| # | 端点 | 前端调用点 | 现在传的 |
| --- | --- | --- | --- |
| 1 | `GET /windows/:petId` | `DetailScreen.tsx:123` `api.windowDetail(petId)` | `petIdOfCard(cardId)` |
| 2 | `POST /windows/:petId/seen` | `DetailScreen.tsx:133` `api.windowSeen(petId)` | 同上 |
| 3 | `POST /windows/:petId/flower` | `DetailScreen.tsx:190` `api.flower(petId, …)` | 同上 |
| 4 | `POST /windows/:petId/remember` | `DetailScreen.tsx:235` `api.setRemember(petId, …)` | 同上 |
| 5 | `GET /windows/:petId/remember` | `DetailScreen.tsx:237` `api.rememberWall(petId)` | 同上 |

🟢 **修法只有一处**：`echo-h5-proto/src/lib/ids.ts` 的 `petIdOfCard()` 今天是恒等转换
（`return cardId as PetId`），🔴 **改成从卡自带的 `petId` 键取值**。
前端已经把这五处全部收口到这个函数后面，所以**不需要逐个改调用点**。
⚠️ 该文件写着「不要在这里猜 `GET /plaza` 会长成什么样」——现在不用猜了，形状就是 §6.0.1，
卡上带 `petId`，正是为这个函数准备的。

⚠️ **另外两处 404 与本次变更无关，但一并报出（既有缺陷）**：

| 端点 | 前端调的 | 后端实际提供的 |
| --- | --- | --- |
| 留言 | `POST /windows/:id/messages`（`http.ts:220`） | 🔴 `POST /cards/:cardId/messages` |
| 待处理留言 | `GET /windows/:id/messages/pending`（`http.ts:222`） | 🔴 `GET /cards/:cardId/messages/pending` |

前端注释把**键**说对了（收 cardId），但**路径前缀**写成了 `/windows`。
今天 `IS_MOCK` 挡着不报，🔴 **切真接口那天这两个必 404**，而且和上面五个混在一起会被误判成同一个原因。

---

#### 6.0.4 📋 给前端线的移交清单（**本节可整节转发，自带全部上下文**）

> 后端线交办，2026-08-27。**改动只在 `echo-h5-proto/`，后端不需要配合发版。**
> 三处改动，互相独立，可分别提交。
> 🔴 **核实过后端路由确实存在**（`LeaveWordsApi.java:92-93`），不是照文档抄的。

**背景两句话。** `GET /plaza` 从「下发宠物窗口」改成了「下发回忆卡」，
所以 `items[].id` 的含义从 **petId** 变成了 **cardId**（形状见 §6.0.1，卡上**自带** `petId` 键）。
⚠️ **这类错误不会编译报错、不会类型报错，只会运行时静默 404**，所以下面每一处都写了怎么验。

---

**改动 1 · 🔴 必做，否则详情页整页打不开** —— `src/lib/ids.ts`

```ts
// 现在（恒等转换，广场发窗口时它是对的）
export function petIdOfCard(cardId: CardId): PetId {
  return cardId as string as PetId
}

// 改成：从卡自带的 petId 取
export function petIdOfCard(card: PlazaCard): PetId {
  return asPetId(card.petId)
}
```

🟢 **只改这一个函数。** 前端已经把下面五处全部收口到它后面了，
**所以不需要逐个改调用点**（但函数签名从 `cardId` 变成整张 `card`，五处传参要跟着换成卡对象）：

| # | 端点 | 调用点 |
| --- | --- | --- |
| 1 | `GET /windows/:petId` | `DetailScreen.tsx:123` `api.windowDetail(…)` |
| 2 | `POST /windows/:petId/seen` | `DetailScreen.tsx:133` `api.windowSeen(…)` |
| 3 | `POST /windows/:petId/flower` | `DetailScreen.tsx:190` `api.flower(…)` |
| 4 | `POST /windows/:petId/remember` | `DetailScreen.tsx:235` `api.setRemember(…)` |
| 5 | `GET /windows/:petId/remember` | `DetailScreen.tsx:237` `api.rememberWall(…)` |

📌 **`GET /windows/:id` 这个端点本身没有变，它收的仍然是 petId。**
变的只有「广场下发的 `id` 是什么」。⚠️ **不要去改这五个端点的路径。**

✅ **怎么验**：从广场点进任意一张卡，详情页能出内容 + 能献花 + 能看到面孔墙。
🔴 `ids.ts:43` 那句「谁都不许绕过这个函数直接 `as PetId`」要继续守住 ——
绕过去的那一处正是迁移当天唯一一个不报错只 404 的地方。

---

**改动 2 · 既有缺陷，与改动 1 无关** —— `src/api/http.ts` 两个路径前缀写错

```ts
// leaveMessage（约 220 行）
- `/windows/${encodeURIComponent(windowId)}/messages`
+ `/cards/${encodeURIComponent(cardId)}/messages`

// pendingMessages（约 222 行）
- `/windows/${encodeURIComponent(windowId)}/messages/pending`
+ `/cards/${encodeURIComponent(cardId)}/messages/pending`
```

🟢 **传的值本来就是对的，只有前缀错了。** 接口声明
（`backend.ts:217`/`219`）写的是 `cardId: CardId`，调用点
（`LeaveMessage.tsx:45`、`MessageTriage.tsx:38`）传的也确实是 cardId ——
🔴 **只有 `http.ts` 里的形参名叫 `windowId`，然后顺着这个名字拼出了 `/windows/` 前缀。**
建议连形参名一起改成 `cardId`，否则下一个人还会照着名字再拼错一次。

⚠️ **这两处今天被 `IS_MOCK` 挡着不报。** 🔴 切真接口那天必 404，
而且会和改动 1 混在一起，被误判成「广场改卡引起的」——**它跟广场没关系，独立存在很久了**。

✅ **怎么验**：关掉 `IS_MOCK`，在详情页留一句话、作者侧打开待处理队列，两者都不 404。

---

**改动 3 · 可选，只影响动效** —— `POST /pet/me/visit` 新增出参 `echoGenerated: boolean`

回访近况已改成 🔴 **一天一条**：同一天再回访，`newEchoes` 里返回的是**今天那一条**
（不是空列表，也不是新生成的第二条）。`echoGenerated` 告诉你这一条是不是刚生成的，
前端**可以**据它决定要不要做「有新内容」的动效。

🔴 **不下发「今天第几次来」的计数，也不要自己在前端数** ——
那会变成对回访行为的计量反馈，踩 `DP2`。

✅ **怎么验**：同一天连点两次回访，第二次 `echoGenerated: false` 且 `newEchoes` 与第一次同一条。

---

**⚠️ 一处不要动的** —— `/messages/arrivals` 出参里的 `cardId` 键**今天装的是 petId**。

🔴 **不要为此改前端。** 这个键名是错的，但改法未定（改键名 / 改成读卡级的 `t_resonance`），
🔴 **等后端裁定后再动**；此前它的值一直是 petId，前端按 petId 用是对的。
⚠️ **也不要相信「以后它会自动变成 cardId」——那个说法已被撤销**（`RK-H`：互动不搬家）。

### GET /plaza — 共鸣广场瀑布流（🔴 公开**回忆卡**）
- 分页信封 `{items,nextCursor}`（§14.1）；`items[]` = §6.0.1 的 card，**非作者视图**（不含 `pinnedAt`/`visibility`/`visibilityIntent`）。
- 只出**生效可见性 = public 且已过审**的卡。
- 🔴 **顺序归排序引擎**（权重衰减 / 制动 / SURGE），**不看 `pinnedAt`**。
```json
{ "items": [ { "id":"7301","petId":"5012","title":"","excerpt":"它最后一次趴在窗台上晒太阳。",
               "cover":"k/abc","hasCover":true,"sourceType":"record","topicIds":["t12"],
               "publishedAt":1756200000000 } ], "nextCursor":null }
```
- ⚠️ **曝光记账**：本端点的 `reqId` 登记为 `surface=grid`，🔴 **网格层的曝光整批拒收、不记 `n`**
  （`SPEC-feed-surfaces` 概述第 1 条：`n` 只在全屏层 + 视口内连续驻留 ≥1000ms 时记）。

### GET /pet/me/cards — 我的卡列表（作者视图）
- 出参 `{items,nextCursor}`；card **含**作者侧三键；含**全部状态**（草稿 / 审核中 / 被打回也出）。
- 🔴 顺序 `pinnedAt DESC NULLS LAST, publishedAt DESC`。

### GET /users/:id/cards — 别人的卡列表
- 出参同上，但 card 为**非作者视图**，且只出生效可见性对当前观看者可见的卡。
- 本人调它时等价于作者视图（同一个人）。

### PATCH /cards/:id/visibility — 作者改卡的可见性（`C-5`）
- 入参 `{ "visibility":"public|friends|private", "expect":"<改动前的值，可选>" }`
- 🔴 **硬约束「卡不得宽于窗」**：卡设得比窗宽时 **报 400 而不是静默收窄**。
  ⚠️ 静默收窄的话作者点了「公开」、界面回成功，而这张卡只有亲友能看——
  他会以为自己已经发出去了，要等到「怎么没人看」才发现，那时已经过了分发窗口期。
  文案要落到「先把窗改成公开」，而不是只报一句失败。
- `expect` 不匹配回 409（另一个请求抢先改过）。
- 🔴 收窄导致卡不再是公开态时，`pinnedAt` **同一次操作一并清空**，不留悬空。
- 落一条 `t_card_visibility_log`，`changedRole=author`。

### PUT / DELETE /cards/:id/pin — 置顶 / 取消置顶
- 🔴 **作用域 = 作者自己那一页的公开卡列表。绝不进共鸣厅公开流** ——
  那会和权重衰减正面打架（衰减刚把老卡压下去、置顶又顶回第一位），等于开一个绕过排序机制的后门。
- 上限 **3** 张，🔴 后台可配（`card.pinned.max`；配 0 回落到 3，**不当成「不限」**）。
- 仅**生效可见性 public 且已过审**（`status=public` 且 `reviewedAt≠null`）可置顶。
  ⚠️ 两个条件都判：`reviewedAt` 写后不可变，所以**被下架的卡它也非空**，只判它会让下架的卡还能置顶。
- `PUT` 幂等（已置顶的再置顶不占额度）；额度满回 409。
- 🔴 不是自己的卡回 **404 而不是 403** —— 403 本身就是一次归属探测。
- 🔴 **自动解除**：取消发布 / 审核打回 / 运营下架 / 作者收窄可见性时清空 `pinnedAt`。
  ⚠️ 留着悬空的后果有两个：① 卡重新过审时**自己跳回置顶位**，而作者没再做这个决定；
  ② 上限计数把隐形置顶算进去，作者会遇到「我只置顶了 1 张，系统说满了」，而他**看不到**那两张是谁。

### GET /windows/:windowId — 窗口详情（游客可看；owner 可见性过滤）
- 出参：`Window` 字段 + `lifeBook[]` + `flowerAllowed` + `visibility` 决定字段裁剪 + **`rememberWall`（键名固定为 `rememberWall`，形状同 §5 GET remember：`{warmthLevel, faces:[{accountId,avatar}], meRemembered}`）**。
- ⚠️ 契约要点（QA M-3）：键名必须是 **`rememberWall`** 且**必含 `faces`**（前端面孔墙依赖），不得只返 `remember{warmthLevel,meRemembered}`。

### POST /windows/:windowId/seen — 记一次"看过"（被动脚印）
- 出参：`{ "ok": true }`；**看过数只 owner 内部可见，不对外**（§0.6）。

### GET /pet/me/insights — owner 私域数据（含看过数）
- 出参：`{ "seenCount": 128, "rememberFacesCount": 42, "flowersReceived": 60 }`（仅本人可见）
- ❄️ 🔴 **这三个字段前端现在都不显示数值了，且 `seenCount` 按层级口径本身就不该存在** ——
  它把**卡那一层**的量汇总到了**对象那一层**。这条不是「加两个出参」，**是删一个、加两个**。见 §18.2。

---

## 7. 明信片墙（§2.15 · 里程碑解锁 + 付费只加速/款式）

### GET /pet/me/postcards — 明信片墙
- item：`{ "id","date","caption","placeholder":{},"locked":true,"unlockHint":"相伴满100天解锁" }`

### POST /pet/me/postcards/:id/unlock — 解锁（里程碑达成时）
- 出参：`{ "unlocked": true }`；护栏：**内容永远靠陪伴解锁**，付费仅"加速/款式"，服务端拒绝对"内容本身"付费解锁。

### GET /shop/postcard-skins /  POST /shop/purchase — 限定款式购买（只卖皮肤/边框/材质，不锁内容，§0.7 #2）

---

## 8. 亲友列表 & 动态圈（§2.9 · 关系层）

### GET /relations — 亲友列表（在线优先 + 置顶 + 静音过滤）
- 分页；item = FE `RelationUser`（含 `online/lastActive/priority/mutedUntil/hasUnseenReel/viewableByMe/reels[]/pet`）
- ⚠️ 契约要点（QA M-5）：`pet` 形状须为 **FE `MyPet`**（非 Window）；必返 **`lastActive`**（毫秒）；`reels[]` 与 `hasUnseenReel` 反映真实动态；**`viewableByMe` 依对方可见性真实计算**（无权查看者其 `reels`/动态不下发，落实 TC-08"无权查看者不显动态"）。
- **前端必须接真后端**（QA M-5：现状用 seed 数据、从不调用本接口，须改为 `api.relations()`）。
- 排序：置顶 > 在线 > 最近活跃；`mutedUntil>now` 的过滤/降权。

### PATCH /relations/:id — 调整关系（置顶/不看三档）
- 入参：`{ "priority"?: true, "mute"?: "7d|3m|permanent|clear" }`

### POST /relations/:id/reel-seen — 标记某亲友动态已看（清光环）

---

## 9. 记录（§2.14 · 双向：给它 & 给自己）

### GET /records?scope=pet|self|all — 记录流
- **分页；响应统一为 `{ items:[...], nextCursor }`**（QA M-2：前端须取 `.items`，不得把响应当数组）。
- item：`{ "id","scope":"pet|self","text","placeholder"?,"createdAt" }`

### POST /records — 留一笔（freeform + 可选温柔提问引导）
- 入参：`{ "scope":"pet|self","text","photoRefs"?:[] }`
- 护栏：**绝不做成打卡任务**（无连续天数压力/无红点催促，§2.14）。`scope=self` 的记录喂养 §2.13 向前的光谱。

---

## 10. 消息集散地（§2.14 · 克制的中枢）

### GET /messages — 统一消息流（三类：亲友/系统/宠物更新）
- **分页；响应统一为 `{ items:[...], nextCursor }`**（QA M-1：前端须取 `.items`；未读柔性暖点由 `items.some(!read)` 判定）。
- item：`{ "id","kind":"friend|system|pet","title","preview","createdAt","read":false,"routeTo":{"type":"window|relation|record|echo","id"} }`
- 注：**回声到达也进本流**（`kind:"pet"`，`routeTo` 跳回声本体）；未读=克制柔性暖点、不带数字（social §2.14）。
- 说明：消息只"露出更新 + 导进统一互动系统"（§2.14），点击按 `routeTo` 跳转，不自带独立互动。

### POST /messages/read — 批量已读 `{ "ids":[...] }`

---

## 11. 我的光谱（§2.11 · solo 自我回溯）

### GET /spectrum — 我的光谱（暖光星云 + 内在阴影）
- 出参：`{ "nodes":[SpectrumNode], "shadows":[ShadowArea] }`
- **职责划分（QA M-4 · 2026-07-28 定案：前端持布局、后端只下发语义）**：
  - 后端 `SpectrumNode` 语义形状：`{ "id","label","intensity":0-1,"createdAt" }`
  - 后端 `ShadowArea` 语义形状：`{ "id","whisper","depth":0-1 }`
  - **坐标/尺寸/色相/延迟（x/y/size/tone/delay）由前端从语义值映射生成**，后端不下发布局字段。前端 `types.ts` 的 `SpectrumNode/ShadowArea` 应拆为「后端语义 DTO」+「前端视觉 VM」两层，避免把布局字段当后端契约。
- 生成侧：`shadows[].whisper` 由潜台词理解涌现，**第一人称、氛围化、非指控、不可归因**（§2.11 红线）；服务端保证光面结构地板（光不被暗吞）。

### POST /spectrum/anchor — 留一个锚点（自己给自己的一句话）
- 入参：`{ "label" }`；出参：新 `SpectrumNode`

### POST /spectrum/shadows/:id/integrate — 把一处暗面"整合"回暖成光点
- 出参：`{ "node": SpectrumNode }`（暗区消失、生成暖光点）

---

## 12. 六项定案 · 服务端强制清单（验收口径）

| # | 定案 | 服务端强制点 |
|---|---|---|
| 1 | 可见性直白三档 | `visibility ∈ {private,friends,public}`，默认 private；公开字段按档裁剪 |
| 2 | 明信片付费只加速/款式 | 拒绝对"内容本身"付费解锁；款式购买不影响解锁进度 |
| 3 | 献花每日5朵/可买/不加温/不排名 | 额度校验；献花不写温度；无排名字段 |
| 4 | 记得=暖光面孔墙/无数字/看过内部 | remember 接口不返精确总数；seen 只 owner 内部可见 |
| 5 | 外部献花不加温度 | 温度接口与献花接口完全解耦 |
| 6 | 文案过词表 | 所有 AI 生成与错误文案过 COPY-GUIDE 禁用词过滤 |

---

## 13. 埋点（自然流量收口用，对齐 RELEASE §3.4 / §6）

事件：`guest_created`、`onboarding_start/refine/confirm`、`pet_visit`、`echo_view`、`echo_reply`、`flower_offer`、`remember_toggle`、`window_seen`、`window_open`、`postcard_unlock`、`share_click`、`record_create`、`spectrum_anchor`、`spectrum_integrate`、`bind_account`。
每事件带：`accountId(匿名)`、`isGuest`、`ts`、`ctx`。漏斗：`guest_created → onboarding_confirm → pet_visit(D1回访) → flower/remember → share/bind`。

---

## 14. 契约修复约定 & 架构对齐（QA 2026-07-28 · 定案）

> 背景：QA 全量重测发现"编译测试全绿、12 条产品红线全过，但前后端契约整体错位 + 亲友链路悬空 + 文档架构失真"。以下为制作人裁定，作为修复唯一口径（真后端=生产真源，M-1~M-5 上线必修）。

| 项 | 裁定 | 影响接口 |
|---|---|---|
| **生产真源** | **真后端为生产真源**（DEPLOY §5）；契约错位=上线必修（Blocker 级） | 全部 |
| **分页信封统一** | **所有列表接口统一返 `{items,nextCursor}`**，前端一律取 `.items`（与 echoes/plaza 对齐） | §9 records、§10 messages、§8 relations（M-1/M-2） |
| **记得墙键名** | 窗口详情记得墙键名固定 **`rememberWall`** 且**必含 `faces`** | §6（M-3） |
| **光谱职责** | **前端持布局**：后端只下发语义值（intensity/depth/whisper/label），前端映射坐标/色相/尺寸 | §11（M-4） |
| **亲友接真后端** | 前端 `useRelations` 改接 `api.relations()`；后端补 `lastActive/reels/viewableByMe` 真实值、`pet` 用 MyPet 形状 | §8（M-5） |
| **架构：WS+HTTP 并存共享服务** | **HTTP 层真正复用 WS 侧领域服务**（EchoService/MindSpaceService/ResonanceService 等），两传输共享同一领域，交后端落实（非维持平行自建域） | 全部（M-6） |
| **补测试** | 新增**前后端契约/集成测试**（真后端适配器 `http.ts` 目前 0 契约测试，是错位漏网主因） | 前端 + 后端 |

**Minor 一并跟进**：WS 端口文档统一（9001 vs 9101，mi-1）；~~`DELETE /pet/me`(resetPet) 后端补 dev-only 路由或前端移除并入契约（mi-2）~~ → **mi-2 已于 2026-08-24 按 QA 复签 A-4 结案：端点下线，正式路径定死 `DELETE /pet/:id`（软删语义），见 §3 与 §15.1**；`harness.*` 移出 `src/main`（mi-3）；生产 CORS 按域收敛（mi-4）；死方法/死端点接线或标 TODO（mi-5）。

**修复后**：由 QA 按 `ACCEPTANCE.md` TC-01~13（真后端模式）+ 本节逐条复审，Blocker=0 且 Major=0 方可放行。

### 14.1 跨接口契约铁律（QA 第二轮 2026-08-04 提炼 · 防同类错位再逃逸）
> 第二轮复测发现两处**同源**漏网：亲友 reels 时间字段(M-7)、明信片墙信封(M-8)。据此固化两条**逐端点必扫**的铁律：
1. **所有列表接口一律 `{items,nextCursor}` 完整信封**（含 postcards；nextCursor 可为 null），三层一致：后端返信封、前端 `http.ts` 取 `.items`、mock 同形。
2. **所有毫秒时间戳由前端统一映射为展示串**：后端只下发 `createdAt/lastActive`(ms number)，前端在 `http.ts`（或纯映射函数）统一转相对时间；**禁止**后端下发展示串、也禁止前端漏映射。
> 落地要求：新增/改动任一列表或含时间戳的接口时，必须补一条前端映射单测 + 后端信封断言；QA 复审逐端点扫这两条。

---

## 15. 合规 P0 契约（导出 / 删除 / 授权账本 / 审计）

> **新增 2026-08-24**，补 QA 复签必补项 **C-5**（`qa/QA-REVIEW-compliance-p0-20260824.md` U-5.1~U-5.4、U-5.3）。
> **产品规格**：`SPEC-trust-and-compliance.md §CM-G1/§CM-G3/§CM-G0/§CM-G0S`。**验收**：`ACCEPTANCE.md §1E`。
> **本节所有列表端点遵 §14.1 铁律**：一律 `{ items, nextCursor }` 完整信封，`nextCursor` 可为 `null`；所有时间为**毫秒时间戳（number）**，前端统一映射展示串。

### 15.1 删除（软删）

#### DELETE /pet/:id — 移除回忆集（**语义 = 软删置位**）
- 入参：路径 `:id`；body `{ "reason"?: "<可选，用户填写的原因>" }`
- 出参：`{ "ok": true, "deletedAt": <ms> }`
- 语义（`SPEC G0-1` / `DECISIONS CM-D1`）：置 `deletedAt / deletedBy / deleteReason`，**不删任何数据行、不做级联清理**；关联互动 / 明信片 / 回声一并转为不可见。
- **归属校验**：非 owner 一律 `403`；**共同守护者也不能删**（`DECISIONS D11`：删除/抹除只归原拥有者）。
- **不提供** `?mode=hard`。硬删能力见 `SPEC G0-2` 配置开关，本期不对外暴露。
- 单条内容的移除沿用各自端点（如 `DELETE /cards/:id`，见 `SPEC-publish-and-ops §1.6`），语义同为软删置位。

#### 软删后的读行为（**所有端点统一**）
| 场景 | 约定 |
|---|---|
| 列表端点 | 目标 `id` **不出现在任何 `items[]`** 中（含 owner 自己的列表，`CM-D11`） |
| 详情端点 | 统一返回 **`404`**（不是 `410`）——对外不暴露"这里曾经有过东西"，前端按普通"内容不存在"兜底文案处理，不需要第二套文案 |
| 素材下发 | 原签名 URL **立即失效** |
| 一致性上限 | 从置位到各视图不可见 **≤ 5 秒**（`SPEC §CM-G0S S-1`） |

### 15.2 导出

#### POST /export — 发起导出
- 入参：`{ "petId": "...", "scope": "all" }`
- 出参：`{ "jobId", "status": "queued", "createdAt" }`
- **限流（`SPEC §CM-G0S S-5`）**：每账号**每日 3 次**（可配 `ECHO_EXPORT_DAILY_LIMIT`，默认 3）、**并发 1**（已有进行中任务再发起返 `3xxx` 业务错误 + 温柔文案）。超限**不静默失败**，返回可读原因。
- **需已绑定身份**（`SPEC-security §2.1` S1′：导出是批量数据出口，纯游客不可）。

#### GET /export/:id — 查状态 + 拿下载链接
- 出参：`{ "jobId", "status": "queued|running|ready|expired|failed", "downloadUrl"?: "<签名URL>", "expiresAt"?: <ms>, "failReason"?: "..." }`
- **越权必拒**：`jobId` 不属于当前账号一律 `403`（防猜 jobId 拿别人的包）。
- **链接时效：24 小时**（`expiresAt = readyAt + 24h`），走 CM-G4 签名 URL。过期后 `status=expired`，`downloadUrl` 不再下发，前端给温柔文案（"这个链接已经过期了，重新导出一次吧"），**不是报错脸**。
- **导出临时文件**：`expired` 后由清理任务物理删除。这**不违反 G0-1** —— 导出临时文件是**派生的临时产物、非业务数据**，已显式登记在 CR 红线白名单（`SPEC §CM-G0S S-9` 第 6 项）。

#### GET /export — 我的导出记录（列表）
- 出参：`{ "items": [ { "jobId","status","scope","createdAt","expiresAt" } ], "nextCursor": null }`

#### 导出包结构（`manifest.json` schema，解 U-5.1）
```
echo-export-<petId>-<yyyyMMdd>.zip
├── manifest.json           # 结构索引（下方 schema）
├── media/                  # 图片/音视频原件，文件名 = <resourceId>.<ext>
├── records.json            # 记录流
├── echoes.json             # 回声/近况
├── lifebook.json           # 生命之书
├── postcards.json          # 明信片
└── README.txt              # 一页大白话说明（这是什么、怎么看、包含什么不包含什么）
```
- **编码 UTF-8**（无 BOM）；**时间一律 ISO-8601 带时区**（如 `2026-08-24T14:18:00+08:00`）——注意这是**导出包内**的约定，与接口传输用毫秒时间戳不冲突。
- `manifest.json` **最小字段集**（缺一即 Fail）：
```json
{
  "manifestVersion": "1.0",
  "exportedAt": "2026-08-24T14:18:00+08:00",
  "account": { "accountId": "...", "nickname": "..." },
  "pet": { "petId": "...", "name": "...", "createdAt": "..." },
  "scope": "all",
  "excluded": { "removedContent": true, "note": "已移除（软删）的内容不包含在本导出包中" },
  "counts": { "media": 42, "records": 18, "echoes": 30, "postcards": 6, "lifebookPages": 4 },
  "files": [ { "path": "media/xxx.jpg", "type": "image/jpeg", "sourceType": "portrait", "sha256": "..." } ]
}
```
- **`excluded.removedContent` 恒为 `true`**：导出包**不含已软删内容**（`DECISIONS CM-D12`）。`README.txt` 与 C 端导出说明须同样写明，避免用户以为移除的东西还能从包里捞回来。

### 15.3 授权账本（「我」页查看 + 撤回）

> 补 `SPEC CM-G3` 字段表里缺的端点（G0-5 说「我」页有入口，但契约里没有）。

#### GET /consents — 我的授权列表
- 出参（**遵 §14.1 信封**）：
```json
{ "items": [
    { "capability": "识别|定妆生成|近况生成|向量检索|训练",
      "group": "usage|vector|training",
      "granted": true, "grantedAt": 1756000000000, "revokedAt": null,
      "source": "onboarding|settings|supplement", "version": "1.0",
      "separatelyRevocable": true }
  ], "nextCursor": null }
```
- `group` 决定「我」页的呈现分块（`DECISIONS CM-D7/CM-D10`）：
  | group | 含哪些 | 呈现 |
  |---|---|---|
  | `usage` | 识别 / 定妆生成 / 近况生成 | **打包一次同意**（服务所必需），三项同进同出 |
  | `vector` | 向量检索 | **单列一行**，随使用类明示告知，但**可单独关闭** |
  | `training` | 训练 | **独立 opt-in、默认关**，与 `usage` 视觉分块、不同勾选框 |

#### GET /consents/notice — 授权告知全文
- 出参：`{ "version": "1.0", "sections": [ { "capability", "whatWeProcess", "whatFor", "storage", "retention" } ], "necessityStatement": "...", "updatedAt": <ms> }`
- 建档时与「我」页**取同一份**（`SPEC §CM-G0S S-3` 要件 9：建档后能查到**同一份**告知全文）。

#### POST /consents/revoke — 撤回某一项
- 入参：`{ "capability": "近况生成" }`
- 出参：`{ "ok": true, "revokedAt": <ms>, "affected": { "stopFutureUse": true, "existingContentKept": true } }`
- 语义（`SPEC G0-4` / PIPL 15）：自撤回起停止使用与辅助生成；**撤回前已产生的产物不清除、已训练进权重的不回滚**。
- 撤回 `training` 时**同步剔除训练语料库中的对应样本**；撤回任一项后，该素材及其**全部派生物**退出对应能力（`SPEC G0-10 ②`）。
- 前端须先给温柔确认，说清"以后不再用了，但已经做出来的东西还留着"（文案过 COPY-GUIDE）。

#### 未授权时的调用行为（补 U-5.8 / C-6）
- 未授权能力对应的生成端点**不触发任何 AI 调用**，返回业务错误码 **`3401`**：
  `{ "code": 3401, "msg": "<温柔说明，过词表>", "detail": "consent_required", "data": { "capability": "近况生成", "actionHint": { "text": "去打开", "routeTo": "/me/consents" } } }`
- 前端据此渲染**温柔提示 + 「去打开」入口**，`routeTo` 直达「我」页对应项；**不卡死、不报错脸、不静默无反应**。文案与交互要求见 `SPEC §CM-G0S S-6`。

### 15.4 审计表 `t_audit_log`（补 U-5.4）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | bigint PK | |
| `actor` | text | 操作者 id（用户 / 后台运营 / 系统任务） |
| `actorType` | text | `user` / `staff` / `system`。🆕 🔴 **不是 `t_resonance.actorType`，见下方辨异** |
| `action` | text | `export.create` / `export.download` / `content.softDelete` / `content.restore` / `consent.grant` / `consent.revoke` |
| `targetType` | text | `pet` / `card` / `record` / `material` / `consent` |
| `targetId` | text | |
| `scope` | jsonb | 影响范围（如导出的 `petId` 与条目数、删除波及的关联项） |
| `ts` | timestamptz | |
| `ip` | text? | 可空 |
| `reviewerId` | text? | **双人复核的第二人**（后台恢复必填，见 15.5） |

- **保留期 ≥ 3 年**（合规追溯窗口），期满按 `G0-1` 处置（置软删位，不物理删除）。
- **C 端零暴露**：无任何 C 端路由读取本表（守 `D4`/`CM-G5`「数据只后台可见」）。验收断言见 `ACCEPTANCE §1E TC-EXP-07`。
- 「谁 / 何时 / 对哪些内容 / 做了什么」四要素 = `actor` / `ts` / `targetType+targetId+scope` / `action`，**一样不缺**。

> 🆕 🔴 **`actorType` 辨异（2026-08-25 · `DECISIONS §G⁗⁗⁗⁗″ MOD6`）**
>
> 🔴 **项目里有两个 `actorType`，取值域不同，严禁互相套用：**
>
> | | 本表 `t_audit_log.actorType` | `t_resonance.actorType` |
> |---|---|---|
> | 取值 | `user` / **`staff`** / `system` | `user` / **`ops`** / `system` |
> | 记的是 | 谁做了这次后台或系统操作 | 这条回声是谁产生的 |
> | 约束 | 本表字段说明 | 🔴 **CHECK + 触发器**（从账号 `accountType` 快照、一经写入禁止 UPDATE）|
>
> 🔴 **`t_resonance.actorType` 是四个指标的判据**：北极星分子（`='user'`）· 兜底回应触发率（`IN ('ops','system')`）· 🔴 **官方号响应率只认 `ops` 不认 `system`**（系统自动回复不算「有人读了」）· 深共鸣率。
> ⚠️ 🔴 **把本表的 `staff` 套过去会怎样**：`CHECK` 约束直接拒绝写入；而若顺手放宽约束去「修好」它，🔴 **四个指标的 SQL 里写的是字面量 `'ops'`，改完匹配不到任何行 —— 指标不会报错，只会变成 0**，而「兜底回应触发率恒 0」恰好是规格里「兜底事实上没运行」的告警形态。**一次改名会伪装成一个运营问题。**
> 📌 **两个值域各自保留，不统一。** 若将来确要统一，须同批改 CHECK + `t_account.accountType` + 四个指标 SQL + 两条验收用例 —— 🔴 **那是一次数据迁移，不是一次改名。**

### 15.5 后台恢复（内部端点，非 C 端）

> 对应 `DECISIONS CM-D13`（B-6）：本期交付最小能力。

- `POST /admin/restore` — 入参 `{ "targetType", "targetId", "ticketId", "reviewerId" }`；出参 `{ "ok": true, "restoredAt": <ms> }`
- 实现 = **反置软删位**（`deletedAt = NULL`），原公开状态 / 互动 / 明信片**原样回来**（因为从没被删过，只是不可见）。
- **双人复核**：`reviewerId` 必填且**不得等于发起人**，否则拒绝执行。
- 每次恢复**写 `t_audit_log`**（`action=content.restore`，含 `reviewerId`）。
- 仅后台装配，**生产 C 端不暴露此路由**；需身份校验通过的人工客服工单（`ticketId`）作为前置。

---

## 16. 分享物料契约（分享落地页 meta + 预览图合成）

> **新增 2026-08-25**，补「站外分享的 AI 标识缺口」——此前该缺口无 owner 且无端点落点。
> **产品规格**：`SPEC-trust-and-compliance.md §CM-G0S S-11`（方案倾向 / 微信约束 / 边界红线 / 判定口径 / 职责矩阵 / 阻塞判定）。
> **叠标识的裁定与物料边界**：`TECH-DESIGN-feed-recall-and-exposure.md §3.12`。**部署形态**：`DEPLOY §1.5`。**出入口安全**：`SPEC-security §4.12`。
>
> 🔴 **本节存在的唯一理由**：纯静态 SPA 无法按窗下发不同的 `og:image`（社交平台爬虫**不执行 JS**，抓到的永远是同一份 `index.html`），而站外只有静态图、DOM 角标在那里等于不存在。**meta 渲染与预览图叠标识两件事缺一不可**，故三个端点必须同批交付。

### 16.1 GET /w/:windowId — 分享落地页（**返回 HTML，不是 JSON**）

⚠️ **本端点是全契约唯一的 HTML 端点**，故不在 `/api/v1` 之下、不遵 §0 的 JSON 约定。

- **不需要鉴权**（分享链接要能被未登录用户和爬虫打开）。
- **服务端直出**一份最小 HTML 骨架：
  - `<head>`：注入**该窗各自的** `og:title` / `og:image` / `og:description` / `og:url` / `og:type`，并一并输出 `twitter:card` 系列（微信不读，但对外分享不止微信一处，成本为零）。
  - `<body>`：可见首屏（封面 + 标题 + **DOM 角标**），随后挂载 SPA 接管。
- 🔴 **对爬虫与真人返回同一份 HTML，不做 UA 分流**（不按 `MicroMessenger` 判爬虫）：UA 会漂移、多平台各有抓取 UA，靠白名单必漏一个；且差异化返回属 cloaking。理由见 `S-11 ②` 微信约束第 5 条。

| 情况 | 返回 |
|---|---|
| 窗存在、`visibility=public`、已过审 | `200` + HTML |
| 窗不存在 / **已软删** / `visibility ∈ {private, friends}` / 未过审 | 🔴 **`404`**（与 `S-1 ②` 一致，**不是 410**；且**不得在 meta 里泄露任何内容字段**） |

- 🔴 **软删过滤与可见性过滤在服务端完成**，不得依赖前端。生效上限 **≤5 秒**（`S-1 ③`）。
- **缓存**：`Cache-Control: no-cache`（内容可被作者收回或改判，与 `DEPLOY §1.3` 的 `index.html` 策略一致）。

### 16.2 GET /share/meta/:windowId — 落地页 meta 数据源

供 16.1 的模板渲染使用；独立成端点便于 QA 直接断言取值，无需解析 HTML。

- 出参：
  ```json
  { "code": 0, "data": {
      "windowId": "...", "title": "<≤30 字>", "description": "<≤60 字，过 COPY-GUIDE 词表>",
      "ogImageUrl": "https://.../share/og/....png",
      "aiGenerated": true, "updatedAt": 1756... } }
  ```
- `ogImageUrl` **必须是长期有效的公开 HTTPS 绝对 URL**。🔴 **不得使用 `CM-G4` 的限时签名 URL**——签名过期后微信侧缩略图直接失效，且微信缓存拿不到。这不违反 `CM-G4`：预览图是**我方合成的派生物料、不是用户素材**（判定走 `TECH-DESIGN §3.12.1` C1–C3）。
- 不存在 / 软删 / 非公开：同 16.1 返回 `404`。

### 16.3 POST /share/og-image — 合成分享预览图（叠 AI 标识）

**前端已确认可以把 `cover.aiGenerated` 一并传给本端点**，服务端据此决定是否叠标识。

- 入参：
  ```json
  { "windowId": "...", "cover": { "key": "<封面对象存储 key>", "aiGenerated": true },
    "title": "<≤30 字>", "templateVersion": "v1" }
  ```
- 出参：`{ "code": 0, "data": { "url": "https://.../share/og/<cardId>-<hash>.png", "aiLabeled": true, "cached": false } }`

| # | 契约约束 |
|---|---|
| 1 | 🔴 **服务端不自行推断内容含不含 AI 成分**，只认入参的 `cover.aiGenerated`。判定口径的唯一出处是 `SPEC-recommendation-ranking §5.3.2`，**本契约不另立标准** |
| 2 | 🔴 **`aiGenerated` 缺省 / `null` 一律按 `true` 处理并叠标识**。漏叠是合规事故，多叠只是多一行小字。**不得把缺省当 `false`** |
| 3 | `aiGenerated=false` 的窗**不叠**；两种预览图走**同一套模板、只差这一行**（`§3.12.4`） |
| 4 | 叠加文案与前端角标**共用同一份文案常量**（「该内容由 AI 生成」，`COPY-GUIDE §2.4`），不另起一套——否则合规核查会查出两个口径 |
| 5 | 缓存键 = `(windowId, aiGenerated, templateVersion)`；🔴 `aiGenerated` **被审核改判时必须失效重生成**（第三方已缓存的旧图属**已知不可控残留**，见 `§3.12.4`） |
| 6 | 🔴 **派生管线不得丢弃隐式标识元数据**，合成后须**重新写入** `S-8 ②` 的四项字段 + AI 标记（对应 `TC-AIP-05`） |
| 7 | 🔴 **只叠「AI 标识」这一个语义**：不得夹带 logo、水印、二维码、作者 ID、追踪码（红线 `L3`） |

#### 🔴 边界（写死，防后人扩大范围）

> **只有分享预览图叠标识。站内原图与用户素材一律不动。**（`TECH-DESIGN §3.12` 裁定原文）

- 本端点**只读**封面素材、**只写**一张新的合成图；🔴 **绝不回写、覆盖或以任何方式修改用户的原始素材字节**（原图 / 压缩图 / 缩略图 / 裁剪图）。
- 🔴 **16.1 落地页首屏的封面图同样不叠标识**（红线 `L4`）——它是用户素材的呈现，标识由该页的 **DOM 角标**承担。
- 「导出 / 下载」产出的文件**永远不叠**（红线 `L2`）。

#### 滥用防护

- 本端点**不对 C 端开放为通用出图能力**：只接受**已存在且公开**的 `windowId`，其余一律 `404`；`title` / `cover` 与该窗库内值不一致时以**库内值为准**（不信任前端传入的展示内容）。防止被当免费图床或伪造预览图。限流与出入口登记见 `SPEC-security §4.12`。

### 16.4 前端配合项

| 方 | 项 |
|---|---|
| 前端 | ① 出图时传 `cover.aiGenerated`（已确认可行）；② 落地页首屏复用既有 `AiGeneratedBadge` 组件；③ 微信内 JS-SDK `updateAppMessageShareData` 的转发用图**指向 16.3 产出的同一张预览图**（JS-SDK 管"已在微信内打开后再转发"，meta 管"链接首次被抓取"，**两条互补、不可互相替代**；JS-SDK 依赖公众号认证等运营前置，见 `S-11` **P-6**） |
| 后端 | 三个端点同批交付；🔴 **不得按"先做一个、另一个后补"排期**（`S-11 ①`） |

### 16.5 验收

`SPEC-trust-and-compliance §CM-G2` 的 **`TC-AIP-06/07`**；完整 10 条判据见 **`§CM-G0S S-11 ⑦`**，在 `ACCEPTANCE §1E` 补齐用例正文前**以 S-11 ⑦ 为验收依据**。

---

## 17. 审核 / 申诉 / 举报契约（补规格缺口 B12）

> **新增 2026-08-25**。来源：`PRODUCT-MINDMAP.md §6.2a` 台账 **B12** —— 判定为**规格缺口而非口径冲突**：`SPEC-admin-console §0.2` 指出「审核队列 REST 路径：`SPEC-publish-and-ops §2` **只定义了规则与表，没有定义任何 API 路径**（只有 §3.5 的 `/ops/topics`、`/ops/curations`）」，研发照现状开工只能自行发挥。
>
> **分工（按本文档「前后端并行的唯一真源」定位划线，不两处各写一套）**：
> | 谁写什么 | 落点 |
> |---|---|
> | **端点契约**（路径 / 方法 / 入参 / 出参 / 错误码 / 鉴权 / 幂等） | 🔴 **本节，唯一真源** |
> | **流程与状态机**（三档风险分级 / 谁能做哪个动作 / SLA / 状态迁移合法性） | `SPEC-publish-and-ops §2`（该节已加指针指向本节） |
> | **后台承载**（队列 tab、版面、角色权限链、审计取舍） | `SPEC-admin-console §4.3` / `§6.4` |
> | **数据表** | `t_moderation`（`SPEC-publish-and-ops §2.6`）· `t_card_visibility_log`（同 `§1.8.5`）· `t_audit_log`（本文档 §15.4） |
>
> **路径命名沿用 `SPEC-admin-console §6.4` 已提出的四条**（`GET /admin/moderation/queue`、`POST /admin/moderation/:id/handle`、`GET /admin/reports`、`POST /admin/appeals/:id/handle`），本节只做契约化补齐，**不改名、不另起一套**。
>
> **本节所有列表端点遵 §14.1 铁律**：一律 `{ items, nextCursor }` 完整信封；所有时间为**毫秒时间戳（number）**。

### 17.0 🔴 三条必须先说的既有裁定约束

补这些端点时**最容易踩**的三处，全部与已定裁定直接相关：

| # | 约束 | 依据 |
|---|---|---|
| **M-A** 🔴 | **过审动作必须在同一事务内写 `t_memory_card.reviewedAt`**，且**只在 `reviewedAt IS NULL` 时写**。它是北极星「被接住的发布率」7 天窗口的**起点**——不是 `publishedAt`。编辑后复审、下架再上架**一律不刷新**（否则作者靠反复微编辑就能给自己续窗口期），数据库触发器会直接拒绝改写 | `SPEC-publish-and-ops §1.8.3` 写入时机表 + 禁改触发器 · `SPEC-admin-console §2.1.1 ①` · `DECISIONS RK-D` |
| **M-B** 🔴 | **审核动作一律不得写、不得改 `originType`。** 该字段在**发布时**由发布路径显式落库（无默认值，`CHECK IN ('user','official')`），官方号内容**整条不进北极星分母**（正向白名单 `originType='user'`，🔴 不是"只从分子剔掉"）。审核台把一张卡改判来源，等于追溯性改写历史北极星 | `SPEC-publish-and-ops §1.8.3b` · `SPEC-recommendation-ranking §11.1` / `RK35 ②` · `SPEC-admin-console §2.1.1` 锁二 |
| **M-C** 🔴 | **每一次审核状态变更都要落两处流水，🔴 且与状态变更在同一事务内**：① `t_card_visibility_log` 一行（`changedRole='moderator'`，同时记 `visibility` 与 `status` 迁移——只记 `visibility` 分不出「作者撤回」与「运营下架」）；② `t_audit_log` 一行（新增 `action` 见 §17.5）。**留痕含快照**（谁 / 何时 / 动作 / 理由码 / 快照）。<br>🔴 **「每一次」= 全部动作，不只 `approve`**：`reject` / `takedown` / `restore` / `escalate` / 申诉 `uphold`/`overturn` 同样适用。分事务写就会出现「状态变了、流水没留」的**不可追溯窗口**，而流水表只追加、事后修不回来 | `SPEC-publish-and-ops §1.8.5`（只追加、不修改、不删除）+ `§2.2.2` 第 3 条 + `§2.4` 留痕要求 · 本文档 §15.4 · `DECISIONS §G⁗⁗⁗′ MOD1 ③` |

### 17.1 运营侧 · 审核队列（`/api/v1/admin/**`，独立鉴权链）

> 鉴权、角色与错误回显沿 `SPEC-admin-console §6.4`：后台**可以**回显技术细节（与 C 端相反）。角色权限见 `SPEC-publish-and-ops §2.5`（审核员 / 审核主管 / 只读运营）。

#### GET /admin/moderation/queue — 审核队列

- 入参（query）：`?tab=pending|blocked|appealing|handled` · `?risk=low|mid|high` · `?cursor=&limit=`
- 出参：
```json
{ "code": 0, "data": { "items": [
    { "moderationId": "...", "cardId": "...", "submitBy": "...",
      "state": "pending", "autoRiskLevel": "mid", "autoSignals": { "wordlist": ["..."], "minorSuspect": false },
      "cardSnapshot": { "title": "...", "body": "...", "coverUrl": "...", "topicIds": ["..."] },
      "originType": "user", "assistedByOps": false,
      "createdAt": 1756000000000, "slaDueAt": 1756014400000, "slaBreached": false }
  ], "nextCursor": null } }
```
- 默认排序 = **待处理 + 高风险优先**（`SPEC-admin-console §4.3`）。
- `slaDueAt` 由服务端按 `SPEC-publish-and-ops §2.4` 算（人工队列 ≤4h、高风险 ≤1h），**前端不自算**。
- `originType` 只读下发，供审核员知晓这是官方号内容；🔴 **不提供修改入口**（M-B）。

#### GET /admin/moderation/:id — 单条详情

- 出参：队列 item 全字段 + `note` + `handledBy` + `handledAt` + `reasonCode` + `appeal`（若有）+ `history[]`（该卡历次处置，取自 `t_card_visibility_log`）。

#### POST /admin/moderation/:id/handle — 人工处置

- 入参：
```json
{ "action": "approve|reject|takedown|escalate",
  "reasonCode": "<驳回/下架必填，取自理由码字典>",
  "note": "<可选，内部备注>" }
```
- 出参：`{ "code": 0, "data": { "moderationId": "...", "cardId": "...", "state": "approved", "cardStatus": "public", "reviewedAt": 1756000000000, "handledAt": 1756000000000 } }`

| `action` | 卡 `status` 迁移 | 是否写 `reviewedAt` | 备注 |
|---|---|---|---|
| `approve` | `pending → public` | ✅ **写**（🔴 仅当 `reviewedAt IS NULL`，M-A） | 出参回显 `reviewedAt`，便于 QA 直接断言 |
| `reject` | `pending → rejected` | ❌ 不写 | `reasonCode` 必填，随驳回**回给作者**（`TC-MOD-03`） |
| `takedown` | `public → takendown` | ❌ **不写、不清空** | 已闭合窗口的历史数字不受影响 |
| `escalate` | 状态不变，标记复核 | ❌ 不写 | 仅审核主管可见的升级队列 |

- **幂等**：同一 `moderationId` 重复提交同一 `action` 返回当前状态、不重复写流水；提交与当前状态不兼容的 `action` 返回 `3xxx`（如已 `takendown` 再 `approve`）。合法迁移以 `SPEC-publish-and-ops §2.2` 状态机为准，**服务端校验，不信任前端**。
- **权限**：`reject`/`takedown` 需审核员及以上；`escalate` 结果只进主管队列；只读运营调用一律 `403`。
- 🔴 **副作用**：`approve` 之外的三个动作都会让卡从共鸣厅消失，**生效上限 ≤5 秒**（`SPEC-trust-and-compliance §CM-G0S S-1`，同 `TC-CARD-03`）。

#### POST /admin/appeals/:id/handle — 申诉处置

- 入参：`{ "action": "uphold|overturn", "reasonCode": "...", "note"?: "..." }`
  - `uphold` = 维持原处置（卡保持 `rejected`/`takendown`）；`overturn` = 撤销原处置（回 `pending` 重新走人工，**不直接放行**）。
- 出参：`{ "code": 0, "data": { "appealId": "...", "cardId": "...", "state": "handled", "cardStatus": "pending", "handledAt": <ms> } }`
- **权限**：🔴 **仅审核主管**（`SPEC-publish-and-ops §2.5`：处理申诉是主管权限）。
- 🔴 `overturn` **不写 `reviewedAt`** —— 它把卡送回 `pending`，真正过审时才由 `approve` 写（且仍受"只写一次"约束）。

#### GET /admin/reports — 举报列表

- 入参（query）：`?status=open|handled` · `?cardId=` · `?cursor=&limit=`
- 出参：`{ "code": 0, "data": { "items": [ { "reportId","cardId","reporterId","reasonCode","note","status","createdAt","handledAt" } ], "nextCursor": null } }`
- 用途：支撑 `SPEC-publish-and-ops §4` 的**举报率**指标与人工核查入口。
- ⚠️ **本节只补运营侧的读取端点。** C 端**提交**举报的端点（如 `POST /cards/:id/report`）与举报理由码字典、举报表结构**在任何现行规格里都没有定义**，属**另一处缺口**，本轮**不代拟**——见 §17.6。

#### PATCH /admin/moderation/settings — 先发后审 / 先审后发开关

- 入参：`{ "mode": "review_first|publish_first", "scope"?: { "riskLevel": "low", "authorTier": "veteran" } }`
- 出参：`{ "code": 0, "data": { "mode": "review_first", "updatedAt": <ms>, "updatedBy": "..." } }`
- **为什么必须有这个端点**：`TC-MOD-05` 的过标准是「先发后审/先审后发开关**后台可切，无需发版**」。没有端点，这条验收无法通过。默认 `review_first`（种子期先审后发，`SPEC-publish-and-ops §2.2`）。
- **权限**：审核主管及以上。每次变更**写 `t_audit_log`**（`action=moderation.settings.update`）。

### 17.2 作者侧 · 审核结果与申诉（C 端，沿 §0 通用约定）

> 🔴 **这两个端点是 `SPEC-admin-console §6.4` 那份清单里缺掉的一半。** 它只列了运营侧四条，但 `SPEC-publish-and-ops §2.2` 状态机里有**作者的两个动作**（看驳回理由、申诉一次）——没有 C 端端点，`TC-MOD-03`「驳回带理由码回作者；作者可申诉一次」无法实现。

#### GET /cards/:id/moderation — 我的卡的审核状态

- **归属校验**：非 owner 一律 `403`。
- 出参：
```json
{ "code": 0, "data": {
    "cardId": "...", "status": "rejected",
    "reasonCode": "sensitive_portrait", "reasonText": "<温柔文案，过 COPY-GUIDE 词表>",
    "appealable": true, "appealUsed": false, "appeal": null,
    "reviewedAt": null, "handledAt": 1756000000000 } }
```
- 🔴 **对作者只下发 `reasonCode` 对应的温柔文案**，不下发 `autoSignals`、`note`、审核员身份（后台内部信息不出 C 端，守 `D4` / `CM-G5`）。
- `appealable=false` 的两种情形：已申诉过（`appealUsed=true`）或当前状态不可申诉。
- 🔴 **`appealUsed` 的唯一判据 = `t_moderation.appealAt IS NOT NULL`**（`DECISIONS §G⁗⁗⁗′ MOD2` · `SPEC-publish-and-ops §2.6.1`）。它是**服务端由该时间戳派生的布尔**，🔴 **不得由计数列或 `appealCount` 之类的字段推导，也不得新增这类字段**——计数列可被改小从而绕过限制，时间戳一旦写入即为不可逆事实。<br>🔴 这是「用什么字段」的裁定，不是实现细节，**不得在实现时改回计数列**。

#### POST /cards/:id/appeal — 申诉（🔴 一张卡一生只有一次）

- 入参：`{ "text": "<≤200 字，过 COPY-GUIDE 词表>" }`
- 出参：`{ "code": 0, "data": { "appealId": "...", "state": "appealing", "createdAt": <ms> } }`
- **幂等与上限**：🔴 **一张卡一生只允许申诉一次**（`SPEC-publish-and-ops §2.2`：「作者：对驳回/下架可**申诉一次**」）。**判据 = `t_moderation.appealAt IS NOT NULL`**，🔴 **刻意不设计数列**（`MOD2`）。第二次调用返回 `3xxx` + 温柔文案（不是 `409` 裸错），`detail: "appeal_already_used"`。<br>⚠️ `overturn` 把卡送回 `pending` 后**不重置 `appealAt`** —— 撤销原处置不等于退还申诉机会，否则「一生一次」不成立（`SPEC-publish-and-ops §2.6.1`：`appealAt` 一经写入不可变更）。
- **前置**：卡当前状态 ∈ `{rejected, takendown}`，且为 owner 本人。其余一律拒绝。
- 提交后卡进 `appealing` 队列（`GET /admin/moderation/queue?tab=appealing`）。

### 17.3 错误码

沿 §0 错误码段，本节新增业务码（`3xxx`）：

| 码 | 含义 | detail |
|---|---|---|
| `3410` | 申诉机会已用完（一张卡只能申诉一次） | `appeal_already_used` |
| `3411` | 当前状态不可申诉 | `appeal_not_applicable` |
| `3412` | 审核动作与当前状态不兼容（非法状态迁移） | `moderation_state_conflict` |
| `3413` | 驳回 / 下架未带 `reasonCode` | `reason_code_required` |

### 17.4 前端配合项

| 方 | 项 |
|---|---|
| 前端（C 端） | ① 卡列表 `GET /cards/mine` 上对 `rejected`/`takendown` 的卡露出「看看为什么」入口 → `GET /cards/:id/moderation`；② 申诉入口**只在 `appealable=true` 时出现**，不要出现了再报错；③ `pending` 状态给"正在看，通常几小时内"的克制提示，🔴 **不显示排队位次、不倒计时**（会制造焦虑，违反调性红线） |
| 前端（后台） | 队列四 tab 直接对应 `?tab=`；SLA 超时用服务端下发的 `slaBreached`，**不在前端算时间差** |
| 后端 | 🔴 `approve` 写 `reviewedAt` 与写两条流水**必须同一事务**（M-A + M-C）。分开写就会出现"卡已公开但北极星窗口没起算"或"公开了但没留痕"，两者都是事后无法修的 |

### 17.5 §15.4 `t_audit_log` 的 `action` 增量

在既有取值之外新增六个（其余字段沿用 §15.4，**表结构不变**）：

| `action` | 触发时机 | `targetType` |
|---|---|---|
| `moderation.approve` | `POST /admin/moderation/:id/handle` action=approve | `card` |
| `moderation.reject` | 同上 action=reject | `card` |
| `moderation.takedown` | 同上 action=takedown | `card` |
| `moderation.escalate` | 同上 action=escalate | `card` |
| `moderation.appeal` | `POST /cards/:id/appeal`（作者发起，`actorType=user`） | `card` |
| `moderation.settings.update` | `PATCH /admin/moderation/settings` | `config` |

- `scope`（jsonb）记 `{ moderationId, fromStatus, toStatus, reasonCode, autoRiskLevel }`，便于事后还原一次处置的全貌。
- 保留期与 C 端零暴露约束沿 §15.4 不变。

### 17.6 ⚠️ 本节明确没有补的（不代拟，留待派单）

| 缺口 | 为什么不在本轮补 |
|---|---|
| **C 端举报提交端点**（`POST /cards/:id/report` 之类）+ 举报表结构 + 举报理由码字典 | `SPEC-publish-and-ops §4` 只把「举报率」列为指标、把"举报表"当既有物提了一句，**举报流程本身在任何现行规格里都没有定义**（谁能举报、游客能不能举报、重复举报怎么算、举报后是否立即降权）。这些是**产品决策**，不是契约细节，不能由契约文档反向定义。本节只补了运营侧的 `GET /admin/reports` 读取端点，因为 `SPEC-admin-console §6.4` 已经点名要它 |
| **理由码字典**（`reasonCode` 的取值集合） | `SPEC-publish-and-ops §2.3` 只写「驳回(选理由码)」，未给码表。码表既要过 `COPY-GUIDE`（要回给作者看），又牵涉合规分类，需产品与合规一并给 |
| **`/ops/*` → `/admin/*` 前缀迁移** | `SPEC-admin-console §6.4` 建议把 `SPEC-publish-and-ops §3.5` 的 `/ops/topics`、`/ops/curations` 统一迁到 `/admin/*`，并注明「迁移需回改该文件（**待 QA 复签后执行**）」。🔴 **本轮不执行该迁移**——它有明确的前置条件尚未满足。本节新增的审核端点**直接落在 `/admin/*` 下**，不制造第二处 `/ops/*` |

---

## 18. ❄️ 冻结项 · 线上出参侧的「可反解的量」（`C-8` / `C-9` / `C-10`）

> 2026-08-27 · 前端视觉线登记。🔴 **状态一律是「冻结·待系统切分落定后处理」，不是「待办」，也不是「已知问题」。**
> 产品负责人已下令冻结这一批，**看到这一节不要开工**；要动之前先确认冻结已解除。
>
> 三条为什么放在一起：**它们是同一类** —— 都在**网线侧**，都不是「屏幕上画了什么」的问题。
> 分开处理没有意义：`H-8` 的面孔墙阈值只挡住了眼睛，**网线不收口等于没挡**。
>
> 判准与排查方法见 `docs/visual/CHECKLIST-number-leak.md`。
>
> 🔴 **解冻的人先看这一句：这一批里每一条的修复，都会让本仓库现存的断言（甚至一条现存契约条款）变红。**
> **那是正确的信号，不是回归。** 各格末尾有「解冻时会撞什么」，写明撞哪一条、以及**红了之后最容易做错什么**。
> ⚠️ 这些断言不归本线改，**也不在冻结期间改**；这里只登记，免得解冻的人把自己的修复当成改坏了。

### 18.1 `C-8` —— `GET /windows/:windowId/remember` 仍下发 `faces[]`

**是什么。** 出参里 `faces[]` 是一排真实头像。前端已按裁定 `H-8` 加了阈值：**≤5 张照常渲染，>5 张不画那一排、只留光晕**（`DetailScreen.tsx` 的 `FACE_WALL_MAX`）。但**服务端仍然把整批头像发下来**。

**后果。** 🔴 **渲染层不给 ≠ 数据没发。** 超过阈值的窗，前端一张脸都不画，而 `faces.length` 就在响应体里——打开控制台数一下就是精确人数。**阈值只挡住了眼睛。**

**状态。** ❄️ **冻结·待系统切分落定后处理。** 解冻后要定的是：超过阈值时还传不传；若传，是不是要截成恒定条数（⚠️ 那等于在数据上撒谎，与诚实红线冲突，需要产品先判）。

#### 🔴 解冻时会撞什么（`C-8`）

**① 撞的不只是测试，是本文自己的一条现存条款。** `M-3` 要求 `rememberWall` **必含 `faces`**，并有三处断言焊死：

| 位置 | 断言 | 焊死了什么 |
| --- | --- | --- |
| `EchoApiTest` `windowDetailRememberWallKeys`（约 `:432-440`） | `containsKeys("warmthLevel", "faces")`、`faces` `isNotEmpty()` | 键必在、且非空 |
| `WindowVisibilityTrimTest` `facesAreOwnerOnlyAndNeverCarryAccountId`（约 `:298-308`） | 非本人裁成**空数组**（键还在）、本人侧 `isNotEmpty()` | 同上，且写明「空数组与『还没人记得』不可区分」 |
| `EchoApiTest` `rememberWallHasNoExactCount`（约 `:286`） | `containsKeys("warmthLevel", "faces", "meRemembered")` | 同上 |

🔴 **所以「超过阈值就不发 `faces`」这条路，第一步不是改服务端，是改 `M-3` 条款** —— 而 `M-3` 是拍过板的，要产品重新判。⚠️ 直接让服务端不发，会同时违反 `M-3` 并让三处断言变红，**看起来像三处回归，实际上是一处未经重判的条款冲突。**

**② 🟢 顺带说明：`WindowVisibilityTrimTest` 的「裁成空数组而不是删键」是做对了的。** 空数组与「还没人记得」不可区分 —— 这正是 `CHECKLIST-number-leak.md` §三 的正面模板形态（**让那个量不在数据里，而不是禁止读它**）。**收口 `C-8` 时应当沿用这个形态，不要改成删键**：删键会让「被裁剪」和「没有人」重新可区分。

**③ 最容易犯的错。** 见 §18.3 那一格末尾同名小节 —— **它对本格同样成立，而且本格更险**：这里变红的三处里有一处（`WindowVisibilityTrimTest`）是**真守卫**，不能跟着一起改掉。

### 18.2 `C-9` —— `GET /pet/me/insights` 的三个字段现在都「传了但前端不据以显示数值」

**是什么。** 现出参 `{ seenCount, rememberFacesCount, flowersReceived }`。前端 `MeScreen` 现状：

| 字段 | 前端怎么用 |
| --- | --- |
| `rememberFacesCount` | **完全不渲染**（裁定 `H-5`，已换成暖光） |
| `seenCount` | **完全不渲染**（层级裁定，见下） |
| `flowersReceived` | 只用来判 `> 0`，**不显示数值**（渲染成「也有人给它带过花」） |

**🔴 后果之一：这是 `C-8` 的同形态问题。** 三个精确数仍在下发，只是前端不画了。

**🔴 后果之二（更要紧，别把这条读成「只是加两个出参」）：按层级口径，`seenCount` 这个字段本身就不该存在。**

产品裁定（2026-08-27）：**「记得」对应到对象身上，「看见」放在卡上面**，且这是**数据层面**的口径，不是展示口径。

`seenCount` 是**跨卡累计**——它把**卡那一层**的量汇总到了**对象那一层**。前端原来把三个数并排成一行、同字号同颜色，只是**把这个出参的形状照抄了一遍**；**根在数据，不在版面。** 所以这条要做的是**删一个、加两个**：

- ❌ **删 `seenCount`。** 它衡量的是曝光；曝光是内容平台的指标，不是一个替人存放思念的地方的指标，而且**多发卡就涨**，主人有动机去刷。
- ➕ **补卡那一层的状态**：前端 mock 现用 `cardCount` / `unseenCardCount`（「你放出去几张卡」「其中还没有人看过几张」），或任何等价的 per-card「有没有被看过」。取这个量而不是「被看了多少次」是有意的：**有上限（自己的卡数）、越小越好、有终点，且多发一张卡只会让它变大**——刷不出好看的结果。
- ⚠️ `cardCount` / `unseenCardCount` **服务端尚未提供**，前端 mock 先给（`echo-h5-proto/src/api/mock.ts`），字段名归服务端线定，前端跟着改。

**状态。** ❄️ **冻结·待系统切分落定后处理。**

#### 🔴 解冻时会撞什么（`C-9`）

**删 `seenCount` 会让 `EchoApiTest.seenCountOnlyInOwnerInsights`（约 `:295-309`）变红**，因为它最后一行断言 owner 侧 `insights.seenCount ≥ 1`。

⚠️ 🔴 **这条测试半对半错，不能整条删掉。** 它由两个断言组成，性质完全不同：

| 行 | 断言 | 判 |
| --- | --- | --- |
| 约 `:304` | 对外窗口详情 `doesNotContainKey("seenCount")` | 🟢 **真守卫，必须留** —— 它守的是「看过数不外泄」，与本条无关 |
| 约 `:308` | owner 侧 `insights.seenCount ≥ 1` | ❌ **把「这个字段必须存在」焊死了**，正是本条要删的东西 |

**最容易犯的错**：看到测试名 `seenCountOnlyInOwnerInsights` 与本条冲突，**整条删掉或整条改写** —— 那会把上半那条真红线一起带走，**而且没有任何东西会变红来提醒你**。🔴 **只改下半。**

### 18.3 `C-10` —— `warmthLevel` 是连续值，一步反解出精确人数

🔴 **本批里最重要的一条。** 它是前面几处的**根**：契约层特意去掉了 `rememberCount`，而这个字段把它原样送了回来。

**是什么。**

```java
// echo-server/src/main/java/com/echo/http/EchoApi.java
private double warmthLevel(int faces) {
    // 记得人数 → 暖光浓度（0..1），饱和函数，绝不对外暴露精确数字
    return Math.min(1.0, faces / 20.0);
}
```

- 出参是**连续 double**，不是三档。**前端渲染成三档，数据不是三档。**
- 🔴 **反解算式：`faces = round(warmthLevel × 20)`。** 在 `warmthLevel < 1`（即人数 < 20）时**严格可逆，精确到人**。
- 🔴 **算式就写在这个仓库里**，反解成本约等于零。

**🔴 后果（这一段是重点，不要只读成「暴露了精确数字」）。**

只写「暴露精确数字」的话，读的人会以为是**主人自己那一屏**的问题。不是。真正的后果是：

1. **每个访客都拿得到，不只是主人。** 该字段出现在 `GET /windows/:windowId`（§6，游客可看）、`GET /users/:id/windows`、`GET /windows/:windowId/remember`（§5）。**任何能看到这扇窗的人，都能算出有多少人记得它。**
2. **可批量枚举，因而可排名。** 广场（`GET /plaza`）虽然自 `OM1` 起发的是卡、卡里不含 `warmthLevel`，但卡带 `petId`；**翻广场收 N 个 `petId`，再逐个打 `GET /windows/:petId`，就能就地排出一份名次**，翻几页就是全站的。⚠️ **也就是说 `D14`（不做全站作者排行榜）在服务端没有被兜住，只是被抬高了成本。**
3. 🔴 **而抬高成本这件事是顺带做到的，不是为这条红线做的。** `OM1` 把广场从「发窗」改成「发卡」是模型重构，它恰好顺手拿掉了「一次请求拿一页 `warmthLevel`」。**没有任何一处在守这条红线**——下一次接口改动可能就把它还回来，而且不会有人察觉。
4. ⚠️ **前端 mock 仍是旧形状**：`echo-h5-proto/src/api/mock.ts` 的 `plaza()` 仍逐窗附 `warmthLevel`。**照着 mock 判契约会判错。**

**🔴 顺带记一条，这条比前三条更该被记住 —— 红线条文自己给了漏洞一张通行证。**

§5 `GET /windows/:windowId/remember` 那行写着：

> **红线**：**不返回精确总数字段、不排名**（前端也不得展示数字）

**这句话字面为真** —— 出参里确实没有整数总数字段。但 `warmthLevel` 就在**同一个出参里、上面一行**，一步反解。

这行条文**描述的是实现（没有整数字段），不是后果（读的人算不出人数）**，所以看见它的人会以为这一处已经检查过了 —— 我自己前两轮就是这么跳过去的。通则见 `docs/COPY-GUARD-CROSSWALK.md` §3：**写红线要写「什么情况下它不生效」，不要写「它做了什么」。**

**状态（2026-08-27 更新）。** 🔴 **范围缩小，但未关闭。**

`P2` 已裁定 —— **暖意对陌生人不出（取②）**。对本条的影响是**一路消失、一路照旧**：

| 那一路 | 状态 |
|---|---|
| **陌生人 / 游客** | 🟢 **自动消失。** 上面「后果」段的第 1、2、3 条（每个访客都拿得到 · 可批量枚举因而可排名 · `D14` 在服务端没被兜住）**随之失效** |
| 🔴 **owner** | ⚠️ **不受影响，`C-10` 不因此关闭。** 它还连着**面孔墙阈值**那条已知代价 —— **低于 5 人时主人仍能数出精确人数**，两条是同一条线上的 |

🔴 **不要把这条写成「`P2` 解决了 `C-10`」。它没有。** 🔴 **也不要因为「陌生人那一路没了」就把本条从冻结表里摘掉** —— 摘掉等于把 owner 那一路一起丢了。

⚠️ 🔴 **落地关键：收起来 = 服务端不下发，不是前端不渲染。**

> **执行条件（不是补充说明）：陌生人视角的响应体里不得包含 `warmthLevel`，也不得包含任何可反解出精确人数的字段。**

`warmthLevel` 只要还出现在给陌生人的响应里，可反解面就**一点没少**（`faces = round(warmthLevel × 20)`，一步到人）。🔴 **本条前两轮漏掉的正是这个形状：屏幕上看不见，网线上全都在。**

⚠️ **这条执行条件的可检测性有明确边界，见下方「怎么发现它被违反」一小节** —— **不要以为写下它就等于守住了。**

**解冻后 owner 那一路可考虑的方向**（**不是方案，只是备选**）：出参改发档位枚举而非连续值；或把饱和分母做成非公开常量（⚠️ 只是抬高成本，不解决）。**仍需产品先判「档位有几档」，那个数还没拍**（`README-home-warmth.md` 待定项⑥）。📌 裁定原文归 `DECISIONS.md`（另一条线在写）；产品侧登记见 `ARCHITECTURE-system-split.md §0.7`（🟢 **该文档产品待裁定项已清零**）。

#### 🔴 怎么发现「陌生人响应体含 `warmthLevel`」被违反 —— 老实说：**一半能，一半不能**

**这一小节存在的理由**：本仓库已经栽过一次「只靠一句注释撑着」（`不许直读 card.visibility` 那条今天已登记为风险）。🔴 **所以执行条件写下来的同时必须回答：它被违反时，有什么东西会响。**

**🟢 能被机械发现的那一半：`warmthLevel` 这个具名字段。**

可行做法是**按视角的出参断言**：以陌生人身份打那几个端点，断言序列化后的响应体里**不含这个键**。⚠️ **但它有三个已知的失效形状，写的时候必须一并处理，否则就是本文档 §18 反复讲的那种假绿：**

| # | 失效形状 | 怎么防 |
|---|---|---|
| 1 | 🔴 **断言恒真**：身份 fixture 其实不是陌生人、或端点返回了 4xx，于是「键不存在」凭空成立 | **先正向断言**这一屏确实渲染出了陌生人该看到的别的东西，再断言 `warmthLevel` 缺席 |
| 2 | 🔴 **断言的是解析后的值不是序列化的体**：`json.get("warmthLevel") == null` 在字段值为 `null` 时也通过，**而 `null` 仍然出现在网线上** | 断言**序列化文本**里不含该键 |
| 3 | 🔴 **只覆盖已知端点**：新增端点默认不在断言范围内，**漏了不会有任何东西变红** | 只有把出参裁剪收敛到**单一裁剪点**才能治本；逐端点断言治不了 |

**🔴 不能被机械发现的那一半，这是本小节真正要说的：**

> **「或任何可反解出精确人数的字段」这半句，没有办法机械检测。**

**因为「可反解」不是字段的机械属性，是一次语义判断。** 举例：将来若有人加一个 `rememberFacesCount`、或一个 `bondRank`、或一个带人数分母的百分比，**它们都不叫 `warmthLevel`，任何针对字段名的检查都不会响**，而反解面一模一样。

🔴 **所以老实的结论是**：具名字段能守住（靠上表那三条防假绿的写法），**「可反解」这个类别守不住** —— 它只能靠**每次新增出参字段时人过一遍**。⚠️ **这正是「只靠一句注释撑着」的形状，本条不假装解决了它，只把它标出来。** 📌 与 `visual/CHECKLIST-number-leak.md` 是同一件事的两端（那份查的是屏幕上漏没漏，这条查的是网线上漏没漏），**两份都不能替代对方。**

#### 🔴 解冻时会撞什么（`C-10`）——**先读完这一小节再动手**

**① 有一条名字里写着「红线」的测试，实际上在守这条红线的反面。**

```java
// echo-server/src/test/java/com/echo/http/EchoApiTest.java · rememberWallHasNoExactCount()（约 :286-289）
assertThat(wall).containsKeys("warmthLevel", "faces", "meRemembered");   // ← 把泄漏面断言成了必须存在
// 红线：不返回精确总数/排名字段
assertThat(wall).doesNotContainKeys("count", "total", "rememberCount", "rank");
```

最后一行只检查四个**键名**在不在 —— `warmthLevel` 在场即通过，所以它**从来没有守住过**这条红线。
而上面那一行 🔴 **把 `warmthLevel` 和 `faces` 断言成了必须存在的契约**。
同型断言另见 `EchoApiTest` 约 `:436`、`WindowVisibilityTrimTest` 约 `:301`（后者写着「暖光浓度对三档都可见」）。

**② 所以修 `C-10` 会让它变红，而这是正确的信号，不是回归。**

把 `warmthLevel` 改成档位枚举、或对非 owner 不发，都会让 `containsKeys("warmthLevel", ...)` 失败。
**红了说明修复生效了。** ⚠️ 不要去查「我是不是改坏了兼容性」—— 没有，是这条断言本来就该红。

**③ 🔴 最容易犯的错：把修复改回去，而不是把测试改掉。**

这一步很难自己发现，因为**变红的那一方长得像正确的一方**：它在 `EchoApiTest` 里、名字里写着 `NoExactCount`、
注释里写着「红线」、断言看起来在守。**一个刚接手、正在小心翼翼不破坏契约的人，
最自然的反应就是回滚自己的改动去让它变绿** —— 而那正好是把唯一一次真正的修复撤销掉。

> 🔴 **解冻后第一件事是改这条测试，不是改实现。**
> 先把它改成断言**后果**（拿不到精确人数：`warmthLevel` 不可反解 / 不在场），再动出参。
> 顺序反过来的话，你会在一片红里判断自己错了。

⚠️ 🔴 **这不是孤例，同一类信号在本仓库还有另一种长法** —— 见 `docs/ARCHITECTURE-system-split.md` §8.6「两个错互相抵消」：
`GET /messages/arrivals` 那个叫 `cardId` 的键装的其实是 `petId`（源码注明是永久错名），而前端此前按卡片键盖章，
**两个错方向相反，于是一直跑得通**；此时**修任何一边都会立刻炸，而炸的那边看起来才是刚被改坏的那个**。

两者的共同点，是解冻这一批时真正要防的东西：

> 🔴 **正确的动作会产生一个看起来像「你弄坏了」的信号。**

**本格是「修复让一条看起来正确的校验变红，人会回滚修复」；§8.6 是「修对一边让另一边立刻炸，人会回滚那一边」。**
两种形态下，回滚都是最自然、也最错的反应。⚠️ **所以红了之后先判「红的这一方原本是对的吗」，再决定回不回滚。**

⚠️ 这条测试的形态问题已作为**第五处假绿**登记在 `echo-server/docs/BUILD-VERIFICATION.md` §7.2
（🔴 它与前四处不同：**代码跑了、断言也求值了，它绿只是因为查的是字段名，不是测试名承诺的那个后果**）。
判准与同类清单见 `docs/visual/CHECKLIST-number-leak.md` §四。

### 18.4 ⚠️ 顺带登记：广场排序口径没有明禁

`GET /plaza` 写着「顺序归排序引擎（权重衰减 / 制动 / SURGE）」，**没有一条禁止排序由暖光或记得人数派生**。

今天不漏（排序引擎不看这些）。但 🔴 **一旦哪天按暖光排，位置本身就是名次**，而且**前端完全看不出来** —— 这正是 `CHECKLIST-number-leak.md` 里「手法②：有序列表里的位置」。建议解冻这一批时一并补一句明禁。

**状态。** ❄️ 同批冻结。
