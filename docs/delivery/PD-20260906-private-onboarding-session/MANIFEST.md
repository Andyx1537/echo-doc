# 级联交付账本 · PD-20260906-private-onboarding-session

状态：`READY_FOR_DEVELOPMENT`
任务版本：`v1.2`
决策编号：`G-29 / G-37 FC1-FC2`
产品基线提交：`be20048`
契约版本/提交：`347e846`
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
| Onboarding 持久化与 API | 后端 | `echo` / `backend/private-onboarding-session` | Onboarding 表、领域、路由、迁移和专项测试 | 身份/生成边界契约桩 | 可开工 |
| 建档页面与恢复 | 前端 | `echo-client` / `frontend/private-onboarding-session` | Onboarding 页面、状态容器、DTO 和组件测试 | 冻结 API；独立干净 worktree | 可开工 |
| 专项用例与真联调 | QA | 测试资产 / 同任务标识 | 本单元验收、数据和报告 | 前后端候选构建 | 可准备；候选完成后执行 |

共享契约唯一 Owner：后端提供 OpenAPI/固定样例，产品与 QA 复核；前端不得自造状态。

合并顺序：后端契约/迁移 → 前端消费者 → 真联调 → QA → 产品验收。

## 5. 并行评估回执

### 前端回执

ACK：`accepted-with-risks`。契约无阻断；现有客户端 9 个脏文件中 5 个与本单元共享文件重叠，必须从干净基线建独立 worktree，合并时人工协调，不覆盖既存 Plaza 改动。

### 后端回执

ACK：`accepted`。建档专用匿名 multipart、consent CAS/撤回和稳定选项码已关闭阻断。

### QA 回执

ACK：`accepted-with-risks`
可测性：`PASS`。风险仅为孤立上传对象物理清理 SLA/监控口径需由后端实现方案登记；不阻塞开发。

## 6. 联合冻结门

- FE_ACK：`accepted-with-risks`
- BE_ACK：`accepted`
- QA_ACK：`accepted-with-risks / PASS`
- 冻结契约版本：`347e846`
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

## 8. 缺陷闭环

| 缺陷 | 严重度 | 状态 | Owner | 定案/契约 | 修复提交 | 复验报告 |
|---|---|---|---|---|---|---|

## 9. 验收与归档

- 必须证据：持久化会话、单宠一致性、四题多选、生成前绑定门、失败恢复、确认 CAS、服务重启恢复、真实前后端接口和 QA 专项报告。
- QA 入口：`TEST-PLAN.md`；固定夹具：`fixtures/onboarding-v1.json`；候选执行门：`QA-EXECUTION-CHECKLIST.md`。
- 组合主线不在本单元验收；完成后只向最终组合单元提供固定构建和契约版本。
- 最终状态：待开发与验收。
