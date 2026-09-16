# 阶段账本 · topology-code-sync

状态：`CLOSED`
依据：`CURRENT-DELIVERY-STATUS`；两端拓扑仍写 9 月 8 日缺口
更新：2026-09-16
执行约定：`docs/skills/agent-handoff/SKILL.md`

## 概述

- 两端拓扑按当前 develop 回写 B04–B07 / BE-G，避免把已合入的当缺口。
- 建档称呼保存跟 `update_profile` 走，补 FE-04 最后一处只看 busy 的写操作。
- 不做：全屏层、漫画/视频、真短信、打 Tag、占 5180/18080、改两份锁住夹具、签整版 PASS。

## 占用

| 资源 | 状态 |
|---|---|
| echo / echo-client / echo-doc develop | 已释放 |
| `BlockSilentFailureTest.java`、`WindowVisibilityTrimTest.java` | 锁，未改 |
| 5180 / 18080 | 未碰 |

## 阶段

| 块 | 状态 | 提交 | 验证 | 备注 |
|---|---|---|---|---|
| 1. 称呼能力门 | `done` | `echo@42ed8ce` `echo-client@177bbcd` | `OnboardingApiTest` 15/15；vitest 17；mock 5176 第一题保存可点，落成「麦麦」 | FE-04 称呼 |
| 2. 拓扑按代码回写 | `done` | `echo-doc` 本提交 | 对照 develop：广场 Work、评论收藏 PG、投稿唯一约束、启动收成失败 | 只改概述与缺口表 |

## 下一块入口

```text
仓库：公共区下一未锁缺口
动作：七单元已关。漫画/视频、真短信、打 Tag、全屏层仍后置。不要签完整 QA PASS。
禁止：占 5180/18080；改两份锁住的测试夹具；打 Tag
```
