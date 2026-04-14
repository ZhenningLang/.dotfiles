---
name: se-quality
description: 代码质量与 AI-friendly 结构评估。用于判断代码/架构/diff 是否更可预测、可局部修改、可验证，并给出下一步路径。
---

# Quality

用于回答一个更基础的问题：这段代码是否容易被正确修改？

当用户出现以下意图时使用：

- 提升代码质量
- 判断代码是否适合 agent 持续修改
- 评估模块/架构是否 review-friendly
- 做 feature 前的结构体检
- 审查 diff 的结构质量，而不只是找 bug

## 1. 确定范围

解析 `$ARGUMENTS`：

- 文件/目录路径 -> 审查该模块的结构质量
- `diff` / 分支名 / commit range -> 审查改动的结构质量
- 留空 -> 结合当前任务上下文判断；范围不清时先让用户指定

对陌生仓库或复杂模块，先 `/se-map` 再开始。
对技术选型或架构模式不确定，先 `/se-research` 再评估候选方案。

## 2. 评估模型

### PIEV

- **Predictable** — 模式稳定，行为与改法容易预测
- **Isolated** — 改动局部，影响面可控
- **Explicit** — 规则、约束、边界是显式的
- **Verifiable** — 改完有办法快速验证

### 六个检查维度

1. **Boundary** — 职责、分层、输入输出、side effect 边界是否清晰
2. **Locality** — 一个需求是否主要集中在少数几个文件内完成
3. **Convention** — 是否存在稳定、统一、可续写的实现模式
4. **Explicitness** — 业务规则、约束、前提是否写出来，而不是藏在 tacit knowledge 里
5. **Testability** — 是否容易写单测/集成测试/contract test，验证回路是否短
6. **Diff Purity** — 变更是否单一目的；机械改动、重构、行为修改是否混在一起

## 3. 分析步骤

1. 确定 scope，并读代码/调用点/相关 diff
2. 按六个维度逐项检查
3. 找出 strengths 和 issues，并标记 `file:line`
4. 用 PIEV 总结整体状态
5. 给出下一步路径，而不是只说“可以优化”

## 4. 输出格式

```md
## Quality Assessment

### Strengths
- ... file:line

### Issues
#### P0
- ... file:line — 风险 — 建议
#### P1
- ...
#### P2
- ...

### PIEV Summary
- Predictable: High/Med/Low
- Isolated: High/Med/Low
- Explicit: High/Med/Low
- Verifiable: High/Med/Low

### Recommended Path
- 先 `/se-plan`
- 或先 `/se-refactor`
- 或先 `/se-tdd`
- 或可直接进入实现 / review / verify
```

## 5. 裁决规则

结尾必须给出明确裁决：

- **可直接实现** — 结构已足够清晰，风险可控
- **先拆边界** — Boundary/Locality 太差，直接改风险高
- **先补测试** — 行为会变，但缺少验证护栏
- **先拆 diff** — 目标混杂，review 成本过高
- **先重构再改行为** — 结构问题已开始掩盖真实意图

## 6. 与其他技能的联动

- 需要先设计约束或写 spec -> `/se-plan`
- 涉及行为变化且缺测试 -> `/se-tdd`
- 主要问题是结构债务 -> `/se-refactor`
- 需要审查具体改动 -> `/se-review`
- 即将声称完成 -> `/se-verify`

## 7. 判断启发式

出现以下信号时，优先判定为“先做结构工作”：

- 一个小需求预计要改很多文件
- 业务规则散落在多个层级/模块
- 同类问题已有多种写法
- side effect 和核心逻辑混在一个函数里
- 没有快速验证路径
- 一个 diff 同时混入重构、命名调整、行为变化、格式化

## 禁止

- 只给抽象评价，不给 `file:line`
- 把“更优雅”当成充分理由
- 不区分结构问题、逻辑 bug、测试缺口、diff 粒度问题
- 范围不清时直接下结论
- 替代 `/se-plan`、`/se-refactor`、`/se-review`、`/se-verify` 的职责
