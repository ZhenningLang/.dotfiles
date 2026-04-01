# vercel-labs/agent-browser

- 上游仓库：`https://github.com/vercel-labs/agent-browser`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/vercel-labs/agent-browser`
- 主分类：**浏览器自动化与前端调试**
- 能力标签：`CLI`, `测试`, `抓取`, `桌面自动化`
- 一句话总结：原生 Rust 驱动的浏览器自动化 CLI，并附带多套面向 AI 代理的技能文档。

## 能力概览

- 支持打开页面、快照、点击、填表、截图、PDF、键鼠操作、等待、导航。
- 支持 profile/session/state/auth vault、请求拦截、HAR、console/errors、trace、profiler。
- 支持连接现有 Chrome/CDP、自动化 Electron 桌面应用、iOS Simulator。
- 提供 dogfood、electron、slack、vercel-sandbox 等配套 skills。

## 资产盘点

- 5 个 skills。
- 9 个参考文档。
- 5 个模板。
- 10 个脚本、benchmarks 与 docs 站点源码。

## 关键文件

- `README.md`
- `package.json`
- `skills/agent-browser/SKILL.md`
- `skills/slack/SKILL.md`
- `skills/electron/SKILL.md`

## 备注

- 仓库同时是 CLI + 技能文档 + 文档站源码，能力面大于单纯 npm 包。
