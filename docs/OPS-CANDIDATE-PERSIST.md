# 定妆候选落盘

状态：现行 · 2026-09-17
依据：`GeneratedMediaPublisher`；`ProvenanceConfig`；`SPEC-trust-and-compliance` S-8
执行：`docs/handoff/candidate-image-persist.md`

## 概述

- 定妆图的展示地址必须是本方 `IStorage`（默认本地盘，`GET /api/v1/files/{key}`）。供应商临时链只作拉取源。
- 落盘唯一入口是 `GeneratedMediaPublisher`：先写隐式标识，再存盘。不给生成侧直接 `IStorage.put`。换仓储实例仍能按本方 key 读回。
- `ECHO_AIGC_PROVIDER_CODE` 没配好时，生成失败，不把供应商地址写进候选。编码由合规登记，代码不得编造。
- 漫画/视频、阿里云对象存储仍后置。本切片只收定妆图这一条。

## 路径

```text
万相出图（url 或字节）
    → 编码已配？否 → 失败，候选不落供应商链
    → 有字节或拉取成功？否 → 失败
    → 打隐式标识并写入 IStorage
    → 候选 imageUrl = /api/v1/files/{key}
重开：读会话里的本方地址，不再依赖供应商临时链
```

| 条件 | 结果 |
|---|---|
| 编码未配 | 失败，文案点出服务提供者编码 |
| 无字节且拉不下 | 失败，不定展示地址 |
| 编码已配且有字节 | 本方文件，带标识 |

## 红线

- 不把供应商临时地址当作候选图。
- 不编造 27 位服务提供者编码。
- 不把用户上传和生成图走同一条打标口。
