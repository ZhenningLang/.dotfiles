# 其他工程流程方向调研

排除已有的 plan/tdd/debug/review/refactor，评估剩余能力是否值得独立成 command。

## 推荐提取的方向

### 1. map — 代码地图

**来源**: GSD `map-codebase` + Superpowers `brainstorming`

系统化分析代码库的技术栈、架构、约定、依赖和测试覆盖，生成结构化文档。所有其他 command 的前置条件——plan/debug/review 都假设你已了解代码库，map 解决"还不了解"的问题。适用：接手新项目、大重构前摸底、长期未碰的项目重新上手。

### 2. ship — 交付

**来源**: GSD `ship` + `pr-branch` + Superpowers `finishing-a-development-branch`

关闭 plan→implement→verify→ship 循环。验证测试通过 → push → 创建 PR（自动生成描述）→ 可选 review。Superpowers 提供四种交付路径：merge locally / create PR / keep branch / discard。避免"代码写完了但忘了提 PR"。

### 3. research — 技术调研

**来源**: GSD `research-phase`

实现前的技术调研，回答"不知道自己不知道什么"。搜索最佳实践、标准技术栈、常见坑、不应手写的东西。research 的输出是 plan 的输入。适用：用不熟悉的技术栈开发、选型对比、评估可行性。

### 4. verify — 验证

**来源**: GSD `verify-work` + Superpowers `verification-before-completion`

功能完成后从用户视角逐条确认是否正确。核心原则：evidence before claims——没有跑过验证就不能声称完成。tdd 关注单元正确性，verify 关注整体功能完整性。

### 5. secure — 安全审查（可选）

**来源**: GSD `secure-phase`

STRIDE 威胁建模 + 安全缓解措施审查。对涉及用户输入、认证、支付、敏感数据的功能有价值。使用频率取决于项目类型，可先作为 review 的可选模式观察需求。

## 不推荐提取的方向

| 方向 | 来源 | 不推荐原因 |
|------|------|-----------|
| forensics (故障取证) | GSD | 与 debug 高度重叠 |
| add-tests (补测试) | GSD | 作为 tdd 的参数模式（`tdd retrofit`）更合适 |
| docs-update (文档更新) | GSD | 作为 ship 的可选步骤 |
| brainstorming (头脑风暴) | Superpowers | 与 plan 前置阶段重叠 |
| analyze-dependencies | GSD | plan 或 map 的子步骤 |
| autonomous/manager/workstreams | GSD | 调度层，不是独立工程流程 |
| 项目管理系列 (milestone/phase/backlog) | GSD+CCPM | 过于重型，适合团队级工具 |
| UI 相关 (ui-review/ui-phase) | GSD | 领域特定，只对前端有价值 |
| 基础设施层 (git-worktrees/dispatching-agents) | Superpowers | 支撑其他 command 的基础设施 |

## 完整 Command 版图建议

```
已有:  refactor
调研中: plan, tdd, debug, review
新增:  map, ship, research, verify
可选:  secure (先观察需求)
```
