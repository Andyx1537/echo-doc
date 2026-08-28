# 后端联调说明 · HTTP/JSON REST 网关（BACKEND-RUN）

| 项 | 值 |
|---|---|
| 归属 | 后端 · echo-server HTTP 网关联调手册 |
| 接口真源 | `docs/API-CONTRACT.md`（v1）；产品规则 `PRD-echo-social.md` §0.6/§0.7、`PRD-echo-pet.md` §3.11、`COPY-GUIDE.md` |
| Base URL | `http://<host>:<port>/api/v1` |
| 健康检查 | `GET http://<host>:<port>/healthz` → `ok` |

---

## 1. 这是什么

在 `echo-server` 上**新增的轻量 HTTP/JSON REST 网关**，落地 H5 核心闭环。与既有 **WebSocket 9001**
（心跳/protobuf 协议层）**完全隔离、互不影响**——WS 侧代码、harness 一律未改动。

- **HTTP 库**：JDK 自带 `com.sun.net.httpserver.HttpServer`，**零新增依赖**；JSON 复用工程已有 Gson。
- **端口**：系统属性 `-Decho.http.port` 配置，默认 **8080**。
- **鉴权**：首次 `POST /auth/guest` 取 `token`，此后请求头 `Authorization: Bearer <token>`。
- **六项定案服务端强制**（API-CONTRACT §12）：可见性默认 private；明信片付费只款式/加速、拒绝对内容付费解锁；
  献花每日 5 朵额度校验、不写温度、无排名；记得不返精确总数、看过仅 owner 内部；温度与献花完全解耦；
  所有 AI 生成与错误文案过 `CopyGuardFilter` 禁用词过滤。

---

## 2. 启动

编译：

```bash
cd Echo/echo-server
mvn -q -DskipTests compile
```

> 需要 **JDK 26**（与 Aengine 对齐）。本机 JDK 26 路径示例：
> `/opt/homebrew/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home`。

### 模式 A：无 DB（推荐联调）

不接 PostgreSQL 也能完整跑通核心闭环——新域（往宠/献花/记得/明信片/记录/消息/亲友/光谱）走
**内存态实现**（`com.echo.http.store.EchoStore`），并预置 2 个演示广场窗口。

```bash
# 生成 classpath（一次即可）
mvn -q -DskipTests dependency:build-classpath -Dmdep.outputFile=/tmp/echo-cp.txt

export JAVA_HOME=/opt/homebrew/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home
CP="target/classes:$(cat /tmp/echo-cp.txt)"

# 第一个参数 9101 = WebSocket 端口；-Decho.http.port=8080 = HTTP 端口
"$JAVA_HOME/bin/java" -cp "$CP" -Decho.http.port=8080 com.echo.bootstrap.EchoServer 9101
```

启动日志应出现：`EchoServer HTTP 网关已启动: http://0.0.0.0:8080/api/v1`。

### 模式 B：带 DB（新域已落库）

开启 PostgreSQL（含 pgvector），既有 WS 业务闭环 + `t_account` 落库启用；HTTP 网关此时会
**复用 `AccountService`** 建/取正式账号行（游客一等公民），并自动改用 **`PgEchoStore`** 把新域
（往宠/近况/献花/记得/明信片/记录/消息/亲友/账号概要）**落库到 PostgreSQL**——`PgEchoStore`
构造时幂等建表（`CREATE TABLE IF NOT EXISTS`，共 9 表 + 索引，与 `schema.sql` 新域段一致）。
启动日志会打印 `HTTP 网关存储实现: PgEchoStore(PostgreSQL 落库)`。

> 会话 token / 建档流程态 onboarding / 光谱 nodes·shadows 无独立表，进程内维护（重启可重建）；
> 其中账号-设备映射走 `t_account_profile.deviceId` 查询，**重启后同 deviceId 游客仍取回原账号与宠物**。

```bash
"$JAVA_HOME/bin/java" -cp "$CP" \
  -Decho.db.enabled=true -Decho.db.config=/path/to/echo-db.properties \
  -Decho.http.port=8080 com.echo.bootstrap.EchoServer 9101
```

`echo-db.properties` 示例：

```
db.name=echo
jdbcUrl=jdbc:postgresql://127.0.0.1:5432/echo
driverClassName=org.postgresql.Driver
username=echo
password=echo
maximumPoolSize=8
```

---

## 3. 核心闭环 curl 示例

> 领游客 → 建档 → 回访 → 看近况 → 献花 → 记得 → 看暖光面孔墙

```bash
B=http://127.0.0.1:8080/api/v1

# 1) 领游客身份（同 deviceId 幂等）
TOKEN=$(curl -s -X POST $B/auth/guest -H 'Content-Type: application/json' \
  -d '{"deviceId":"loop-dev"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")
AUTH="Authorization: Bearer $TOKEN"

# 2) 建档：start → confirm（memoryScene.allowUse 必须 true）
OB=$(curl -s -X POST $B/pet/onboarding/start -H "$AUTH" -H 'Content-Type: application/json' \
  -d '{"petName":"麦麦","species":"金毛","traits":["温柔","粘人"]}')
OID=$(echo "$OB" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['onboardingId'])")
CID=$(echo "$OB" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['candidates'][0]['id'])")
curl -s -X POST $B/pet/onboarding/confirm -H "$AUTH" -H 'Content-Type: application/json' \
  -d "{\"onboardingId\":\"$OID\",\"finalCandidateId\":\"$CID\",\"memoryScene\":{\"caption\":\"相遇那天\",\"allowUse\":true}}"

# 3) 主人回访（温度回暖，地板 60、只由回访驱动）
curl -s -X POST $B/pet/me/visit -H "$AUTH"

# 4) 看我的它 + 近况
curl -s $B/pet/me -H "$AUTH"
curl -s "$B/pet/me/echoes?limit=10" -H "$AUTH"

# 5) 广场取一个公开窗口 id
WID=$(curl -s $B/plaza -H "$AUTH" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['items'][0]['id'])")

# 6) 献花（每日 5 朵；不加温度、无排名；超额回 3001）
curl -s $B/flowers/quota -H "$AUTH"
curl -s -X POST $B/windows/$WID/flower -H "$AUTH" -H 'Content-Type: application/json' -d '{"count":2}'

# 7) 记得（状态开关，幂等）
curl -s -X POST $B/windows/$WID/remember -H "$AUTH" -H 'Content-Type: application/json' -d '{"remembered":true}'

# 8) 暖光面孔墙（只 warmthLevel/faces/meRemembered，绝无精确总数/排名）
curl -s $B/windows/$WID/remember -H "$AUTH"

# 9) owner 私域数据（看过数/记得面孔数/收花数，仅本人可见）
curl -s $B/pet/me/insights -H "$AUTH"
```

成功信封 `{"code":0,"data":{...}}`；错误信封 `{"code":<非0>,"msg":"<温柔文案>","detail":"<英文原因>"}`。

---

## 4. 端点清单（已实现）

| 域 | 端点 |
|---|---|
| §1 鉴权/账号 | `POST /auth/guest`、`POST /auth/bind`、`GET /me` |
| §2 建档 | `POST /pet/onboarding/{start,refine,confirm}`、`POST /upload`(真实落存储) |
| §3 我的它 | `GET/PATCH /pet/me`、`POST /pet/me/visit` |
| §4 近况/来信 | `GET /pet/me/echoes`、`POST /pet/me/echoes/:echoId/reply` |
| §5 献花&记得 | `GET /flowers/quota`、`POST /windows/:id/flower`、`POST/GET /windows/:id/remember` |
| §6 窗口/广场 | `GET /plaza`、`GET /windows/:id`、`POST /windows/:id/seen`、`GET /pet/me/insights` |
| §7 明信片/商店 | `GET /pet/me/postcards`、`POST /pet/me/postcards/:id/unlock`、`GET /shop/postcard-skins`、`POST /shop/purchase` |
| §8 亲友 | `GET /relations`、`PATCH /relations/:id`、`POST /relations/:id/reel-seen` |
| §9 记录 | `GET /records?scope=`、`POST /records` |
| §10 消息 | `GET /messages`、`POST /messages/read` |
| §11 光谱 | `GET /spectrum`、`POST /spectrum/anchor`、`POST /spectrum/shadows/:id/integrate` |

---

## 5. 降级 / TODO

- **`POST /upload`**：✅ **已落地**。`HttpGateway` 直接处理（原始字节 + 二进制安全 multipart 解析，上限 25MB），
  经 `IStorage` 存储（默认 `LocalDiskStorage` 落 `ECHO_STORAGE_DIR`，预留 OSS/COS/MinIO），返回 `{resourceId,url}`；
  本地存储由 `GET /api/v1/files/{key}` 公开下发。配置见环境变量表 `ECHO_STORAGE_*`。
- **新域 PG 落库**：✅ **已落地**。DB 关 → `InMemoryEchoStore`（无库联调/单测）；DB 开 → `PgEchoStore`
  落库耐久域。`EchoStore` 已抽象为接口，两实现行为一致（`EchoApi` 改字段后统一 put/update 回写）。
  多实例下献花额度的跨进程超发控制仍为 TODO（单实例 MVP 用进程内 `flowerLock` 足够）。
- **献花购买余额 / 商店实扣**：`purchasedBalance` 恒 0、`/shop/purchase` 仅回款式确认（护栏：不影响解锁进度），
  真实计费为 TODO。
- **亲友/消息 种子**：内存态默认空列表；可通过后续 seed 或 DB 落库补充。

---

## 6. 构建与测试

### 6.1 🔴 `mvn test` 在本机禁用

surefire 的 fork 会挂死，**沙箱内外都复现**，实测 26 分钟零输出后被人工中止。本会话已因此吊死两条工作线。
问题在 fork，不在代码。**不要再试**，除非你是专门来修构建环境的。

未尝试过的绕法（`-DforkCount=0` / `-Djava.awt.headless=true` / 只跑不依赖 Mockito 的用例）留在这里备查，
🔴 但要试就单独起一条线专门试，不要夹在别的任务里——它挂死时不会报错，只会静静吃掉一条线的额度。

**当前欠账**：整批回归（含 `FeatureSwitchServiceTest` 等存量用例）跑不了，产品侧已知情接受「无整批回归背书」交付。
接库前必须解决。

### 6.2 全量编译验证：可靠，两个前提

```bash
cd Echo/echo-server && mvn -o clean test-compile     # 🔴 必须在沙箱外跑
```

- 🔴 **加 `-o` 离线开关**。不加时一大半时间在等依赖解析，加了之后全量只要 **7 秒**。
- 🔴 **`clean` 之后必须沙箱外**。沙箱禁止拷贝可执行文件，`protobuf-maven-plugin` 要把 `protoc` 复制进
  `target/protoc-plugins`，会报 `Operation not permitted`。⚠️ **增量编译在沙箱内没事**（不重新拷 protoc），
  所以这个坑只有想做干净校验的人才撞得上，而且很容易被误判成「代码编译不过」。

### 6.3 纯逻辑断言可以真跑，不必经 surefire

```bash
J=/opt/homebrew/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home
$J/bin/javac -cp target/classes -d /tmp/scratch Check.java
$J/bin/java  -cp target/classes:/tmp/scratch Check
```

🔴 **必须显式指向 JDK 26**：shell 默认的 `javac`/`java` 是 17，而 maven 用 26，直接敲会报
`bad class file ... wrong version 70.0, should be 61.0`——⚠️ **这个报错看起来像代码坏了，其实只是 JDK 选错了。**

这条办法不是摆设：它当场逮到过一个编译看不出来的真 bug——`List.of(...).contains(null)` 抛 NPE 而不是回 false，
于是读一条补列前的老宠物档案会直接炸（已修，`a790acd`）。写完「兜底方向」「归一化」这类纯函数断言，用上面三行跑一遍。

### 6.4 需要真实 PG 的集成测试

```bash
# 不设环境变量则整类 assumeTrue 跳过，保证无库 CI 全绿
ECHO_TEST_PG_URL="jdbc:postgresql://127.0.0.1:5432/echo" ECHO_TEST_PG_USER=echo \
  mvn test -Dtest=PgEchoStoreTest
```

🔴 走 `mvn test`，所以在本机同样跑不了（见 6.1）。**PG 侧至今零自动化验证**：`UNION ALL` 查询与
`t_reaction_seen` 的 UPSERT 一次都没执行过，现有用例盖的全是内存实现。接库时必验。
