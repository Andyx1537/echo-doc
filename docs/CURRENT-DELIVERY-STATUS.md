# 当前执行进展与两端架构对照

更新时间：2026-09-17。回到用户确认的七个最小单元，不以局部测试代替整版完成。

## 当前完成态

- 两专业架构梳理：已完成代码核查与相互对照。后端表/FK/JSON承载与前端页面/动作/展示，用B01—B07同一编号连接。
- 私域正常主路径：单照片→单宠裁切→四题→新号绑定→原资料续接→开发候选→授权→确认建窗，真实浏览器与PG已走通；关闭重开恢复第四题已验证。
- 七单元可做块与私域可做恢复已合 develop。定妆图生图已接万相，建档页用上传肖像走出三张绘本定妆。漫画/视频、真短信仍后置；不得用百分比掩盖未过门项。

## 两专业交付入口

| 业务节点 | 前端承载与操作 | 后端承载与关系 |
|---|---|---|
| B01 身份 | 手机弹窗、绑定/切号确认、原路返回 | account/session/device/phone/challenge/resolution |
| B02 建档 | 上传、选宠裁切、四题与总结 | onboarding_session和五张JSON投影、resource |
| B03 生成建窗 | 生成查询、候选、授权、最终确认 | anchor/job/candidates、确认事务、petId=windowId |
| B04 作品审核 | 发布页、作品墙、状态与管理入口 | work及目标审核凭证/单通道/重提 |
| B05 Plaza | 公共瀑布流、全屏单卡与作者主页 | 已合 develop：只发已公开作品，点进全屏单卡，左滑进作者主页，主页墙读公开作品；从主页再进全屏或评论不卸掉主页；广场全屏进评论不卸掉全屏；想说的话进同一条详情；匿名批次与广场 reqId 快照已落库；网格或他人主页点进全屏驻留满一秒才记 n |
| B06 互动收藏 | 两层评论、登录展开、私有收藏 | 已合 develop：游客三加二，收藏无私有计数；游客进「我的收藏」按 1002 出绑定，不再当成空页；我的作品 / 收藏进详情不卸掉墙 |
| B07 行为 | 事件采集与主动反馈 | 已合 develop：收下、服务端记账、反馈与软清除 |

- [后端架构拓扑与数据承载](architecture/BACKEND-TOPOLOGY.md)：系统图、ER、真实PK/FK及逻辑关联、表内数据、接口写表、缺失。
- [前端架构拓扑与操作流](architecture/FRONTEND-TOPOLOGY.md)：页面图、操作分支、展示字段、接口与状态来源、缺失。

## 七单元总清单

| 顺序 | 已确认任务 | 当前结果 | 未完成/下一责任 |
|---|---|---|---|
| 1 | private-onboarding-session | 已有实现；新号正常浏览器主链贯通。挂死收成、写后读、切号空草稿已合 develop。定妆真出图已在独立联调页走出三张。候选图落本方盘已合 `echo@6cc7d2a`（编码未配则失败，不挂供应商链） | 漫画/视频、真短信后置 |
| 2 | phone-account-resolution | 固定9999开发增量QA PASS，真实新号绑定，HTTP已有号切换通过；切号不迁资料已由专项测试锁住 | I01/I09 已合 develop；阿里云后置 |
| 3 | work-publication-review | 名额/墙/重提/凭证复用已合 develop。并发双发唯一约束 `echo@0c5e9ce`。人工通过/驳回已合 `echo@ed46982`。下架/恢复已合 `echo@ad088ef`。作者申诉一次与主管维持/推翻已合 `echo@cab832a`。C 端「看看为什么」已合 `echo-client@7decd24`。内容运营台（作品/回忆卡/开关）已合 `echo@206c1ab` / `echo-client@94d1f00`（`?ops=`）。回忆卡已公开可下架已合 `echo-client@9cc1f07`（下架后不能直接恢复） | 举报提交规格未定；看板/TOTP/客服/收入后置 |
| 4 | plaza-work-read | 广场只读公开作品；匿名两小时一批约 30 条，批次已落库。reqId 快照已落库（`echo@c9348a6`）。点网格进全屏已合 `echo-client@c1bf7c9`。左滑进作者主页已合 `echo-client@515c240`。主页墙改读作品已合 `echo-client@f20e8c7`。主页进全屏不卸挂已合 `echo-client@05ffe53`。主页全屏进评论不卸挂已合 `echo-client@a027592`。广场全屏进评论不卸挂已合 `echo-client@59fea15`。网格进全屏记 n 已合 `echo@22a190d` / `echo-client@dfc48cc`。作者主页进全屏记 n 已合 `echo@56542d7` / `echo-client@d1ec754` | 账本 CLOSED |
| 5 | work-comments-favorites | 详情三加二、展开登录、私有收藏。已合 develop。游客收藏入口 1002 已改成绑定提示（`echo-client@78da741`）。我的作品 / 收藏进详情不卸挂已合 `echo-client@82ebbd7` | 账本 CLOSED |
| 6 | behavior-phase0-ledger | 收下、服务端成功事实、明确反馈、软清除。已合 develop | 账本 CLOSED |
| 7 | foundation-combination-e2e | 广场到详情到评论收藏一条链。已合 develop。评论/收藏已接 PG，隔离库组合 1/1 | 账本 CLOSED |

## 精确缺失登记

| 编号 | 缺失 | 状态/责任 |
|---|---|---|
| I01 | 已有手机号切换后新建档、重传、不迁移源资料 | 专项测试已锁。账本已关闭。已随 I09 合入 develop |
| I02 | 生成查询失败后的重新查询交互 | 只重 GET 已合 develop（`echo-client@4c96d62`） |
| I03 | 生成任务中断后的服务端交代 | 启动收成失败已合 develop（`echo@4b7b2f0`） |
| I04 | 开发候选错误显示内部评审JSON | 已关闭：BE修复、专项通过，更新后真实页面显示开发预览文案而非评分JSON |
| I05 | 真正宠物图片/漫画/视频生成；主体/素材/事实快照消费 | 定妆：万相 img2img 已浏览器走出三张（竖图须按图生图尺寸，不能走视觉 768 压缩）。候选图落本方盘已合 `echo@6cc7d2a`。漫画/视频仍未做 |
| I06 | 选宠后追加素材入口、视频首传反馈 | 建档内不做（`ON1`/`ON2`）。补素材后置。选宠只收图片：上传已拒视频（`echo@42c205f` / `echo-client@abcb002`） |
| I07 | 建档写成功但后续GET失败的恢复、幂等键复用 | 复用钥匙已合 develop（`echo-client@4c96d62`） |
| I08 | 前后端功能分支合入develop及整版标签 | 已合 develop，未打 Tag。后端 `echo@42ed8ce`，前端 `echo-client@177bbcd`。夹具红灯不在公共区做 |
| I09 | 切号后受控唤醒旧匿名会话 | mock 整链 + 隔离 PG 真接口已过。已合 develop：`echo@5564fdc` / `echo-client@fafacb1`。账本 CLOSED |

## 版本与证据

- 文档之前基线：76f8a1d；本次文档以当前develop提交为准。
- 后端：`develop` @ `6cc7d2a`（定妆图落盘；功能头 `62a8ff2`）。
- 前端：`develop` @ `9cc1f07`（回忆卡下架；功能头 `15c003f`）。
- schema：2026091409（工单含 `appealing`；`appealAt` 只写一次）。9 月 8 日旧联调栈 5180/18080 已停；不要再当占用。短信固定9999。
- 本轮：定妆候选落本方盘已合 `echo@6cc7d2a`。体系见 [OPS-CANDIDATE-PERSIST.md](OPS-CANDIDATE-PERSIST.md)。真出图须配 `ECHO_AIGC_PROVIDER_CODE`。漫画/视频、真短信、打 Tag、看板仍后置。
- 工作备忘（2026-09-17）：图像和吃 CPU 的预览一律系统 Chrome，禁止塞进 Cursor 对话或内置浏览框。见 [MEMO-preview-to-external-browser.md](MEMO-preview-to-external-browser.md)。
- QA核查：两拓扑对应一致；正常主路径证据来自主执行者浏览器，QA未独立重跑；仍须收尾复验，不签完整私域PASS。
- 原“手机号接口404阻塞建档”已解除，旧账本该记录仅作历史。
