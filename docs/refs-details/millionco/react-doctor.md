# millionco/react-doctor

- 上游仓库：`https://github.com/millionco/react-doctor`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/millionco/react-doctor`
- 主分类：**代码质量 / 审查 / 调试**
- 能力标签：`React 静态分析`, `GitHub Action`, `Agent Skill`
- 一句话总结：React 代码体检工具仓库，核心是 CLI 扫描器，同时附带 GitHub Action、agent skill 和网站。

## 能力概览

- 扫描 React 代码库的安全、性能、正确性、架构、bundle size、state/effects 问题。
- 输出 0–100 健康分与可操作诊断。
- 支持 diff 模式、workspace 选择、config ignore。
- 可作为 GitHub Action 在 PR 中发评论。

## 资产盘点

- 1 个 skill。
- 1 个 GitHub Action。
- 2 个 package：CLI + website。
- 11 个规则模块。

## 关键文件

- `package.json`
- `packages/react-doctor/README.md`
- `skills/react-doctor/SKILL.md`
- `action.yml`

## 备注

- skill 很薄，核心能力在 CLI/package 源码里。

## 最近 14 天更新（2026-03-31 ~ 2026-04-14）
<!-- recent-updates:start -->
- [事实] 检查基线：`origin/main`
- [事实] 提交数：`6`
- [事实] 代表提交：
  - `2026-04-10` `0.0.33`
  - `2026-04-10` `0.0.32`
  - `2026-04-06` `0.0.31`
  - `2026-04-10` `fix: restrict setter detection to direct Identifier callees (#122)`
- [推断] 发布 `0.0.31`/`0.0.32`/`0.0.33`，重点修复 setter 检测与 catalog resolution、file ignoring、CLI、React Native、Next.js、offline、monorepo 等问题。
<!-- recent-updates:end -->
