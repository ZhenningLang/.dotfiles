# nyldn/claude-octopus

- 上游仓库：`https://github.com/nyldn/claude-octopus`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/nyldn/claude-octopus`
- 主分类：**多智能体协作与工作流编排**
- 能力标签：`多模型编排`, `代码审查与安全`, `Hooks/MCP`, `Personas`
- 一句话总结：超大体量的多模型编排插件，把 Claude Code/Droid 扩展成带工作流、角色、hooks、MCP 和兼容层的协作系统。

## 能力概览

- 通过 /octo:auto 把自然语言路由到研究、构建、调试、TDD、安全、PRD、设计等工作流。
- 支持 Claude、Codex、Gemini、Copilot、Qwen、Ollama、Perplexity、OpenRouter 等并行协作。
- 提供 consensus gate、reaction engine、provider routing、memory 集成。
- 带大量 personas/agents、hooks、脚本库、MCP server 和 OpenClaw 扩展。

## 资产盘点

- 仓库自述：47 commands、50 skills、32 personas。
- 含 mcp-server 与 openclaw 两套 TypeScript 包。
- tests/ 下有大规模 smoke/unit/integration/live 测试。

## 关键文件

- `README.md`
- `package.json`
- `.claude-plugin/README.md`
- `commands/octo-auto.md`
- `skills/octopus-architecture/SKILL.md`

## 备注

- 仓库层次非常多，更像编排平台；README 中数量以仓库自述为准。
