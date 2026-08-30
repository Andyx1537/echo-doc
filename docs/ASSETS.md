# 资源管理规范

**约束对象**：一切二进制物料——运营封面、设计稿、文档配图、用户上传的照片/音视频。

**核心规则（两条，强度不同）**：

1. **用户上传物永不进任何仓库。** 这是合规红线，无例外。
2. **可分发物料随 `echo-doc` 仓分发。** 这是权衡后的选择，不是红线。

## 0. 2026-08-30 更正：旧前提已被拆仓推翻

本文原先写的是"**物料不进代码库**，资源根刻意放在仓库之外"。**该前提在 2026-08-28
拆仓时被推翻**：产品侧仓 `echo-doc` 被定义为承载美术源文件，`Echo-assets/static/`
（31MB、133 个文件）因此**已经入库**。

推翻的原因不是原判断错了，而是取舍变了——原判断只算了 git 体积这一笔账，
拆仓后要算的是另一笔：物料散在仓外时，克隆下来的仓跑不起来，新人得额外拿一次资源包，
而这件事没有任何机制保证会发生。**用 31MB 的仓体积换"clone 完就能跑"**，是明知代价的选择。

两条规则里只有第 1 条是红线：`runtime/` 至今被 `echo-doc/.gitignore` 硬封，一步没让。

## 1. 为什么当初要挡

首次提交把 33 张 PNG（多数单张 2MB 以上）灌进了版本库，`.git` 因此撑到 65MB，
而代码本身只有几 MB。图片改一次就在历史里多存一份完整副本，git 的增量压缩对二进制基本无效。

这条顾虑今天**仍然成立**，只是被上面那笔取舍接受了。**它没有失效，是被付掉了**——
所以加物料前照样得压到 200KB 以内（§5），别把付掉的额度当成没有额度。

用户上传物那一条是另一回事：一旦误入版本库，删除请求就没法真正兑现。
那是合规问题，不是体积问题，**不参与任何取舍**。

## 2. 资源根

资源根就是 **`echo-doc/Echo-assets/`**，跟着 `echo-doc` 仓走。

```
workSpace/
├── echo/            ← 服务端仓
├── echo-client/     ← 前端仓（echo-h5-proto + unity-legacy）
└── echo-doc/        ← 产品仓
    └── Echo-assets/     ← 资源根
        ├── MANIFEST.json
        ├── static/      ← 可分发，已随本仓入库
        │   ├── seed-covers/
        │   │   └── thumb/    ← 同名缩略档
        │   ├── design-ref/
        │   └── docs/
        └── runtime/     ← 不可分发，被 .gitignore 硬封，本地才有
            └── uploads/
```

`runtime/` 这一层在仓里是**看不到的**——它只在跑过后端的机器上存在。
在别人的 clone 里没有这个目录，属于正常，不要以为是漏拉了。

### static 与 runtime 必须分开

| | `static/` | `runtime/` |
| --- | --- | --- |
| 内容 | 内部生成的运营物料、设计稿 | 用户上传的照片/音视频 |
| 敏感度 | 无个人信息 | 敏感个人信息，受 PIPL 约束 |
| 可否同步给团队 | 可以 | **不可以** |
| 可否进构建产物/CDN | 可以 | **不可以** |
| 删除/撤回授权时 | 无关 | 必须能连带清理，见 `SPEC-trust-and-compliance` |

这条分区是合规红线。把两者混在一个目录，等于让用户隐私数据跟着构建流水线到处跑。

## 3. 配置

| 端 | 变量 | 指向 | 缺省 |
| --- | --- | --- | --- |
| 前端 开发/预览 | `ECHO_ASSETS_DIR` | 资源根绝对路径 | `../../echo-doc/Echo-assets` |
| 前端 生产构建 | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 | 空 |
| 后端 | `ECHO_STORAGE_DIR` | 持久卷上的上传落点 | `<cwd>/data/uploads` |

前端缺省值已对准 `echo-client` 与 `echo-doc` 并排克隆的布局，不配变量即可跑通。

🔴 **后端那一格与前端不是同一个东西，别顺手对齐。** `ECHO_STORAGE_DIR` 是用户上传的落点，
它**不该**指进任何 git 仓——包括 `echo-doc/Echo-assets/runtime/`。生产环境指持久卷
（见 `DEPLOY.md`），本地开发用缺省的 `<cwd>/data/uploads` 就行。

指进仓内目录不会立刻报错，`.gitignore` 也会挡住入库，**所以这个错误是静默的**：
它只在有人 `git clean -xdf` 或换机器时才暴露成"用户照片没了"。

## 4. 前端怎么取址

统一走 `src/lib/assetUrl.ts`，**不要手写 `/assets/` 字面量**：

```ts
import { assetUrl } from '../lib/assetUrl'

imageUrl: assetUrl('seed-covers/cover-pet-collar.jpg')
```

- 开发/预览：`vite.config.ts` 的 `externalAssets` 中间件把 `/assets/**`
  映射到 `<资源根>/static/**`，直接读磁盘，带目录穿越防护。
- 生产：`VITE_ASSET_BASE_URL` 存在时输出 `${BASE}/seed-covers/xxx.jpg`，走 CDN。

换存储只需改环境变量，代码零改动——这是设这个函数的唯一目的。

### 封面两档

封面出两份，同名，缩略档放在 `seed-covers/thumb/`：

| 档位 | 高 | 质量 | 均值 | 用途 |
| --- | --- | --- | --- | --- |
| 缩略 | 560 | 58 | ~33KB | 共鸣厅瀑布流、搜索结果、明信片墙 |
| 详情 | 1000 | 74 | ~132KB | 详情头图、我的它头图、Reel 全屏 |

调用点不用记两条路径：`coverSrcSet()` 从详情档 URL 推出 `srcSet`，
`CoverPlaceholder` 再结合 `sizes` 让浏览器自己挑。铺满整宽的大图传
`sizes="100vw"`，其余用默认的双列卡片宽度。

出图命令（`sips` 为 macOS 自带）：

```bash
sips -s format jpeg -s formatOptions 74 --resampleHeight 1000 in.png --out seed-covers/x.jpg
sips -s format jpeg -s formatOptions 58 --resampleHeight 560  in.png --out seed-covers/thumb/x.jpg
```

## 5. 加新物料

1. 放进 `static/` 对应分类目录，命名 `分类-主体.jpg`（如 `cover-pet-collar.jpg`）。
2. 压到 200KB 以内：`sips -Z 1200 -s format jpeg -s formatOptions 72 in.png --out out.jpg`
3. 重建清单：`./scripts/assets-manifest.sh`
4. 前端引用走 `assetUrl()`。

运营物料入库前逐条确认：**无可识别人脸、无可读文字、无商标**。
若换成真实用户内容，必须留存授权记录，并在 `MANIFEST.json` 的 `licenseNote` 写明来源与授权范围。

## 6. 新人上手

```bash
./scripts/assets-check.sh
```

会校验资源根是否就位、清单是否对得上、有没有缺文件；缺了会直接告诉你去哪拿，
不用靠"首页封面全裂开"来猜。

## 7. 兜底

拆仓后三个仓各有一份 `.gitignore`，分工不同：

| 仓 | 封掉什么 | 为什么 |
| --- | --- | --- |
| `echo-doc` | `Echo-assets/runtime/`、`uploads/` | 🔴 合规红线，用户上传 |
| `echo-doc` | `*.psd/*.ai/*.sketch/*.fig` | 源文件大且不可 diff |
| `echo` | `echo-server/data/`、`uploads/` | 🔴 同上，后端本地落点 |
| `echo-client` | `public/assets/`、`public/design-ref/` | 物料本该在资源根，这是手滑兜底 |

注意 `echo-doc` **没有**封 `Echo-assets/static/`——那是本仓要分发的东西，封了就白拆了。

**例外**：`docs/assets/` 保留压缩过的文档配图缩略图（每张 <200KB，合计约 1MB），
让 markdown 不依赖 `Echo-assets/` 也能读。原图在 `Echo-assets/static/docs/`。

## 8. 上线时

`static/` 整体同步到 OSS/COS 对应目录，构建时设 `VITE_ASSET_BASE_URL` 指过去。
`runtime/` 留在服务端持久卷，按 `SPEC-trust-and-compliance` §CM-G4 加签名 URL、
水印与缩略图派生，原图最小暴露。
