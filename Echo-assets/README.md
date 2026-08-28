# Echo 资源根

Echo 工程的**素材与资源存放地**，刻意放在代码仓库之外。仓库里只留代码、文档和配置，
物料一律从这里读取，避免二进制把 git 撑大、也避免用户上传物误入版本库。

配套规范见仓库内 `Echo/docs/ASSETS.md`。

## 目录

```
Echo-assets/
├── MANIFEST.json        # 静态物料清单（路径/大小/校验和/来源/授权说明）
├── static/              # 可分发：团队内可同步，随构建上 CDN
│   ├── seed-covers/     # 运营种子封面（共鸣厅瀑布流）
│   ├── design-ref/      # 设计参考稿（不参与运行时）
│   └── docs/            # 文档配图原图（仓库内只留压缩缩略图）
└── runtime/             # 不可分发：运行时产生，含个人信息
    └── uploads/         # 用户上传的照片/音视频（后端 ECHO_STORAGE_DIR 指向这里）
```

`static` 与 `runtime` 的分区是**合规要求**，不是习惯问题：
`static` 是内部生成的运营物料，可以随构建分发；
`runtime` 里是用户上传的敏感个人信息，受 PIPL 约束，只能留在服务端，
不得同步给团队、不得进构建产物、不得进版本库（见 `SPEC-trust-and-compliance`）。

## 怎么让工程找到它

两端各自一个环境变量，都支持指到任意绝对路径：

| 端 | 变量 | 指向 | 缺省 |
| --- | --- | --- | --- |
| 前端（开发/预览） | `ECHO_ASSETS_DIR` | 本资源根 | 仓库同级 `../../Echo-assets` |
| 前端（生产构建） | `VITE_ASSET_BASE_URL` | CDN/OSS 上对应 `static/` 的目录 | 空（走开发中间件） |
| 后端 | `ECHO_STORAGE_DIR` | `runtime/uploads` | `<cwd>/data/uploads` |

缺省值已经对准同级目录，所以按 `workSpace/Echo` + `workSpace/Echo-assets` 这样并排放，
不配任何变量也能直接跑。

## 加新物料

1. 文件放进 `static/` 对应分类目录，命名用 `分类-主体.jpg`（如 `cover-pet-collar.jpg`）。
2. 图片先压到 200KB 以内（`sips -Z 1200 -s format jpeg -s formatOptions 72`）。
3. 重跑清单：`Echo/scripts/assets-manifest.sh`。
4. 前端引用一律走 `assetUrl('seed-covers/xxx.jpg')`，不要手写 `/assets/` 字面量。

运营物料入库前必须确认：无可识别人脸、无可读文字、无商标；若换成真实用户内容，
需逐条留存授权记录，并在 `MANIFEST.json` 的 `licenseNote` 写明。
