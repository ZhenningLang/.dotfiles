# Debug 调研

调研对象：Superpowers (systematic-debugging + verification-before-completion)、GSD (debug + forensics + verifier)。CCPM 无调试相关内容。

## 各项目方案摘要

### Superpowers — 4 阶段根因分析

严格的科学方法：观察 → 假设 → 预测 → 测试 → 结论。4 阶段流程：
1. 理解（复现 bug，精确描述症状 vs 预期）
2. 分析（从错误点回溯，列出假设并排序）
3. 修复（先写失败测试 → 最小修复 → 验证）
4. 验证（原始 bug、回归、边界用例全部验证）

核心原则：不猜测，不撒网式修复（shotgun debugging）。每个假设必须有证据支撑或排除。Reference 文件提供 root-cause-tracing、defense-in-depth、condition-based-waiting 等技术细节。

### GSD — 子 agent 隔离调试

debug 命令派发专门的 debugger agent（42K 字符定义），在独立 context window 中调试，避免污染主 session。流程：
1. 精确复现 → 最小复现
2. 分层假设生成（语法/逻辑/集成/环境/并发/数据）
3. 二分法定位（git bisect / 代码注释 / 日志注入）
4. 根因确认 → 修复 → 回归验证

独特点：失败后自动触发 forensics（事后取证），分析 git 历史和文件状态。HANDOFF.json 支持跨 session 暂停/恢复调试。

## 共识

1. **根因优先** — 不做表面修复，找到真正原因
2. **科学方法** — 假设→预测→测试→结论，不撒网
3. **先复现后修复** — 不能复现的 bug 不要尝试修
4. **证据驱动** — 每个假设必须有证据支撑或排除
5. **先测试后修复** — 先写捕获 bug 的失败测试
6. **最小修复** — 只改必要的，不顺手重构
7. **回归验证** — 修复后验证原始 bug + 周边功能

## 需要决断

### 1. 调试架构

| 方案 | 来源 | 取舍 |
|------|------|------|
| 内联（在当前 session 中调试） | Superpowers | 简单，但消耗主 session context |
| 子 agent 隔离（独立 context window） | GSD | 保护主 session，但增加复杂度 |

### 2. 状态持久化

| 方案 | 来源 | 取舍 |
|------|------|------|
| 无持久化，单 session 内完成 | Superpowers | 简单，适合多数 bug |
| HANDOFF.json 跨 session 暂停/恢复 | GSD | 适合复杂 bug，但增加文件管理 |

### 3. 事后取证

GSD 有 forensics（git 历史分析+状态取证），Superpowers 没有。是否需要独立的 forensics 能力？还是作为 debug 的可选步骤？

### 4. 调试日志注入

GSD 用自动日志注入辅助定位。是否作为标准步骤？还是只在二分法不够时使用？

### 5. 假设数量限制

Superpowers 不限制。GSD 限制最多 5 个假设并排序。是否设上限防止发散？

## 精华提取

| 技巧 | 来源 | 说明 |
|------|------|------|
| 假设分层 | GSD | 语法/逻辑/集成/环境/并发/数据，按层排序减少搜索空间 |
| 二分法定位 | GSD | git bisect + 代码注释 + 日志注入三种手段 |
| 不做撒网修复 | Superpowers | "try this and see if it works" = 禁止 |
| 最小复现 | 两者 | 从完整场景逐步剥离到最小触发条件 |
| Red Flags | Superpowers | "改了好几个地方但不确定哪个修好了" = 停下来，回退 |
| defense-in-depth | Superpowers | 多层防御而非单点修复 |
| condition-based-waiting | Superpowers | 用条件等待替代 sleep/延时 |
