# github/awesome-copilot

- 上游仓库：`https://github.com/github/awesome-copilot`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/github/awesome-copilot`
- 主分类：**技能集合与市场**
- 能力标签：`agents`, `instructions`, `skills`, `hooks`, `agentic workflows`, `plugins`, `marketplace`, `MCP`
- 一句话总结：GitHub 官方运营的 Copilot 定制资源集合：把 agents / instructions / skills / hooks / agentic workflows / plugins 六类资产统一放进一个社区仓库，配套 marketplace、网站、`llms.txt` 与 CLI 安装路径。

## 能力概览

- [事实] 覆盖 6 条一等资源线：`agents/`（`*.agent.md`）、`instructions/`（`*.instructions.md`，按 `applyTo` 文件模式注入）、`skills/`（每个目录一个 SKILL.md + 可选 bundled assets，遵循 Agent Skills spec）、`hooks/`（`README.md` + `hooks.json`，走 Copilot Coding Agent 的 hook 事件）、`workflows/`（GitHub Agentic Workflows `.md`，编译成 GHA）、`plugins/`（`.github/plugin/plugin.json`，通过 `copilot plugin install <name>@awesome-copilot` 分发）。
- [事实] 规模大：`agents` 204 个、`instructions` 177 个、`skills` 307 个、`plugins` 62 个、`workflows` 7 个、`hooks` 6 个；近 14 天（2026-04-05~2026-04-19）默认分支 73 次提交，`staged` 才是实际贡献分支，`main` 走 `chore: publish from staged` 发布节奏。
- [事实] 工程化完备：`eng/` 下有 17 个 `.mjs` 脚本，负责 README 生成、marketplace 生成、plugin/skill 校验、plugin materialize、website 数据生成、prompts→skills 迁移；`package.json` 暴露 `npm run build` / `skill:validate` / `plugin:validate` / `plugin:create` / `skill:create` / `website:*` 等入口。
- [事实] 有独立 `website/`（Astro）、`cookbook/`（目前是 Copilot SDK 多语言 recipes）、`docs/` 六份分门别类 README（agents/instructions/skills/hooks/workflows/plugins），以及机读入口 `llms.txt`（通过 `awesome-copilot.github.com`）。
- [推断] 相对其它 refs 里常见的个人/小团队 skill 包，它更像“官方中心化 registry + 规范试验场”：同时充当 Agent Skills spec、Copilot hooks spec、Agentic Workflows spec 的参考实现和活跃样本库。

## 资产盘点

- [事实] 6 类资源数量：agents 204、instructions 177、skills 307、plugins 62、workflows 7、hooks 6。
- [事实] `cookbook/` 只有 1 条顶层条目（`copilot-sdk`），目录下再按 .NET/Go/Java/Node/Python 分语言给 recipes。
- [事实] `docs/` 提供 6 份 README 专门讲各资源怎么用、怎么贡献。
- [事实] `.github/workflows/` 中同时存在 `.yml` 经典 Actions 与 `.md` Agentic Workflows（`*.md` + 配套 `*.lock.yml`）：`duplicate-resource-detector`、`learning-hub-updater`、`pr-duplicate-check`、`resource-staleness-report` 等都以 agentic workflow 形式维护仓库自身质量。
- [事实] `hooks/` 6 个官方示例：`dependency-license-checker`、`governance-audit`、`secrets-scanner`、`session-auto-commit`、`session-logger`、`tool-guardian`。
- [事实] `plugins/` 下既有普通 plugin，也有 `external.json`——允许用 `source` 指向 GitHub repo / git / npm / pip 包注册“外部插件”，由 `generate-marketplace.mjs` 一起打进 marketplace。

## 关键文件

- `README.md`（77KB 自动生成，列全部资源）
- `AGENTS.md`（贡献者/AI agent 手册：6 类资源 frontmatter 规范 + PR checklist + `bash scripts/fix-line-endings.sh` 等硬约束）
- `CONTRIBUTING.md`
- `package.json`（`build` = `update-readme.mjs` + `generate-marketplace.mjs`；有 `skill:validate`、`plugin:validate` 等）
- `eng/update-readme.mjs`、`eng/generate-marketplace.mjs`、`eng/validate-skills.mjs`、`eng/validate-plugins.mjs`、`eng/materialize-plugins.mjs`、`eng/migrate-prompts-to-skills.mjs`
- `docs/README.{agents,instructions,skills,hooks,workflows,plugins}.md`
- `skills/*/SKILL.md`（典型：`skills/architecture-blueprint-generator/SKILL.md`）
- `agents/*.agent.md`（典型：`agents/api-architect.agent.md`）
- `instructions/*.instructions.md`（典型：`instructions/a11y.instructions.md`，含 `applyTo: '**'`）
- `workflows/*.md`（典型：`workflows/daily-issues-report.md`）
- `hooks/session-auto-commit/hooks.json` 等
- `plugins/awesome-copilot/.github/plugin/plugin.json`（meta plugin：suggest-awesome-github-copilot-* 系列）
- `.schemas/`、`.codespellrc`、`.editorconfig`、`scripts/fix-line-endings.sh`（CRLF→LF 强制）

## 备注

- [事实] README 顶部明确说明 PR 必须发往 `staged` 分支，不是 `main`；`main` 由 `chore: publish from staged` 统一发布。
- [事实] README/AGENTS 都强调“customizations here are sourced from third-party developers”，并把它放到 CLI 安装路径后（`copilot plugin install <name>@awesome-copilot`）——即仓库同时承担 curated catalog 和官方 marketplace 前置清单的角色。
- [推断] 相对 `anthropics/skills`（偏“规范 + 官方 demo”）、`vercel-labs/skills`（偏 CLI/包管理器）、`travisvn/awesome-claude-Skills`（偏导航站），它横跨三者：既有规范与生成脚本，又有 CLI 分发路径，又有社区 curated 内容，还额外叠了 hooks / agentic workflows / plugins 这些 Copilot 专属形态。
- [推断] 对我们仓库的直接参考价值在四处：`skills/` 目录布局与 SKILL.md frontmatter 约束、`instructions/*.instructions.md` 的 `applyTo` 模式注入（适合与我们的 `commands/`、`AGENTS.md` 分层对照）、`hooks/` 以 `hooks.json` 为接口的最小 hook 包、以及 `eng/validate-*.mjs` + `scripts/fix-line-endings.sh` 这类可工程化的 catalog 校验思路。
- [推断] `workflows/` 里的 agentic workflow 用 `.md` + `.lock.yml` 的方式管线化 GH Actions，比直接维护一堆 `.yml` 更好 review，值得在“仓库自身的自动化”场景参考；但它依赖 `gh aw compile`，不是直接可移植到本仓库的东西。
- [未验证] `copilot plugin install ...@awesome-copilot` 的具体 CLI 版本支持范围与权限要求，需按 GitHub Copilot CLI 实际版本确认。

## 最近 14 天更新（2026-04-05 ~ 2026-04-19）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`73`
- [事实] 代表提交：
  - `2026-04-17` `feat: add copy install command from skills list and modal (#1424)`
  - `2026-04-17` `feat: Move to xml top tags, plan review, hints and more (#1411)`
  - `2026-04-17` `feat: Qdrant skills (#1412)`
  - `2026-04-14` `Improve skills validation runs (#1387)`
  - `2026-04-14` `Adds a new Agent Skill - Acquire-Codebase-Knowledge (#1373)`
  - `2026-04-13` `fix(agents): replace deprecated tool names with official namespaced equivalents 🤖🤖🤖 (#1382)`
  - `2026-04-13` `Add whatidid skill — turn your Copilot sessions into proof of impact (#1319)`
  - `2026-04-10` `feat(instructions): update security, a11y, and performance to 2025-2026 standards (#1270)`
- [推断] 主线依然是 `skills/` + `agents/` 的持续扩充：大批新加的 Azure / Qdrant / Foundry / LinkedIn / browser investigation / code-tour / whatidid 等 skill，同时通过 `fix(agents): remove invalid tool names` / `replace deprecated tool names` 批量刷 agents 的 tool 兼容性。
- [推断] 配套工程化侧同步推进：`Improve skills validation runs`、`fix: remove shell usage from plugin check`、`docs: update go sdk examples`，以及更新 `a11y / security / performance` instructions 的“2025-2026 standards”。
- [推断] 网站与机读入口也在演进：`copy install command from skills list and modal` 说明 `awesome-copilot.github.com` 的 skills 列表已加了一键安装命令。
<!-- recent-updates:end -->
