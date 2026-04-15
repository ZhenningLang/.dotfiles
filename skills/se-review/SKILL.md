---
name: se-review
description: 用户要求 review、审查代码变更、合并前把关时使用；默认先看 diff，再给分级结论与 merge 裁决。
argument-hint: <分支名|commit-range|--deep|留空=未提交变更>
---

# Review

## 1. 确定范围

解析 `$ARGUMENTS`：

- 分支名 → `git diff $(git merge-base HEAD <branch>)..HEAD`
- diff 范围（如 `a1b2c3..HEAD`）→ 使用指定 commit range
- `--deep` → 启用多模型对抗性审查
- 留空 → 审查未提交变更

## 2. Simple Review（默认）

派发单个 subagent 审查 diff，输出结构化报告：

### 默认聚焦策略

- **先看 diff，再看直接影响面**：默认只审查改动文件、同模块调用链、被改测试和明显受影响的配置/脚本。
- **不要一上来做 repo-wide 猎巫**：范围外的担忧可以记录，但不能和当前 diff 里的确定性问题混在一起。
- **严重度要有证据门槛**：只有存在明确失败路径、触发条件、影响范围时，才能升到 `Critical` / `Important`。

### 审查维度

- [ ] 正确性：逻辑、边界、错误处理
- [ ] 架构：关注点分离、耦合度、依赖方向
- [ ] 安全：输入验证、敏感数据、注入风险
- [ ] 测试：覆盖关键路径、测试行为而非实现
- [ ] 需求：变更是否满足目标、无范围蔓延
- [ ] 可修改性：改动是否局部、规则是否显式、是否破坏既有 convention、diff 是否足够单一

### 输出格式

```
### Strengths
[具体优点，带 file:line]

### Issues

#### Critical（必须修复）
- **问题** — file:line — 影响 — 修复建议

#### Important（应当修复）
- ...

#### Minor（建议修复）
- ...

### Out-of-scope observations
- [范围外但值得记录的观察；不影响当前 Ready to merge 结论]

### Structural assessment
- Boundary / Locality / Convention / Explicitness / Testability / Diff Purity 中，哪些维度在退化，哪些在改善

### Assessment
Ready to merge? Yes / No / With fixes
```

## 3. Deep Review（--deep）

多个 subagent（不同模型）独立审查相同 diff，汇总为：

- **Agreed Strengths** — 2+ reviewer 都提到的优点
- **Agreed Concerns** — 2+ reviewer 都提到的问题（最高优先级）
- **Divergent Views** — 分歧点（值得深入调查）

每个 reviewer 的独立报告附在后面供参考。

## 4. 接收反馈

对审查发现的问题：

1. 对照代码库验证（先 grep，不盲目接受）
2. 技术上合理 → 实施修复，每条单独测试
3. 不合理 → 带理由推回（破坏现有功能 / 违反 YAGNI / 技术不适用）
4. 不明确 → 全部澄清后再动手

## 5. Gotchas

- 没有明确失败路径、触发条件和影响面，不要上升到 `Critical` / `Important`
- review 的对象默认是当前 diff，不是借题发挥做全仓库猎巫
- 没有 `file:line` 或明确 diff 片段的意见，价值很低
- “建议更优雅”不等于问题；优先判断是否影响正确性、需求、结构质量或可维护性

## 扩展阅读

- `docs/software-engineering-research/review.md`

## 禁止

- 表演性回应（"Great point!", "You're absolutely right!"）
- 不验证就实施 reviewer 建议
- 模糊反馈（"这里可以优化"没有 file:line 和具体建议）
- 没有明确失败路径就上升严重度
- 把 repo 级猜测混进当前 diff 的主结论
- 没有裁决的审查（必须给出 Ready to merge? 结论）

## 关联技能

- Critical issues 涉及安全 → `/se-secure` 深入审查
- 需要统一结构质量语言 → `/se-quality`
- 发现需要重构 → `/se-refactor`
- Review 通过后交付 → `/se-ship`
