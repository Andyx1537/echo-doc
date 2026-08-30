# 作品域规格（SPEC-works）

> 状态：v0.1 · 2026-08-30 · 首版随实现一起落
> 关联：`PRODUCT-IMPLEMENTATION-AUDIT §0`（主线第 10 步无入口）、`§0b`（广场契约不一致）
> 实现：`echo` 仓 `t_work` / `WorksApi` / `WorkStore`；`echo-client` 仓 `PublishScreen` / `WorksFeedScreen`

## 概述

**本次落地补上了主线第 10 步。** 此前服务端没有任何创建可发布内容的入口，
审核、分发、曝光整条下游只能处理测试代码手塞的数据。现在有了。

已拍板并已实现的结论：

1. **作品与回忆卡分开建模，各有各的发布页。** 回忆卡是私域产物（用户什么都不做也会长出来，
   默认私密）；作品是公开物（每一条对应一次明确的作者意图）。两者由 `t_work.sourceCardId`
   外键连接——作者把一张回忆卡「发出去」，就长出一个作品，外键记住来路。
2. **发布口从第一天同时收图片与视频。** AI 生成管线接进来时不需要再改契约。
3. **发布 ≠ 公开。** `POST /works` 落 `status='pending'`，回执文案是「已提交」。
   依据 `DECISIONS OM3`（生成/发布/过审是三个时刻，不得合并）。
4. **AI 生成标识 `aiGenerated` 独立成列，不从外键 join 推导。** 来路卡被删不该让作品
   变成「非 AI 生成」——那是对监管说的假话。列表面每一条都下发这个键（S-8 显式标识）。
5. **服务端存原始宽高，不存 `tall`/`short` 档位。** 瀑布错落是渲染决定，档位会把布局焊进数据。
6. **软删（G0-1）。** `WorkStore` 不提供物理删除方法；所有读路径带 `deletedAt IS NULL`。
7. **一张回忆卡只能发出一个未删除的作品**（局部唯一索引，S-7）。删掉之后可以重发。

🔴 **仍然待定的**：

- **广场（`/plaza`）到底展示什么** —— 现在服务端发回忆卡、前端按「窗」解析，两边对不上
  （`§0b`）。作品瀑布走的是独立的 `GET /works`，**刻意没有复用那条链路**。
  要收口得先拍板广场是「窗的瀑布」「卡的瀑布」还是「作品的瀑布」。
- **AI 生成的视频从哪来** —— `GeneratedMediaPublisher` 的类注释写明「Echo 当前不生成
  任何图片/音频/视频，AI 只产出文本」。发布口已经能收视频，但**生成侧不存在**。
  定它需要先做 AI 中台那条线（`PLAN-worklines-20260830` L2）。
- **`originType` 对 AI 作品怎么记** —— 该列只有 `user | official`，是运营口径不是 AI 口径。
  AI 生成、用户发布的作品算 `user` 就会进北极星分母，而北极星要看的是「真人发的卡有没有人理」。
- **视频首帧谁来抽** —— 库约束（`t_work_ck_video_poster`）已经强制视频必须有 `posterKey`，
  但客户端目前没有抽帧实现，前端暂时拿素材本身顶替。定它需要选客户端抽帧还是服务端转码。
- **媒体下发的鉴权与吊销** —— `GET /api/v1/files/{key}` 无鉴权无吊销，作品下架后 URL 仍可开，
  与 `CM-G4` 冲突。归属安全线（L1 `E1`/`E5`）。⚠️ 同线的 `E4`（素材归属）已于 2026-08-30
  修完（`echo@c97da41`，见 `SPEC-security §4.14 E4`），顺带补出 `t_resource`——
  它是吊销的前置：`IStorage` 没有 delete 方法，要清字节得先知道有哪些 key。
- 🔴 **`t_work.status` 没有「生成中」这一态** —— 现有六态（`draft`/`pending`/`public`/
  `rejected`/`takendown`/`appealing`）默认媒体在发布那一刻已经存在。而 AI 生成是异步的
  （`ILlmClient.complete` 是 20 秒同步调用，连异步任务模型都还没有），生成期间这条作品
  处在哪一态、`mediaKey` 填什么，现在无解。**定它必须和异步任务模型一起定**，
  单独给枚举加一个值只会造出一批 `mediaKey` 为空却又不是草稿的行。
  来源：`TECH-AI-PLATFORM` 视频作品九项缺口盘点。

## 1. 数据模型

`t_work`，建表语句在 `echo/echo-server/src/main/resources/sql/schema.sql` 末尾。

| 列 | 说明 |
|---|---|
| `sourceCardId` | 来路回忆卡。自制上传为 `NULL`——🔴 是合法值，不要用 0 代替 |
| `mediaType` | `image \| video` |
| `mediaKey` / `posterKey` | `POST /upload` 返回的 resourceId。视频必须另有首帧 |
| `durationMs` / `width` / `height` | 客户端读出后带上 |
| `visibility` | `private \| friends \| public` |
| `status` | `draft \| pending \| public \| rejected \| takendown \| appealing \| deleted` |
| `originType` | `user \| official`，无默认值（G-1 前置闸门，漏写则报错） |
| `aiGenerated` | 独立列，见概述第 4 条 |
| `deletedAt/By/Reason` | 软删三列（G0-1） |

**状态比回忆卡少两态**，是刻意的：`active` 在卡那边表示「已存在但未公开」，
而作品没有这种中间态（没发布就是 `draft`）；`blocked` 是机审直拦，
作品走的是先 `pending` 后人工，没有机审直拦这条路。

## 2. 端点

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| POST | `/works` | 登录 + **绑定**（S1′） | 发布。落 `pending` |
| GET | `/works` | 登录 | 作品瀑布，过拉黑 |
| GET | `/works/:workId` | 登录 | 详情，含正文全文 |
| GET | `/users/:userId/works` | 登录 | 个人作品页。本人可见未公开的 |
| DELETE | `/works/:workId` | 登录 | 作者软删自己的作品 |

**下发面拆成两个方法**（`WorkView.listItem` / `detail`），不是一个带 flag 的：
合并之后漏传一个 `false` 就是正文全文泄漏，而这个漏传在页面上看不出来。

**不可见一律回 404**，不区分「不存在」与「你看不了」——区分开来等于泄漏「它存在」。

## 3. 前端

`PublishScreen` 三态：`pick`（选素材）→ `edit`（填写）→ `done`（已提交）。
`WorksFeedScreen` 一个组件两种用法，「广场」看全站公开作品，「我的」看自己的（含审核中）。

瀑布按累计高度往矮的那一列放，比奇偶分列更贴近真实错落。

### 3.1 出图核对（390 视口）

六态实拍见 `docs/visual/works/`。**两处布局问题是出图才看出来的**，光读代码判断不了：

- 第一版「发布」按钮跟着内容走，390×844 上掉出折线——页面看起来「没有发布入口」。
- 改成 `position: sticky` 之后，它压住了「谁能看见」那一栏，标题被切掉半行，
  看起来像渲染坏了。**最终解是把页脚移出滚动区**，内容自己滚、页脚固定。

## 4. mock

`echo-client/echo-h5-proto/src/api/worksMock.ts`。种子用 `echo-doc/Echo-assets/static/seed-covers/`
的**真实封面**，宽高刻意造得散（2:3 到 4:5 之间，另有两条横构图）——
样本全挤在同一比例里，有没有按真实宽高排版会长得一模一样，对比就白做了。

种子里分两条挂到当前用户名下（一条 `public`、一条 `pending`），
否则「我的作品」永远是空的，验不到「审核中」角标长什么样。

🔴 mock 的 `deleteWork` 是真删数组，服务端是软删。对前端行为等价，别照着 mock 理解后端语义。
