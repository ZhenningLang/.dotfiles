# dotfiles

My Droid skills/scripts

## Commands

| Command | Description |
|---------|-------------|
| `/droid-mod` | 修改/检查/恢复 droid 二进制（截断禁用、model 切换、effort 级别等） |

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
