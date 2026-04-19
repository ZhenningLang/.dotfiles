---
name: guard-diff-scan
description: 当改动已完成但未 commit、需要确认没留调试遗留物时使用；扫描 git diff 中的 TODO/FIXME/调试语句。
---

# Diff Scan

在 commit 前扫一遍当前工作树的 diff，确认没有调试残留。

## 核心循环

```
1. 跑 git diff（工作树 + 暂存区）
2. 按固定清单扫遗留物
3. 输出每条命中 + 建议处理
4. 全部确认后才 commit
```

## 扫描清单

| 类型 | 触发模式 |
|------|----------|
| TODO/FIXME/XXX/HACK | `\b(TODO|FIXME|XXX|HACK)\b` |
| 调试打印 | `console\.log`、`print(`、`dbg!`、`pp `、`fmt.Println` |
| 调试断点 | `debugger;`、`breakpoint\(\)`、`pdb.set_trace` |
| 注释掉的代码块 | 连续 3+ 行以注释开头且含代码语法 |
| 硬编码 secret 疑似 | `password=`、`api_key=`、`token=` |
| 临时变量名 | `foo`、`bar`、`tmp1`、`test_xxx` 在生产代码里 |

## 输出格式

```markdown
## Diff Scan 结果

| 类型 | 文件 | 行 | 片段 | 建议 |
|------|------|----|------|------|
| TODO | src/auth.ts | 42 | `// TODO: handle retry` | 保留（有上下文）/ 删除 / 改写成 issue |
| console.log | src/cache.ts | 118 | `console.log('here', data)` | 删除 |

## 总结
- 命中 N 条
- 建议处理：X 条删除、Y 条保留、Z 条转 issue
- [ ] 用户确认通过，可以 commit
```

## 与其他 skill 的边界

- `guard-review` 做代码逻辑 review（是否有 bug、设计问题），范围大
- `guard-ship` 做交付前总预检（git status、敏感信息、分支），关注可交付性
- 本 skill 最窄：只扫 diff 中的文本遗留物，不做逻辑判断

## Gotchas

- TODO 不等于一定要删——有的 TODO 记录了真实后续工作，应转成 issue 或保留
- 测试文件里的 `console.log` / `print` 可能是有意的，不要一刀切
- 注释掉的代码块 vs 文档注释需要人工判断

## 未来增量

可加脚本做自动化扫描（backlog，见 docs/software-engineering-research/skill-patterns.md 里 tool-backed 升级思路）。
