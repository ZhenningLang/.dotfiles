# tirth8205/code-review-graph

- 上游仓库：`https://github.com/tirth8205/code-review-graph`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/tirth8205/code-review-graph`
- 主分类：**代码质量 / 审查 / 调试**
- 能力标签：`增量知识图谱`, `代码审查`, `Blast Radius`, `MCP`, `Tree-sitter`
- 一句话总结：面向 AI 编码工具的本地代码知识图谱，用 Tree-sitter、SQLite 与 MCP 把审查上下文缩到真正相关的 blast radius。

## 能力概览

- 用 Tree-sitter 解析 23 种语言与 Jupyter/Databricks notebook，构建函数、类、导入、调用、继承和测试覆盖关系图。
- 支持 `detect-changes` / `get_review_context` / `get_impact_radius` 一类审查工作流，把 diff 映射到受影响文件、调用链、测试缺口与风险评分。
- 支持增量更新、watch mode、git/file hooks，本地 SQLite 图谱可在提交或保存后持续刷新。
- 除 review 外，还覆盖 architecture/debug/onboard/pre-merge 场景，附带可视化、wiki 生成、GraphML/Neo4j/Obsidian/SVG 导出与多仓库 registry。
- `install` 会自动探测 Codex、Claude Code、Cursor、Windsurf、Zed、Continue、OpenCode、Antigravity、Kiro，并写入对应 MCP 配置与规则注入。

## 资产盘点

- 1 个 Python 主包：`code_review_graph/`。
- 1 个 VS Code 扩展子项目：`code-review-graph-vscode/`。
- 3 个 skills：`build-graph`、`review-delta`、`review-pr`。
- 10 份顶层 docs 文档。
- 5 个 MCP prompts：`review_changes`、`architecture_map`、`debug_issue`、`onboard_developer`、`pre_merge_check`。
- [事实] `code_review_graph/main.py` 当前暴露 30 个 `@mcp.tool()`；README 的“28 MCP tools”表述与源码数量不完全一致。
- 26 个顶层测试文件，覆盖 parser、graph、incremental、changes、wiki、registry、eval、TS path alias 等模块。

## 关键文件

- `README.md`
- `pyproject.toml`
- `code_review_graph/main.py`
- `code_review_graph/parser.py`
- `code_review_graph/graph.py`
- `code_review_graph/changes.py`
- `code_review_graph/prompts.py`
- `code_review_graph/visualization.py`
- `docs/FEATURES.md`
- `skills/review-pr/SKILL.md`

## 备注

- 它不是单纯的 review prompt 仓库，而是“本地结构索引 + MCP server + CLI + hooks + 导出资产”的完整工具链。
- [事实] 仓库自身强调 local-first：图谱存放在 `.code-review-graph/graph.db`，无外部数据库、无云端依赖。
- [推断] 和 `millionco/react-doctor` 相比，它更像“上下文裁剪/影响面分析基础设施”；和 `addyosmani/web-quality-skills` 相比，它更偏代码结构与调用关系，而不是 Lighthouse 式页面质量规范。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`1`
- [事实] 代表提交：
  - `2026-04-14` `fix: suppress both arg-type and return-value mypy codes for sort keys`
- [推断] 近 14 天节奏明显偏维护收尾；公开提交主要围绕 `mypy` 类型检查噪声收敛，未见明确的新功能主线。
<!-- recent-updates:end -->
