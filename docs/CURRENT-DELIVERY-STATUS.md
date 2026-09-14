# 当前执行进展与两端架构对照

更新时间：2026-09-14。回到用户确认的七个最小单元，不以局部测试代替整版完成。

## 当前完成态

- 两专业架构梳理：已完成代码核查与相互对照。后端表/FK/JSON承载与前端页面/动作/展示，用B01—B07同一编号连接。
- 私域正常主路径：单照片→单宠裁切→四题→新号绑定→原资料续接→开发候选→授权→确认建窗，真实浏览器与PG已走通；关闭重开恢复第四题已验证。
- 当前不是完整私域验收或整版完成。旧号重传、异常恢复、媒体生成等缺口见下表；不得用百分比掩盖未过门项。

## 两专业交付入口

| 业务节点 | 前端承载与操作 | 后端承载与关系 |
|---|---|---|
| B01 身份 | 手机弹窗、绑定/切号确认、原路返回 | account/session/device/phone/challenge/resolution |
| B02 建档 | 上传、选宠裁切、四题与总结 | onboarding_session和五张JSON投影、resource |
| B03 生成建窗 | 生成查询、候选、授权、最终确认 | anchor/job/candidates、确认事务、petId=windowId |
| B04 作品审核 | 发布页、作品墙、状态与管理入口 | work及目标审核凭证/单通道/重提 |
| B05 Plaza | 公共瀑布流与详情导航 | 功能分支已改发 Work 公开投影；未合 develop |
| B06 互动收藏 | 两层评论、登录展开、私有收藏 | 功能分支已接 workId 评论/收藏；未合 develop |
| B07 行为 | 事件采集与主动反馈 | 功能分支已接下、反馈与开关；未合 develop |

- [后端架构拓扑与数据承载](architecture/BACKEND-TOPOLOGY.md)：系统图、ER、真实PK/FK及逻辑关联、表内数据、接口写表、缺失。
- [前端架构拓扑与操作流](architecture/FRONTEND-TOPOLOGY.md)：页面图、操作分支、展示字段、接口与状态来源、缺失。

## 七单元总清单

| 顺序 | 已确认任务 | 当前结果 | 未完成/下一责任 |
|---|---|---|---|
| 1 | private-onboarding-session | 已有实现；新号正常浏览器主链贯通。挂死收成失败、写后读失败、切号空草稿已锁 | 真媒体与短信后置；功能分支未合 develop |
| 2 | phone-account-resolution | 固定9999开发增量QA PASS，真实新号绑定，HTTP已有号切换通过；切号不迁资料已由专项测试锁住 | I01/I09 已合 develop；阿里云后置 |
| 3 | work-publication-review | 产品契约冻结；名额/墙/重提/凭证复用已锁功能分支 | 账本 CLOSED。未合 develop |
| 4 | plaza-work-read | 广场已改读公开作品；匿名两小时一批约 30 条 | 账本 CLOSED。功能分支未合 develop |
| 5 | work-comments-favorites | 详情三加二、展开登录、私有收藏 | 账本 CLOSED。`echo@2bf949a` / `echo-client@3e1dd90`。未合 develop |
| 6 | behavior-phase0-ledger | 收下、服务端成功事实、明确反馈、软清除 | 账本 CLOSED。`echo@8e0497d` / `echo-client@c92f94a`。未合 develop |
| 7 | foundation-combination-e2e | 未完成 | 各单元通过后整线组合 |

## 精确缺失登记

| 编号 | 缺失 | 状态/责任 |
|---|---|---|
| I01 | 已有手机号切换后新建档、重传、不迁移源资料 | 专项测试已锁。账本已关闭。已随 I09 合入 develop |
| I02 | 生成查询失败后的重新查询交互 | 只重 GET 已锁。`echo-client@6bc6585`。未合 develop |
| I03 | 生成任务中断后的服务端交代 | 启动收成失败已推 `echo@defff3a`。未合 develop |
| I04 | 开发候选错误显示内部评审JSON | 已关闭：BE修复、专项通过，更新后真实页面显示开发预览文案而非评分JSON |
| I05 | 真正宠物图片/漫画/视频生成；主体/素材/事实快照消费 | 未实现完整媒体链 / 生成单元 |
| I06 | 选宠后追加素材入口、视频首传反馈 | 建档内不做（`ON1`/`ON2`）。补素材后置；选宠只收图片 |
| I07 | 建档写成功但后续GET失败的恢复、幂等键复用 | 前端已复用钥匙 `echo-client@bc68c42`。vitest 170/170。未合 develop |
| I08 | 前后端功能分支合入develop及整版标签 | 合入已完成，未打 Tag。后端 `echo@c4fbc69`，前端 `echo-client@55053e5`。账本 `docs/handoff/I08-archive-integration.md`。测试夹具红灯不在公共区做 |
| I09 | 切号后受控唤醒旧匿名会话 | mock 整链 + 隔离 PG 真接口已过。已合 develop：`echo@5564fdc` / `echo-client@fafacb1`。账本 CLOSED |

## 版本与证据

- 文档之前基线：76f8a1d；本次文档以当前develop提交为准。
- 后端：`develop` @ `5564fdc`（含 I01 `20759ac`、I09 `6d2b1b3`）。
- 前端：`develop` @ `fafacb1`（含 I01 `54298de`、I09 `5c4efde`）。
- schema：2026090702；开发API 18080、页面5180；真实PostgreSQL，短信固定9999；视觉/生成使用开发适配器，非真实模型效果验收。
- 本轮：行为账本已关（`echo@8e0497d` / `echo-client@c92f94a`）。影子假设怎么算还没有冻结算法，没编打分。未合 develop，未打 Tag。
- QA核查：两拓扑对应一致；正常主路径证据来自主执行者浏览器，QA未独立重跑；仍须收尾复验，不签完整私域PASS。
- 原“手机号接口404阻塞建档”已解除，旧账本该记录仅作历史。七单元功能块已齐到行为；下一本是整线组合。
