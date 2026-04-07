---
name: se-review
description: 代码审查（支持 simple/deep 两种模式）。用户要求 review、审查代码变更时使用。
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

### 审查维度

- [ ] 正确性：逻辑、边界、错误处理
- [ ] 架构：关注点分离、耦合度、依赖方向
- [ ] 安全：输入验证、敏感数据、注入风险
- [ ] 测试：覆盖关键路径、测试行为而非实现
- [ ] 需求：变更是否满足目标、无范围蔓延

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

## 禁止

- 表演性回应（"Great point!", "You're absolutely right!"）
- 不验证就实施 reviewer 建议
- 模糊反馈（"这里可以优化"没有 file:line 和具体建议）
- 没有裁决的审查（必须给出 Ready to merge? 结论）
