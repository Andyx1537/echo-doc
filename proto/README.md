# 前后端协议 · 真源

**这里是 `.proto` 的唯一真源。** 产品负责人 2026-08-28 裁定。

## 谁在用

| 仓 | 副本位置 | 消费方式 |
| --- | --- | --- |
| `echo` | `echo-server/src/main/proto/` | `pom.xml` 的 protobuf 插件从这里编译到 `target/generated-sources` |
| `echo-client` | **无副本** | H5 走 HTTP/JSON，当前不消费 protobuf |

`echo-server` 之所以留副本而不是直接引本仓，是因为 Maven 插件写死从 `src/main/proto` 读，
搬走后端就编译不过。

## 🔴 这个安排的已知代价

**两份不一致时不会有任何报错。** 后端照旧编译、照旧通过，只是编出来的协议和真源对不上。

这是当时明确知情后仍然选定的方案（备选是 git submodule，代价是每人 clone 要 `--recursive`）。
唯一的补救是 `scripts/proto-check.sh`——它把静默失效变成一个非零退出码，但**它不会自己跑**。

## 规矩

1. 改协议**先改这里**，再同步到消费仓。反方向改副本再往回抄，迟早两边都乱。
2. 提交前跑 `scripts/proto-check.sh /path/to/echo`，不一致会退 1。
3. 同步用 `scripts/proto-check.sh --fix /path/to/echo`，它只往「真源 → 副本」一个方向写。
4. 新增消费仓时，在 `scripts/proto-check.sh` 的 `CONSUMERS` 数组里加一行，
   否则它不在校验范围里——而**不在校验范围和校验通过在输出上长得很像**，
   脚本为此会打一行「跳过」，别把那行当成通过。
