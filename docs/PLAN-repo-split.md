# 仓库拆分勘察报告

**状态**：勘察已完成，**拆分未执行**。本文档只存档事实与裁定，不是执行记录。
**勘察锚点**：`84a3e86ad7f2ba7d85c77c2ba3178fd61e2d350c`（2026-08-27 05:50，第 172 个提交）
**勘察时间**：2026-08-27

---

## 0. 概述

### 0.1 已勘察清楚的事实

- **`Echo` 仓顶层跟踪十项**：`.git-blame-ignore-revs`、`.gitattributes`、`.gitignore`、
  `deploy/`、`docs/`、`echo-client/`、`echo-h5-proto/`、`echo-server/`、`scripts/`、`tools/`。
- **拆分代价很低**：锚点上 172 个提交中只有 **14 个跨目录（8%）**，且**零 merge 提交**，
  历史是一条直线。用 `git filter-repo --path` 按目录切分，跨目录提交会被裁成各仓那一份，
  裁空的自动丢弃，不需要处理合并冲突。
- **各仓预期提交数（锚点上）**：`echo.git` 39、`echo-client.git` 31、`echo-doc.git` 114、
  `monitor.git` 36。🔴 这四个数字**只对锚点成立**，真拆时必须在新基准上重算，见 §5。
- 🔴 **存在命名撞车，会导致推错仓**：目录 `echo-client/` 是**冻结的 Unity 工程**，
  而远端 `echo-client.git` 要装的是 **`echo-h5-proto/`**。详见 §3。
- **工具与认证均已就绪**：`git filter-repo 2.47.0` 已装（未进 PATH）、SSH 已通、
  四个远端仓存在且为空。详见 §6。
- **原仓未被改动**：勘察全程只跑只读命令，未加 remote、未跑 `filter-repo`、未 push。

### 0.2 无归属内容的处置（全部已裁定，无待定项）

三个目标目录之外的七项内容，去向已全部拍板：

| 内容 | 去向 |
|---|---|
| `deploy/` | → `echo.git` |
| `echo-client/`（Unity） | → `echo.git`（留在服务器仓，不单独开仓） |
| `scripts/` | → `echo-doc.git`（跟引用它的 `docs/ASSETS.md` 走） |
| `.gitattributes` + `.gitignore` | → 三个仓**各带一份**（连同真实历史，不产生新提交） |
| `.git-blame-ignore-revs` | **丢弃**（改写后成坏指针） |
| `tools/` | **丢弃** |

理由见 §4。这些裁定都是可逆的——原仓历史完整保留，随时可以重切。

### 0.3 🔴 一条通用教训（不限于拆仓）

**任何拿"数量"做校验的动作，在一个活跃写入的仓上都是陷阱：你数的那一刻和你比对的那一刻
不是同一个仓。** 实证：本次勘察的 15 分钟里，`Echo` 从 157 个提交涨到 172 个。
校验必须钉死在一个 SHA 上。详见 §5。

### 0.4 这份文档什么时候过期

按可靠程度分三层，从最先失效到最耐久：

1. **提交数（§2）——每天都在过期。** 只对锚点 `84a3e86` 成立，仓在持续写入。
   真拆时必须重算，不要引用本文的数字。
2. **顶层内容清单与处置裁定（§1、§4）——顶层目录增删时过期。** 新增一个顶层目录，
   §4 就多一项无归属内容需要裁定。
3. **命名撞车（§3）与通用教训（§5）——只要目录名不改就一直成立。**
   这两节是本文最耐久也最有价值的部分。

**重读顺序建议**：真要动手拆的时候，先读 §3 和 §5，再看 §4 的裁定，最后按 §2 的方法
在新基准上重新算一遍数字。

---

## 1. 顶层内容清单

锚点上 `git ls-tree --name-only HEAD` 的完整结果（不含被 ignore 的）：

```
.git-blame-ignore-revs
.gitattributes
.gitignore
deploy/
docs/
echo-client/
echo-h5-proto/
echo-server/
scripts/
tools/
```

三个目标目录：

| 目录 | 文件数 | 去向 |
|---|---|---|
| `echo-server/` | 245 | `echo.git` |
| `echo-h5-proto/` | 89 | `echo-client.git` |
| `docs/` | 153 | `echo-doc.git` |

三个目标目录**之外**的七项：

| 内容 | 文件数 | 涉及提交 | 是什么 |
|---|---|---|---|
| `echo-client/` | 71 | 2 | **Unity 工程**：`Assets/Scenes/Bootstrap.unity`、`Assets/Scripts/EchoClient.cs`、`Assets/Art/` 下的占位 README 及大量 `.meta`。两个提交分别是版本控制基线与行尾归一，**没有一次实质改动，实质冻结** |
| `deploy/` | 8 | 2 | 服务端运维：`docker-compose.yml`（pgvector/pg16）、`echo-db.properties`、`smoke_p1.py`、`RUNBOOK.md`、`start_local.sh`、`stop_local.sh`、`_daemonize.py`、`.cp.txt` |
| `scripts/` | 2 | 1 | `assets-check.sh` / `assets-manifest.sh`，校验仓库外资源根 `Echo-assets/` 是否就位 |
| `tools/` | 1 | 1 | `README-watcher-moved.txt`——一张墓碑，写明监工脚本已收敛为 `.cursor/skills/agent-supervision/`，此处曾有重复副本已删除，勿再放 |
| `.gitignore` | — | 5 | 密钥、用户上传隐私素材、设计原文件、Unity 生成物、素材批次目录 |
| `.gitattributes` | — | 1 | 全仓行尾归一 LF，文件内写明了立它的实证理由 |
| `.git-blame-ignore-revs` | — | 1 | 让 blame 跳过行尾归一提交 `4d55bdc` |

---

## 2. 跨目录提交分布与预期提交数

### 2.1 分布（锚点 `84a3e86`，共 172 个提交）

| 触及的顶层内容 | 提交数 |
|---|---|
| 只 `docs` | 100 |
| 只 `echo-server` | 37 |
| 只 `echo-h5-proto` | 17 |
| `docs` + `echo-h5-proto` | 10 |
| 全仓（版本控制基线 + 行尾归一 367 文件） | 2 |
| `.gitignore` + `docs` + `echo-h5-proto`（其一还带 `scripts`） | 2 |
| 只 `tools` | 1 |
| 三个 dotfile 各自单独 | 3 |

**跨目录提交 = 10 + 2 + 2 = 14，占 172 的 8%。**
**merge 提交 = 0**，历史是一条直线。

### 2.2 为什么这个数字决定代价

跨目录提交是拆分唯一的麻烦来源：一个同时改了 `docs` 和 `echo-h5-proto` 的提交，
在两个输出仓里各出现一次，各只带自己那一半改动。8% 且无 merge 意味着：

- 不需要处理任何合并冲突；
- 14 个提交会在多个仓里各留一份裁剪版，可以接受，不值得为此做人工归并；
- 那 2 个"全仓"提交（基线 + 行尾归一）会出现在全部三个仓里，这是正常的。

### 2.3 各仓预期提交数（🔴 只对锚点成立）

| 远端 | 内容来源 | 锚点上的提交数 |
|---|---|---|
| `git@github.com:Andyx1537/monitor.git` | `agent-supervision` 整仓（不拆） | 36 |
| `git@github.com:Andyx1537/echo.git` | `echo-server/` + `deploy/` + `echo-client/` | 39（仅 `echo-server`） |
| `git@github.com:Andyx1537/echo-client.git` | `echo-h5-proto/` | 31 |
| `git@github.com:Andyx1537/echo-doc.git` | `docs/` + `scripts/` | 114（仅 `docs`） |

计算口径：`git rev-list --count --full-history <锚点> -- <路径>`。
加入 `deploy/`、`echo-client/`、`scripts/` 后各仓数字会略增（它们分别只涉及 2、2、1 个提交，
且大部分与已计入的提交重叠）。

🔴 **真拆时不要引用这一节的数字**，按 §5 在新基准上重算。

---

## 3. 🔴 命名撞车：按目录名理解映射表会把 Unity 工程推错仓

这是本文档最重要的一条。

**目录 `echo-client/` 不是 `echo-client.git` 的内容来源。**

| | 是什么 | 去哪 |
|---|---|---|
| 目录 `echo-client/` | Unity 工程，71 个文件，自基线起冻结 | `echo.git`（服务器仓） |
| 目录 `echo-h5-proto/` | H5 客户端原型，89 个文件，活跃开发 | **`echo-client.git`** |

真正的客户端是 `echo-h5-proto/`；`echo-client/` 是更早的 Unity 尝试，已经不动了。
谁看到映射表里"`echo-client.git` ← 客户端"就顺手去拿 `echo-client/` 目录，
推上去的会是一个冻结的 Unity 工程，而真正的 H5 客户端一个文件都没上去。

**这个错误不会报错。** `filter-repo --path echo-client/` 会正常执行、正常产出一个
71 个文件 2 个提交的仓、正常推送成功。只有人去看远端内容时才会发现推的是另一个东西。
这正是执行纪律里"从远端重新克隆并 `diff -r` 对比源目录"那一步不能省的原因——
它是唯一能抓住这类错误的检查。

**给拆分执行者的一条动作要求**：写 `--path` 参数时逐条念出"这个路径对应哪个远端仓"，
不要靠名字相似度推断。

---

## 4. 无归属内容的处置裁定与理由

### 4.1 `deploy/` → `echo.git`

与 `echo-server` 强耦合，不是泛用运维脚本：

- `echo-db.properties` 是按 `com.echo.infra.persistence.PgDb` 的**真实解析逻辑**写的键；
- `smoke_p1.py` 打的是 `EchoServer` 的 WebSocket 9001 端口；
- `RUNBOOK.md` 通篇讲怎么起 `EchoServer`，含 `-Decho.db.enabled` 等系统属性。

离开 echo-server 这些文件没有独立意义。

### 4.2 `echo-client/`（Unity）→ `echo.git`

已拍板：留在服务器仓，**不单独开第五个仓**。

它已冻结、只有 2 个提交，单独开仓的维护成本换不来价值；同时原仓历史完整保留，
将来真要独立出去随时可以重切。丢弃则是不必要的信息损失。

### 4.3 `scripts/` → `echo-doc.git`

跟引用它的 `docs/ASSETS.md` 走。

`assets-check.sh` 校验的是仓库外资源根 `Echo-assets/`，而资源根的规范定义在
`docs/ASSETS.md` 里。脚本与规范同仓，改规范时能一眼看到要不要同步改脚本。
（备选是归 `echo-client.git`，因为 H5 是素材消费方；此项可逆，不值得再讨论一轮。）

### 4.4 `.gitattributes` + `.gitignore` → 三个仓各带一份

用 `filter-repo --path .gitattributes --path .gitignore --path <目标目录>` 一起带过去，
**连同真实历史，不产生新提交**。

不能丢，因为这两份文件是护栏而非配置：

- `.gitattributes` 立的是全仓 LF 归一。文件里记着立它的实证：索引中 281 个源文件里
  279 个存的是 CRLF，任何一次整体重写都会把整个文件报成改写，真实改动被噪音淹没
  （2026-08-25 曾有一次提交看起来重写 1814 行，真实改动只有 224 增 58 删）。
  三个新仓若不带它，这个问题会立刻在每个仓里重演一次。
- `.gitignore` 排除的是密钥（`.env.*`、`*.key`、`*.pem`）与用户上传的隐私素材
  （`echo-server/data/`、`uploads/`）。丢掉等于让三个新仓在第一次提交时就有泄密敞口。

**注意**：`.gitignore` 里有针对特定目录的规则（如 `echo-h5-proto/public/assets/`、
`echo-client/Library/`、`deploy/pgdata/`）。带过去之后这些路径在新仓里位置会变，
规则会失效但不会报错——这是拆分完成后需要单独过一遍的收尾项，不是本次勘察的结论。

### 4.5 `.git-blame-ignore-revs` → 丢弃

它的全部内容就是点名提交 `4d55bdc082e6fa30d5cd77e3c6c8eb62d768d0b1`（行尾归一），
而 `filter-repo` 会重写所有 SHA，**这个 hash 在任何输出仓里都不存在**。
留着是一个静默失效的坏指针：`blame.ignoreRevsFile` 读到不存在的 revision 不会报错，
只是什么都不跳过。

要在新仓里保留这个能力，得在拆分后查出行尾归一提交的新 SHA 重新写一份——那需要新建提交，
属于拆分后的收尾工作，不在拆分本身的范围内。

### 4.6 `tools/` → 丢弃

唯一的文件是一张墓碑，警告的是"别再往 `Echo/tools/` 放监工脚本副本"。
拆分之后这个位置本身就不存在了，警告失去对象。
（监工脚本的正本在 `agent-supervision`，会整仓推到 `monitor.git`，不受影响。）

---

## 5. 🔴 通用教训：在活跃写入的仓上，数量校验必须钉死 SHA

### 5.1 实证

本次勘察开始时 `Echo` 有 **157** 个提交，15 分钟后再数是 **172** 个；
写这份文档时又变成 **173**（HEAD `e2cf91f`）。多条工作线在持续提交。

第一轮算出的各目录提交数（`echo-server` 34、`echo-h5-proto` 28、`docs` 105）
与第二轮（39、31、114）全部不一致。两轮都没算错——它们数的不是同一个仓。

### 5.2 教训本身

**任何拿"数量"做校验的动作，在一个活跃写入的仓上都是同一个陷阱：
你数的那一刻和你比对的那一刻不是同一个仓。**

这不是拆仓的注意事项，是通则。同样会踩的场景包括：

- 「未提交文件数」告警——别人 checkout 一下数字就变；
- 「测试用例数应为 N」——另一条线加了用例就红；
- 「接口数量与文档条目对齐」——文档线和后端线同时在写；
- 「资源清单文件数与 MANIFEST 对得上」——出图线正在往资源根里放东西。

**正确做法**：先取一个 SHA（或快照 ID）并记录下来，之后所有计数与比对都对着它做，
把这个 SHA 写进结论里。**没有 SHA 的数量结论没有意义，因为它不可复核。**

**判断是否踩坑的一个提问**：这个数字，换一个人在另一个时刻重跑，能不能得到同一个值？
答不出"能"，就说明缺一个锚点。

---

## 6. 工具与认证现状（勘察时点）

| 项 | 状态 |
|---|---|
| `git filter-repo` | **2.47.0 已装**，可执行文件在 `~/Library/Python/3.9/bin/git-filter-repo`，**未进 PATH**，用时加前缀 `PATH=~/Library/Python/3.9/bin:$PATH` |
| `brew install git-filter-repo` | **走不通**，Homebrew 目录属主不是 `andy`，会报权限错误。不需要——上面那份就够用 |
| `curl` 下载单文件脚本 | **走不通**，沙箱不放行 `raw.githubusercontent.com`，会挂住直到超时（exit 28） |
| SSH 认证 | **已通**。`ssh -T git@github.com` 返回 `Hi Andyx1537!` |
| 远端地址 | 🔴 必须用 SSH（`git@github.com:...`），本机**没有 https 凭据** |
| 四个远端仓 | **全部存在且为空**（`git ls-remote` 返回零个 ref），推送不存在覆盖既有内容的风险。此结论有时效，真推之前重新探一次 |
| `agent-supervision` 的 `origin` | ⚠️ 指向 **https** 地址 `https://github.com/Andyx1537/monitor.git`，推之前需改成 SSH |

---

## 7. 🔴 基准 SHA 的性质：`84a3e86` 不是拆分基准

`84a3e86ad7f2ba7d85c77c2ba3178fd61e2d350c` **只是本次勘察的锚点**，
作用是让 §2 那些数字可复核。**它不是拆分基准，不要拿它开拆。**

真要拆的时候：

1. **先让所有工作线停手并提交完**——工作树里有未提交改动时拆出来的仓会缺内容，
   而且缺得静默（`filter-repo` 只看历史，不看工作树）。
2. **然后重新钉一个 SHA**，记录下来。
3. **在新 SHA 上重算 §2 的全部数字**，作为推送前核对的预期值。
4. 拆分在**副本**上做（克隆到 `/tmp` 或 `~/echo-split-work/`）。
   🔴 `Echo` 本地工作仓的结构一个字节都不许动——多条工作线的工作目录就是它，
   在原地重写历史会让它们当场崩掉，且不可逆。原仓只允许加 remote。

如果拆分与勘察相隔较久，§2 的数字已经完全没有参考价值，
但 §3（命名撞车）、§4（处置裁定）、§5（通用教训）依然成立。

---

## 8. 本次勘察的执行边界

按裁定，本轮**只做勘察与存档，不执行拆分**。已确认未做的事：

- 未在 `Echo` 仓加任何 remote；
- 未跑 `filter-repo`；
- 未 push 任何内容；
- 未 stage 或提交除本文档之外的任何文件（提交本文档时工作树里有其他工作线的未提交改动，
  只 `git add docs/PLAN-repo-split.md`，未触碰）。
