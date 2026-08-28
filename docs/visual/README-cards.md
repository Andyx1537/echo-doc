# B18 回忆卡卡型 · 第三轮

## 概述

本轮只做一件事：**重排回忆卡**，并把「它的一生」收成一个点。暖光线按指令**全线停手**，本轮没有动暖光的任何代码与图。

**已定论：**

- ✅ **卡型定为甲「图下一行」**（产品拍板 2026-08-26）。3:2 大图 354×236 + 图外一行 46px，图占 84%。
  🔴 **甲的真实落地（接进陌生人窗口页）尚未做**，它依赖后端 `cards[]` 契约（`C-2`）。现在能看到的只有 `src/dev/` 里的设计稿。
- ✅ **默认排序 = 作者置顶的在前，其余按发布时间倒序**（产品拍板 2026-08-26）。
  🔴 **置顶的字段与端点归后端**，本线只出前端形态，不自造接口。前端形态见 §八。
- **一行文字的取值链 = `title` → 正文首句**，不是「只取 `title`」。AI 回声与手写 `record` 都没有标题，只取 `title` 会让这两类卡整类露出空位。实现见 `designData.ts` 的 `cardLine()`。
- **日期与文字同一行，日期 `flex:none` 永不收缩**，文字先让位收省略号。
- **无图的卡不留空图位，换成「便签」形态**：暖色竖边 + 正文三行 + 底部日期。便签把「一行」的约束放宽到三行 —— 没有图的时候字就是内容本身。
- **「它的一生」从横滑一整行收成 44px 的一行**，就地展开成**纯文字**时间线（不给图）。里程碑本来常常没有对应照片，上一版那三张抽象封面是排版凑出来的，不是内容。
- **卡片上不出互动数、不出「被记得」**。那是窗级信号，落到每张卡上就变成逐条比数量（`D5`）。

- 🔴 **主题标签不上卡封面（已拍板 2026-08-27，已在代码里删干净）**。题材改走**列表顶上的筛选器**，那是另一件事。理由与对比图见 §七。

**🔴 仍然待定（需产品拍板）：**

- **折叠阈值取 3 还是别的数。** 本轮沿用 3。定它需要知道公开卡数量的真实分布 —— 目前没有线上数据。
- ~~主题标签出不出在卡封面上。~~ 🔄 **2026-08-27 已拍：不出。** 见 §七。

**与其他文档的关系：** 可见性红线与本轮无关，一格未动，见 `README-redesign.md`；卡级可见性的契约需求同样见该文档，本轮未新增契约项。

---

## 一、四种卡型，同一份数据、同一个位置

![四种卡型并排](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-4types-side-by-side.png)

| | 图 | 版式 | 代价 |
| --- | --- | --- | --- |
| **甲 图下一行（推荐）** | 84% | 354×236（3:2）+ 图外一行 | 每张卡多 46px 米色纸 |
| 乙 全图压字 | 100% | 354×300（5:6）文字压在图底渐变 | 强制竖裁 + 字压在图上 |
| 丙 双列相册 | 83% | 1:1 双列，一屏六张 | 一行只剩十来个字 |
| 丁 大图浮层 | 100% | 与甲同一张 3:2 大图，一行改成毛玻璃胶囊浮在图内 | 胶囊压掉照片下半的一条带 |

⚠️ **「图占比」这个数会骗人。** 四种卡型的图**一样宽**（都是 354），甲和丁的图**连高度都一样**（236）。84% 与 100% 的差别不是「图更大」，是**那 46px 说明文字落在纸上还是压在图上**。真正让图变大的只有乙（300 高的竖构图），而它的代价是强制竖裁。

单张大图见：
`cards-type-A-image-below-text-RECOMMENDED.png` ·
`cards-type-B-full-bleed-overlay.png` ·
`cards-type-C-two-column-album.png` ·
`cards-type-D-floating-capsule.png`

## 二、为什么推荐甲

1. **字不压图。** 这是纪念类产品里唯一不该让步的一条。乙和丁都要在照片上挖出一条带来放字，而这条带落在照片的下三分之一 —— 恰恰是宠物最常出现的位置。对照 `cards-type-D-floating-capsule.png` 第二张卡：胶囊正好压住了那只猫窝。
2. **暗照片、亮照片都稳。** 甲的字在米色纸上，和照片的明暗无关。乙靠压暗带，丁靠毛玻璃 —— 丁的胶囊做到 `.94` 不透明才在暗巷那张上读得出来（`.84` 时第一个字直接糊掉）。
3. **无图卡的落差最小。** 乙和丁的文字寄生在图上，没有图时整个卡型不成立，必须整体换形态；甲只是去掉上半张图，那一行的位置和读法都没变。
4. **不强制裁剪比例。** 3:2 对横图友好，对竖图也只裁掉上下；乙的 5:6 会把横图切掉一半宽，而用户相册里横图占多数。
5. **丙不适合做主列表。** 一行只剩十来个字（见图上「雨夜屋檐下…」），文案是这一屏的情绪来源，砍到六个字就只剩索引功能了。丙更适合将来的「全部回忆卡」二级页。

**如果产品要的是「图再大一点」**，第二顺位是乙而不是丁 —— 乙的图确实更大（300 vs 236），丁只是把 46px 的纸省掉了，付出的却是压住照片。

## 三、边界

![四种卡型的边界表现](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-4types-edge-cases.png)

推荐卡型下逐条看：

![超长标题](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-edge-longtitle-recommended.png)

![无标题与无图](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-edge-notitle-noimage-recommended.png)

- **超长标题**（`title` 上限 30 字，样本顶格）：「那年冬天特别冷，它在窗台上守…」+ 日期。日期不被顶走。
  ⚠️ 实现上的坑：`.ct-line-text` 必须写 `min-width: 0`。flex 子项默认 `min-width: auto`，不改的话超长文字会把日期整个顶出容器而不是自己收省略号。
- **无标题**（AI 回声 / 手写 record 的常态）：回落到正文首句「风把窗帘吹得轻轻动，它好像在…」。卡上看不出它没有标题。
- **无图**（手写 record）：退成便签，暖色竖边 + 正文三行 + 主题 + 日期。一列大图里夹一张纸，在节奏上反而是一次换气；给它配一个灰框才是承认排版失败。

## 四、密度

![只有一张卡](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-density-1card-recommended.png)

![十二张卡](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-density-12cards-top-recommended.png)

![十二张卡 · 往下刷](/Users/andy/Documents/workSpace/Echo/docs/visual/cards-density-12cards-scrolled-recommended.png)

- **1 张**：不折叠、不出「看全部」。这一屏下面还有明信片和动作条接着，所以不会真的空（见 §五的完整一屏）。
- **12 张**：默认只出前 3 张 + 「还有 N 张 · 看全部」。上面两张密度图是**放开折叠后**的样子，用来看连续刷的节奏 —— 每张 282px，一屏两张半，读起来是相册而不是瀑布流。

## 五、推荐卡型的完整一屏

![完整一屏 · 上](/Users/andy/Documents/workSpace/Echo/docs/visual/stranger-v2-recommended-cards-screen1.png)

![完整一屏 · 下](/Users/andy/Documents/workSpace/Echo/docs/visual/stranger-v2-recommended-cards-screen2.png)

顺序：封面 hero → 一句引言 → **「它的一生」一行** → **公开回忆卡（主体）** → 明信片 → 动作条。

版面预算的分配是刻意的：一生 44px、引言约 110px，其余全部给回忆卡。省下来的空间**没有填别的**。

## 六、「它的一生」收成一个点

![收起态与展开态](/Users/andy/Documents/workSpace/Echo/docs/visual/lifebook-dot-collapsed-vs-expanded.png)

单张：`lifebook-dot-collapsed.png` · `lifebook-dot-expanded.png`

- **收起态**：一行 44px。左边一个暖色圆点，「它的一生」+ 年份区间 + 「3 个节点」+ ⌄。
- **展开态**：**就地**展开，不用弹层。这一段是「顺手看一眼」的性质，弹层会把它升格成一次独立浏览，比横滑还重。
- **展开也不给图。** 上一版三张抽象封面是为了撑横滑片凑出来的；里程碑本来就常常没有照片（「相遇那天」谁也没来得及拍）。纯文字时间线反而更像一份年表。
- 竖线只连节点之间，不从头拉到尾 —— 拉满会被读成进度条。

对照上一版（`stranger-v2-full.png`）：横滑片带走 120px 且**带图**，在视觉上和下面的回忆卡是同一个量级，等于给它保留了一块和主内容抢注意力的位置。收成一行之后，这一屏只剩一个主体。

## 七、主题标签 chip 出不出

同一份数据、同一个位置、都用甲卡型，只差 chip 在不在。

**一屏之内（真实 390 视口，一次三张）——** 看不出问题，两版都干净：

![chip 有无 · 手机一屏](/Users/andy/Documents/workSpace/Echo/docs/visual/topic-chip-on-vs-off-phone.png)

**连着看六张（版面仍按 390 排，整体缩着显示）——** 差别才出来：

![chip 有无 · 多卡密度](/Users/andy/Documents/workSpace/Echo/docs/visual/topic-chip-on-vs-off-density-RECOMMEND-OFF.png)

**我的建议：不上封面。** 三条理由，都能在第二张图上直接看到：

1. **它们排成了一条竖线。** chip 固定在每张封面的右上角，六张连着看就是右边缘一串位置完全一样的深色药丸。眼睛会先把这一串读成界面构件，再去读照片 —— 而这一列的主角本该是照片。
2. **标签在重复，信息却没增加。** 图里六张有四张挂着「日常」。一个在多数卡上取同一个值的标签，占的是每张卡固定的一个角，换回来的区分度接近零。
3. **一张封面已经有一个角标了。** AI 角标在左下、必须留（那是出处披露，不是装饰）。再加一个就是两个角都被占，"碎"正是从这里来的。

**主题本身有用，只是不该按张出。** 它的价值在「我想找它散步的那些」这种筛选诉求上 —— 那是列表顶上一行筛选器该干的事，或者点进卡之后详情里的一行，而不是在每一张卡上重复一遍。

🔴 **2026-08-27 已拍：不上封面。** chip 已从代码里删除（`CardTypes.tsx` 的 `TopicChip` 与 `Cover` 的 `chip` 参数、`NoteCard` 的 `ct-note-topic`、`DesignBoard` 的 `chip-*` 四个 key、`design.css` 的 `.ct-topic` / `.ct-note-topic` / `.dz-strip`）。

连带一并撤掉的还有旧卡型封面上的同一枚标签（`StrangerWindow` 的 `.sw-card-topic` / `.sw-row-topic`、`AuthorCardVisibility` 的同一处）——留着它们会让同一份数据在两种卡上说法不一致。

⚠️ `designData.ts` 的 `topic` 字段**保留但目前无人渲染**：它是 `t_memory_card.topicIds` 的真实契约，筛选器要用同一份数据。已在字段注释里标明它现在不设防（改坏了没有任何一张图会变样）。

## 八、默认排序的前端形态

排序规则已拍板：**作者置顶的在前，其余按发布时间倒序**。

🔴 **字段与端点归后端，本线不造接口。** 前端这边只需要两件事：

- 列表**照后端给的顺序渲染**，前端不再排一次 —— 前端排会和分页游标打架（第二页的置顶卡会插到第一页后面）。
- 置顶卡在视觉上**要能认出来**，否则「它在最前面」只会被读成「它最新」。形态尚未设计，落地时一并出图。

**未定：** 置顶能置几张、置顶卡自己之间怎么排。这两条也归后端契约。

## 九、怎么复现 / 怎么撤

出图脚手架全部在 `echo-h5-proto/src/dev/design/`，只在 `import.meta.env.DEV` 下挂载，线上不打包：

- `CardTypes.tsx` —— 四种卡型 + 便签 + 那一行
- `LifeBookDot.tsx` —— 一生的收起 / 展开
- `designData.ts` —— 卡样本、边界样本（无图 / 无标题 / 超长标题）、12 张密度样本
- `DesignBoard.tsx` —— `?design=<key>` 路由

本轮用到的 key：`cards-a` `cards-b` `cards-c` `cards-d` `cards-all` `cards-edge` `cards-edge-all` `cards-one` `cards-many` `life-collapsed` `life-expanded` `life-both` `stranger-v2-cards`。

🔄 `chip-cmp` / `chip-cmp-few` / `chip-on` / `chip-off` / `chip-strip` 已随 chip 的裁定一起删除。上面 §七 的两张图原样留着，那是当时的决策依据。

🔄 **`CardList` 的 `chip` 开关已删（2026-08-27）**，落选那一支连同开关本身一并撤除，没有留成运行时开关。

`.dz-strip` 上的 `zoom: .58` 同理，只为把六张卡塞进一张图，撤除时一并删。

撤除方式：删掉 `src/dev/design/` 整个目录，并去掉 `main.tsx` 里对 `?design=` 的判断。
