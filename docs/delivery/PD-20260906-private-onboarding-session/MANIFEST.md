# 级联交付账本 · PD-20260906-private-onboarding-session

状态：`INTEGRATING`
任务版本：`v1.6`
决策编号：`G-29 / G-37 FC1-FC2`
产品基线提交：`be20048`
契约版本/提交：`5e00d2f`
协调负责人：产品
创建时间：2026-09-06
目标完成窗口：三方评估后确定

## 1. 用户结果与主线定位

- 目标用户结果：匿名用户完成单宠素材、主体、裁切和四题问卷；生成前绑定；生成或细化失败后可恢复；确认候选后只创建一扇窗口。
- 产品主线步骤：安顿阶段的“建档/识别/定妆 → 建立私域窗口”。
- 主责系统：Onboarding；核心对象 `OnboardingSession`。
- 最小边界：只消费身份系统的 `phoneBound/accountId/returnToAllowed`，只调用生成系统的异步任务边界。
- 非目标：不实现短信供应商、账号合并、公开 Work、Plaza、评论、行为账本或推荐；不改生成模型内部策略。

## 2. 四层差额

| 层 | 结论 | 证据 |
|---|---|---|
| 以前确认的产品方案 | 先绑定、一次性开始生成、两轮候选后确认 | `API-CONTRACT §2` 旧实现登记 |
| 当前实际实现 | `detect/start/refine/confirm` 存在；会话在进程内 Map；`start` 要求已绑定并立即生成 | 基础 v4 后端核查回执 |
| 本次确认的新方案 | 匿名先上传与答题，服务端持久状态机，生成前绑定，失败可恢复，确认 CAS 原子建窗 | `SPEC-private-pet-onboarding-questionnaire §7`、`API-CONTRACT §2.1` |
| 精确开发差额 | 六类持久对象、完整状态/DTO/幂等/CAS、异步任务恢复、旧接口退出、对应页面和专项测试 | `be20048` |

被替代条目：旧“上传前绑定”和一次性 `/pet/onboarding/start` 新客户端主路径。

保留不变量：P0 一窗一宠；多宠必须选并裁切一只；不推测死亡；用户事实与模型派生分存；匿名不得正式生成；服务端拥有状态和授权权威。

## 3. 对象、流程与契约

- 主对象：`OnboardingSession`；状态为 `collecting → ready_to_bind → ready_to_generate → generating → candidate_ready ↔ refining → ready_to_confirm → confirmed`，可主动 `abandoned`。
- 附属对象：`OnboardingSubject/OnboardingAsset/OnboardingAnswer/PetProfileFact/GenerationAnchor`，只服务本会话。
- 页面：上传 → 单宠选择/裁切 → 四题问卷 → 总结 → 绑定边界 → 生成 → 候选/细化 → 确认。
- API：以 `API-CONTRACT §2.1` 为唯一目标契约；修改请求统一幂等键与 `expectedSessionVersion`，错误统一 `{code,msg,detail,data}`。
- 身份边界：`bind_current` 可继续；`switch_existing` 不迁移匿名资料并返回 `restart_in_existing_account`。
- 失败：生成失败回 `ready_to_generate`，细化失败回 `candidate_ready`，确认失败回 `ready_to_confirm`；不得静默建窗。
- 兼容：新客户端切换后停用旧端点；若发布盘点存在活跃旧端，兼容 30 天、最长 60 天后返回 410。

## 4. 任务依赖与所有权

| 任务 | 专业/Owner | 仓库与业务分支 | 允许修改范围 | 依赖 | 状态 |
|---|---|---|---|---|---|
| Onboarding 持久化与 API | 后端 | `echo` / `backend/private-onboarding-session` | Onboarding 表、领域、路由、迁移和专项测试 | 身份/生成边界契约桩 | 已固定候选 `ac868a9` |
| 建档页面与恢复 | 前端 | `echo-client` / `frontend/private-onboarding-session` | Onboarding 页面、状态容器、DTO 和组件测试 | 冻结 API；独立干净 worktree | 已固定候选 `d280246` |
| 专项用例与真联调 | QA | 测试资产 / 同任务标识 | 本单元验收、数据和报告 | 前后端固定候选 | 待真实边界联调 |

共享契约唯一 Owner：后端提供 OpenAPI/固定样例，产品与 QA 复核；前端不得自造状态。

合并顺序：后端契约/迁移 → 前端消费者 → 真联调 → QA → 产品验收。

## 5. 并行评估回执

### 前端回执

ACK：`accepted-with-risks`。契约无阻断；现有客户端 9 个脏文件中 5 个与本单元共享文件重叠，必须从干净基线建独立 worktree，合并时人工协调，不覆盖既存 Plaza 改动。

### 后端回执

ACK：`accepted`。建档专用匿名 multipart、consent CAS/撤回和稳定选项码已关闭阻断。

### QA 回执

ACK：`accepted-with-risks`
可测性：`PASS`。已对 `5e00d2f` 称呼增量短复签：默认“它”、profile 修改、快照恢复及幂等/CAS 均可执行且不改变四题；`pet_name_invalid` 的长度/字符触发边界待实现前固定样例，不阻塞最小主链。既有孤立上传对象物理清理 SLA/监控风险不变。

## 6. 联合冻结门

- FE_ACK：`accepted-with-risks`
- BE_ACK：`accepted`
- QA_ACK：`accepted-with-risks / PASS`
- 冻结契约版本：`5e00d2f`
- 产品/技术重新定调项：无；实现事实若推翻边界则触发停止闸。
- 开工结论：`READY_FOR_DEVELOPMENT`

## 7. 开发、联调与反馈

| 时间 | 角色/任务 | 新差额或证据 | 状态变化 | 下一责任方 |
|---|---|---|---|---|
| 2026-09-06 | 产品拆分 | 从基础大账本拆出单一 Onboarding 用户结果 | `DISTRIBUTED` | FE/BE/QA 评估 |
| 2026-09-06 | 三方初评 | 发现匿名上传、授权写入和稳定选项码三个本单元缺口 | `REWORK` | 产品/契约修订 |
| 2026-09-06 | 产品/契约 | 采用建档专用 multipart 原子挂接；新增 consent CAS；冻结 Q1～Q4 选项码 | `CONTRACT_REVIEW` | FE/BE/QA 复签 |
| 2026-09-06 | 三方复签 | FE/BE/QA 均接受；无契约阻断 | `READY_FOR_DEVELOPMENT` | 前端/后端实现，QA 准备专项 |
| 2026-09-06 | QA 准备 | 建立 `TEST-PLAN.md`、固定机器夹具和 `QA-EXECUTION-CHECKLIST.md`；尚无候选，不执行真联调 | `READY_FOR_DEVELOPMENT` | 等待前端/后端固定候选 |
| 2026-09-06 | 后端实现核查 | 发现称呼存在于产品流程但目标 API 无写入字段，停止相关接线 | `STOP_PRODUCT_REVIEW` | 产品/契约最小修订 |
| 2026-09-06 | 产品/契约 | 冻结 `petName`：可选、默认“它”、会话快照返回、独立 profile CAS 修改 | `CONTRACT_REVIEW` | 三方字段短复签 |
| 2026-09-06 | QA 短复签 | `5e00d2f` 称呼增量可测，新增默认/修改/恢复/幂等/CAS 用例与夹具 | `CONTRACT_REVIEW` | 等待 FE/BE 短复签后重开开发 |
| 2026-09-06 | FE/BE 短复签 | 称呼增量均 `accepted`；QA=`accepted-with-risks/PASS` | `IMPLEMENTING` | 前端/后端继续实现 |
| 2026-09-06 | 前端环境 | 独立工作树与 `frontend/private-onboarding-session` 已创建，原脏 develop 未改 | `IMPLEMENTING` | 前端实现 |
| 2026-09-06 | 前端候选 | `0aa3d17`：可恢复建档页、受控素材 URL 适配；专项 9/9、全量 155/155、生产构建通过 | `IMPLEMENTING` | 后端候选/真联调 |
| 2026-09-06 | 后端候选 | `20a2279`：持久会话、专用匿名上传、四题/称呼、幂等/CAS、异步生成恢复、授权与原子确认；专项 22/22 通过 | `INTEGRATING` | QA 真实边界联调 |
| 2026-09-06 | 契约静态对照 | 前端问卷版本 `1/v1` 不一致；后端终态仍返回非契约 generationJob 状态 | `REWORK` | FE/BE 最小修正 |
| 2026-09-06 | 契约修正 | FE `d280246` 统一为 `v1`；BE `4495fe1` 在任务终态清空 generationJob；FE 全量 156/156、build 通过，BE 专项 22/22 | `INTEGRATING` | QA 真 HTTP |
| 2026-09-06 | QA 真 HTTP | 内存态主链到 confirmed、确认幂等、受控素材/CAS/绑定门通过；发现 ONB-007 跨素材单宠一致性未实现 | `REWORK` | 后端 |
| 2026-09-06 | 后端返工与 QA 复验 | BE `ac868a9` 实现明显异宠拒绝、未知同宠用户确认并簇、未确认不越过 collecting；建档 API 10/10，总专项 24/24，QA=`VERIFIED` | `INTEGRATING` | PG 环境/身份单元组合联调 |

### 7.1 固定候选与未过门证据

- 前端：`echo-client@d280246`，分支 `frontend/private-onboarding-session`。
- 后端：`echo@ac868a9`，分支 `backend/private-onboarding-session`，schema 版本 `2026090601`。
- 后端专项：`OnboardingApiTest + PgOnboardingRepositoryTest + SchemaContractTest + UploadStorageTest + ResourceStoreTest`，共 24 项通过；本机未配置真实 PostgreSQL，因此 PG 用例实际执行 0 项。
- QA 内存态真 HTTP 已走通到 `confirmed`；ONB-007 修正后以后端专项和代码路径复验为 `VERIFIED`，尚未重跑修正后的真 HTTP 用例。
- 仓库既有全量回归：Aengine 79/79 通过；`echo-server` 444 项中 42 错误、2 失败，集中于旧测试夹具以未绑定账号调用旧建档入口，本切片未改动 `BindingGuard`；作为既有回归债务保留，不宣称全量通过。
- 尚未通过：真实 PostgreSQL 重启恢复/确认失败注入；前端需要的手机号 challenge/verify/resolution 由下一 `phone-account-resolution` 单元提供，当前请求 404，因此本候选无法完成真 UI 整链。两项未过门前不进入 `QA_VERIFYING`。

## 8. 缺陷闭环

| 缺陷 | 严重度 | 状态 | Owner | 定案/契约 | 修复提交 | 复验报告 |
|---|---|---|---|---|---|---|
| ONB-007 跨素材单宠一致性缺失 | Major/P0 | `VERIFIED` | 后端 | `5e00d2f` / TEST-PLAN ONB-007 | `ac868a9` | OnboardingApiTest 10/10；明显异宠回滚、未知素材确认并簇、pending 不越过 collecting |

## 9. 验收与归档

- 必须证据：持久化会话、单宠一致性、四题多选、生成前绑定门、失败恢复、确认 CAS、服务重启恢复、真实前后端接口和 QA 专项报告。
- QA 入口：`TEST-PLAN.md`；固定夹具：`fixtures/onboarding-v1.json`；候选执行门：`QA-EXECUTION-CHECKLIST.md`。
- 组合主线不在本单元验收；完成后只向最终组合单元提供固定构建和契约版本。
- 最终状态：本单元代码缺陷已销账；待真实 PostgreSQL 门禁及下一身份单元交付后的真 UI 组合联调，未进入最终 QA/产品验收。
