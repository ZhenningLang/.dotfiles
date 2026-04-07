# 上下文 / 记忆管理调研

## 参考项目

### mksglu/context-mode

MCP server + Hooks 工程项目，解决两个问题：(1) 大输出隔离在沙箱进程中不进入 context（98% 压缩率）；(2) SQLite 持久化 session 事件，compact/resume 后恢复工作状态。

核心能力：
- 沙箱执行（ctx_execute）：子进程运行代码，只返回 stdout
- FTS5 知识库（ctx_index/ctx_search）：Markdown 分块 → SQLite FTS5 + BM25 + Trigram + RRF 融合
- Session 事件捕获：PostToolUse hook 提取 14 类事件 → SQLite
- PreCompact 快照：事件 → 优先级排序 → ≤2KB XML
- SessionStart 恢复：快照 + FTS5 索引 → 15 段 Session Guide → 注入新 context

体量：中重量级（源码 ~20 文件，预编译 bundle ~1MB，依赖 SQLite native binding）

### muratcankoylan/Agent-Skills-for-Context-Engineering

13 个教程 skill 的知识库，覆盖 context fundamentals / compression / optimization / multi-agent / memory systems / filesystem patterns / evaluation 等。纯知识项目，无运行时代码。

体量：轻量（每个 SKILL.md 200-500 行，纯 Markdown）

## 可复用概念分层

### 直接可用（纯策略/prompt，零依赖）

**1. 结构化压缩模板**

context-mode 的 Session Guide 用固定结构恢复 compact 后状态：

```
Session Intent → Files Modified → Key Decisions →
Current State → Errors Encountered → Next Steps
```

**2. 锚定迭代摘要法**

只摘要新截断内容 → 合并到已有摘要（质量 3.70/5），优于重新生成完整摘要（2.79/5）。Factory 内部也采用此策略。

**3. 渐进式披露三层**

| 层 | 时机 | 对应实现 |
|---|------|---------|
| Skill Selection | session 启动 | 只加载 name + description |
| Document Loading | skill 被调用 | 加载 SKILL.md + refs/ |
| Tool Result Retention | 工具执行后 | 只保留关键输出 |

**4. 事件优先级分层**

| 级别 | 内容 | compact 时 |
|------|------|-----------|
| P1 | 当前任务目标、未完成项 | 必须保留 |
| P2 | 文件修改、关键决策 | 尽量保留 |
| P3 | 错误记录、环境信息 | 空间够才保留 |
| P4 | 历史搜索、中间输出 | 可丢弃 |

**5. Observation Masking**

工具输出在 3 轮对话后价值骤降，可遮蔽。Debugging 场景豁免。

**6. 70% 触发阈值**

Context 利用率到 70% 时主动压缩/清理，不等溢出。

### 可控集成（需少量文件操作，无外部依赖）

**7. Scratch Pad 模式**

在 `.factory/scratch/` 下维护临时文件（计划、中间发现、子 agent 通信），跨 session 持久化。

**8. Plan Persistence**

执行计划写到文件，每完成一步更新状态。Compact 后重新读文件恢复进度。

### 不建议集成

| 概念 | 理由 |
|------|------|
| FTS5 知识库 | 需要 SQLite native binding，grep/glob 够用 |
| 沙箱执行 | 需要完整 MCP server，droid 已有截断机制 |
| Session 事件捕获（完整版） | 需要持续 hook + 数据库 |
| Temporal Knowledge Graph | 需要图数据库 |
| BDI 认知架构 | 学术概念，无法落地 |

## 关键发现：Hooks 方案 vs Skill 方案

### Skill 路线 = 纯污染

Factory 的 compact 是内部系统，用自己的结构化摘要逻辑（anchored iterative summarization）。Skill 文本只是被压缩的 context 的一部分，compact 系统不会"遵守" skill 指令改变压缩方式。放 compact-guidelines skill = 白占 context。

### Hooks 路线 = 可行

Droid 支持两个直接相关的 hook 事件：

| Hook | Matcher | 时机 | 能做什么 |
|------|---------|------|---------|
| PreCompact | `manual` / `auto` | compact 执行前 | 读 transcript_path，提取关键状态，保存到磁盘 |
| SessionStart | `compact` | compact 后新 session 启动 | 读取保存的状态文件，通过 additionalContext 注入新 context |

工作流：
1. PreCompact hook 读取 `transcript_path`（完整对话 JSONL），提取 P1/P2 事件，保存到 `.factory/scratch/compact-state.json`
2. Factory 内部 compact 运行（不可控）
3. SessionStart(compact) hook 读取状态文件，格式化后注入 `additionalContext`，补充 Factory 摘要可能丢失的细节

优势：不污染正常 context，只在 compact 前后做旁路补充。

## Factory 官方数据

### 压缩质量评测（0-5 分）

| 方法 | 总分 | 准确性 | 上下文 | 文件追踪 | 完整性 | 连续性 |
|------|------|--------|--------|---------|--------|--------|
| Factory | **3.70** | **4.04** | **4.01** | **2.45** | **4.44** | **3.80** |
| Anthropic | 3.44 | 3.74 | 3.56 | 2.33 | 4.37 | 3.67 |
| OpenAI | 3.35 | 3.43 | 3.64 | 2.19 | 4.37 | 3.77 |

所有方法的文件追踪（artifact trail）得分都很低（< 2.5/5），说明 compact 后容易丢失"改了哪些文件"的信息。这正是 hooks 方案可以补充的价值点。

### 压缩率

- Factory: 98.6%（保留最多）
- Anthropic: 98.7%
- OpenAI: 99.3%（最激进）

### 官方记忆方案

Factory 推荐的跨 session 记忆：`~/.factory/memories.md`（个人）+ `.factory/memories.md`（项目），通过 AGENTS.md 引用。这是静态记忆，不是 compact 恢复。

## 参考链接

- Factory 压缩评测：https://factory.ai/news/evaluating-compression
- Factory 记忆管理：https://docs.factory.ai/guides/power-user/memory-management
- Factory Hooks 参考：https://docs.factory.ai/reference/hooks-reference
- context-mode：refs/mksglu/context-mode/
- Agent-Skills-for-Context-Engineering：refs/muratcankoylan/Agent-Skills-for-Context-Engineering/
