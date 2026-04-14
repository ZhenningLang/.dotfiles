# mksglu/context-mode

- 上游仓库：`https://github.com/mksglu/context-mode`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/mksglu/context-mode`
- 主分类：**上下文 / 记忆管理**
- 能力标签：`MCP 工具链`, `会话连续性`, `多运行时适配`, `Hooks`
- 一句话总结：面向多种 AI 编码运行时的 MCP/plugin，用来减少上下文窗口占用并保留会话连续性。

## 能力概览

- 提供 ctx_execute / ctx_batch_execute 等沙箱执行能力，避免大输出进入上下文。
- 支持文档与网页索引、搜索、抓取并落库到 SQLite FTS5/BM25。
- 通过 hooks 记录文件编辑、git 操作、任务、错误、用户决策并在 compact 后恢复。
- 为 Claude Code、Gemini CLI、Cursor、Codex、Kiro 等生成不同配置。

## 资产盘点

- 4 个 skill。
- 36 个 hook 文件。
- 20+ 个跨平台配置模板。
- 4 个脚本与完整 src 实现。

## 关键文件

- `README.md`
- `package.json`
- `skills/context-mode/SKILL.md`
- `hooks/hooks.json`
- `src/session/db.ts`

## 备注

- 并非所有平台都有完整 hook 支持；许可证是 Elastic-2.0。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`114`
- [事实] 代表提交：
  - `2026-04-14` `feat(insight): add ctx-insight skill for /ctx-insight slash command`
  - `2026-04-14` `feat(insight): add personal analytics dashboard with ctx_insight tool`
  - `2026-04-13` `feat(search): content-type-aware title boost in reranking (#265)`
  - `2026-04-13` `feat(web): add open-to-opportunities badge with tooltip`
- [推断] 连续发布 `1.0.79`~`1.0.88`，新增 `ctx-insight` skill 与个人 analytics dashboard/工具链，并补强 search、upgrade 与 CI 稳定性。
<!-- recent-updates:end -->
