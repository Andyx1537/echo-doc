# 级联交付账本 · PD-20260906-phone-account-resolution

状态：`DISTRIBUTED`
任务版本：`v1.0`
决策编号：`G-28 / G-32 / G-35`
产品基线提交：`be20048`
契约版本/提交：`5e00d2f`
协调负责人：产品
创建时间：2026-09-06
目标完成窗口：三方评估后确定

## 1. 用户结果与主线定位

- 目标用户结果：未绑定用户验证手机号后，明确选择“绑定当前匿名账号”或“切回手机号已有账号”，服务端只签发正确的新会话和返回结果。
- 产品主线步骤：任一受限操作的手机号登录边界；首个消费方是私域 Onboarding 生成前绑定墙。
- 主责系统：身份系统；核心对象 `PhoneChallenge / PhoneResolution`。
- 最小边界：接收当前匿名会话与 `returnTo`，返回 `accountId/phoneBound/sessionToken/deviceCredential/returnToAllowed/nextAction`。
- 非目标：不实现 Onboarding 页面或状态机；不迁移/合并匿名资料；不做作品、Plaza、评论；不实现“手动唤醒旧匿名账号”的账号选择器。

## 2. 四层差额

| 层 | 结论 | 证据 |
|---|---|---|
| 以前确认的产品方案 | 首次进入即建匿名账号；新手机号升级当前账号，已有手机号需二次确认切号；匿名资料不迁移 | `PRODUCT-DECISION-ANONYMOUS-ACCESS §1.1`、`API-CONTRACT §19.8` |
| 当前实际实现 | `/auth/guest` 直接信任前端 `deviceId` 并可恢复任何命中账号；`/auth/bind` 仅验证非空 credential 后把 `guest=false`，不写手机号归属、不处理冲突、不撤销 token/设备关系；会话 token 只在进程内 | `EchoApi.authGuest/authBind`、`EchoStore`、`PgEchoStore` |
| 本次确认的目标方案 | `challenge → verify → resolution confirm`；验证成功前不暴露号码归属；新号绑当前账号，已有号切原账号；确认前不改会话，确认失败保留当前匿名会话 | `API-CONTRACT §19.8–19.9` |
| 精确开发差额 | 持久挑战/解析/手机凭据/设备凭据/会话；手机唯一性与 E.164；滑动窗口频控；单次解析 token；原子绑定或切号与旧凭据失效；稳定错误和消费方契约测试 | 当前实现与目标契约对照 |

被替代条目：旧 `/auth/bind {type,credential}` 新客户端主路；前端生成并持久化可直接登录账号的 `deviceId` 模型。

保留不变量：后端永远是账号、绑定、手机归属、凭据失效和新账号创建权威；已绑账号只能手机登录；切已有账号不迁移匿名数据；失败不替换当前会话。

## 3. 对象、流程与契约

- 对象/生命周期：`PhoneChallenge(created→verified|expired|locked|superseded)`；`PhoneResolution(created→used|expired)`；手机凭据与设备凭据作为原子确认的边界数据。
- 主流程：输入号码 → 发送验证码 → 校验码 → 返回 `bind_current|switch_existing` 但不改会话 → 用户确认 → 服务端原子绑定/切号并签新会话。
- 安全与可见性：挑战创建不暴露号码是否存在；解析 token 绑当前匿名会话、有效 10 分钟、单次；已绑账号不可再由设备凭据登录。
- API：`POST /auth/phone/challenges`、`POST /auth/phone/challenges/:challengeId/verify`、`POST /auth/phone/resolutions/:resolutionToken/confirm`；设备会话目标为 `POST /auth/device/session`。
- DTO：challenge=`{challengeId,expiresAt,resendAvailableAt}`；verify=`{resolution,resolutionToken,resolutionExpiresAt}`；confirm=`{accountId,phoneBound:true,sessionToken,deviceCredential:null,returnToAllowed,nextAction}`。
- 参数：验证码 5 分钟，重发 60 秒，单挑战错 5 次；手机 5/小时、10/日，设备 10/小时、30/日，IP 20/小时、100/日；resolution 10 分钟。
- 错误：`phone_invalid/code_invalid/challenge_expired/challenge_locked/resend_cooldown/rate_limited/resolution_expired/resolution_used/resolution_session_mismatch/sms_provider_unavailable`，统一 `{code,msg,detail,data}`。
- 失败：任一失败保留当前匿名会话；短信不可用不可伪造已发送；原子确认部分失败整笔回滚。
- 兼容：新流程上线后旧 `/auth/bind` 退出新客户端主路；具体兼容窗由后端评估活跃旧客户端后回执，不先行破坏。
- 待技术冻结：设备凭据精确错误/轮换标识、幂等键和并发建号去重；`SmsProvider` 在无真实云账号的测试环境必须显式 stub 且不得在生产装配。

## 4. 任务依赖与所有权

| 任务 | 专业/Owner | 仓库与业务分支 | 允许修改范围 | 依赖 | 状态 |
|---|---|---|---|---|---|
| 身份持久化、挑战/解析/会话 API | 后端 | `echo` / `backend/phone-account-resolution` | 身份表、凭据、会话、频控、SmsProvider 边界与专项测试 | 无外部云账号时可先 stub | 待评估 |
| 全局手机号登录组件与会话替换 | 前端 | `echo-client` / `frontend/phone-account-resolution` | 身份 API、会话/设备凭据存储、绑定/切号窗与 returnTo | 固定后端 DTO/错误 | 待评估 |
| 身份安全与真联调用例 | QA | 测试资产 / 同任务标识 | 枚举、频控、重放、会话固定、冲突、回滚与消费方恢复 | 可控 SmsProvider | 待评估 |

共享契约唯一 Owner：后端提供固定 DTO/错误/时序与安全约束，产品、前端、QA 共同复核。

合并顺序：后端持久化与提供者契约 → 前端消费与会话替换 → Onboarding 组合联调 → QA → 产品验收。

## 5. 并行评估回执

### 前端回执

ACK：`pending`
预计窗口/条件/置信度：
复用/新增/迁移/替换/废弃/不变：
页面、状态与接口影响：
风险/阻塞/产品问题：
验证计划：

### 后端回执

ACK：`pending`
预计窗口/条件/置信度：
复用/新增/迁移/替换/废弃/不变：
数据、接口、状态机与运行影响：
风险/阻塞/产品问题：
验证计划：

### QA 回执

ACK：`pending`
可测性：`pending`
受影响用例与红线：
环境、数据与联调要求：
风险/阻塞/产品问题：
验证计划：

## 6. 联合冻结门

- FE_ACK：`pending`
- BE_ACK：`pending`
- QA_ACK：`pending`
- 冻结契约版本：
- 产品/技术重新定调项：无产品主线待决；待技术回执凭据细节与兼容窗。
- 开工结论：`NOT_READY`

## 7. 开发、联调与反馈

| 时间 | 角色/任务 | 新差额或证据 | 状态变化 | 下一责任方 |
|---|---|---|---|---|
| 2026-09-06 | 产品 | 从基础总账本拆出第 2 个最小单元；已有 G-28/G-32/G-35 定案不变 | `DISTRIBUTED` | FE/BE/QA 并行评估 |

固定联调版本：待三方冻结。
真实请求响应证据：待实现。

## 8. 缺陷闭环

| 缺陷 | 严重度 | 状态 | Owner | 定案/契约 | 修复提交 | 复验报告 |
|---|---|---|---|---|---|---|

## 9. 验收与归档

- 必须证据：手机号不枚举；挑战过期/锁定/重发/频控；解析 token 单次与会话绑定；新号原子绑当前账号；已有号切原账号且匿名资料不迁移；旧匿名 token/设备关系失效；已绑账号不可由设备凭据恢复；Onboarding `bind_current/switch_existing` 真联调。
- 迁移/回滚/监控：待后端评估持久表、旧 `deviceId` 兼容和短信/风控监控。
- 最终状态：待三方评估与契约冻结。
