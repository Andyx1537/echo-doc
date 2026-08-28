# 资源管理规范

**约束对象**：一切二进制物料——运营封面、设计稿、文档配图、用户上传的照片/音视频。
**核心规则**：**物料不进代码库**。仓库里只留代码、文档、配置；物料存在仓库之外的
**资源根**，由环境变量定位，构建期由 CDN 供给。

## 1. 为什么

首次提交把 33 张 PNG（多数单张 2MB 以上）灌进了版本库，`.git` 因此撑到 65MB，
而代码本身只有几 MB。图片改一次就在历史里多存一份完整副本，git 的增量压缩对二进制基本无效。
再叠加用户上传物一旦误入版本库，删除请求就没法真正兑现——这是合规问题，不只是体积问题。

## 2. 资源根

默认位置：与代码仓库同级的 `Echo-assets/`。

```
workSpace/
├── Echo/            ← 代码仓库（git）
└── Echo-assets/     ← 资源根（不受 git 管理）
    ├── MANIFEST.json
    ├── static/      ← 可分发
    │   ├── seed-covers/
    │   │   └── thumb/    ← 同名缩略档
    │   ├── design-ref/
    │   └── docs/
    └── runtime/     ← 不可分发
        └── uploads/
```

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
| 前端 开发/预览 | `ECHO_ASSETS_DIR` | 资源根绝对路径 | 同级 `../../Echo-assets` |
| 前端 生产构建 | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 | 空 |
| 后端 | `ECHO_STORAGE_DIR` | `<资源根>/runtime/uploads` | `<cwd>/data/uploads` |

缺省值已对准同级目录，按上面的并排结构放，不配任何变量即可跑通。

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

`.gitignore` 已封掉 `echo-h5-proto/public/assets/`、`public/design-ref/`、
`echo-server/data/`、`uploads/` 以及 `*.psd/*.ai/*.sketch/*.fig`。
即使有人手滑把物料放回仓库内，也不会入库。

**唯一例外**：`docs/assets/` 保留压缩过的文档配图缩略图（每张 <200KB，合计约 1MB），
让 markdown 脱离资源根也能读。原图在 `<资源根>/static/docs/`。

## 8. 上线时

`static/` 整体同步到 OSS/COS 对应目录，构建时设 `VITE_ASSET_BASE_URL` 指过去。
`runtime/` 留在服务端持久卷，按 `SPEC-trust-and-compliance` §CM-G4 加签名 URL、
水印与缩略图派生，原图最小暴露。
