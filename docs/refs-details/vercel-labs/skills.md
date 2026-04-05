# vercel-labs/skills

- 上游仓库：`https://github.com/vercel-labs/skills`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/vercel-labs/skills`
- 主分类：**MCP / 工具链 / 安装分发**
- 能力标签：`CLI`, `技能包管理`, `多 Agent 兼容`
- 一句话总结：开放 Agent Skills 生态的 CLI/包管理器，用于发现、安装、列出、删除、更新技能，并维护多代理兼容性。

## 能力概览

- 从 GitHub URL、owner/repo、git URL、本地路径安装技能。
- 支持按 agent、skill、scope 过滤安装。
- 提供 list、find、remove、check update、update all、init 模板。
- 维护 44 种 agent 的安装路径与检测逻辑。

## 资产盘点

- 1 个内置 skill：find-skills。
- 26 个 TypeScript 源文件。
- 4 个维护脚本。
- 18 个测试文件。

## 关键文件

- `README.md`
- `package.json`
- `src/cli.ts`
- `src/agents.ts`
- `skills/find-skills/SKILL.md`

## 备注

- 重点是 CLI 与 agent 兼容层，不是技能内容库；README 很多内容由脚本生成。
