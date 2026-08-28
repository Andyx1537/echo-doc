# QA 报告 · 前端 shop 接线（mi-B）· 2026-08-04

| 项 | 值 |
|---|---|
| 对应交付 | **前端 shop 接线（mi-B）**——把明信片款式商店接到真后端 |
| 交付文件 | `echo-h5-proto/src/types.ts`（+`PostcardSkin`/`PurchaseResult`）、`src/api/backend.ts`（+`postcardSkins()`/`purchase(skinId)`/`FLOWER_TOPUP_SKU`）、`src/api/http.ts`、`src/api/mock.ts`、`src/components/DetailScreen.tsx`、`src/api/track.ts`、`src/api/http.test.ts`（+2 测试） |
| QA 范围 | **聚焦前端验证**（后端 agent 并发编辑 echo-server 中）：`npm run build` + `npm test`；后端仅**只读**核对 `EchoApi.java` 的 `/shop/*` 契约结构，未构建/未跑 `mvn test` |
| 结论 | **PASS** |
| 统计 | **Blocker 0 · Major 0 · Minor 3** |

> 门槛：Blocker=0 且 Major=0 → 允许合入。本次达标，判 **PASS**（Minor 记录跟进，其中主项应派回后端）。

---

## L1 产品红线（最高优先，任一 Fail=Blocker）

- **[PASS] 付费不锁纪念内容（D2 / CR-M / 定案 #2）** — `PostcardSkin.kind ∈ {gradient,frame,material}`（皮肤/边框/材质，纯装扮增值）；`PurchaseResult.affectsUnlock` 前后端恒 `false`；购买路径不触碰任何 `unlock` 逻辑。内容解锁走独立端点 `POST /pet/me/postcards/:id/unlock`，且对带 `paid` 的请求显式拒绝。 — 文件：`src/types.ts:95-111`、`src/api/mock.ts:577-588`、`echo-server/.../EchoApi.java:627-632`、`:604-608`
- **[PASS] 去游戏化措辞（COPY-GUIDE §2.1 / E3）** — 全链路无「金币/道具/充值/背包/商城」等硬词；对外文案统一「心意/留一束心意/补充一些心意/心意商店/心意点数」。词表扫描命中均为注释里的**否定用法**（"不排名""非点赞""绝不展示数字"）。 — 文件：`src/components/DetailScreen.tsx:113,131,261,274`、`src/types.ts:99`
- **[PASS] 献花/记得无数字·无排名红线未被触动（D3/D4）** — 本次改动未触及记得面孔墙与广场暖光呈现；DetailScreen 仍以暖光浓度+面孔墙渲染记得（无计数、无排名）。花额度「今天还剩 N 朵」与 `bondMark`「你已为它留下 N 束心意」属**契约 §5 owner 私域羁绊反馈**（非公开榜单），不构成红线冲突。 — 文件：`src/components/DetailScreen.tsx:209-241,264-278`
- **[PASS] 失败/成功走温柔文案** — 购买成功「补充了一些心意，慢慢留给想记挂的它」；额度用尽「今天的心意先到这里啦，想多留一点可以补充一些」；失败「这份心意还没能收下，待会儿再试试」；记得「你的暖光落在这里 · 你也记住了这个瞬间」（对齐 CR6）。均过词表。 — 文件：`src/components/DetailScreen.tsx:95,114-115,131-133,148`

---

## L2 验收用例

- **TC-07 明信片墙（里程碑解锁 / 付费只加速款式）** — **PASS**。付费入口只买款式（皮肤/边框/材质），`affectsUnlock:false` 保证不影响解锁进度；内容解锁独立且拒绝付费解锁。前端购买接线正确接 `api.purchase`。
- **TC-04 献花额度制（相关联，未回归）** — **PASS（回归观察）**。补心意复用 `POST /shop/purchase`（`FLOWER_TOPUP_SKU`）后重新拉 `flowerQuota`；额度扣减/温度解耦逻辑未被本次改动破坏。
- **契约铁律 §14.1 第 1 条（列表 `{items}` 信封）** — **PASS**。款式列表后端返 `{items}`，`http.ts` 取 `.items`，mock 同形，三层一致。

---

## L3 测试与构建（前端）

- `npm run build`：**过**（`tsc -b && vite build`，62 模块，无类型/lint 报错）。
- `npm test`：**绿**（3 文件 / 18 用例全过，含本次新增 `http.test.ts` 款式商店 2 用例）。
- 新代码覆盖：**有**。`postcardSkins()` 验 `{items}` 信封解析 + `kind` 枚举约束；`purchase()` 验 `POST /shop/purchase`、body=`{skinId}`、护栏 `affectsUnlock:false`。
- `mvn test`：**按指令未运行**（后端并发变动中，结果不可信）。

---

## L4 通用质量（契约一致性 / 可读性）

- **契约一致性（§7 / §14.1）— 对齐**：
  - `GET /shop/postcard-skins` → 后端 `{items:[{id,name,kind,price}]}`，前端 `postcardSkins()` 取 `.items`，`PostcardSkin{id,name,kind,price}` 字段/类型/`kind` 枚举完全对齐。 — `http.ts:185-186`、`EchoApi.java:617-624,1052-1058`
  - `POST /shop/purchase` → body `{skinId}`、响应 `{ok,skinId,affectsUnlock:false}`，与 `PurchaseResult` 三字段逐一对齐。 — `http.ts:187`、`EchoApi.java:627-632`
- **DetailScreen 真接后端 — 达标**：`purchase()` 已改调 `api.purchase(FLOWER_TOPUP_SKU)` 后再 `api.flowerQuota()` 刷新，**不再本地 mock 加额度**；mock 后端仍在 `purchase()` 内为 `FLOWER_TOPUP_SKU` 落 `purchasedBalance`，离线可完整跑通。 — `DetailScreen.tsx:121-137`、`mock.ts:577-588`

- **[Minor · 派回后端] 真后端 `/shop/purchase` 对 `flower_topup` 只回执不落额度** — 后端 `shopPurchase` 仅返回 `{ok,skinId,affectsUnlock:false}`，未对 `flower_topup` SKU 增记 `purchasedBalance`；真后端模式下点「补充一些心意」→ 后续 `flowerQuota` 不变，但前端已弹「补充了一些心意」，存在 UX 诚实性小落差。**属后端范围，非前端 Blocker**（前端已正确调用契约端点、mock 态完整可跑）。 — 文件：`echo-server/.../EchoApi.java:627-632` — 建议：后端对 `flower_topup` SKU 落额度（或返回到账数量供前端校对）。
- **[Minor · 前端·同源] `purchase()` 成功文案偏乐观** — 真后端未实际到账时仍提示成功。建议校验 `flowerQuota` 前后 delta（或依后端到账回执）再给成功文案，与上一条一并闭环。 — 文件：`src/components/DetailScreen.tsx:127-131`
- **[Minor · 前端] `postcardSkins()` 暂无 UI 消费方** — 契约/`http`/`mock`/测试齐备，但尚无款式商店界面调用它（当前仅 `purchase(FLOWER_TOPUP_SKU)` 接线补心意）。符合 §14 mi-5「死方法接线或标 TODO」口径，属预期的分步交付。 — 文件：`src/api/backend.ts:131`、`http.ts:185-186` — 建议：款式商店 UI 落地时接入，或暂标 TODO。

---

## 已知项核对（交付说明第 5 条）

- 前端说明「真后端 `/shop/purchase` 目前是 stub、只回执不落额度」经核对属实（见 `EchoApi.java:627-632`）。**判定：后端范围问题，记为后端 Minor/TODO，非前端 Blocker。** 依据：本次交付=前端接线，前端已按契约正确调用；契约 §7 未强制 purchase 落额度；mock 态离线完整可跑（ACCEPTANCE §3「后端未就绪 mock 仍可跑通」达标）。

---

## 阻断清单（必须修）

- 无（Blocker=0 · Major=0）。

## 跟进清单（Minor，可择期 / 派回后端）

1. 【后端】`/shop/purchase` 对 `flower_topup` SKU 落 `purchasedBalance`（或回执到账数），消除真后端「提示已补充但额度未变」落差。
2. 【前端】`DetailScreen.purchase()` 依到账结果再给成功文案（与 1 同源）。
3. 【前端】`postcardSkins()` 待款式商店 UI 接入或暂标 TODO（mi-5 口径）。
