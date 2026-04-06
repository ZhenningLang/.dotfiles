# Review 调研

调研对象：Superpowers (requesting/receiving-code-review)、GSD (review + verifier + plan-checker)。CCPM 无专门审查规范。

## 各项目方案摘要

### Superpowers — 双向审查体系

三个文件构成闭环：请求审查 → 审查执行 → 接收反馈。通过 git SHA range 派发 code-reviewer subagent。反馈分级：Critical（必修）→ Important（应修）→ Minor（可选）。明确裁决：Ready to merge? Yes/No/With fixes。接收反馈时禁止表演性回应（"Great point!"），要求 READ → VERIFY → EVALUATE → IMPLEMENT。支持带理由推回不合理的建议。

### GSD — 跨 AI 对抗性评审

审查对象是计划（plan），不是代码 diff。多个外部 AI CLI 独立评审取共识。自我回避：当前运行时不参与自身评审。输出：Agreed Strengths / Agreed Concerns / Divergent Views。verifier 做目标反向验证：不信任声称，验证代码库中实际存在的。4 级验证：Exists → Substantive → Wired → Data-flowing。

### CCPM

明确排除 review（"Do NOT use for: reviewing PRs"）。但全链路追溯性（PRD→Epic→Issue→Code→Commit）本身是审查基础设施。

## 共识

1. **验证优先于信任** — 不盲目接受 reviewer 反馈，对照代码库验证
2. **结构化分级输出** — 模糊反馈没有价值，必须具体可操作 + 分级
3. **明确裁决** — 审查必须给出结论，不能"建议参考"了事
4. **对 spec/requirements 的对照** — 代码是否满足需求是核心审查问题
5. **推回是义务** — reviewer 错了就推回，带技术理由
6. **先搜后判** — YAGNI check 先 grep 再定论

## 需要决断

### 1. Review 的对象

| 方案 | 来源 | 说明 |
|------|------|------|
| 代码 diff | Superpowers | git SHA range，聚焦变更 |
| 计划文档 | GSD | 执行前审查 |
| 全流程 | 综合 | 计划审查 + 代码审查 + 验证 |

### 2. 审查者

| 方案 | 来源 | 说明 |
|------|------|------|
| 单一 subagent | Superpowers | 一个 reviewer 看 diff |
| 多 AI 对抗 | GSD | 多模型独立审查取共识，成本高 |

### 3. 表演性语言

Superpowers 严格禁止（"Great point!", "Thanks for catching that!"）。是否写入 review command？对 AI agent 有价值（减少 token），但涉及人类时需灵活。

### 4. 审查时机

| 时机 | 来源 | 强制/可选 |
|------|------|-----------|
| 每个 task 完成后 | Superpowers | 强制 |
| 合并前 | Superpowers | 强制 |
| 计划编写后 | GSD | 强制 |
| 卡住时 / 重构前 | Superpowers | 可选 |

"每个 task 后都 review" 在小变更场景下是否过重？

### 5. 冲裁机制

当 reviewer 和 implementer 意见冲突时，谁是最终裁决者？建议：用户始终是最终裁决者。

## 精华提取

| 技巧 | 来源 | 说明 |
|------|------|------|
| 审查输出模板 | Superpowers | Strengths → Issues(Critical/Important/Minor) → Assessment(Ready?) |
| 反馈接收协议 | Superpowers | READ → VERIFY → EVALUATE → RESPOND → IMPLEMENT |
| 对抗性评审 | GSD | 多 reviewer → Agreed Strengths / Concerns / Divergent Views |
| 目标反向验证 | GSD | 不问"做了什么"，问"目标达成了吗" + 4 级验证 |
| YAGNI check | Superpowers | reviewer 建议"更专业"时先 grep 是否有人用 |
| 推回模板 | Superpowers | 建议破坏现有功能 / 违反 YAGNI / 技术不适用 → 带理由推回 |
