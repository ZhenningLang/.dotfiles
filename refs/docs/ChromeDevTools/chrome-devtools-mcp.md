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
