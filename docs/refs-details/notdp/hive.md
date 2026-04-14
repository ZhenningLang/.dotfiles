# notdp/hive

- 上游仓库：`https://github.com/notdp/hive`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/notdp/hive`
- 主分类：**多智能体协作与工作流编排**
- 能力标签：`tmux 自动化`, `Agent 通信`, `插件/通知`
- 一句话总结：基于 tmux 的多 agent 协作运行时/CLI，围绕 Factory Droid 工作流构建。

## 能力概览

- 在 tmux pane 中创建 team、spawn agent、绑定 workspace。
- 通过 <HIVE ...> 内联消息在 agent 间通信。
- 提供 status-set / status / wait-status 等控制面状态同步。
- 支持 capture、interrupt、exec、terminal 等 pane 控制。

## 资产盘点

- 1 个核心 skill：skills/hive。
- 4 个一方插件：cvim、cross-review、fork、notify。
- 20+ 测试文件。
- 若干通知脚本与完整 CLI 源码。

## 关键文件

- `README.md`
- `pyproject.toml`
- `AGENTS.md`
- `src/hive/cli.py`
- `skills/hive/SKILL.md`

## 备注

- 强依赖 tmux + droid + Python 3.11+，不是通用编排框架。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`69`
- [事实] 代表提交：
  - `2026-04-13` `feat: add send gate to block `hive send/reply` when target is asking user`
  - `2026-04-13` `feat: add `hive register` command for external pane registration`
  - `2026-04-13` `feat: upgrade HIVE envelope to markdown code fence + frontmatter`
  - `2026-04-13` `feat: add delivery ACK to hive send and reply`
- [推断] 新增 send gate、`hive register`、delivery ACK、frontmatter 化的 HIVE envelope，以及跨 `droid`/`claude`/`codex` 的 hooks 安装与更顺手的 spawn/fork/kill 工作流。
<!-- recent-updates:end -->
