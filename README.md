# dotfiles

My Droid skills/scripts

## Commands

| Command | Description |
|---------|-------------|
| `/droid-mod` | 修改/检查/恢复 droid 二进制 |
| `/se-plan` | 需求分析→设计→执行计划（多粒度 spec） |
| `/se-debug` | 系统化调试（科学方法，子 agent 隔离分析） |
| `/se-review` | 代码审查（simple/deep 两种模式） |
| `/se-refactor` | 代码重构（分支比较、未提交变更、自定义范围） |
| `/refactor` | 兼容旧入口，转到 `/se-refactor` |
| `/se-map` | 分析代码库结构、技术栈、约定和依赖 |
| `/se-ship` | 交付（测试→review→push→PR） |
| `/se-research` | 实现前技术调研（选型、最佳实践、风险） |
| `/se-secure` | 安全审查（STRIDE 威胁建模） |

## Skills

| Skill | Description |
|-------|-------------|
| `tdd` | TDD 工作流 skill；可手动 `/tdd`，也可由 agent 在相关任务中调用 |
| `verify` | 完成前验证 skill；用于要求验证证据，不代表仓库已配置强制 hook |

## 工程流程 Commands 设计

### 问题

参考项目（superpowers、GSD 等）提供了严谨的研发流程，但存在两个实践问题：

1. **Prompt 竞争** — Skill 形态在 session 启动时注入大量提示词（5-80K chars），与 AGENTS.md 争夺 agent 注意力，削弱用户自定义准则的权威性
2. **刚性过强** — 强制所有操作走完整流程（设计→规划→TDD→review），不适合快速修复和小改动

### 方案

将工程流程拆为独立 Command（`se-` 前缀），用户按需触发，不污染 idle context：

- **AGENTS.md 保持权威** — 全局准则不受干扰
- **用户控制粒度** — 快速修复直接改，严谨开发时 `/se-plan` → `/tdd`
- **零 idle 开销** — Command 仅在触发时加载

调研文档：`docs/software-engineering-research/`

## Refs

`refs/` 以 git submodule 形式收集第三方 Agent Skills 项目，按 `refs/{owner}/{repo}` 组织。

### 目录结构

```text
refs/
├── {owner}/
│   └── {repo}/          # git submodule → github.com/{owner}/{repo}
└── docs/                # 研究文档（gitignored，本地生成）
    ├── README.md        # 汇总表格 + 分类
    └── {owner}/{repo}.md
```

### 分类

| 分类 | 项目 |
|------|------|
| 浏览器自动化 | `ChromeDevTools/chrome-devtools-mcp`, `vercel-labs/agent-browser` |
| 多智能体协作 | `Yeachan-Heo/oh-my-claudecode`, `notdp/hive`, `nyldn/claude-octopus` |
| 前端 UI / 设计系统 | `google-labs-code/stitch-skills`, `nextlevelbuilder/ui-ux-pro-max-skill`, `pbakaus/impeccable`, `vercel-labs/agent-skills` |
| 研发流程 / 项目管理 | `automazeio/ccpm`, `gsd-build/get-shit-done`, `obra/superpowers` |
| 上下文 / 记忆管理 | `mksglu/context-mode`, `muratcankoylan/Agent-Skills-for-Context-Engineering` |
| 技能集合与市场 | `anthropics/skills`, `Dimillian/Skills`, `affaan-m/everything-claude-code`, `glittercowboy/taches-cc-resources`, `libukai/awesome-agent-Skills`, `travisvn/awesome-claude-Skills` |
| 代码质量 / 审查 | `millionco/react-doctor` |
| MCP / 工具链 | `vercel-labs/skills` |
| 行为协议 / 提示工程 | `tanweai/pua` |

### 常用操作

```bash
# 克隆后初始化 submodule
git submodule update --init --depth 1

# 添加新项目
git submodule add --depth 1 https://github.com/{owner}/{repo} refs/{owner}/{repo}

# 更新全部
git submodule update --remote --depth 1
```
