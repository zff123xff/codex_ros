# 用户级 Codex 与 ROS 通信

在普通终端执行一次 `python3 tools/codex_ros/install.py`，然后退出并重新启动 Codex。安装器默认写入 `$CODEX_HOME`，未设置时写入 `~/.codex`，无需 sudo。

安装内容：全局 AGENTS.md 中的 ROS 约定、通用 ROS 2 环境加载器、Fast DDS UDP 配置，以及 config.toml 中的 workspace-write 和 network_access=true。保留其他配置和已有约定，修改前备份；重复安装不会重复追加。

以后从已加载机器人环境的终端运行 `codex` 即可；ROS_DOMAIN_ID、中间件和发现配置由该终端传入。agent 也可以依据项目或运行进程自行确认目标通信域，加载工作空间后执行 ROS 指令。没有任何固定项目路径、机器人命名空间或通信域。多发行版时需选中正确 ROS_DISTRO。

手动验证示例：`source ~/.codex/ros/setup.bash` 后执行 `ros2 topic list --no-daemon --spin-time 5`，再对已知活跃话题做有超时的数据读取。话题列表不等于数据已连通。不会为测试发布运动指令。

适用范围是本机用户的 Codex CLI。系统或组织托管权限、容器网络、远端防火墙仍需允许 ROS 通信；全局配置无法覆盖这些限制。默认不改 shell 启动文件，不影响普通 ROS 终端的 DDS 传输设置。

全局约定按 [OpenAI Docs 的 AGENTS.md 机制](https://learn.chatgpt.com/docs/agent-configuration/agents-md)加载。
