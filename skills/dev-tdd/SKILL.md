---
name: dev-tdd
description: 新功能、修 bug、改行为前使用；先写失败测试再写实现，纯配置/文档/样式变更跳过。
argument-hint: <功能点|bug 描述|行为变更>
---

当任务属于以下场景时使用本 skill（除非用户明确说不要）：

- 新增功能/函数/模块
- Bug 修复
- 行为变更（非纯重构）

## 核心循环

```
RED    → 写一个失败测试（一个行为、名字说清行为）
       → 跑测试，确认失败原因是"功能缺失"而非 typo
GREEN  → 写最少的代码让测试通过（不加料、不优化）
       → 跑测试，确认通过 + 其他测试不挂
REFACTOR → 消除重复、改名、提取（保持绿灯）
```

## 判断启发式

能在写实现之前写 `expect(fn(input)).toBe(output)` → TDD

不能（UI 布局、配置、胶水代码、原型探索）→ 标准流程，事后补测试

## 跳过条件

用户明确说以下任一时，不强制 TDD：
- "不要 TDD" / "跳过测试" / "先探索"
- AGENTS.md 或项目配置中禁用了 TDD
- 纯配置/文档/样式变更

## 测试质量

- 测试行为，不测实现
- 一个测试一个概念
- Mock 只在外部边界使用（fs/http/db），不 mock 内部纯函数
- 提交模式：`test(scope): failing test` → `feat(scope): implement`

## Gotchas

- 先写实现、再补测试，不叫 TDD
- 红灯必须因为“行为缺失/不符合预期”，不能只是 typo 或测试本身坏掉
- UI 探索、样式调整、纯配置改动不要生搬硬套 TDD
- GREEN 阶段只做让测试过的最小实现，不顺手优化、不顺手重构

## 扩展阅读

- `docs/software-engineering-research/tdd.md`

## 关联技能

- 发现边界混乱、规则不显式、难以落测试时 → 先 `/think-quality` 或 `/think-plan`
- TDD 完成后 → `/guard-verify` 最终验证
- 连续失败 2 次 → `/think-unstuck`
