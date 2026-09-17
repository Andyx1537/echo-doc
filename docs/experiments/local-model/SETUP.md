# 安装与运行规范

## 位置

- 工具：Homebrew 管理的 /opt/homebrew/bin/ollama；不重复装桌面版。
- 模型：/Users/andy/Models/echo-local/models/，通过 OLLAMA_MODELS 显式指定。
- 原始输出：/Users/andy/Models/echo-local/runs/。
- 运行日志：/Users/andy/Models/echo-local/logs/。
- 启停配置/脚本的权威文本放本实验目录；后续必要运行脚本也随公共仓版本管理。
- 工具可能另建 /Users/andy/.ollama 配置；安装后盘点登记，不移动已有用户文件。

## 启停与安全

安装和下载需系统授权。先确认端口11434没有已有监听；有占用则停止并说明，不杀其他服务。
服务仅监听127.0.0.1:11434；设置 OLLAMA_NO_CLOUD=1，禁用云端和搜索。手动启动，不注册开机服务，不更改全局shell配置。环境变量只作用于本实验进程。
启动后核对模型目录、本地监听和云功能关闭；仅下载qwen3:14b，不下载其他候选。
单请求、num_ctx=4096、think=false、temperature=0、num_predict=1024；完整参数随每次请求保存。输出截断记失败，不能静默当成功。失败不自动转云，不无限重试。
测试结束停止本实验进程并释放模型内存，磁盘模型保留。清理先列精确文件与空间、获批准后执行，不递归删除用户根目录。卸载仅移除本次安装对象，不连带其他模型或工具。

## 参考

- https://ollama.com/library/qwen3:14b
- https://docs.ollama.com/faq

下载需要联网；「本地推理」不表示工具安装和模型下载无需联网。
