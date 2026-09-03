# 回声三仓开发状态对齐 · 2026-09-03

> 类型：基线摸底，不代表发布验收。
> 统一基线标记：`baseline-2026.09.03`。
> 产品状态来源：`docs/delivery/PD-20260903-product-foundation-v34/MANIFEST.md`。

## 1. 仓库与已提交基线

| 仓库 | `develop` 基线 | 已提交能力摘要 | 未进入基线的本地修改 |
|---|---|---|---|
| 产品文档 | 本报告提交前为 `c927635`，本报告提交后以远端 `develop` 为准 | G-27～G-30、公共开发标准、级联交付与三方反馈闭环 | 无 |
| 服务端 | `22ecbf9` | 统一持久化基础、作品表及发布/列表/详情/软删骨架、匿名账号和绑定骨架、旧卡审核与安全能力 | 2 个测试文件，共 54 增/6 删，未确认归属、未纳入基线 |
| 客户端 | `5dfbc5b` | 作品发布页、作品瀑布与基础 Work 类型/适配器 | 9 个 H5 文件，共 129 增/41 删，未确认归属、未纳入基线 |

三个仓的提交哈希不同是正常的；它们通过同一基线 Tag 名、交付编号、产品提交和契约版本建立对应关系。

## 2. 当前产品与实现差额

| 领域 | 产品目标 | 服务端状态 | 客户端状态 | 联合结论 |
|---|---|---|---|---|
| Plaza/作品墙 | Plaza 只分发 Work，Works 是作品墙 | 作品公开读面与旧 Card Plaza 并存 | 有 Works 瀑布骨架，主 App 仍有旧广场链 | 未对齐，需冻结 Work DTO 与迁移路径 |
| 作品详情 | 匿名可读，公开互动归 workId | 基础作品详情存在，互动/评论/作者投影缺失 | 无完整 WorkDetail 链，卡片入口未闭合 | 未对齐 |
| 审核复用 | 有效公开凭证可复用，否则作品审核 | 只有卡审核基础设施，作品完整状态机和凭证缺失 | 仅列表状态角标，无作者审核详情/申诉 | 未对齐 |
| 匿名与手机号 | 匿名有限浏览/试填，生成和写操作前绑定，原账号升级 | 匿名与通用绑定骨架存在，短信挑战/批次账本缺失 | 有匿名 token 和通用错误，独立手机号流程与原路续接缺失 | 未对齐 |
| 单宠建档 | 一窗一宠、四题问卷、确认后原子建窗 | 会话/事实分存/目标状态机未实现 | 新目标页面链未核实完成 | 未对齐 |
| 行为适配 | 四账本、三域隔离、Phase 0 仅影子 | 尚无四账本与受控字典 | 尚无冻结事件字典接入 | 可设计骨架，不能接线上排序 |

## 3. 当前开发门禁

首轮级联回执为：前端 `accepted-with-risks`、后端 `accepted-with-blockers`、QA `REWORK`。所以本次分支与 Tag 只做状态对齐，不表示允许跨端开发或发布。

恢复开发前必须先完成：

1. Work 的 Plaza、详情、互动、评论、审核、申诉和消息唯一契约；
2. 手机验证码、匿名批次和绑定冲突契约；
3. 单宠建档请求、响应、错误、恢复、幂等与并发契约；
4. 行为层首批事件/动作/假设字典；
5. G-27～G-30 对应的统一验收基线。

## 4. 本地未提交修改保护

### 服务端

- `echo-server/src/test/java/com/echo/http/BlockSilentFailureTest.java`
- `echo-server/src/test/java/com/echo/http/WindowVisibilityTrimTest.java`

### 客户端

- `echo-h5-proto/src/App.tsx`
- `echo-h5-proto/src/api/backend.ts`
- `echo-h5-proto/src/api/feedLogic.test.ts`
- `echo-h5-proto/src/api/feedLogic.ts`
- `echo-h5-proto/src/api/http.test.ts`
- `echo-h5-proto/src/api/http.ts`
- `echo-h5-proto/src/api/mock.ts`
- `echo-h5-proto/src/components/PlazaScreen.tsx`
- `echo-h5-proto/src/types.ts`

以上修改已随工作区保留在各自 `develop`，但不属于 `baseline-2026.09.03`。确认归属前不得覆盖、删除、暂存或混入其他任务。

## 5. 后续状态同步格式

每次产品定案或技术交付后，在对应级联账本更新：文档 `develop` 提交、客户端 `develop` 提交、服务端 `develop` 提交、契约版本、被测构建、QA报告和剩余差异。只发送新差额，不要求技术重新通读全部历史。
