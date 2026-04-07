# refs 研究汇总

## 分类说明

- **浏览器自动化与前端调试**：围绕浏览器控制、前端诊断、性能分析、页面抓取与 UI 调试。 代表项目：`ChromeDevTools/chrome-devtools-mcp`、`vercel-labs/agent-browser`
- **技能集合与市场**：以 skills 汇总、分发、导航或精选集合为主，常附带少量示例或插件。 代表项目：`Dimillian/Skills`、`affaan-m/everything-claude-code`、`anthropics/skills`、`glittercowboy/taches-cc-resources`、`libukai/awesome-agent-Skills`、`travisvn/awesome-claude-Skills`
- **多智能体协作与工作流编排**：围绕 agent 角色分工、并行执行、状态同步、团队工作流编排。 代表项目：`Yeachan-Heo/oh-my-claudecode`、`notdp/hive`、`nyldn/claude-octopus`
- **上下文 / 记忆管理**：围绕上下文压缩、记忆持久化、检索、session 连续性与 context engineering。 代表项目：`mksglu/context-mode`、`muratcankoylan/Agent-Skills-for-Context-Engineering`
- **前端 UI / 设计系统**：围绕视觉设计、组件模式、设计系统、界面审查与 UI 生成。 代表项目：`google-labs-code/stitch-skills`、`nextlevelbuilder/ui-ux-pro-max-skill`、`pbakaus/impeccable`、`vercel-labs/agent-skills`
- **研发流程 / 项目管理**：围绕 spec/planning/execution/verification/ship 等工程流程与项目管理。 代表项目：`automazeio/ccpm`、`gsd-build/get-shit-done`、`obra/superpowers`
- **代码质量 / 审查 / 调试**：围绕静态分析、review、质量门禁、调试与诊断。 代表项目：`millionco/react-doctor`、`addyosmani/web-quality-skills`
- **MCP / 工具链 / 安装分发**：围绕 MCP、CLI、安装器、技能包管理、多 Agent 兼容与基础设施。 代表项目：`vercel-labs/skills`
- **行为协议 / 提示工程**：围绕提示协议、行为约束、激励/约束机制、触发词和 hook 协同。 代表项目：`tanweai/pua`
- **Agent 配置管理 / 工具链**：围绕跨 Agent 统一配置、安装分发、二进制修改与工具增强。 代表项目：`notdp/.dotfiles`

## 项目总表

| 项目 | 分类 | 一句话总结 |
|---|---|---|
| [`affaan-m/everything-claude-code`](./refs-details/affaan-m/everything-claude-code.md) | 技能集合与市场 | 超大号跨 harness agent-performance 系统，整合 agents、skills、commands、hooks、rules 和安装器。 |
| [`addyosmani/web-quality-skills`](./refs-details/addyosmani/web-quality-skills.md) | 代码质量 / 审查 / 调试 | 面向 Web 质量审查与优化的技能仓库，围绕 Lighthouse、Core Web Vitals、可访问性、SEO 和现代最佳实践组织。 |
| [`anthropics/skills`](./refs-details/anthropics/skills.md) | 技能集合与市场 | Anthropic 官方示例 skills 仓库，附带规范、模板，以及文档处理与开发类技能示例。 |
| [`automazeio/ccpm`](./refs-details/automazeio/ccpm.md) | 研发流程 / 项目管理 | 单技能形态的项目管理与交付编排系统，把 PRD、Epic、Issues、并行 agents 和状态跟踪串成 spec-driven workflow。 |
| [`ChromeDevTools/chrome-devtools-mcp`](./refs-details/ChromeDevTools/chrome-devtools-mcp.md) | 浏览器自动化与前端调试 | 通过 MCP 控制真实 Chrome，提供自动化、调试、性能分析和配套 skills。 |
| [`Dimillian/Skills`](./refs-details/Dimillian/Skills.md) | 技能集合与市场 | 偏精选型的 skills 集合，覆盖 Apple 平台开发、GitHub 操作、review swarm、React 性能和重构。 |
| [`glittercowboy/taches-cc-resources`](./refs-details/glittercowboy/taches-cc-resources.md) | 技能集合与市场 | 面向 Claude Code 的资源仓库，主打技能开发、规划分层、MCP 服务生成、调试方法论与 Ralph 自治循环。 |
| [`google-labs-code/stitch-skills`](./refs-details/google-labs-code/stitch-skills.md) | 前端 UI / 设计系统 | 围绕 Stitch MCP 的 Agent Skills 库，用于 UI 设计生成、设计系统提炼、React 转换和演示视频生成。 |
| [`gsd-build/get-shit-done`](./refs-details/gsd-build/get-shit-done.md) | 研发流程 / 项目管理 | 跨多种 AI 运行时的 spec-driven development / context engineering 系统，覆盖立项、规划、执行、验证、交付全流程。 |
| [`libukai/awesome-agent-Skills`](./refs-details/libukai/awesome-agent-Skills.md) | 技能集合与市场 | 以 curated list 为主的技能资源集市，汇总教程、市场、官方项目，并附带少量实作 skill 与插件。 |
| [`millionco/react-doctor`](./refs-details/millionco/react-doctor.md) | 代码质量 / 审查 / 调试 | React 代码体检工具仓库，核心是 CLI 扫描器，同时附带 GitHub Action、agent skill 和网站。 |
| [`mksglu/context-mode`](./refs-details/mksglu/context-mode.md) | 上下文 / 记忆管理 | 面向多种 AI 编码运行时的 MCP/plugin，用来减少上下文窗口占用并保留会话连续性。 |
| [`muratcankoylan/Agent-Skills-for-Context-Engineering`](./refs-details/muratcankoylan/Agent-Skills-for-Context-Engineering.md) | 上下文 / 记忆管理 | 围绕 context engineering 的 Agent Skills 集合，重点讲生产级 agent 的上下文设计、记忆、工具与评测。 |
| [`nextlevelbuilder/ui-ux-pro-max-skill`](./refs-details/nextlevelbuilder/ui-ux-pro-max-skill.md) | 前端 UI / 设计系统 | 面向 UI/UX 生成的设计情报包，结合大规模 CSV 规则库、Claude skills 与安装 CLI。 |
| [`notdp/.dotfiles`](./refs-details/notdp/.dotfiles.md) | Agent 配置管理 / 工具链 | 统一管理 33+ AI 编码 Agent 的 skills、commands 和全局指令的 dotfiles 框架。 |
| [`notdp/hive`](./refs-details/notdp/hive.md) | 多智能体协作与工作流编排 | 基于 tmux 的多 agent 协作运行时/CLI，围绕 Factory Droid 工作流构建。 |
| [`nyldn/claude-octopus`](./refs-details/nyldn/claude-octopus.md) | 多智能体协作与工作流编排 | 超大体量的多模型编排插件，把 Claude Code/Droid 扩展成带工作流、角色、hooks、MCP 和兼容层的协作系统。 |
| [`obra/superpowers`](./refs-details/obra/superpowers.md) | 研发流程 / 项目管理 | 强调纪律化开发流程的技能包，让 coding agent 按“先规格、后计划、再实现与复核”的方式工作。 |
| [`pbakaus/impeccable`](./refs-details/pbakaus/impeccable.md) | 前端 UI / 设计系统 | 面向前端设计质量的跨平台技能/命令打包仓库，附带官网、下载 API 和构建系统。 |
| [`tanweai/pua`](./refs-details/tanweai/pua.md) | 行为协议 / 提示工程 | 面向多种 AI 编码代理的“高压/高主动性”技能包，核心是 PUA/PIP 风格提示、命令、hooks 和多平台分发素材。 |
| [`travisvn/awesome-claude-Skills`](./refs-details/travisvn/awesome-claude-Skills.md) | 技能集合与市场 | 纯 curated list 仓库，汇总官方和社区 Claude Skills、教程、资源、安全建议与 FAQ。 |
| [`vercel-labs/agent-browser`](./refs-details/vercel-labs/agent-browser.md) | 浏览器自动化与前端调试 | 原生 Rust 驱动的浏览器自动化 CLI，并附带多套面向 AI 代理的技能文档。 |
| [`vercel-labs/agent-skills`](./refs-details/vercel-labs/agent-skills.md) | 前端 UI / 设计系统 | Vercel 出品的技能集合，覆盖 React/React Native、组合模式、UI 评审与 Vercel 部署。 |
| [`vercel-labs/skills`](./refs-details/vercel-labs/skills.md) | MCP / 工具链 / 安装分发 | 开放 Agent Skills 生态的 CLI/包管理器，用于发现、安装、列出、删除、更新技能，并维护多代理兼容性。 |
| [`Yeachan-Heo/oh-my-claudecode`](./refs-details/Yeachan-Heo/oh-my-claudecode.md) | 多智能体协作与工作流编排 | 完整的 Claude Code 多智能体编排系统，含 CLI、skills、agents、hooks、tmux worker runtime 和验证模块。 |

## 补充观察

- `travisvn/awesome-claude-Skills`、`libukai/awesome-agent-Skills` 更偏导航/市场/索引；适合找来源，不适合直接当能力实现。
- `ChromeDevTools/chrome-devtools-mcp`、`vercel-labs/agent-browser` 是浏览器自动化/前端调试类的两条重要主线，前者偏 DevTools MCP，后者偏 agent-browser CLI/runtime。
- `Yeachan-Heo/oh-my-claudecode`、`notdp/hive`、`nyldn/claude-octopus` 属于多智能体/多模型协作平台型项目。
- `mksglu/context-mode` 与 `muratcankoylan/Agent-Skills-for-Context-Engineering` 更适合归入上下文工程/记忆管理范畴。
- `automazeio/ccpm`、`gsd-build/get-shit-done`、`obra/superpowers` 更偏工程流程与项目执行方法学。
- `google-labs-code/stitch-skills`、`nextlevelbuilder/ui-ux-pro-max-skill`、`pbakaus/impeccable`、`vercel-labs/agent-skills` 更偏前端 UI / 设计系统。
- `millionco/react-doctor` 与 `addyosmani/web-quality-skills` 都属于代码质量/审查范畴，前者偏 React 代码体检，后者偏 Lighthouse / CWV / a11y / SEO 的 Web 质量审查。
- `tanweai/pua` 明显是行为协议/提示工程类。
