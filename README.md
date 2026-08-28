# echo-doc — 产品

Echo 的文档、规格、裁定、比稿图、前后端协议真源与美术资源。

## 概述

读完这一节就等于拿到了本仓的全部结论。

- **本仓是产品侧的唯一落点**：文档、裁定、规格、比稿图、协议真源、静态美术资源都在这里。
  代码不在这里（见下面的边界表）。
- **`proto/` 是前后端协议的唯一真源**，`echo` 仓持有副本。🔴 两份不一致时不报错，
  唯一的补救是 `scripts/proto-check.sh`，而它不会自己跑。
- **`Echo-assets/` 是资源根**，`static/` 随本仓分发；🔴 `runtime/`（用户上传）
  受 PIPL 约束不得入库，`.gitignore` 已硬挡。
- **拆分基准 `67a62ae`（2026-08-28）**，四仓均按快照重开，不带拆分前的改动历史，
  原单仓在本地完整保留。
- **已知欠账三条**，见文末，都不影响本仓自身，影响的是跨仓引用。

## 目录

| 目录 | 内容 |
| --- | --- |
| `docs/` | 全部文档：产品规格、技术设计、裁定记录（`DECISIONS.md`）、工作日志、脑图；`docs/visual/` 是 87 张比稿图 |
| `proto/` | 🔴 前后端协议真源，见 `proto/README.md` |
| `Echo-assets/` | 资源根：`static/`（运营封面、设计参考、文档配图原图）+ `MANIFEST.json` |
| `scripts/` | `assets-check.sh` / `assets-manifest.sh`（资源校验与清单）、`proto-check.sh`（协议一致性） |

想快速了解产品全貌，从 `docs/PRODUCT-MINDMAP.md` 与 `docs/PRODUCT-MAINLINE.md` 入手。

## 仓库边界

| 找什么 | 去哪个仓 |
| --- | --- |
| 服务端代码、建表 SQL、本地运维 | `echo` |
| H5 前端、Unity 旧工程 | `echo-client` |
| 并行工作线监控 skill | `monitor` |

## 前后端怎么从这里读

**协议**：`echo` 仓的 `echo-server/src/main/proto/` 是副本，改动方向只能是
「本仓 `proto/` → 副本」。校验与同步都用 `scripts/proto-check.sh`，详见 `proto/README.md`。

**资源**：两端各一个环境变量指向资源根，缺省值在拆仓后已经不对了——
原先假设 `Echo-assets/` 是代码仓的同级目录，现在它在本仓里。

| 端 | 变量 | 拆仓后该指向 |
| --- | --- | --- |
| 前端（开发/预览） | `ECHO_ASSETS_DIR` | 本仓 clone 路径 + `/Echo-assets` |
| 前端（生产构建） | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 |
| 后端 | `ECHO_STORAGE_DIR` | 仓外的 `runtime/uploads`，**不在本仓** |

`scripts/assets-check.sh` 的缺省已经跟着改了；🔴 **前端 `vite.config.ts` 那个没有**，
见下面的欠账。

## 🔴 拆分留下的三条欠账

1. **前端资源根缺省失效且不报错。** `echo-client` 仓 `echo-h5-proto/vite.config.ts:64`
   仍回落到 `../../Echo-assets`，那是单仓时代的相对位置。拆仓后这个路径不存在，
   而 vite 只 warn 不 fail，表现是**封面图全部裂开但构建成功**。
   在 `echo-client` 仓设 `ECHO_ASSETS_DIR` 可绕过，但缺省值本身该改。
2. **`docs/ASSETS.md` 与 `Echo-assets/README.md` 还写着「资源根刻意放在代码仓库之外」。**
   那条前提在本次拆分中被推翻了（`static/` 进了本仓），两份文档需要跟着改口径，
   并按项目规矩保留原文、标注推翻时间与原因。
3. **`docs/PLAN-repo-split.md` 已经过期。** 它记的是 2026-08-27 的勘察（172 个提交、
   计划用 `filter-repo` 保留历史），而实际执行是 8-28、334 个提交、快照重开。
   §3（命名撞车）与 §5（数量校验必须钉 SHA）两节仍然成立且有价值，其余已不作数。

## 拆分来源

从单仓 `Echo` 于 2026-08-28 按快照拆出，基准 `67a62ae1702322cc051eb240375359e06f6614f8`。
