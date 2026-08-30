# Echo 资源根

Echo 工程的**素材与资源存放地**，就在 `echo-doc` 仓内，跟着这个仓分发。
`static/` 已随仓入库；`runtime/` 被 `.gitignore` 硬封，只在本地存在。

配套规范见 `echo-doc/docs/ASSETS.md`。

> **2026-08-30 更正**：本文原先写"刻意放在代码仓库之外"。该前提在 2026-08-28 拆仓时
> 被推翻——`echo-doc` 被定义为承载美术源文件，`static/` 因此入库。取舍理由见
> `docs/ASSETS.md §0`。被推翻的只有"放在仓外"这一条，`runtime/` 不得入库那条没动。

## 目录

```
echo-doc/Echo-assets/
├── MANIFEST.json        # 静态物料清单（路径/大小/校验和/来源/授权说明）
├── static/              # 可分发：随本仓入库，随构建上 CDN
│   ├── seed-covers/     # 运营种子封面（共鸣厅瀑布流）
│   ├── design-ref/      # 设计参考稿（不参与运行时）
│   └── docs/            # 文档配图原图（docs/assets/ 内只留压缩缩略图）
└── runtime/             # 🔴 不可分发：运行时产生，含个人信息，已被 .gitignore 硬封
    └── uploads/         # 用户上传的照片/音视频
```

`runtime/` 在 clone 出来的仓里**是不存在的**，只有跑过后端的机器上才有。看不到它是正常的。

`static` 与 `runtime` 的分区是**合规要求**，不是习惯问题：
`static` 是内部生成的运营物料，可以随构建分发；
`runtime` 里是用户上传的敏感个人信息，受 PIPL 约束，只能留在服务端，
不得同步给团队、不得进构建产物、不得进版本库（见 `docs/SPEC-trust-and-compliance`）。

## 怎么让工程找到它

| 端 | 变量 | 指向 | 缺省 |
| --- | --- | --- | --- |
| 前端（开发/预览） | `ECHO_ASSETS_DIR` | 本资源根 | `../../echo-doc/Echo-assets` |
| 前端（生产构建） | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 | 空（走开发中间件） |
| 后端 | `ECHO_STORAGE_DIR` | 持久卷上的上传落点 | `<cwd>/data/uploads` |

前端缺省已对准 `workSpace/echo-client` + `workSpace/echo-doc` 并排克隆的布局，
不配任何变量也能直接跑。

🔴 **后端那一格不要指进本目录的 `runtime/`。** 它是用户上传的落点，该指持久卷。
指进仓内不会报错、`.gitignore` 也会挡住入库，**所以这个错是静默的**——
只在 `git clean -xdf` 或换机器时才暴露成"用户照片没了"。

## 加新物料

1. 文件放进 `static/` 对应分类目录，命名用 `分类-主体.jpg`（如 `cover-pet-collar.jpg`）。
2. 图片先压到 200KB 以内（`sips -Z 1200 -s format jpeg -s formatOptions 72`）。
   入库不等于没有代价，见 `docs/ASSETS.md §1`。
3. 重跑清单：`echo-doc/scripts/assets-manifest.sh`。
4. 前端引用一律走 `assetUrl('seed-covers/xxx.jpg')`，不要手写 `/assets/` 字面量。

运营物料入库前必须确认：无可识别人脸、无可读文字、无商标；若换成真实用户内容，
需逐条留存授权记录，并在 `MANIFEST.json` 的 `licenseNote` 写明。
