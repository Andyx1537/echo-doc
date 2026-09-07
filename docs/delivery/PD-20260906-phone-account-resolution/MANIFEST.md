# 级联交付账本 · PD-20260906-phone-account-resolution

状态：`IN_DEVELOPMENT`
任务版本：`v1.3`
决策编号：`G-28 / G-32 / G-35/DC9`
产品基线提交：`d6c2090`
契约版本/提交：`phone-account-resolution-v1 / d6c2090`
协调负责人：产品
创建时间：2026-09-06
目标完成窗口：后端候选 6–9 个工作日；前端候选 3–4 个工作日；固定双端后联调验收 1 个工作日

## 1. 用户结果与主线定位

- 目标用户结果：未绑定用户验证手机号后，明确选择“绑定当前匿名账号”或“切回手机号已有账号”，服务端只签发正确的新会话和返回结果。
- 产品主线步骤：任一受限操作的手机号登录边界；首个消费方是私域 Onboarding 生成前绑定墙。
- 主责系统：身份系统；核心对象 `PhoneChallenge / PhoneResolution`。
- 最小边界：接收当前匿名会话与服务端认可的 `continuation` 枚举，返回 `accountId/phoneBound/sessionToken/deviceCredential/returnToAllowed/nextAction`。
- 非目标：不实现 Onboarding 页面或状态机；不迁移/合并匿名资料；不做作品、Plaza、评论；不实现“手动唤醒旧匿名账号”的账号选择器。

## 2. 四层差额

| 层 | 结论 | 证据 |
|---|---|---|
| 以前确认的产品方案 | 首次进入即建匿名账号；新手机号升级当前账号，已有手机号需二次确认切号；匿名资料不迁移 | `PRODUCT-DECISION-ANONYMOUS-ACCESS §1.1`、`API-CONTRACT §19.8` |
| 当前实际实现 | `/auth/guest` 直接信任前端 `deviceId` 并可恢复任何命中账号；`/auth/bind` 仅验证非空 credential 后把 `guest=false`，不写手机号归属、不处理冲突、不撤销 token/设备关系；会话 token 只在进程内 | `EchoApi.authGuest/authBind`、`EchoStore`、`PgEchoStore` |
| 本次确认的目标方案 | `challenge → verify → resolution confirm`；验证成功前不暴露号码归属；新号绑当前账号，已有号切原账号；确认前不改会话，确认失败保留当前匿名会话 | `API-CONTRACT §19.8–19.9` |
| 精确开发差额 | 持久挑战/解析/手机凭据/设备凭据/会话；手机唯一性与 E.164；滑动窗口频控；单次解析 token；原子绑定或切号与旧凭据失效；稳定错误和消费方契约测试 | 当前实现与目标契约对照 |

被替代条目：旧 `/auth/bind {type,credential}` 新客户端主路；前端生成并持久化可直接登录账号的 `deviceId` 模型。

保留不变量：后端永远是账号、绑定、手机归属、凭据失效和新账号创建权威；已绑账号只能手机登录；切已有账号不迁移匿名数据；失败不替换当前会话。`bind_current` 才撤销该匿名账号的设备登录凭据；`switch_existing` 只撤销当前匿名会话，匿名账号及受控恢复凭据必须保留。

## 3. 对象、流程与契约

- 对象/生命周期：`PhoneChallenge(created→verified|expired|locked|superseded)`；`PhoneResolution(created→used|expired)`；手机凭据与设备凭据作为原子确认的边界数据。
- 主流程：输入号码 → 发送验证码 → 校验码 → 返回 `bind_current|switch_existing` 但不改会话 → 用户确认 → 服务端原子绑定/切号并签新会话。
- 安全与可见性：挑战创建不暴露号码是否存在；解析 token 绑当前匿名会话、有效 10 分钟、单次；已绑账号不可再由设备凭据登录。
- 登录生命周期：匿名账号、匿名 session token、device credential 以及本单元签发的已绑定 session 均不按时间或不活跃自动失效；仅明确绑定、切号、主动退出/清除或安全治理撤销。验证码和 resolution 的 5/10 分钟期限保持不变。
- API：`POST /auth/phone/challenges`、`POST /auth/phone/challenges/:challengeId/verify`、`POST /auth/phone/resolutions/:resolutionToken/confirm`；设备会话目标为 `POST /auth/device/session`。四类写操作均使用 `Idempotency-Key`，同键同载荷重放原结果，同键异载荷冲突。
- DTO：challenge=`{challengeId,expiresAt,resendAvailableAt}`；verify=`{resolution,resolutionToken,resolutionExpiresAt}`；confirm=`{accountId,phoneBound:true,sessionToken,deviceCredential:null,returnToAllowed,nextAction,previousAnonymousCredentialDisposition,anonymousRecovery?}`；device session=`{accountId,phoneBound:false,sessionToken,deviceCredential,deviceCredentialAction}`。
- 参数：验证码 5 分钟，重发 60 秒，单挑战错 5 次；手机 5/小时、10/日，设备 10/小时、30/日，IP 20/小时、100/日；resolution 10 分钟。
- 错误：手机号链路包含 `phone_invalid/code_invalid/challenge_expired/challenge_locked/resend_cooldown/rate_limited/resolution_expired/resolution_used/resolution_session_mismatch/phone_ownership_changed/continuation_invalid/sms_provider_unavailable/idempotency_conflict`；设备链路包含 `device_credential_malformed/device_credential_recovery_required/device_session_idempotency_conflict/auth_persistence_unavailable`，统一 `{code,msg,detail,data}`。
- 失败：任一失败保留当前匿名会话；短信不可用不可伪造已发送；原子确认部分失败整笔回滚。
- 场景续接：challenge 接收结构化 `continuation`，首版仅 `none|private_onboarding_generation`；服务端校验归属和状态并把快照绑定到 challenge/resolution，禁止自由 URL。`switch_existing + private_onboarding_generation` 固定不续接；目标失效时完成登录但回安全入口。
- 凭据处置：confirm 的 `deviceCredential:null` 只描述新的已绑活动会话。`switch_existing` 把旧匿名恢复凭据转为独立休眠恢复槽，不能被通用设备入口自动使用；恢复页面/API 另开单元。
- 竞态：verify 仅给归属快照；confirm 前手机号归属变化返回 `phone_ownership_changed`，不得静默改分支。confirm 同一幂等键在响应丢失后重放原成功结果。
- 幂等交付窗：含原始登录/设备/恢复凭据的加密响应只允许在 10 分钟且不超过对应 challenge/resolution 有效期的窗口内重取；过窗或结果凭据被显式撤销时清除可还原密文。活动登录凭据本身仍不自然到期。
- 兼容：项目尚未发布，不保留不安全旧语义；`/auth/bind` 直接退役，旧 `/auth/guest` 同步退出账号恢复主路，不设旧客户端兼容窗。
- 技术冻结：设备凭据错误、`deviceCredentialAction`、`bootstrapNonce + Idempotency-Key` 并发建号去重已按 `API-CONTRACT §19.8–19.9` 冻结；`SmsProvider` 在无真实云账号的测试环境必须显式 stub 且不得在生产装配。

## 4. 任务依赖与所有权

| 任务 | 专业/Owner | 仓库与业务分支 | 允许修改范围 | 依赖 | 状态 |
|---|---|---|---|---|---|
| 身份持久化、挑战/解析/会话 API | 后端 | `echo` / `backend/phone-account-resolution` | 身份表、凭据、会话、频控、SmsProvider 边界与专项测试 | 无外部云账号时可先 stub | 首候选 `13220f9`；补负路径 |
| 全局手机号登录组件与会话替换 | 前端 | `echo-client` / `frontend/phone-account-resolution` | 身份 API、会话/设备凭据存储、绑定/切号窗与 returnTo | 固定后端 DTO/错误 | 候选 `e933848` |
| 身份安全与真联调用例 | QA | 测试资产 / 同任务标识 | 枚举、频控、重放、会话固定、冲突、回滚与消费方恢复 | 可控 SmsProvider | 可准备；候选后执行 |

共享契约唯一 Owner：后端提供固定 DTO/错误/时序与安全约束，产品、前端、QA 共同复核。

合并顺序：后端持久化与提供者契约 → 前端消费与会话替换 → Onboarding 组合联调 → QA → 产品验收。

## 5. 并行评估回执

### 前端回执

ACK：`accepted-with-risks`
预计窗口/条件/置信度：契约冻结和可控后端夹具后 3–4 个工作日，真联调 0.5–1 日；80%。
复用/新增/迁移/替换/废弃/不变：复用 Onboarding 两种归属提示和会话读取入口；新增全局手机号协调器、倒计时/错误状态和版本化会话/恢复凭据存储；替换 `/auth/guest + deviceId` 与 `/auth/bind`；废弃前端 deviceId 作为登录权威。
页面、状态与接口影响：登录窗覆盖输入、发送、倒计时、验证、两种确认、确认中、恢复/重启；成功后重读 `/me`，不沿用匿名 `hasPet`。
风险/阻塞/产品问题：需要冻结 continuation、两分支凭据处置、稳定幂等键和会话寿命；H5 凭据不得进入日志/埋点。
验证计划：契约/状态/reducer/UI/会话专项，全量测试、类型检查、构建和真联调；Mock 不作安全证据。

### 后端回执

ACK：`accepted`
预计窗口/条件/置信度：契约冻结后 6–9 个后端工作日；真实短信另 2–4 日且取决于供应商；70%。
复用/新增/迁移/替换/废弃/不变：复用事务、错误信封、路由和账号表；新增独立身份服务、持久 session/device/phone/challenge/resolution/idempotency/rate/audit；替换内存 token 与 deviceId 权威；退役旧绑定。
数据、接口、状态机与运行影响：token 只存 hash，手机号 hash 唯一且密文保存；生产无 PG/密钥或误装 Stub 必须 fail closed；绑定/切号和全部凭据变化单事务。
风险/阻塞/产品问题：会话不按时间失效已由 `G-35/DC9` 收口；continuation、凭据分支、幂等重放和旧接口策略均已冻结。
验证计划：单元、真 PG、真 HTTP、并发/故障注入、重启持久、隐私日志、真实供应商冒烟。

### QA 回执

ACK：`accepted-with-risks`
可测性：条件可测；冻结后自动化 0.5–1 日、后端候选后真 PG/HTTP 0.5 日、固定双端后浏览器联调 0.5 日。
受影响用例与红线：防枚举、E.164、供应商失败、挑战时限/锁定/重发/频控、resolution 过期/错会话/重放、两分支原子性、响应丢失、归属竞态、设备恢复与旧接口绕过。
环境、数据与联调要求：正式 migration 的真 PostgreSQL、真 HTTP 网关、可控 Clock/SmsProvider、固定双端提交；发布前真实短信冒烟。
风险/阻塞/产品问题：Mock、内存仓和 Provider Stub 均不能替代真 PG、真 HTTP 与真实短信证据。
验证计划：`PH-01`～`PH-30`，覆盖事务故障注入、并发、进程重启、PII 日志与 Onboarding 真浏览器恢复。

## 6. 联合冻结门

- FE_ACK：`accepted-with-risks`（风险已进入冻结契约与验收）
- BE_ACK：`accepted`
- QA_ACK：`accepted-with-risks`（风险已进入冻结契约与验收）
- 冻结契约版本：`phone-account-resolution-v1 @ d6c2090`
- 产品/技术重新定调项：无。不得重新加入 30/180 天或其他自然到期。
- 开工结论：`READY_FOR_DEVELOPMENT`

## 7. 开发、联调与反馈

| 时间 | 角色/任务 | 新差额或证据 | 状态变化 | 下一责任方 |
|---|---|---|---|---|
| 2026-09-06 | 产品 | 从基础总账本拆出第 2 个最小单元；已有 G-28/G-32/G-35 定案不变 | `DISTRIBUTED` | FE/BE/QA 并行评估 |
| 2026-09-07 | FE/BE/QA | 三方只读评估完成；确认 continuation 缺口、两分支凭据范围、幂等重放与旧接口安全封口 | `NEEDS_PRODUCT_DECISION` | 产品确认会话有效期 |
| 2026-09-07 | 产品 | 明确账号与登录凭据不按时间/不活跃失效；验证码与 resolution 短期安全期限不变 | `READY_FOR_DEVELOPMENT` | FE/BE 按独立分支开发 |
| 2026-09-07 | 前端 | 统一手机号协调器、长期活动会话/设备凭据/休眠恢复槽和 Onboarding/我的页接线；身份专项 8/8、全量 164/164、构建 PASS | 候选 `e933848` | QA/后端联调 |
| 2026-09-07 | 后端 | schema `2026090701`、持久身份服务、四类接口、网关鉴权和旧入口退役；编译 PASS、真实 PG 首批专项 5/5 | 首候选 `13220f9` | 补负路径/真 HTTP |
| 2026-09-07 | QA/产品 | 候选审查发现 `nextAction=none` 前端漏接及幂等响应永久可重放；前者已修，后者冻结为短时交付窗 | 阻断返工 | FE/BE |

固定联调契约：`phone-account-resolution-v1 @ d6c2090`；前端 `e933848`；后端首候选 `13220f9`；schema `2026090701`。
真实请求响应证据：真实 PostgreSQL 服务层首批 5/5；真 HTTP 与浏览器证据待补，当前不得宣称端到端完成。

## 8. 缺陷闭环

| 缺陷 | 严重度 | 状态 | Owner | 定案/契约 | 修复提交 | 复验报告 |
|---|---|---|---|---|---|---|

## 9. 验收与归档

- 必须证据：手机号不枚举；挑战过期/锁定/重发/频控；解析 token 单次、场景绑定与幂等恢复；新号原子绑当前账号并撤销其设备凭据；已有号切原账号且匿名资料不迁移、仅当前匿名会话失效、受控匿名恢复凭据保留；已绑账号不可由设备凭据恢复；Onboarding `bind_current/switch_existing` 真联调。
- 迁移/回滚/监控：按后端回执新增持久身份表、把旧 `deviceId` 降为非权威历史字段，并补短信/风控监控；旧接口不得在回滚时恢复不安全语义。
- 最终状态：双端首候选已固定；后端负路径、真 HTTP、真浏览器和真实短信冒烟尚未完成，不可归档。
