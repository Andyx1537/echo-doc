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

**资源**：资源根就是本仓的 `Echo-assets/`。两端的缺省都已跟着拆仓改过（见 `docs/ASSETS.md §3`）。

| 端 | 变量 | 指向 | 缺省 |
| --- | --- | --- | --- |
| 前端（开发/预览） | `ECHO_ASSETS_DIR` | 本仓的 `Echo-assets/` | `../../echo-doc/Echo-assets` |
| 前端（生产构建） | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 | 空 |
| 后端 | `ECHO_STORAGE_DIR` | 持久卷上的上传落点 | `<cwd>/data/uploads` |

🔴 **后端那一格不要跟着前端对齐指进本仓。** 它是用户上传的落点，`Echo-assets/runtime/`
虽然被 `.gitignore` 挡着不会入库，但指过去照样是错的——`git clean` 或换机器时数据就没了，
而在那之前不报任何错。

`scripts/assets-check.sh` 与前端 `vite.config.ts`／`.env.example` 的缺省都已改完并实测过。

## 🔴 拆分留下的欠账

1. ~~前端资源根缺省失效~~ **已修**（2026-08-29，`echo-client` 仓 `855b464` 之前那个提交）：
   缺省从 `../../Echo-assets` 改成 `../../echo-doc/Echo-assets`。
   原缺省的危险不在于失效，而在于**工作区里那份遗留副本多半还在**——
   旧路径能读到东西，只是过期物料，不裂开、不报错，比直接失败难发现得多。
2. ~~文档正文里还有约 140 处旧路径前缀~~ **已清**（2026-08-30）。判准是
   **指路的改，记事的不改**：改了之后引用能打开、且不改变对过去行为的陈述的就改；
   本身就是「本轮未修改 `Echo/docs/` 下任何文档」这类**行为记录**的一律保留。

   | 类别 | 处数 | 结果 |
   | --- | --- | --- |
   | `docs/visual/` 三份文档里的图片绝对路径 | 39 | 改成相对路径（同目录互指），31 条图链逐条验过能打开 |
   | 代码引用块 ```` ```N:M:Echo/… ```` | 12 | 改成 `echo/` 与 `echo-client/`，9 个目标文件逐个验过存在 |
   | 活指针（`ART`/`PRD`/`QA-CHARTER`/`shot-taxonomy.json` 等） | 12 | 改成仓内相对路径，JSON 重新解析通过 |
   | `echo` 仓 `deploy/` 里的 `cd` 与注释 | 3 | 改掉，见 `echo` 仓 `7dd6bd6` |
   | 行为记录（WORKLOG、QA 报告、各规格的「本轮边界」栏） | 18 | 🔴 **不改**——记的是当时的事实 |

   🔴 无差别 sed 会把历史记录改成一段从没发生过的事，那比路径失效更糟。

   顺带查出一处**图片本身丢了**：`README-cards.md` 引用的 `stranger-v2-full.png`
   全工作区检索无果，已就地标注"没有留存"，不留成一条看起来能打开的死链。
3. ~~`docs/ASSETS.md` 与 `Echo-assets/README.md` 的「资源根在仓外」前提~~
   **已改**（2026-08-30，`38da7a4`）：核心规则拆成强度不同的两条——用户上传物不进仓是
   红线，可分发物料入库是取舍；旧结论原文保留并标了推翻时间与理由。
4. ~~`docs/PLAN-repo-split.md` 已经过期~~ **已降级为存档**（2026-08-30，`9d85785`）：
   新增 §0.0 逐条列出被执行推翻的项。其中最值得看的是勘察本身的漏项——
   拿 `git ls-tree` 列顶层，必然看不见没被版本控制的 `Echo-assets/`，
   也看不出 `proto/` 是共享契约，**而清单看起来是完整的**。

## 拆分来源与工作区布局

从单仓 `Echo` 于 2026-08-28 按快照拆出，基准 `67a62ae1702322cc051eb240375359e06f6614f8`。
2026-08-29 起**新仓为权威**，原单仓改名 `Echo-legacy/` 只读归档，不再在里面干活。

四个仓建议并排克隆——`echo-client` 的资源根缺省与 `proto-check.sh` 的仓定位都按这个布局算：

```
workSpace/
├── echo/            服务端
├── echo-client/     前端（echo-h5-proto/ 活跃，unity-legacy/ 冻结）
├── echo-doc/        本仓
├── agent-supervision/   监控 skill（远端是 monitor.git）
├── Echo-assets/     🔴 遗留副本：static 已随本仓入库，这里只有 runtime/uploads 还有用
└── Echo-legacy/     单仓归档，只读
```

🔴 `Echo-assets/static/` 现在是本仓 `Echo-assets/static/` 的过期重复品，
留着是因为同目录下的 `runtime/uploads/` 仍是后端 `ECHO_STORAGE_DIR` 的落点，不能整个删。
清理时**只删 `static/` 与 `.backup/`，不要动 `runtime/`**。
