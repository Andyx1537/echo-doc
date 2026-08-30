# 交付部署说明 · 回声（DEPLOY）

| 项 | 值 |
|---|---|
| 归属 | 交付 · 生产/预发部署手册（前端静态托管 + echo-server 后端 + 环境配置） |
| 配套文档 | 联调 `BACKEND-RUN.md`；上线策略/合规 `RELEASE.md`；接口真源 `API-CONTRACT.md`；AI 装配 `AI-CAPABILITIES.md` |
| 架构 | 前端纯静态 H5（Nginx/OSS/COS/CDN）＋ 后端 echo-server（HTTP/JSON 网关 8080 · WebSocket 9101）＋ 可选 PostgreSQL(pgvector)。⚠️ **一处例外**：分享落地页 `/w/*` 与预览图 `/share/*` **不能走静态托管**，须后端直出，见 **§1.5** |
| 环境 | 后端 **JDK 26**；前端 Node ≥ 18 |

> 本手册只讲「怎么把这一版部署上线」。**本地联调**看 `BACKEND-RUN.md`；**为什么这么发、合规排期、版号/备案**看 `RELEASE.md`。

---

## 0. 拓扑总览

```
浏览器(H5)
   │  https://echo.example.com            (静态站点：OSS/COS/CDN 或 Nginx)
   │      ├─ 反代 /api/   → 后端 8080     (同源，规避跨域/Cookie 复杂度)
   │      └─ 反代 /w/ /share/ → 后端 8080 (分享落地页与预览图，必须先于 SPA 回落匹配，见 §1.5)
   ▼
echo-server (一台/一组)
   ├─ HTTP/JSON REST 网关  :8080/api/v1   (H5 核心闭环)
   ├─ 分享落地页 HTML 直出  :8080/w/{id}   (按窗 og/twitter meta；爬虫不执行 JS，见 §1.5)
   ├─ WebSocket           :9101           (心跳/protobuf；H5 MVP 可暂不接)
   ├─ ILlmClient          → 近况/来信生成 (ECHO_LLM_* 配置；无 key 回落 Mock)
   ├─ IVisionClient       → 建档识别      (桩：ECHO_VISION_STUB_MULTI 控演示)
   └─ 可选 PostgreSQL(pgvector)           (echo.db.enabled=true 时落库)
```

**推荐同源部署**：静态站点把 `/api/` 反代到后端 8080，前端 `VITE_API_BASE` 设为空或站点自身域名，避免跨域与 token 头处理的额外成本。

---

## 1. 前端：纯静态构建与托管

### 1.1 构建

```bash
cd Echo/echo-h5-proto
npm ci                 # 或 npm install
# 生产构建：产出纯静态 dist/
VITE_API_BASE=https://echo.example.com \
VITE_TRACK_ENDPOINT=https://echo.example.com/collect \
npm run build
```

- 根路径部署（`https://echo.example.com/`）：无需 `VITE_BASE`。
- 子路径部署（`https://cdn.example.com/echo/`）：加 `VITE_BASE=/echo/`。
- `VITE_API_BASE` **留空** = 前端走本地 mock（localStorage），可先发一个「无后端也能完整体验」的演示站，后端就绪后再重构建切真接口。

### 1.2 环境变量（构建期注入，`.env.production` 或命令行）

| 变量 | 作用 | 默认 |
|---|---|---|
| `VITE_API_BASE` | 真后端 Base URL；前端请求 `${VITE_API_BASE}/api/v1/...`。空=本地 mock 回退 | 空（mock） |
| `VITE_BASE` | 静态部署子路径 | `/` |
| `VITE_TRACK_ENDPOINT` | 埋点上报端点；空=仅 console | 空 |

> 注意：Vite 环境变量在 **build 时**烘焙进产物，改值需重新 `npm run build`。

### 1.3 托管 A：对象存储 + CDN（推荐，成本低）

阿里云 OSS / 腾讯云 COS 均可：

1. 建 Bucket（私有读写关闭、开启静态网站托管），把 `dist/` 全量上传到根（或子目录，需与 `VITE_BASE` 一致）。
2. 设静态网站首页/404 均为 `index.html`（SPA 路由需要 404 回落 index）。
3. 前挂 CDN，回源指向 Bucket；缓存策略：
   - `index.html`：**不缓存 / 短缓存**（`Cache-Control: no-cache`），保证发版即时生效。
   - `assets/*`（带指纹哈希）：**长缓存**（`max-age=31536000, immutable`）。
4. 绑定自定义域名 + HTTPS 证书。
5. **同源反代**：在 CDN/网关把 `/api/*`、`/collect`（埋点）回源到后端 8080。

上传示例（OSS，`ossutil`）：

```bash
ossutil cp -r echo-client/echo-h5-proto/dist/ oss://echo-h5/ --update
# index.html 覆盖为不缓存
ossutil cp echo-client/echo-h5-proto/dist/index.html oss://echo-h5/index.html \
  --meta "Cache-Control:no-cache" --update
```

### 1.4 托管 B：Nginx（自有机器，前后端同机）

```nginx
server {
    listen 443 ssl http2;
    server_name echo.example.com;
    ssl_certificate     /etc/ssl/echo/fullchain.pem;
    ssl_certificate_key /etc/ssl/echo/privkey.pem;

    root /var/www/echo/dist;
    index index.html;

    # 静态资源长缓存
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    # index.html 不缓存，保证发版即时生效
    location = /index.html { add_header Cache-Control "no-cache"; }

    # 后端 API 同源反代
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    # 埋点回源（如启用 VITE_TRACK_ENDPOINT）
    location /collect { proxy_pass http://127.0.0.1:8080; }

    # SPA 路由回落
    location / { try_files $uri $uri/ /index.html; }
}
```

同源部署时前端 `VITE_API_BASE` 可设为 `https://echo.example.com`（或留空走站点自身相对路径，视 http 客户端实现）。

### 1.5 分享落地页：`/w/*` 必须绕开静态托管，交后端直出

> 🔴 **这是纯静态托管的一处硬约束，不是优化项。** 产品规格 `SPEC-trust-and-compliance.md §CM-G0S S-11`；接口契约 `API-CONTRACT.md §16`。

**问题**：`§1.3`/`§1.4` 的 SPA 回落（404 → `index.html` / `try_files … /index.html`）把**所有**未命中的路径都返回同一份 `index.html`。而社交平台爬虫（微信、微博、QQ 等）**不执行 JS**，所以：

- 每扇窗的分享链接被抓到的都是**同一份** `index.html`，**无法按窗下发不同的 `og:image`**；
- 站内的 AI 标识是 `<span class="ai-gen-badge">` **DOM 角标**（有意为之，不污染用户素材原图），在爬虫眼里**等于不存在** → 《AI 生成合成内容标识办法》的显式标识在这条路径上**未覆盖**。

**方案（已定，倾向 C1）**：**不做全站 SSR、不做构建期预渲染**（窗是 UGC、持续新增，构建期无法穷举），改为**后端直出一条分享落地页路由**——主站仍是纯静态 CDN，只多一条动态路由。方案对比与微信生态六条约束见 `S-11 ②`。

#### 路由分流（必须先于 SPA 回落匹配）

Nginx（对应 `§1.4`，🔴 **`location /w/` 必须写在 `location /` 之前**）：

```nginx
    # 分享落地页：后端直出按窗 meta（爬虫不执行 JS，必须服务端已渲染）
    location /w/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        # 内容可被作者收回或 aiGenerated 被改判，不缓存
        add_header Cache-Control "no-cache";
    }
    # 合成的分享预览图：长期公开可读（见下方"两条与既有策略冲突的地方"）
    location /share/og/ {
        proxy_pass http://127.0.0.1:8080;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
    }
```

CDN + OSS/COS（对应 `§1.3`）：在 CDN 回源规则里把 `/w/*`、`/share/*` **回源到后端 8080**，与 `/api/*`、`/collect` 同一处配置；**优先级高于**静态 Bucket 与 404 回落规则。

#### 🔴 两条与既有策略冲突的地方（不处理就上线即失效）

| # | 冲突 | 处置 |
|---|---|---|
| 1 | **SPA 404 回落会吞掉 `/w/*`** | `/w/` 的路由规则**必须先匹配**。验证方式：`curl -s https://<域名>/w/<某个窗 id> \| grep 'og:image'`，取到的值在**两扇不同的窗**上必须不同。若两次相同，说明还在走静态回落 |
| 2 | **`og:image` 不能用 `CM-G4` 的限时签名 URL** | 签名过期后微信侧缩略图直接失效，且微信缓存拿不到。**分享预览图走长期有效的公开 URL**（`/share/og/*`）。这不违反 `CM-G4`：预览图是**我方合成的派生物料、不是用户素材**（判定见 `TECH-DESIGN-feed-recall-and-exposure.md §3.12.1`）。🔴 **用户上传的原图仍然一律走签名 URL，不因本条放宽** |

> 🔴 **`/share/og/` 目录只放我方合成的预览图**，不得混入用户上传素材。`runtime/`（用户上传）**不得**进 CDN 这条既有规则（见 `§3.2`）继续全额生效。

#### 域名前置

- **域名须完成 ICP 备案**，否则链接在微信内会被拦截，连打开都做不到（备案见 `RELEASE.md`）。
- `og:image` 须是**可公网匿名访问的 HTTPS 绝对 URL**——用无 Cookie 环境 `curl` 验一次。

---

## 2. 后端：echo-server 部署

### 2.1 前置：把 Aengine 装进本地/私有 Maven 仓

echo-server 依赖 `com.aengine:Aengine:1.0-RELEASE`。构建机需先安装引擎：

```bash
cd Aengine
mvn -q -DskipTests install    # 装到 ~/.m2（或私有 Nexus：mvn deploy）
```

### 2.2 构建产物（classpath 方式，零新增插件）

工程当前**未打 fat-jar**，用「classes + 依赖 classpath」运行（与 `BACKEND-RUN.md` 一致，已验证）：

```bash
cd Echo/echo-server
mvn -q -DskipTests clean compile
# 一次性导出依赖 classpath 到文件
mvn -q -DskipTests dependency:build-classpath -Dmdep.outputFile=echo-cp.txt
```

部署时打包 `target/classes` + `echo-cp.txt` 指向的依赖 jar（或直接在目标机 `mvn` 拉取）。

> 如需单文件可执行 jar（更利于容器化/systemd），可在 `pom.xml` 增 `maven-shade-plugin` 产出 `echo-server-all.jar`——属构建改动，按团队约定确认后再加，本手册先用已验证的 classpath 方式。

### 2.3 运行

```bash
export JAVA_HOME=/opt/homebrew/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home  # 生产按实际 JDK26 路径
CP="target/classes:$(cat echo-cp.txt)"

# 第一个程序参数 = WebSocket 端口；-Decho.http.port = HTTP 网关端口
"$JAVA_HOME/bin/java" -cp "$CP" \
  -Decho.http.port=8080 \
  com.echo.bootstrap.EchoServer 9101
```

启动成功日志：`EchoServer HTTP 网关已启动: http://0.0.0.0:8080/api/v1`。
健康检查：`curl http://127.0.0.1:8080/healthz` → `ok`。

### 2.4 systemd 常驻（自有机器）

`/etc/systemd/system/echo-server.service`：

```ini
[Unit]
Description=Echo Server (HTTP gateway + WebSocket)
After=network.target postgresql.service

[Service]
Type=simple
User=echo
WorkingDirectory=/opt/echo/echo-server
Environment=JAVA_HOME=/usr/lib/jvm/jdk-26
# ── AI / 业务开关（见 §3）──
Environment=ECHO_LLM_PROVIDER=doubao
Environment=ECHO_LLM_API_KEY=__FILL_ME__
# ── 素材存储：本地磁盘用持久卷（规模化后切云对象存储）──
Environment=ECHO_STORAGE_TYPE=local
Environment=ECHO_STORAGE_DIR=/var/lib/echo/uploads
EnvironmentFile=-/opt/echo/echo-server/echo.env
ExecStart=/usr/lib/jvm/jdk-26/bin/java -cp "target/classes:$(cat /opt/echo/echo-server/echo-cp.txt)" \
  -Decho.db.enabled=true -Decho.db.config=/opt/echo/echo-server/echo-db.properties \
  -Decho.http.port=8080 com.echo.bootstrap.EchoServer 9101
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

> `ExecStart` 里 `$(...)` 不会被 systemd 展开，建议改为把完整 classpath 写死到 `echo-cp.txt` 内容后直接粘贴，或用启动脚本 `ExecStart=/opt/echo/run.sh` 包一层。敏感 env（`ECHO_LLM_API_KEY` 等）放 `echo.env`（`EnvironmentFile`，权限 600）勿入库。

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now echo-server
sudo systemctl status echo-server
```

### 2.5 容器化（可选）

无 fat-jar 时最简 Dockerfile（多阶段，运行期带 classpath）：

```dockerfile
FROM maven:3.9-eclipse-temurin-26 AS build
WORKDIR /src
COPY Aengine /src/Aengine
COPY Echo/echo-server /src/echo-server
RUN cd Aengine && mvn -q -DskipTests install \
 && cd /src/echo-server && mvn -q -DskipTests clean compile \
 && mvn -q -DskipTests dependency:copy-dependencies -DoutputDirectory=target/libs

FROM eclipse-temurin:26-jre
WORKDIR /app
COPY --from=build /src/echo-server/target/classes /app/classes
COPY --from=build /src/echo-server/target/libs   /app/libs
EXPOSE 8080 9101
ENTRYPOINT ["sh","-c","java -cp 'classes:libs/*' -Decho.http.port=8080 com.echo.bootstrap.EchoServer 9101"]
```

---

## 3. 环境配置一览（后端）

### 3.1 运行参数（JVM 系统属性 `-D...`）

| 属性 | 作用 | 默认 |
|---|---|---|
| `echo.http.port` | HTTP/JSON 网关端口 | `8080` |
| 程序第 1 参数 | WebSocket 端口 | `9001`（本手册用 9101） |
| `echo.host` | 绑定地址 | `0.0.0.0` |
| `echo.db.enabled` | 是否接 PostgreSQL（`true` 启用业务落库/账号真表） | `false`（内存态） |
| `echo.db.config` | DB 配置文件路径（见 `BACKEND-RUN.md` §2 模式 B） | — |
| `echo.workerId` | 雪花 ID workerId | `1` |

> **MVP 建议**：无库时 `echo.db.enabled=false`（内存态）即可跑通核心闭环做联调；**正式留存用户数据请开 `echo.db.enabled=true`** —— 新域已由 `PgEchoStore` 落库（已验证重启持久化）。开 DB 前确保 `t_self_vector` 依赖的 `vector` 扩展已建（`CREATE EXTENSION IF NOT EXISTS vector;`，供 WS 侧向量库）。

### 3.2 AI 装配（环境变量，见 `AI-CAPABILITIES.md`）

| 变量 | 作用 | 默认 |
|---|---|---|
| `ECHO_LLM_PROVIDER` | `doubao`\|`deepseek`\|`qwen`\|`openai`\|`local`\|`mock`（近况/来信生成） | `mock` |
| `ECHO_LLM_BASE_URL` | OpenAI 兼容端点根；缺省按 provider 取内置默认 | 按 provider |
| `ECHO_LLM_API_KEY` | 密钥；**缺省即回落 Mock**（无 key 也能编译/联调/演示） | 空 |
| `ECHO_LLM_MODEL` | 模型名/推理接入点 ID（豆包建议显式配） | 按 provider |
| `ECHO_LLM_TEMPERATURE` | 采样温度 | `0.8` |
| `ECHO_VISION_PROVIDER` | `qwen`\|`stub`（建档第 1 步肖像识别） | `stub` |
| `ECHO_VISION_BASE_URL` | OpenAI 兼容多模态端点根；缺省按 provider 取内置默认 | 按 provider |
| `ECHO_VISION_API_KEY` | 密钥；**缺省即回落桩实现**（返回兜底值，出参标 `source=fallback`）。🔄 **原写「中性默认」，措辞按 `DECISIONS SR-D13` 更正** —— 🔴 **兜底值 `animal` 不是中性值，是能力最宽的那一档** | 空 |
| `ECHO_VISION_MODEL` | 多模态模型名 | `qwen-vl-plus` |
| `ECHO_VISION_MAX_EDGE` | 送模型前图片缩放的最长边 px；调大更清晰但更慢（耗时与视觉 token 数正相关） | `768` |
| `ECHO_VISION_STUB_MULTI` | `=1` 时建档识别桩返回多主体演示；否则始终单主体 | 关闭（单主体） |

**对象存储（素材上传，`POST /upload`）**

| 变量 | 作用 | 默认 |
|---|---|---|
| `ECHO_STORAGE_TYPE` | `local`\|`oss`\|`cos`\|`minio`（后三者为预留适配位，未接入会显式报错） | `local` |
| `ECHO_STORAGE_DIR` | local 落盘目录；应指向资源根的 `runtime/uploads`（见 `ASSETS.md`） | `<cwd>/data/uploads` |
| `ECHO_STORAGE_BASE_URL` | 返回 url 的绝对前缀；空则相对 `/api/v1/files/<key>`（同源部署即可，跨源联调设为后端源） | 空 |
| `ECHO_STORAGE_ENDPOINT/BUCKET/AK/SK/REGION` | oss/cos/minio 预留，本期未接入 | 空 |

> 生产建议：`local` 磁盘目录需持久卷 + 定期备份；规模化后切云对象存储（实现对应 `IStorage` + `ECHO_STORAGE_TYPE`），
> 此时 `url` 直接是云对象地址，不再经 `/api/v1/files/` 网关下发（省带宽、走 CDN）。

> 兜底安全网：即便接了真 LLM，所有对外文案仍过 `CopyGuardFilter` 禁用词过滤（`COPY-GUIDE.md`），冰冷/制造内疚/游戏化字眼不会漏出。

**静态物料（运营封面、设计稿）**

资源根是 `echo-doc` 仓的 `Echo-assets/`，`static/` 随该仓分发，规范见 `ASSETS.md`。
（2026-08-28 拆仓前是"存在仓库外"，该前提已推翻，见 `ASSETS.md §0`。）

| 变量 | 作用 | 默认 |
|---|---|---|
| `ECHO_ASSETS_DIR` | 资源根绝对路径；开发/预览期 Vite 中间件把 `/assets/**` 映射到 `<资源根>/static/**` | `../../echo-doc/Echo-assets` |
| `VITE_ASSET_BASE_URL` | 生产物料前缀，指向 CDN/OSS 上对应 `static/` 的目录（构建期注入） | 空（走开发中间件） |

> 上线步骤：把资源根的 `static/` 整体同步到 OSS/COS，构建时设 `VITE_ASSET_BASE_URL` 指过去。
> `runtime/`（用户上传）**不得**进 CDN，留在服务端持久卷，按 `SPEC-trust-and-compliance` §CM-G4 加签名 URL 与水印。
> 部署前跑 `./scripts/assets-check.sh` 确认物料齐全，避免上线后满屏破图。

### 3.3 前端 ↔ 后端对齐检查

- 前端 `VITE_API_BASE` + `/api/v1` ＝ 后端 `echo.http.port` 暴露路径。
- 同源反代时确认 Nginx/CDN 把 `/api/` 完整转发（含 `Authorization` 头，勿被网关剥离）。
- 首次 `POST /api/v1/auth/guest` 返 token，前端存 localStorage 并带 `Authorization: Bearer`。

---

## 4. 发版顺序与验收

1. **后端先行**：装 Aengine → 编译 echo-server → 起服务 → `curl /healthz` ＝ `ok` → 跑 `BACKEND-RUN.md` §3 curl 闭环（领游客→建档→回访→献花→记得→暖光墙）全绿。
2. **前端切真接口**：`VITE_API_BASE` 指向后端域名 → `npm run build` → 上传 `dist/` → 刷 CDN（`index.html` 不缓存）。
3. **联调冒烟**：浏览器走一遍 `ACCEPTANCE.md` TC-01~12 关键路径 + 六项定案对照。
4. **埋点校验**：确认 `guest_created → onboarding_confirm → pet_visit → flower/remember → share/bind` 漏斗有数。

---

## 5. 上线前检查清单

- [ ] 前端 `dist/` 构建成功，`index.html` 短缓存、`assets/*` 长缓存。
- [ ] HTTPS 证书就绪，`/api/` 同源反代通，`Authorization` 头透传。
- [ ] 后端 `healthz` ok；`ECHO_LLM_API_KEY` 等敏感变量走 `EnvironmentFile`（600，未入库）。
- [ ] `ECHO_VISION_STUB_MULTI` 生产**关闭**（避免单宠误报多主体）。
- [ ] 六项定案服务端护栏在线（可见性默认 private / 明信片不锁内容 / 献花额度不加温度 / 记得不返数字 / 温度献花解耦 / 文案过词表）。
- [ ] 备案/合规按 `RELEASE.md`：ICP、隐私政策(PIPL)、AI 算法备案、版号风险评估到位后再放公网自然流量。
- [ ] **分享落地页（`§1.5`）**：`/w/*` 与 `/share/*` 的回源规则**先于** SPA 404 回落匹配；`curl` 取**两扇不同窗**的 HTML，`og:image` 取值**不同**（相同=还在走静态回落）。
- [ ] **分享预览图**：`og:image` 在**无 Cookie 环境**可匿名取到，且**不是限时签名 URL**；`aiGenerated=true` 的窗其预览图**图上有** AI 标识、文案与前端角标逐字相同。
- [ ] 🔴 **用户原始素材未被修改**：叠标识只发生在合成预览图上；原图/压缩图/缩略图/裁剪图**字节比对一致**，落地页首屏封面图**没有烧字**（完整 10 条判据见 `SPEC-trust-and-compliance §CM-G0S S-11 ⑦`）。
- [ ] 数据留存/训练语料回流：默认关，仅在用户显式勾选 `trainConsent` 后入库（PIPL）。

---

## 6. 已知降级 / TODO（部署相关）

- `POST /upload` ✅ **已落地**：`HttpGateway` 二进制安全 multipart 解析 + `IStorage` 存储（默认本地磁盘，预留 OSS/COS/MinIO），本地文件由 `GET /api/v1/files/{key}` 下发。生产上云只需实现对应 `IStorage` 并设 `ECHO_STORAGE_TYPE`。
- 新域 PG 落库 ✅ **已落地**：`echo.db.enabled=true` 时走 `PgEchoStore`（往宠/献花/记得/明信片/记录/消息/亲友/账号概要持久化，已验证重启后数据仍在）；`false` 时走 `InMemoryEchoStore`（重启即清，仅联调）。会话 token / onboarding / 光谱无独立表，进程内维护。
- 献花购买余额 `/shop/purchase` 仅回款式确认，真实计费为 TODO（护栏：不影响解锁进度）。
- 多实例部署下献花额度的跨进程超发控制为 TODO（单实例用进程内锁足够）。
- 后端未打 fat-jar，容器/systemd 用 classpath 方式；如需单 jar 增 shade 插件（构建改动，需确认）。
