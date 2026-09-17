# 模型与本机运行清单

2026-09-17；本实验独立于 Echo 正式业务。

- 设备：Apple M4 Max，64GB统一内存。
- 运行工具：Homebrew Ollama 0.34.0，/opt/homebrew/bin/ollama。
- 模型：qwen3:14b，Q4_K_M，约9.3GB；下载中，完整摘要待成功后回填。
- 来源：https://ollama.com/library/qwen3:14b 。模型页许可证Apache-2.0，最终以下载元数据为准。
- 实测启动：仅127.0.0.1:11434，OLLAMA_NO_CLOUD=true，指定模型目录成功，无开机服务。
- Ollama首次启动创建 /Users/andy/.ollama/id_ed25519 身份文件；不提交、展示或复制私钥。
- Homebrew安装自动更新了依赖并清理旧版本与缓存；新增依赖含mpdecimal、python@3.14、mlx、mlx-c，升级涉及ca-certificates、openssl@3、readline、sqlite、xz。后续安装禁用自动更新和自动清理，避免不必要环境改动。
- 完整测试结果、模型摘要、加载耗时、生成token速度、内存：待实测，不以估计替代。
