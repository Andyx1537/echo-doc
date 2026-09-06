# QA 测试计划 · 私域单宠建档会话 v1

## 1. 绑定基线与结论规则

- `deliveryId`：`PD-20260906-private-onboarding-session`
- 文档基线：`echo-doc/develop@09ecec2`
- 冻结契约：`347e846`，以 `API-CONTRACT §2.1` 为准
- 被测对象：匿名用户从创建单宠建档会话，到确认候选并原子创建唯一私域窗口
- 当前阶段：仅建立计划、固定夹具和检查清单；没有前后端候选构建，不执行真联调，不给功能 PASS

最终 QA PASS 必须同时满足：固定前端提交、后端提交、构建、数据库迁移版本、环境和夹具；本计划的 P0/P1 用例全部执行；Blocker=0、Major=0；真实接口主链、失败恢复、重启恢复和并发确认均有可追溯证据。

## 2. 范围和边界

### 纳入

- 建档专用匿名 multipart 上传、额度预占、会话挂接和失败回收；
- 单宠主体选择、裁切、质量和同宠一致性；
- Q1～Q4 稳定选项码、基数、修改和恢复；
- 确认前授权的授予、撤回、版本冲突与状态能力；
- 会话状态持久化、刷新/重启恢复、权限隔离；
- 幂等键、`expectedSessionVersion`、并发冲突和确认单窗；
- 身份边界的 `bind_current` / `switch_existing` 消费结果；
- 生成边界的排队、成功、失败、重试和细化恢复；
- 新客户端旧端点退役行为；
- 孤立对象不可引用、额度释放和进入清理队列。

### 明确排除

短信供应商及频控、账号合并、Work、Plaza、评论、行为账本、推荐、生成模型内部质量策略、确认后的全局隐私设置。排除项不得成为本单元通过条件，也不得由本单元测试替其定案。

## 3. 测试分层

1. **提供者契约**：后端以冻结 DTO、状态、错误信封和固定夹具运行；验证所有写请求的幂等和版本控制。
2. **消费者契约**：前端使用同一固定夹具覆盖恢复、禁止、冲突和返回路径，不自行推导服务端权威。
3. **真实接口专项**：前端候选直接连接后端候选，保存真实请求、响应、状态快照和数据库证据。
4. **可靠性专项**：服务重启、任务失败、网络重放、事务故障注入和并发屏障。

Mock 只证明页面状态可呈现；身份和生成可用确定性边界桩，但 Onboarding API、持久化、事务和前端消费必须是真实实现。

## 4. 最小可执行用例

| ID | 级别 | 场景与关键步骤 | 预期结果/证据 |
|---|---|---|---|
| ONB-001 | P0 | 匿名创建会话，刷新客户端并重启服务后 GET | `onboardingId/accountId/status/currentStep/sessionVersion` 保持一致；他账号读取为 `onboarding_forbidden` |
| ONB-002 | P0 | 匿名通过建档专用端点上传 1 张合格单宠照片 | 槽位预占与资源挂接原子成功；返回 asset、主体候选、质量和递增快照 |
| ONB-003 | P0 | 匿名调用全局 `/upload` | 仍受绑定门限制；不得因建档上传放开全局上传 |
| ONB-004 | P0 | 上传中断、对象写入失败、元数据或挂接失败 | 返回全局错误信封；释放额度；对象不可通过会话或公开地址引用；登记清理队列 |
| ONB-005 | P1 | 照片达到 2 张后再传；删除/失败释放后重试；视频 0/1/2/超额 | 服务端按照片上限 2、视频上限 2 判定；失败不永久占额；错误为 `asset_limit_exceeded` 或 `asset_upload_incomplete` |
| ONB-006 | P0 | 多宠照片选择并裁切一只；切换主体；提交模糊/遮挡素材 | 任何时刻只有一个最终主体；裁切可恢复；不可辨识返回 `asset_quality_failed`，不得进入生成 |
| ONB-007 | P0 | 第二份素材为同宠、未知同宠、明显不同宠 | 同宠接收；未知走用户确认；明显不一致返回 `subject_inconsistent` |
| ONB-008 | P0 | 按夹具提交 Q1～Q4 合法答案后刷新/重启；逐题修改 | 当前答案完整恢复；修改产生 `supersedesId`；历史与当前答案可区分 |
| ONB-009 | P0 | 每题提交未知 code、空数组、超出基数 | 未知 code=`answer_code_invalid`；基数非法=`answer_cardinality_invalid`；状态和旧答案不被污染 |
| ONB-010 | P1 | Q3 未选/选中 `special_gesture` 时分别携带短文本或语音转写来源 | 仅选中该 code 时接收 `freeText/freeTextSource`；短文本始终非完成门槛 |
| ONB-011 | P0 | 完成素材/主体/问卷但未绑定，调用 generate | 状态为 `ready_to_bind`；返回 `phone_binding_required`；不创建 generationJob、不消耗生成资源 |
| ONB-012 | P0 | 身份桩返回 `bind_current` 后恢复原会话 | account/session、素材、答案和步骤保持；进入 `ready_to_generate`，可原地继续 |
| ONB-013 | P0 | 身份桩返回 `switch_existing` | 匿名资料不迁移；返回 `restart_in_existing_account`；旧匿名会话不被错误挂入已有账号 |
| ONB-014 | P0 | generate 首次、同键同载荷重放、同键异载荷、旧 sessionVersion | 首次仅一个任务；同载荷返回原结果；异载荷=`idempotency_conflict`；旧版本=`onboarding_version_conflict` 且带最新快照 |
| ONB-015 | P0 | 生成桩依次返回 queued/running/succeeded；过程中刷新并重启服务 | `generationJob` 和状态可恢复；成功进入 `candidate_ready`；不重复生成 |
| ONB-016 | P0 | 生成失败/超时后重试 | 回到 `ready_to_generate` 且 `lastOperation=generate_failed`；既有素材答案保留；重试产生受控新任务 |
| ONB-017 | P0 | 选择候选并细化；细化失败、成功和重放 | 失败回 `candidate_ready`；成功提供新候选；同键不重复任务；候选归属受服务端校验 |
| ONB-018 | P0 | 有候选时授予授权、撤回、重新授予 | 授予可进入 `ready_to_confirm`；撤回保留候选、回 `candidate_ready`、移除 confirm；重授予生成新版本后恢复确认能力 |
| ONB-019 | P0 | 未授权、使用旧 consentVersion 或他会话版本确认 | 分别返回 `consent_required` / `consent_version_conflict` / 权限错误；不得创建 pet/window |
| ONB-020 | P0 | 对同一会话并发发起确认，含相同和不同幂等键 | CAS 下只创建一个 pet 和一个 window；幂等重放返回同一结果；竞争请求稳定冲突，不出现半成功 |
| ONB-021 | P0 | 在 pet 已写入、window 写入失败等事务点注入故障 | 整体回滚或可安全重试；不得残留孤立 pet、重复 window 或假 `confirmed` |
| ONB-022 | P1 | confirmed 后调用建档 consent；abandoned 后尝试上传/生成/确认 | 返回 `onboarding_invalid_state`；不得删除既有窗口或重新激活已放弃会话 |
| ONB-023 | P0 | 新客户端调用旧 `detect/start/refine/confirm` 路径；发布盘点分别模拟有/无活跃旧端 | 新主链不调用旧端点；退出阶段按契约兼容或 410 `endpoint_retired`，不得静默走旧一次性流程 |
| ONB-024 | P1 | 检查建档全部用户文案与生成输入 | 不推测死亡，不把模型派生当用户事实，不把真人默认生成进背景 |

## 5. 状态和权威检查

- 服务端是 status、currentStep、allowedActions、额度、质量、授权、任务和建窗结果唯一权威；前端只展示、收集、恢复和按错误反馈。
- 合法主链：`collecting → ready_to_bind → ready_to_generate → generating → candidate_ready ↔ refining → ready_to_confirm → confirmed`。
- 生成失败只能回 `ready_to_generate`；细化失败只能回 `candidate_ready`；确认失败只能回 `ready_to_confirm`，且均不得静默建窗。
- 所有修改请求都要验证 `Idempotency-Key` 与 `expectedSessionVersion`；响应错误统一为 `{code,msg,detail,data}`。
- `confirmed` 是本单元终点；确认后的隐私设置不在本单元内测试。

## 6. 环境、夹具和可观测性

执行环境必须提供：

- 可重置、可查询的测试数据库及准确迁移版本；至少两实例或可真实重启的服务端；
- 支持事务故障注入、并发屏障和重复请求重放；
- 建档对象存储测试桶、资源引用探针、额度账本、孤儿清理队列查询能力；
- 身份边界桩：未绑定、`bind_current`、`switch_existing`，不实现短信供应商；
- 生成边界桩：queued、running、succeeded、failed、timeout、refine succeeded/failed；
- `fixtures/onboarding-v1.json` 中的稳定题库、状态、错误和边界脚本；
- 实体媒体数据：清晰单宠正面/侧面、模糊单宠、多宠可裁切、人宠同框、明显不同宠、短视频，以及中断上传载荷。媒体文件由 QA 环境登记校验和，不得含真实用户隐私素材；
- 服务日志/trace、Onboarding 六类持久对象查询、generation anchor、幂等记录、pet/window 唯一约束和清理队列证据。

孤立对象物理清理 SLA 尚未冻结，因此本单元当前只把“不可引用、额度释放、已入清理队列”作为 P0；清理实际完成时间记录为实现风险，不阻断候选进入专项测试。

## 7. 候选门与报告

前后端候选到达后，先完成 `QA-EXECUTION-CHECKLIST.md` 的 Gate A～C，再执行用例。任何契约字段、状态、权限、错误或幂等语义偏离 `347e846`，立即停止联调并把账本退回 `CONTRACT_REVIEW`，不得由 QA 自行选择兼容解释。

报告至少绑定：文档基线、契约提交、前端/后端提交、构建号、环境、迁移版本、夹具版本、执行时间、用例结果、缺陷及证据位置。Mock-only 结果不得写为整链 PASS。
