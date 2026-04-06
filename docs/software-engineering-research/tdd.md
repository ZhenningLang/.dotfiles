# TDD 调研

调研对象：Superpowers (test-driven-development)、GSD (tdd reference + verifier)、CCPM (execute phase)。

## 各项目方案摘要

### Superpowers — 硬核 TDD

没有失败测试就不写产品代码。先写了代码？删掉重来。几乎全部场景适用（例外须人类批准：原型、生成代码、配置文件）。提供 12 条"合理化借口反驳表"防止 agent 绕过流程。5 种测试反模式文档。

### GSD — 务实 TDD

判断启发式：能在写实现之前写 `expect(fn(input)).toBe(output)` → TDD；不能 → 标准流程 + 事后补测试。TDD 候选：业务逻辑、API、数据转换、验证规则。跳过 TDD：UI 布局、配置、胶水代码、原型。4 级验证体系（Exists → Substantive → Wired → Data-flowing）。

### CCPM — 测试作为执行层

测试是并行工作流的一个 Layer（与 DB/Service/API/UI 并列），不做方法论层面的约束。"Always run tests before committing"。

## 共识

1. **Red-Green-Refactor 是基本循环**
2. **测试行为而非实现**
3. **每个测试一个行为，名字描述行为**
4. **最小化 mock，优先真实代码**
5. **提交前必须跑通测试**
6. **Bug 修复必须先写失败测试**
7. **验证 > 生成** — 没看到测试失败就不知道测试对不对

## 需要决断

### 1. TDD 适用边界

| 立场 | 来源 |
|------|------|
| 几乎全部场景，例外需人类批准 | Superpowers |
| 有明确输入/输出的才用，UI/配置/胶水跳过 | GSD |
| 不做方法论约束 | CCPM |

### 2. "先写了代码再补测试" 的处理

| 立场 | 来源 |
|------|------|
| 删掉代码，从测试重新开始，无例外 | Superpowers |
| 分类处理：已完成的代码用 add-tests 补测试是正常流程 | GSD |

### 3. Mock 策略

| 立场 | 来源 |
|------|------|
| Mock 是最后手段，必须理解依赖才能 mock | Superpowers |
| 按边界分：mock 外部依赖（fs/http/db），不 mock 内部纯函数 | GSD |

### 4. 探索性编码

| 立场 | 来源 |
|------|------|
| 探索完了丢掉，用 TDD 重写 | Superpowers |
| 探索阶段直接跳过 TDD | GSD |

### 5. 覆盖率目标

无项目设置覆盖率红线。是否以"关键路径全覆盖"为标准？

## 精华提取

| 技巧 | 来源 | 说明 |
|------|------|------|
| 判断启发式 | GSD | 能写 `expect(fn(input)).toBe(output)` → TDD；不能 → 事后补 |
| 提交模式 | GSD | `test(scope): failing test` → `feat(scope): implement` → `refactor(scope): cleanup` |
| 4 级验证 | GSD | Exists → Substantive → Wired → Data-flowing |
| 反模式速查 | Superpowers | 测试 mock 而非代码、产品类加测试方法、盲目 mock、不完整 mock、事后补测试冒充 TDD |
| 合理化反驳表 | Superpowers | 预判 agent 用来绕过 TDD 的借口并逐条反驳 |
| 上下文预算 | GSD | TDD plan ~40%（比标准 plan 的 ~50% 低，因为来回更多） |
| 质量审计 | GSD | 检查禁用测试、循环测试、断言强度（存在性 vs 值 vs 行为级） |
