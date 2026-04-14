# affaan-m/everything-claude-code

- 上游仓库：`https://github.com/affaan-m/everything-claude-code`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/affaan-m/everything-claude-code`
- 主分类：**技能集合与市场**
- 能力标签：`多智能体协作`, `记忆/上下文管理`, `代码审查`, `研发流程`
- 一句话总结：超大号跨 harness agent-performance 系统，整合 agents、skills、commands、hooks、rules 和安装器。

## 能力概览

- 同时面向 Claude Code、Codex、Cursor、OpenCode 等分发资产。
- 提供大量语言/框架技能、review、TDD、e2e、quality gate 能力。
- hooks 覆盖 dev server、MCP 健康检查、质量门禁、session persistence、continuous learning。
- 支持 security scan、cross-harness setup、instinct import/export。

## 资产盘点

- 仓库自述：30 agents、136 skills、60 commands。
- 含 hooks.json 与详细 hooks 文档。
- 顶层有多种 harness 配置目录。
- CLI：ecc / ecc-install。

## 关键文件

- `README.md`
- `package.json`
- `hooks/hooks.json`
- `agents/`
- `commands/`

## 备注

- 范围远大于普通技能包，部分 multi-* 工作流还依赖额外安装。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`324`
- [事实] 代表提交：
  - `2026-04-12` `feat: add dashboard GUI with theme, font customization, and logo`
  - `2026-04-12` `feat(hooks,skills): add gateguard fact-forcing pre-action gate`
  - `2026-04-11` `feat(a11y):add inclusive-ui architect agent for WCAG 2.2 compliance`
  - `2026-04-10` `feat: add ecc2 legacy plugin migration import`
- [推断] 新增 dashboard GUI、gateguard pre-action gate 与 ecc2 legacy 配置导入迁移，随后集中修补安装、发布、权限与并发问题。
<!-- recent-updates:end -->
