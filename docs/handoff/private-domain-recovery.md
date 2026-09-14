# 阶段账本 · private-domain-recovery

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` 私域未完成项；`DECISIONS` G-38 生成中断由服务端交代
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 可做块已齐并合入 develop：挂死收成失败、写后读复用钥匙、生成只重 GET、切号空草稿。
- 真出图仍 blocked，本账本不关。真短信、打 Tag、两份锁住的测试夹具、占 5180/18080 仍不做。
- 作品 / 共鸣厅 / 评论收藏 / 行为账本均已关，并随整线合入 develop。
- 权威来源：`API-CONTRACT` 建档状态机、`DECISIONS` G-38 生成中断、`FRONTEND-TOPOLOGY` 写后 GET 与重新查询。
- 接手先读：块 6 真出图；其余开发在 develop 上做。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/private-generation-recovery` | 已合 develop @ `4b7b2f0`（功能头 `defff3a`）；占用已释 |
| echo-client `frontend/onboarding-write-recovery` | 已合 develop @ `4c96d62`（功能头 `6bc6585`）；占用已释 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 他人占用，不碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@9f70c4d` | | 私域先做；产品块后置 |
| 2. 后端：进程挂死后收成失败 | `done` | `echo@defff3a` | OnboardingApiTest 12/12 | 启动扫描 `generating`/`refining` |
| 3. 前端：写成功读失败复用钥匙 | `done` | `echo-client@bc68c42` | vitest 170/170 | 同键重放，不重做业务 |
| 4. 生成查询失败只重 GET | `done` | `echo-client@6bc6585` | vitest 174/174 | 失败后只 GET，不重 POST 生成 |
| 5. 旧号切走后重传不带原资料 | `done` | `echo-client@6bc6585` | mock 整链 + 后端专项已锁 | 切号后新草稿空，原答案仍留在匿名会话 |
| 6. 真模型出图 | `blocked` | | | 独立媒体单元，本账本不接外网模型 |

## 下一块入口

```text
仓库：echo-doc
动作：可做块已合 develop。真出图仍 blocked，本账本不关。之后开发在 develop 上做。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```

## 发现

- 生成回调只活在进程内线程池；重启后库里仍是 `generating`，客户端会一直轮询。
- 通用建档请求每次新建幂等键；写已成功再点一次会撞版本冲突。
- 建档 create 的会话 ID 由账号+幂等键决定；同一把钥匙会回到同一份草稿。
