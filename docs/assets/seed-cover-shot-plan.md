# 种子封面逐张规划与复盘表

| 项 | 内容 |
|---|---|
| 角色 | 出图规划台账 + 复盘表 + 热度追踪表；**v1.0 · 2026-08-24** |
| 规格依据 | `Echo/docs/SPEC-visual-shot-taxonomy.md`（六维模型 · 题材枚举 · 配额） |
| 机器可读枚举 | `Echo/docs/assets/shot-taxonomy.json` |
| 数据范围 | `Echo-assets/static/seed-covers/` 全部 **43 张**（`mock.ts` 的 12 张 hero 封面 + 6 个栏目封面池，去重后 43） |
| 参数来源 | **43 张全部由本次逐张读图判定**，非生成侧记录。生成参数与实际观感常有偏差，本表一律以**实际观感**为准 |
| 快照时点 | **2026-08-24 20:00**。同期有并行的出图与入库工作在进行，若 `seed-covers/` 已有新文件或重出版本，本表对应行需重新看图回填 |
| 指标口径对齐 | `SPEC-admin-console.md` v0.1（`§1` 指标口径、`§1.3` 停留护栏、`§2.1` 事件数仓、`§11 A4` 软删口径） |
| 本表不做的事 | 不出图、不改图、不动 `MANIFEST.json`、不动 `mock.ts`。表中所有「建议」均需另行执行 |

---

## 1. 表头口径

| 列 | 说明 |
|---|---|
| 题材线 / 年代 / 地域 / 焦距 / 光圈 / 时段 / 景别 / 主体 | 取值必须落在 `shot-taxonomy.json` 的枚举内 |
| 空景 | `SB4` 为「是」，并须有缺席锚点 |
| 质感 | `TX_*` 标签，可多选 |
| 判定 | ✅ 合格 / ⚠️ 可保留但需调整 / ❌ 建议重做 |

「待定」表示尚未出图或已决定重做——本批 43 张全部已出图，故无「待定」行；下一批新增行再用。

---

## 2. 逐张规划表

### 2.1 宠物 `pet`（封面池 6 张，同时是首屏 6 张 hero）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-pet-collar` | 豆豆今天追到了一只蝴蝶 | home-balcony | E5 | R_METRO | F38 | A40 | T_MORN | FR3 | SB4 | 是 | CLEANBRIGHT · OUTDOOR | ❌ |
| `cover-pet-blanket` | 午后的阳光和小憩 | home-livingroom | E5 | 无法判断 | F44 | A28 | T_MORN | FR4 | SB4 | 是 | OLDWOOD | ⚠️ |
| `cover-pet-ball` | 秋天的落叶，是团团最爱的玩具 | pet-walk | E5 | R_JIANGNAN | F50 | A40 | T_MORN | FR3 | SB2 | 否 | OUTDOOR · CLEANBRIGHT | ✅ |
| `cover-pet-leash` | 下雪了，第一次见到雪的开心模样 | pet-doorway | E5 | 无法判断 | F40 | A40 | T_MORN | FR3 | SB3 | 否 | CLEANBRIGHT | ⚠️ |
| `cover-pet-bowl` | 今天的晚霞，很像你回来的那天 | home-kitchen | E5 | 无法判断 | F44 | A28 | T_INDOOR | FR3 | SB3 | 否 | DIMINDOOR | ⚠️ |
| `cover-pet-slippers` | 吹着晚风，看着海，真好呀 | pet-doorway | E4 | 无法判断 | F44 | A28 | T_AFT | FR3 | SB2 | 否 | DIMINDOOR · OLDWOOD | ⚠️ |

> **本组最严重的问题不是画面，是错配**：6 张 hero 宠物卡里 **4 张封面与文案对不上**——文案说「追到蝴蝶 / 第一次见到雪 / 今天的晚霞 / 看着海」，画面分别是阳台晾衣、玄关等出门、厨房吃饭、玄关趴着，**画面里没有蝴蝶、没有雪、没有晚霞、没有海**。
> **根因**：`/Users/andy/.cursor/.../assets/` 里存在 `cover-pet-snow` / `cover-pet-dusk` / `cover-pet-garden` / `cover-pet-leaves` 四张 PNG，但成品 jpg 目录里没有它们——这批因过饱和被判不合格后被新图替换，而 `mock.ts` 的封面槽位映射没有跟着改。
> **建议**（本表不执行）：要么重出四张对得上文案的图，要么由掌管 `mock.ts` 的一方调整映射。**这条必须先拍板，否则首屏第一眼就是假数据。**

### 2.2 青春 `youth`（封面池 9 张）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-youth-desk` | 课桌下的涂鸦 | campus-classroom | 含混 | R_JIANGNAN | F50 | A28 | T_MORN | FR4 | SB1 | 否 | CLEANBRIGHT | ⚠️ |
| `cover-youth-hoop` | 操场边的自动贩卖机 | campus-playground | E3 | R_NORTH | F38 | A56 | T_DUSK | FR3 | SB1 | 否 | OUTDOOR | ✅ |
| `cover-youth-drawer` | 被收走的漫画书 | campus-classroom | E2 | R_JIANGNAN | F40 | A40 | T_AFT | FR3 | SB4 | 是 | OLDWOOD | ⚠️ |
| `cover-youth-controller` | 第一次通宵的网吧 | home-livingroom | **E2** | R_LINGNAN | F44 | A40 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR | ✅ |
| `cover-youth-bike` | 晚自习后的月亮 | campus-wayhome | E5 | R_JIANGNAN | F50 | A40 | T_AFT | FR3 | SB1 | 否 | OUTDOOR · CLEANBRIGHT | ✅ |
| `classroom-fan-v1` | 靠窗第三排的风扇（hero） | campus-classroom | E2 | R_JIANGNAN | F38 | A40 | T_AFT | FR3 | SB4 | 是 | OLDWOOD | ⚠️ |
| `user-classroom-v1` | 校园记忆 | campus-classroom | E4 | R_JIANGNAN | F44 | A40 | T_MORN | FR3 | SB1 | 否 | CLEANBRIGHT | ⚠️ |
| `basketball-v1` | 一场没人录像的球赛 | campus-playground | 含混 | 无法判断 | F44 | A40 | T_MORN | FR3 | SB1 | 否 | CLEANBRIGHT · OLDWOOD | ⚠️ |
| `user-basketball-v1` | 球赛记忆 | campus-playground | E4 | R_COUNTY | F44 | A28 | T_NIGHT | FR3 | SB1 | 否 | DIMINDOOR | ❌ |

### 2.3 家庭 `family`（封面池 5 张）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-family-sewing` | 奶奶织到一半的毛衣 | home-sewing | **E2** | R_NORTH | F50 | A28 | T_BLUE | FR3 | SB1 | 否 | DIMINDOOR | ✅ |
| `cover-family-wok` | 妈妈的菜谱本 | home-kitchen | E2 | R_LINGNAN | F50 | A28 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR · OLDWOOD | ⚠️ |
| `cover-family-wardrobe` | 抽屉里的钥匙串 | home-livingroom | E2 | R_NORTH | F38 | A40 | T_MORN | FR3 | SB4 | 是 | OLDWOOD | ⚠️ |
| `cover-family-heightmarks` | 老家门后的身高线 | home-livingroom | E1 | **无法判断** | F44 | A28 | T_AFT | FR3 | SB4 | 是 | MOTTLED · OLDWOOD | ❌ |
| `red-suitcase-v1` | 那只红皮箱（hero） | home-livingroom | **E5** | 无法判断 | F44 | A40 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR · OLDWOOD | ❌ |

### 2.4 地点 `place`（封面池 5 张）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-place-busstop` | 天桥上的风 | transit-bus | E5 | R_NORTH | F44 | A56 | T_DUSK | FR3 | SB1 | 否 | OUTDOOR · CLEANBRIGHT | ✅ |
| `cover-place-stairlight` | 第一间出租屋 | home-tongzilou | 含混 | 无法判断 | F40 | A28 | T_NIGHT | FR3 | SB4 | 是 | MOTTLED · DIMINDOOR | ❌ |
| `cover-place-alley` | 巷尾的修车铺 | street-longtang | 含混 | R_JIANGNAN | F44 | A40 | T_BLUE | FR2 | SB4 | 是 | MOTTLED · WETREFLECT | ⚠️ |
| `last-bus-v1` | 末班 302（hero 备选） | transit-bus | E5 | R_METRO | F44 | A28 | T_NIGHT | FR3 | SB1 | 否 | WETREFLECT · DIMINDOOR | ⚠️ |
| `user-last-bus-v1` | 末班车记忆 | transit-bus | E4 | R_METRO | F44 | A28 | T_NIGHT | FR4 | SB1 | 否 | DIMINDOOR | ❌ |

### 2.5 关系 `relationship`（封面池 4 张）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-bond-cassette` | 共同用过的歌单 | home-livingroom | E2 | R_NORTH | F44 | A40 | T_MORN | FR3 | SB4 | 是 | OLDWOOD | ⚠️ |
| `cover-bond-letter` | 没有寄出的明信片 | home-livingroom | E1 | R_JIANGNAN | F44 | A28 | T_AFT | FR3 | SB4 | 是 | OLDWOOD · DIMINDOOR | ⚠️ |
| `cover-bond-mugs` | 朋友搬家留下的杯子 | home-livingroom | **E5** | 无法判断 | F38 | A56 | T_MORN | FR3 | SB1 | 否 | CLEANBRIGHT | ⚠️ |
| `cassette-v1` | A 面第七首（hero） | home-livingroom | E1 | R_NORTH | F44 | A40 | T_AFT | FR3 | SB4 | 是 | **MOTTLED · OLDWOOD · DIMINDOOR** | ⚠️ |

### 2.6 日常 `daily`（封面池 6 张）

| 文件名 | 对应文案 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cover-daily-camera` | 每天路过的花店 | home-balcony | E4 | R_LINGNAN | F38 | A56 | T_MORN | FR3 | SB1 | 否 | CLEANBRIGHT · OUTDOOR | ✅ |
| `cover-daily-mug` | 抽屉底的硬币 | home-washcorner | E1 | 无法判断 | **F60+** | **A20** | T_AFT | **FR6 特写** | SB4 | 是 | OLDWOOD · DIMINDOOR | ❌ |
| `cover-daily-shirt` | 雨天晾不干的校服 | home-livingroom | E5 | 无法判断 | F38 | A56 | T_MORN | FR3 | SB4 | 是 | CLEANBRIGHT | ❌ |
| `cover-place-noodle` | 凌晨四点的便利店 | street-nightmarket | E3 | R_LINGNAN | F50 | A28 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR · MOTTLED | ⚠️ |
| `noodle-shop-v1` | 巷口那碗面（hero 备选） | street-nightmarket | E3 | R_LINGNAN | F44 | A28 | T_NIGHT | FR3 | SB1 | 否 | **WETREFLECT · DIMINDOOR** | ⚠️ |
| `user-noodle-shop-v1` | 面馆记忆 | street-nightmarket | E4 | 无法判断 | F40 | A40 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR | ❌ |

### 2.7 仅在 hero 使用 + 未入池的版本变体（8 张）

| 文件名 | 用途 | 题材线 | 年代 | 地域 | 焦距 | 光圈 | 时段 | 景别 | 主体 | 空景 | 质感 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `user-classroom-v3` | hero「靠窗第三排的风扇」 | campus-classroom | E3 | R_JIANGNAN | F38 | A56 | T_MORN | FR3 | SB1 | 否 | CLEANBRIGHT | ✅ |
| `user-last-bus-v3` | hero「末班 302」 | transit-bus | E3 | R_JIANGNAN | F50 | A40 | T_BLUE | FR3 | SB1 | 否 | WETREFLECT | ✅ |
| `user-noodle-shop-v3` | hero「巷口那碗面」 | street-nightmarket | E4 | 无法判断 | F44 | A28 | T_NIGHT | FR5 | SB1 | 否 | DIMINDOOR · WETREFLECT | ⚠️ |
| `user-basketball-v3` | hero「最后一个三分球」 | campus-playground | **E5** | R_METRO | F38 | A80 | T_MORN | FR2 | SB1 | 否 | OUTDOOR · CLEANBRIGHT | ⚠️ |
| `user-classroom-v2` | 未入池 | campus-classroom | E4 | 无法判断 | F44 | A40 | T_DUSK | FR3 | SB1 | 否 | CLEANBRIGHT | ✅ |
| `user-basketball-v2` | 未入池 | campus-playground | E4 | R_COUNTY | F40 | A56 | T_DUSK | FR2 | SB1 | 否 | OUTDOOR · CLEANBRIGHT | ✅ |
| `user-last-bus-v2` | 未入池 | transit-bus | E5 | 无法判断 | F35 | A28 | T_NIGHT | FR3 | SB4 | 是 | DIMINDOOR | ⚠️ |
| `user-noodle-shop-v2` | 未入池 | street-nightmarket | E4 | 无法判断 | F44 | A40 | T_INDOOR | FR3 | SB1 | 否 | DIMINDOOR | ⚠️ |

---

## 3. 优缺总结

### 3.1 标杆（直接作为下一批的参考锚点）

| 文件 | 好在哪 |
|---|---|
| `cover-family-sewing` | 六维全部到位的一张：50mm / f2.8 / 蓝调 / E2 年代道具（脚踏缝纫机、线轴盘、软尺）/ 北方家属院窗景 / 全景 / 人 / 侧脸低头合规。**它同时给出了年代、地域、时段和一个具体动作**，这正是「让人停下 + 让人相信」的画面公式 |
| `cover-youth-controller` | 年代表达的标杆：CRT 电视、录像机、花沙发、台扇、吊灯、瓷砖地——道具密度足够让人一眼读出 90s；两个男孩全是背影，B 档合规且不牺牲叙事 |
| `cover-youth-bike` | 明亮档的标杆：梧桐林荫、两个骑车背影、远处站台有人。**这是全库唯一一张既明亮、又有活物、又有纵深、又不落斑驳的图** |
| `user-classroom-v2` | 叙事最好的教室图：值日生擦窗与扫地、椅子翻上桌、黄昏斜光。可惜未入池 |
| `user-basketball-v2` | 前景锚点用得对：一排堆在地上的书包压住画面下缘，把远景球场稳住，主体没有变成小点 |
| `user-last-bus-v3` | 合规处理的范本：站牌做成**空白无字**，既保留了「站牌」的符号，又零文字风险 |

### 3.2 必须重做（9 张）

| 文件 | 问题 |
|---|---|
| `cover-daily-mug` | **踩死构图红线**：搪瓷杯占满画面的静物大特写（`FR6`），背景纸堆彻底虚化不可读。这是「物体大特写」与「背景不可读」两条红线同时踩 |
| `cover-place-stairlight` | **过暗到不可用**：楼道夜景整体压在暗部，共鸣厅缩略图里几乎是一块黑色。且纯空景无缺席锚点，只是一段空楼梯 |
| `cover-family-heightmarks` | **地域完全跑偏**：法式百叶窗 + 人字拼木地板 + 土黄墙，画面不像任何一个中国家庭。文案是「老家门后的身高线」，画面给的是南欧民居 |
| `red-suitcase-v1` | **年代与文案错位**：文案「红皮箱……拉链一直卡在二十年前」，画面是当代拉杆箱（万向轮 + 复合木地板）。二十年前的红皮箱应该是硬壳、方角、金属搭扣 |
| `cover-daily-shirt` | **样板间**：现代卧室，无年代、无地域、无生活痕迹。缺席锚点（拖鞋、椅背衣服）有，但整张图不属于任何人的记忆 |
| `cover-pet-collar` | **宠物栏目里没有宠物**，也没有任何宠物痕迹（无碗、无窝、无项圈）。作为 hero 首卡，文案还是「追到了一只蝴蝶」 |
| `user-basketball-v1` | 夜晚小区球场压得极暗，篮球题材第 5 张，无增量信息 |
| `user-last-bus-v1` | **暗到细节不可读**：车厢内部几乎全黑，只有窗外霓虹是亮的。B 档人脸处理本身很好（发丝遮脸），可惜整张图在瀑布流里会塌成黑块 |
| `user-noodle-shop-v1` | **B 档执行失败**：人物面部的柔化处理生硬，形成明显的糊状伪影，观感是「图坏了」而不是「侧脸不可辨」。柔化应该靠角度与光线，不是靠后期抹 |

### 3.3 需要调整但可保留

- **偏暗一档**（8 张）：`cover-bond-letter`、`cover-family-wardrobe`、`cassette-v1`、`cover-family-wok`、`cover-pet-bowl`、`cover-pet-slippers`、`noodle-shop-v1`、`user-last-bus-v2`。共同点是**白天/室内场景被压成暗调**——时段填的是上午或午后，实际观感却接近黄昏。这不是时段问题，是明度问题，调色即可救回，不必重出。
- **无地域**（16 张）：见 §3.4 ③。
- **合规存疑，需逐张终判**（7 处）：`cover-youth-controller` 左上挂历的日期栏、`cover-family-wok` 调料瓶标签、`user-classroom-v1` 女生手中书页、`cassette-v1` 桌上摊开的本子与墙上画的落款、`cover-bond-cassette` 书脊、`user-noodle-shop-v3` 手中纸片、`noodle-shop-v1` 面馆门头的圆形标志。**这些位置都存在「像字但不成字」的纹样**，属于典型的 AI 伪文字，在缩略图下不明显、放大后可辨。按 `ASSETS.md §5` 的入库确认口径，这七处需要人工终判。

### 3.4 系统性问题（数据化）

把 43 张按 `shot-taxonomy.json` 的题材线归类，问题一目了然：

| 题材线 | 实际张数 | 占比 | 配额上限 | 状态 |
|---|---|---|---|---|
| 家庭/居所 `home` | **17** | **40%** | ≤8 | 🔴 超一倍 |
| 校园 `campus` | **12** | **28%** | ≤8 | 🔴 超 50% |
| 街巷 `street` | 6 | 14% | ≤8 | ✅ |
| 交通 `transit` | 5 | 12% | ≤7 | ✅ |
| 宠物 `pet`（长在场景里的） | 3 | 7% | ≤8 | ⚠️ 偏少 |
| 工厂 `factory` | **0** | 0% | ≤6 | 🔴 完全空白 |
| 娱乐 `leisure` | **0** | 0% | ≤7 | 🔴 完全空白 |
| 自然节令 `season` | **0** | 0% | ≤7 | 🔴 完全空白 |

**① 两条线吃掉 68%，三条线完全空白。** 枚举里的 49 条具体题材，实际只用到 **14 条**。「元素也多元一些」这句反馈，在数据上就是这张表。

**② 五个题材簇占掉 60%。** 更细一层看，43 张里有 26 张挤在五个簇里：

| 簇 | 张数 | 文件 |
|---|---|---|
| 教室 | **6** | `cover-youth-desk`、`cover-youth-drawer`、`classroom-fan-v1`、`user-classroom-v1/v2/v3` |
| 篮球 | **5** | `cover-youth-hoop`、`basketball-v1`、`user-basketball-v1/v2/v3` |
| 面馆 | **5** | `cover-place-noodle`、`noodle-shop-v1`、`user-noodle-shop-v1/v2/v3` |
| 公交站/末班车 | **5** | `cover-place-busstop`、`last-bus-v1`、`user-last-bus-v1/v2/v3` |
| 卧室/衣柜/床 | **5** | `cover-family-wardrobe`、`cover-daily-shirt`、`red-suitcase-v1`、`cover-bond-cassette`、`cover-family-heightmarks` |

按 DR-2「单条具体题材 ≤2 张」，这五个簇每一个都超标 **2.5–3 倍**。**「同质化」这个抱怨，量化后就是这 26 张。**

**③ 16 张（37%）读不出地域，西南 / 沿海两个地域为 0，县城只有 2 张。**

| 地域 | 实际 | 配额 | 状态 |
|---|---|---|---|
| 江南 | 10 | 7–9 | ⚠️ 略超 |
| 北方 | 6 | 8–10 | 🔴 不足 |
| 岭南 | 5 | 5–6 | ✅ |
| 大城市 | 4 | 5–7 | ⚠️ |
| 县城 | 2 | 6–8 | 🔴 不足 |
| 西南 | **0** | 4–5 | 🔴 空白 |
| 沿海 | **0** | 3–4 | 🔴 空白 |
| **无法判断** | **16** | 0 | 🔴 |

其中 7 张更严重——**画面根本不在中国的语境里**：`cover-bond-mugs`、`cover-daily-shirt`、`cover-pet-blanket` 是北欧/日式样板间；`user-noodle-shop-v1/v2/v3` 是日式居酒屋；`cover-family-heightmarks` 是南欧民居。共鸣厅要的是「我也去过」，一张日式居酒屋换不来中国用户的这句话。

**④ 真正的年代问题不是「太旧」，是「太新」。** 逐张统计年代：

| 年代 | 实际 | 配额 | 状态 |
|---|---|---|---|
| E1 80s | 4 | 4–6 | ✅ |
| E2 90s | **7** | 10–12 | 🔴 不足 |
| E3 00s | **5** | 10–12 | 🔴 严重不足 |
| E4 10s | 10 | 6–8 | ⚠️ 略超 |
| E5 当代 | **13** | 6–8 | 🔴 超 63% |
| 年代含混 | 4 | 0 | 🔴 |

**E2+E3（90s–00s，集体记忆峰值）只有 12 张，占 28%；而 E4+E5 当代占 23 张，53%。** 这与「怀旧主题集」的定位是反的。更麻烦的是，这 23 张当代里有大半是 §3.4 ③ 说的样板间——**既没有年代，也没有地域**。所以下一批的重点不是「再做旧一点」，而是**把年代真正落到 90s–00s 的具体器物上**。

**⑤ 「斑驳」的真实构成，与直觉不完全一致。** 逐张统计质感标签：

| 质感 | 张数 | 占比 | 配额 | 状态 |
|---|---|---|---|---|
| `TX_DIMINDOOR` 昏黄室内 | **18** | **42%** | ≤9 | 🔴 超一倍 |
| `TX_OLDWOOD` 旧木家具 | **13** | **30%** | ≤8 | 🔴 超 63% |
| `TX_MOTTLED` 斑驳墙面 | 5 | 12% | ≤11 | ✅ |
| `TX_WETREFLECT` 潮湿反光 | 5 | 12% | ≤6 | ✅ |
| `TX_CLEANBRIGHT` 明亮干净 | 15 | 35% | ≥13 | ✅ |
| `TX_OUTDOOR` 户外自然光 | **7** | **16%** | ≥17 | 🔴 严重不足 |
| 三件套去重合计 | **27** | **63%** | ≤42% | 🔴 |

两个反直觉的结论：

- **真正超标的不是「斑驳老墙」（只有 5 张，12%，本就不超标），而是「昏黄室内」（18 张，42%）。** 用户看到的「斑驳感」，主要来自**整体压暗的室内**，而不是墙面剥落。
- **户外只有 7 张（16%）**，目标是 ≥17 张。43 张里有 36 张是在室内或夜里拍的。

所以下一批的矫正重点应该是**把光打亮、把人放到户外**，而不是简单地少画几堵破墙。这一条与原话有偏差，需要确认（见 §6 开放问题 4）。

**⑥ 广角几乎不存在。** 43 张里 `F35` 及更广的只有 **1 张**（`user-last-bus-v2`，约 35mm），占 2%，远低于 8–10 张的目标。制作人说「广角什么的都要带点」，目前是一点都没有。

**⑦ 做对了的地方。** 活物 29 张 / 空景 14 张 = **67% / 33%**，7:3 的活物比例**基本达标**；明亮档 `TX_CLEANBRIGHT` 15 张达标；`user-last-bus-v3` 的空白站牌证明「零文字」是能做到的。下一批不需要动这三条。

### 3.5 下一批改进方向（按优先级）

1. **补三条空白线**：工厂线 4–6 张、娱乐线 5–7 张、自然节令线 5–7 张。这是打散同质化最快的手段——这三条线的场景与现有 43 张没有任何重叠，且天然是户外/大空间/明亮的，能一并解决 ③④⑤⑥ 四个问题。
2. **砍题材簇**：教室 6→2、篮球 5→2、面馆 5→2、车站 5→2、卧室 5→2，共腾出 **16 个位置**，正好给第 1 条。
3. **把人放到户外、把光打亮**：`TX_OUTDOOR` 从 7 张补到 ≥17 张，`TX_DIMINDOOR` 从 18 张压到 ≤9 张。其中 §3.3 那 8 张「白天拍成暗调」的调色即可救回，不必重出。
4. **把年代往回拉**：E2+E3 从 12 张补到 20–24 张，E5 从 13 张压到 6–8 张。手段是每张 prompt 强制落 3–4 件该年代的具体器物（见 `SPEC §1.3.2` 的道具表），含混即打回。
5. **补广角**：8–10 张，优先给操场、大礼堂、春运候车、露天电影、秋收晒谷场——都在空白线里，与第 1 条重合。
6. **补地域**：西南、沿海各补 3–5 张，县城补到 6–8 张；7 张「不在中国语境」的重做。
7. **修 hero 宠物卡的封面-文案错配**（见 §2.1）。这一条最便宜，也最紧急。

**净重做规模估算：必须重做 9 张 + 题材簇腾挪 16 张 - 可复用的重叠部分 ≈ 需要新出 14–18 张**，其余可通过调色与重新映射解决。

---

## 4. 热度 / 喜好度追踪列（预留，待后台埋点落地后回填）

> ### 🔴 红线：本节所有指标**只在本表与运营后台出现，永不对 C 端暴露**
> 依据 `DECISIONS D4`（无数字、无排名、不悲伤竞赛）、`SPEC-trust-and-compliance §CM-G5 TC-DW-02`（互动统计仅后台可见）、`SPEC-feature-pages`（结果卡不出现记得数/献花数/看过数，红线落到字段级）、`SPEC-admin-console §0`（后台是唯一允许出现精确数字的地方）。
>
> 另一条：`SPEC-admin-console §1.5` 明令禁止后台出现**用户排行榜**。本表是**素材维度**的复盘表，聚合到封面文件、不聚合到作者——**不得被改造成作者榜或窗口榜**。

### 4.1 指标列定义（口径对齐 `SPEC-admin-console §1` 与 `API-CONTRACT §13`）

| 列名 | 含义 | 计算口径 | 数据来源（既有事件） | 用途 |
|---|---|---|---|---|
| `cover_seen` | 曝光数 | 卡片在共鸣厅被看见 | **`window_seen`**（`API-CONTRACT §13` 已有） | 分母 |
| `cover_open` | 进窗数 | 点开该窗口详情 | **`window_open`**（已有） | 分子 |
| **`open_rate`** | **进窗率** | `cover_open / cover_seen` | 派生 | **封面好坏最直接的指标** |
| `remember_rate` | 记得率 | `remember_toggle / cover_open` | **`remember_toggle`**（已有） | 封面是否吸引到对的人 |
| `heart_rate` | 心意率 | `flower_offer / cover_open` | **`flower_offer`**（已有） | 同上，更强的心意表达 |
| `catch_rate` | 被接住率 | 该窗口 7 天内获 ≥1 条合规回声且作者未撤回 | `SPEC-publish-and-ops §4` 北极星口径下沉到素材 | **与北极星对齐的主目标** |
| `meaningful_action_rate` | 有意义动作率 | 进窗后发生 ≥1 次「有意义动作」的占比 | `SPEC-admin-console §1.3` 的有意义动作清单 | 与 DAU 主口径同源：衡量封面带来的是用户还是观光客 |
| `dwell_p50` | 停留中位数 | 详情页停留时长 P50 | 停留信号 | ⚠️ **护栏，非目标**（见 §4.2） |
| `quick_exit_rate` | 秒退率 | 进窗后 2 秒内退出的占比 | 派生 | ⚠️ 护栏：识别「封面骗点」 |
| `report_rate` | 举报率 | 举报数 / 曝光数 | 审核链路 | 负向 |

聚合方式对齐 `SPEC-admin-console §2.1`：读**离线日聚合表**，不实时扫 `t_event`。

### 4.2 ⚠️ 与 CM1 的冲突，必须先说清楚

制作人点名要「停留时长」这一列，但 `DECISIONS CM1` 明确裁定：**推荐主目标 = 被接住率 / 续发率 / 健康度，停留信号降为弱信号 / 负向护栏，不做最大化目标**（已修订 D19）。`SPEC-admin-console §1.3` 把这条执行得更死：**停留时长只作异常告警项，不得出现在概览主卡、不得设增长目标、不得进推荐权重。**

本表与之保持一致：**保留 `dwell_p50` 列，但改变它的用法**——不用它评选「最好的封面」，只用它做两件事：

1. **配合 `open_rate` 识别封面骗点**：高进窗率 + 低停留 + 高秒退率 = 封面许诺了内容没兑现的东西。这类封面要降权，哪怕它的进窗率很高。
2. **识别「被围观 / 消费悲伤」**：高停留 + 低记得 + 低心意，说明用户在看热闹而不是在共鸣，按 CM1 该降权。

**选封面的主指标用 `catch_rate` + `remember_rate` + `meaningful_action_rate`，不用 `dwell_p50`。** 这一条需要制作人确认（见 §6 开放问题 1）。

### 4.3 需要后台提供的字段（阻塞项）

已与并行落地的 `SPEC-admin-console.md`（v0.1）对齐。结论是：**曝光与互动事件本身已经存在**（`window_seen` / `window_open` / `remember_toggle` / `flower_offer`，见 `API-CONTRACT §13`），缺的不是事件，而是**素材维度**。

| # | 缺口 | 说明 | 阻塞什么 |
|---|---|---|---|
| **1** | **`props.coverId`** | `API-CONTRACT §13` 每事件只带 `accountId / isGuest / ts / ctx`，**没有封面维度**。需要在 `t_event.props` 里加 `coverId`（取 `seed-covers/` 文件名去扩展名，如 `cover-family-sewing`） | 没有它，本表所有热度列**一列都填不了**——行为归因不到具体某张图 |
| **2** | `props.position` | 卡片在瀑布流中的位置序号 | 必须做位置纠偏，否则排在前面的封面天然占优，横向比较无意义 |
| **3** | `props.category` | 栏目（pet/youth/family/place/relationship/daily） | 分栏目复盘 |
| **4** | `window_seen` 的触发阈值 | 目前未定义。建议：卡片进入视口 ≥50% 且驻留 ≥500ms 计 1 次，同一会话同一卡去重 | 阈值不定死，`open_rate` 在不同实现下不可比 |
| **5** | 素材维度日聚合表 | 建议 `t_cover_daily { coverId, date, seen, open, remember, flower, dwellP50, quickExit }` | 对齐 `SPEC-admin-console §2.1`「后台读离线日聚合表」 |
| **6** | 软删口径 | 按 `SPEC-admin-console §11 A4` 的建议——**计入历史分母、不计入当期展示** | 该项**仍待裁定**：同一问题在 `SPEC-trust-and-compliance §P-2`（QA R-2）给的建议是「默认排除软删」，两处口径不一致，需要一次统一裁定 |

> 一个封面会被多个窗口复用（`mock.ts` 按 `index % pool.length` 轮转），所以 `coverId` 与 `windowId` 是**多对多**，聚合时须按 `coverId` 汇总而非按窗口，否则同一张图的数据会被拆散在十几个窗口里。

### 4.4 回填表（列已备好，数据待数据基座上线）

| 文件名 | `cover_seen` | `cover_open` | `open_rate` | `remember_rate` | `heart_rate` | `catch_rate` | `meaningful_action_rate` | `dwell_p50` | `quick_exit_rate` | 复盘结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| （43 行，与 §2 逐张表同序） | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待数据基座 | 待回填 |

> 上线后按 §2 的顺序展开为 43 行。在 `coverId` 埋点落地之前，这些格子一律填**「待数据基座」而不是 0**——对齐 `SPEC-admin-console §3.1`：`0` 和「没接上」是两件事。填了估算值，下一轮复盘就会基于假数据调配额。

---

## 5. 使用闭环

```text
① 出图前 —— 查表规划
   在 §2 新增一行，填满六维 + 地域
   对照 SPEC §4 配额与打散规则，确认不超标
   按 SPEC §3 拼 prompt（STYLE_BASE + 槽位 + NEGATIVE_BASE）
        ↓
② 出图后 —— 回填实际参数
   逐张看图，以实际观感回填（不以生成参数为准）
   逐张过 SPEC §5 合规确认：文字 / 人脸 / 品牌
   判定 ✅ / ⚠️ / ❌，❌ 的回到 ①
        ↓
③ 入库 —— 按 ASSETS.md §5
   压到 200KB 以内 → 重建 MANIFEST.json → 前端走 assetUrl()
        ↓
④ 上线后 —— 回填热度
   按 §4 的列回填，来源是后台离线日聚合表（需先补 props.coverId）
        ↓
⑤ 定期复盘 —— 调整配额与题材权重
   每批出图后跑一次 §3.4 的配额核对
   按 catch_rate / remember_rate 调高表现好的题材线权重
   dwell_p50 只用于识别封面骗点，不用于选优（CM1）
        ↓
   回到 ①
```

**复盘节奏建议**：每批出图后立即跑一次配额核对（不依赖线上数据，当天可做）；热度复盘随运营周报，与 `OPERATION-SEED-CONTENT-RESEARCH-AND-MANIFEST` 的「每周按主题复盘」合并进行，不单开一套节奏。

---

## 6. 待拍板的开放问题

| # | 问题 | 选项 | 建议 |
|---|---|---|---|
| **1** | 选封面的**主指标**用什么？制作人点名要「停留时长」，但 CM1 裁定停留不作最大化目标 | A. 用 `dwell_p50` 选优（与 CM1 冲突）<br>B. 用 `catch_rate` + `remember_rate` 选优，`dwell_p50` 只做护栏 | **B**。CM1 是已裁定项，不宜为封面单开例外；且「停留久」在记忆类内容里可能正是「被围观」，方向相反 |
| **2** | hero 宠物卡的**封面-文案错配**（4/6 张）怎么修 | A. 重出 4 张对得上文案的图（蝴蝶/雪/晚霞/海）<br>B. 由掌管 `mock.ts` 的一方改封面映射<br>C. 改文案 | **B 优先**，改一行映射即可；蝴蝶、晚霞这类题材本身在新枚举里权重不高，为它们单独出图不划算。但**必须尽快定**，这是首屏第一眼 |
| **3** | 密集人群场景中，**前景人物被下框裁切**算不算违反「全身在框内」 | A. 严格执行，`cover-youth-desk`、`user-classroom-v3`、`user-noodle-shop-v1` 等都要重做<br>B. 坐姿/密集人群列为显式例外 | **B**。教室后排、面馆坐姿这类场景，强行让所有人全身入框只能靠退到很远，反而踩「主体变成小点」。建议在规格里写成显式例外而非默认放行 |
| **4** | 「斑驳」的矫正方向 | A. 按字面减少斑驳墙面（实测只有 5 张，12%，本就不超标）<br>B. 按实测矫正**昏黄室内**（17 张，40%，严重超标） | **B**。数据显示用户看到的「斑驳感」主要来自整体压暗的室内。但这与原话有偏差，请确认是否认可这个判断 |
| **5** | 当代档（E4/E5）的画风 | A. 保留现有的「北欧/日式样板间」风（`cover-bond-mugs`、`cover-daily-shirt`、`cover-pet-blanket`）<br>B. 重做成有中国生活痕迹的当代（阳台晾衣、快递纸箱、老小区改造房） | **B**。当代档的意义是让今天的用户找到「我也有」的入口，样板间给不了这个 |
| **6** | 7 处**疑似文字纹样**（§3.3）谁来终判 | A. 出图方自查<br>B. 按 `ASSETS.md §5` 入库前人工逐条确认<br>C. 一律重做 | **B**。这些是「像字但不成字」的 AI 伪文字，在缩略图下看不出、放大可辨，需要人眼确认而非规则判定 |
| **7** | 本批 43 张的**重做规模** | A. 只修 9 张必重做的<br>B. 按配额全面矫正（需新出 14–18 张） | **B**，但可分两批：先出三条空白线（工厂/娱乐/自然节令）的 10 张，跑一轮数据再决定砍哪些簇 |
