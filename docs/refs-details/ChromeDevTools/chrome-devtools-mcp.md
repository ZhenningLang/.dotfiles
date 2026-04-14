# ChromeDevTools/chrome-devtools-mcp

- 上游仓库：`https://github.com/ChromeDevTools/chrome-devtools-mcp`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/ChromeDevTools/chrome-devtools-mcp`
- 主分类：**浏览器自动化与前端调试**
- 能力标签：`MCP/工具集成`, `性能分析`, `前端 UI`
- 一句话总结：通过 MCP 控制真实 Chrome，提供自动化、调试、性能分析和配套 skills。

## 能力概览

- 控制真实 Chrome：打开页面、导航、点击、表单、截图、PDF、脚本执行。
- 读取 console、network、screencast、trace、Lighthouse、性能指标。
- 支持 slim 模式与多种调试/分析工作流。
- 自带 a11y、memory leak、LCP 优化等技能。

## 资产盘点

- 14 组主工具模块，另有 slim 工具集。
- 6 个技能目录。
- 2 个 CLI：chrome-devtools-mcp、chrome-devtools。
- 18 个评测场景脚本，5 个 GitHub workflow。

## 关键文件

- `README.md`
- `package.json`
- `src/tools/tools.ts`
- `skills/chrome-devtools/SKILL.md`

## 备注

- 默认会收集 usage statistics，可通过 flag/env 关闭；官方支持重点是 Chrome / Chrome for Testing。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`13`
- [事实] 代表提交：
  - `2026-04-02` `docs: fix skill and reference documentation issues (#1249)`
  - `2026-04-13` `chore(deps-dev): bump globals from 17.4.0 to 17.5.0 in the dev-dependencies group (#1857)`
  - `2026-04-13` `chore(deps-dev): bump the dev-dependencies group across 1 directory with 9 updates (#1844)`
  - `2026-04-13` `chore(deps): bump basic-ftp from 5.2.1 to 5.2.2 (#1849)`
- [事实] 近 14 天提交标题以依赖升级、README 中新增 Mistral Vibe 配置说明和文档修复为主，未见明显功能型提交。
<!-- recent-updates:end -->
