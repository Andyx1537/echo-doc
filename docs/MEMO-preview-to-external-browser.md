# 备忘：图像与吃 CPU 的预览一律外置浏览器

日期：2026-09-17。工作纪律，不是产品裁定。

## 概述

- 凡是图像、截图、比稿、视频、画布、或任何会在 Cursor 里解码/渲染的预览，**全部拿到系统 Chrome 处理**。
- **不要**用 Cursor 对话、内置 Simple Browser、Markdown 预览、截图工具往这条线塞图。Cursor 不适合扛这些，会把 Helper Renderer 打到数 GB、CPU 打满，整机卡死。
- 对话里只交一条人能点开的地址（Vite、`?visual=`、真实路由）。核对应 DOM / 真 Chrome 操作，不靠贴图。
- 拿不到 Chrome 就写卡在哪，不要改回「我把图贴这边」。

## 为何要外置

2026-09-17 实测：往对话里塞几张 2–3MB 的 PNG，再开 Simple Browser，Cursor Helper（Renderer）内存到约 9GB、CPU 到约 600%，整机卡顿。根因是对话进程解码大图，不是 Vite。

Cursor 这边只适合文字和代码。预览是浏览器的活。

## 什么必须外置

只要会让 Cursor 去解码、合成或常驻一帧画面，就算：

- 对话里的 `![...](路径)`、粘贴的 PNG/JPEG/WebP/GIF
- `browser_take_screenshot`、CDP `Page.captureScreenshot`、为了给对话看而拷进 `docs/visual/` 的图
- Cursor 内置 Simple Browser / 预览页（和对话抢同一套 Renderer）
- 视频、canvas、大图对比板、生成图预览

这些一律在**系统 Chrome**打开。不是 Cursor 自带的那个浏览框。

## 对话里交什么

一条可打开的地址，例如：

- 开发页：`http://127.0.0.1:<port>/?visual=...`
- 真实路由：`http://127.0.0.1:<port>/#/...`

视口用手机宽（约 390）。同一批数据、同一个位置，只改被比较的那一项。文字只写图上看不出来的分界点和造数假设。

## 执行时禁止

- 回复里写会解码大图的 Markdown 图
- 为了给对话看而去截图、贴附件、生成预览图
- 在 Cursor 里堆预览页、比稿页、视频页
- 把「我描述得很清楚」或「贴一张图」当成外置浏览的替代

## 和视觉决策的关系

「该长什么样」仍然要渲染出来看，不能只靠文字想象。改的是**看的地方**：系统 Chrome，不是这条对话。规则副本：工作区 `visual-decisions.mdc`、前端 `.cursor/rules/no-chat-images.mdc`。
