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

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`296`
- [事实] 代表提交：
  - `2026-04-12` `feat(hud): display extra usage spend data in HUD (closes #2570)`
  - `2026-04-13` `feat(hud): add MiniMax coding plan usage provider`
  - `2026-04-12` `feat(hud): split usage cache by provider to eliminate cross-session thrashing`
  - `2026-04-11` `feat(release): rewrite release skill as generic repo-aware assistant (#2501)`
- [推断] HUD 新增花费/Provider/worktree/hostname/cwd 等信息展示，release skill 改写为 repo-aware assistant，引入 LLM Wiki 知识层，并持续强化 permission/runtime/hook/tmux/Ralph 审批链。
<!-- recent-updates:end -->
