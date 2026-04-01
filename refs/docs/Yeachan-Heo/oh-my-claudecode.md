# Yeachan-Heo/oh-my-claudecode

- 上游仓库：`https://github.com/Yeachan-Heo/oh-my-claudecode`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/Yeachan-Heo/oh-my-claudecode`
- 主分类：**多智能体协作与工作流编排**
- 能力标签：`记忆/上下文管理`, `MCP/工具集成`, `研发流程`
- 一句话总结：完整的 Claude Code 多智能体编排系统，含 CLI、skills、agents、hooks、tmux worker runtime 和验证模块。

## 能力概览

- 支持 team-plan → team-prd → team-exec → team-verify → team-fix 流水线。
- 通过 tmux 启动 claude/codex/gemini 等 worker。
- 提供 autopilot、ralph、ultrawork、ultraqa、deep-interview 等模式。
- 用 hooks、verification、writer memory 持久化状态并组织验证证据。

## 资产盘点

- 31 个 skill 目录。
- 19 个 agent prompt 文件。
- hooks.json 覆盖 11 类事件。
- 3 个 CLI 名称：oh-my-claudecode、omc、omc-cli。

## 关键文件

- `README.md`
- `package.json`
- `hooks/hooks.json`
- `src/features/verification/README.md`

## 备注

- README 中关于 agent 数量的说法与目录树可见数量不完全一致。
