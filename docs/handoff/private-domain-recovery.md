# 阶段账本 · private-domain-recovery

状态：`OPEN`
依据：`CURRENT-DELIVERY-STATUS` 私域未完成项；`DECISIONS` G-38 生成中断由服务端交代
更新：2026-09-14
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 这一份要交付的结果：私域建档在生成挂死、写成功读失败、切到旧号重传时都能从服务端接着走，用户看到的是可重试或失败，不会一直转圈。
- 不做：真短信/阿里云（最后接）、真模型出图/漫画/视频、建档内补传、打 Tag、两份锁住的测试夹具、占 5180/18080。
- 作品 / 共鸣厅 / 评论收藏 / 行为：产品已冻，本账本私域块勾完后再逐个开，不另拍板。
- 权威来源：`API-CONTRACT` 建档状态机、`DECISIONS` G-38 生成中断、`FRONTEND-TOPOLOGY` 写后 GET 与重新查询。
- 接手先读：本页未勾选的下一块。

## 占用

| 资源 | 状态 |
|---|---|
| echo `backend/private-generation-recovery` | 已推 `defff3a` |
| echo-client `frontend/onboarding-write-recovery` | 已推 `bc68c42` |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，不改 |
| 5180 / 18080 | 他人占用，不碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 开账本 | `done` | `echo-doc@9f70c4d` | | 私域先做；产品块后置 |
| 2. 后端：进程挂死后收成失败 | `done` | `echo@defff3a` | OnboardingApiTest 12/12 | 启动扫描 `generating`/`refining` |
| 3. 前端：写成功读失败复用钥匙 | `done` | `echo-client@bc68c42` | vitest 170/170 | 同键重放，不重做业务 |
| 4. 生成查询失败只重 GET | `todo` | | | 按钮已有，要故障复验 |
| 5. 旧号切走后重传不带原资料 | `todo` | | | 服务端已锁，要整链验 |
| 6. 真模型出图 | `todo` | | | 独立媒体单元，本账本不接外网模型 |

## 下一块入口

```text
仓库：echo-client
动作：生成查询失败只重 GET 的故障复验；不要占 5180/18080
禁止：改两份锁住的测试夹具；不要合 develop，等私域块验完
```

## 发现

- 生成回调只活在进程内线程池；重启后库里仍是 `generating`，客户端会一直轮询。
- 通用建档请求每次新建幂等键；写已成功再点一次会撞版本冲突。
- 建档 create 的会话 ID 由账号+幂等键决定；同一把钥匙会回到同一份草稿。
