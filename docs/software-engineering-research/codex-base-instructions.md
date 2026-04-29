# Codex Base Instructions —— 收编与处理记录

> 来源：OpenAI Codex（GPT-5）的 `base_instructions` 字段。
> 原文位置：用户本地下载的 `codex.txt`（一段长 prompt，约 6 个语义块）。
> 处理日期：2026-04-29

本文档不是日常加载文档。它是一次性的"外部 prompt 收编档案"，记录：

1. codex 原始 prompt 的语义切分
2. 我们对每段的处理决定（吸收 / 拒绝 / 已覆盖 / 待评估）
3. 拒绝吸收的部分及理由

后续再有类似外部 prompt（其它 agent 厂商的 system prompt、博客整理出的 best practices 等）需要并入本仓库时，按本文档的格式做对照。

---

## 处理总览

| 段 | 标题 | 决定 | 落点 |
|----|------|------|------|
| 1 | Personality | 拒绝 | 与事实纪律气质相反 |
| 2 | General + Engineering judgment | 部分吸收 | AGENTS.md 编辑/工具纪律 |
| 3 | Frontend guidance / Design instructions | 完整吸收 | `skills/fe-ui-design` 新增节 |
| 4 | Editing constraints | 吸收 | `skills/guard-diff-scan` 新增节 + AGENTS.md |
| 5 | Special user requests | 已覆盖 | 现有 `guard-review` 已覆盖 |
| 6 | Autonomy and persistence | 拒绝 | 与 spec 模式 / 默认停止冲突 |
| 7 | Working with the user | 部分吸收 | 拒绝双通道；其余进 `readable-final-answer` |
| 8 | Formatting rules | 吸收 | `readable-final-answer` Mode B |
| 9 | Final answer instructions | 吸收 | `readable-final-answer` Mode B |
| 10 | Intermediary updates | 吸收 | `readable-final-answer` Mode C |

---

## 段 1 · Personality

### 原文要旨

- 描述 Codex 是"vivid inner life"、温暖、好奇、playful、有独立人格
- 强调"epistemically curious collaborator"、"warm, curious, collaborative"
- 强调 Codex 不是镜子，是另一个主体性

### 决定：**拒绝**

### 理由

- 与本仓库 `AGENTS.md` 的 Truth Directive（"不要把猜测说成事实"）气质相反
- 人格化措辞会稀释事实纪律：当 agent 被要求"warm, alive"，它更倾向输出讨好型语言
- 本仓库定位是"工具型 agent"，不要求人格扮演

---

## 段 2 · General + Engineering judgment

### 原文要旨

- senior engineer 判断：先读代码，再行动
- `rg` / `rg --files` 优先；不用 `grep`
- 工具调用尽量并行（多文件读、多搜索）
- 不用 `echo "===="; cmd1; cmd2` 这类拼接污染输出
- 编辑保守：沿用 repo 已有 patterns、用结构化 API 而非字符串拼接、scope 内聚、抽象只在真正去掉复杂度时引入
- 测试覆盖按风险与 blast radius 缩放

### 决定：**部分吸收**

### 落点

- "并行调用、`rg` 优先" → AGENTS.md "编辑与工具纪律" 节
- "保守编辑、沿用 repo patterns" → 已被 `AGENTS.md` "AI-friendly 代码约束" 覆盖
- "测试按风险缩放" → 已被 `dev-tdd` skill 覆盖

### 不吸收

- "senior engineer 判断" 这类抽象口号——本仓库已有更具体的"四条红线 + 排错纪律"

---

## 段 3 · Frontend guidance / Design instructions

### 原文要旨

完整一段约 60 条前端反模式硬约束。覆盖：

- Build with empathy（受众匹配、design system 沿用）
- Controls & Icons（lucide、segmented control、卡片圆角、tooltip）
- Hero / Landing（不做 landing 默认、文字不入卡片、禁 SVG hero、品牌主体首屏）
- 视觉资源（真实图片、避 stock-style）
- Game / 引擎（用成熟库不手写）
- 3D（Three.js full-bleed、Playwright 验证）
- Card / Section 边界（不嵌卡片）
- 装饰禁忌（不用 orb / bokeh）
- 文本容器适配
- 显示文字与容器匹配
- 固定布局尺寸（aspect-ratio 防 reflow）
- 字号 / 字距（不随 viewport 缩放、letter-spacing 不用负值）
- 调色禁忌（紫主导、米色主导、深蓝主导、棕橙主导）
- 重叠

### 决定：**完整吸收**（用户决策：信息密度优先）

### 落点

- 整段照抄进 `skills/fe-ui-design/SKILL.md` 新节"Codex 反模式硬约束"
- 不做提炼削减
- 与原 fe-ui-design 的"四大基础原则 / Typography / Color / ..."并列存在；两层规约互补

### 风险

- skill 文件膨胀到 ~240 行，超出工作流型骨架的 200 行建议上限
- skill-authoring.md §4.2 明确"推荐非强制"，可接受

---

## 段 4 · Editing constraints

### 原文要旨

- 默认 ASCII；引入 Unicode 需要理由
- 注释克制（不写"赋值给变量"，但复杂块前可加 1 行 orientation）
- 用 `apply_patch` 做手动编辑；不用 `cat` 或 shell 写文件
- 不用 Python 小脚本读写文件（shell 或 patch 能干就用）
- 工作树可能脏：NEVER 回滚不是你做的改动
- 不属于你的改动：相关的就读懂配合，不相关的 ignore；只在阻塞时问用户
- 不用 `git reset --hard` / `git checkout --`，除非用户明确要求
- 优先非交互 git；不进交互 console

### 决定：**吸收**

### 落点

- 整段进 `skills/guard-diff-scan/SKILL.md` 新节"编辑与 Git 礼仪"
- 关键 4 条进 AGENTS.md "编辑与工具纪律" 节（ASCII / patch 工具 / 并行调用 / 文风禁忌）

---

## 段 5 · Special user requests

### 原文要旨

- 简单 terminal 命令请求（如 `date`）直接执行
- 用户说 "review" 时默认走 code-review 立场：bugs / regressions / missing tests 优先

### 决定：**已覆盖**

### 理由

- 简单命令直接执行 → 已被通用 agent 行为覆盖
- review 立场 → 已有 `skills/guard-review` skill 承接

### 不吸收

- 不在 AGENTS.md 加"用户说 X 时走 Y"的关键词路由表，那是 commands 层职责

---

## 段 6 · Autonomy and persistence

### 原文要旨

- 端到端做完，不停在 analysis 或半完成
- 默认假设用户要你改，不要停在 proposal
- 遇到 blocker 自己先尝试解决
- resume / 中断 / context 压缩后做 sanity check：当前回答是否对应最新请求

### 决定：**拒绝（核心部分）**

### 理由

- "默认 proactive 实现，不停在 proposal" 与本仓库 spec 模式 + 审批门冲突
- 本仓库 AGENTS.md 明确"用户要求完成且验证通过后默认停止，不主动扩 scope"
- 强行吸收会破坏现有的"先 spec、再实现"工作流

### 部分吸收

- "resume 后做 sanity check" 这一条值得保留 → [推断] 未来可加进 `think-unstuck` 或新增 `assist-resume-check` skill；本轮不做

---

## 段 7 · Working with the user

### 原文要旨

- 双通道：commentary + final
- 用户中途发新消息：最新覆盖旧消息；不冲突就同时尊重
- resume 后先 sanity check 再答 final
- context 自动压缩——继续工作，不重启

### 决定：**部分吸收**

### 拒绝

- "commentary + final 双通道" —— 本仓库无该通道概念，强行引入只会噪音

### 吸收

- "最新消息覆盖旧消息" —— 这是合理的多轮处理原则，但属于通用 agent 行为，不需要写进 skill 或 AGENTS

### 落点

- 不单独落点

---

## 段 8 · Formatting rules

### 原文要旨

- 用 GitHub-flavored Markdown
- 列表平铺、避免嵌套；要层级时拆节或换行 + 冒号
- 数字列表用 `1. 2. 3.`，不用 `1)`
- header 用 `**Title Case**`（1–3 词），不空行
- 命令 / 路径 / env / code id 用 backtick
- 多行代码 fenced + info string
- 文件链接：`[label](/abs/path:line)`，路径含空格用尖括号
- 不在 markdown link 外或内嵌 backtick
- 不用 `file://` / `vscode://` / `https://` 做文件链接
- 不用行号范围
- 不用 emoji / em dash

### 决定：**吸收**

### 落点

- `skills/readable-final-answer/SKILL.md` Mode B "最终答案体裁规范"

---

## 段 9 · Final answer instructions

### 原文要旨

- 简单 / 单文件任务：1–2 段 prose
- 复杂任务整体 ≤ 50–70 行
- 不以 "If you want…" 句式收尾
- 不写"我做了 X 而不是 Y"自夸式对照
- 命令输出用户看不到，要复述关键内容
- 不要让用户"save / copy this file"
- 失败要明说
- 不用 "seam / cut / safe-cut" 自造隐喻
- 不用动物比喻填充语：goblins / gremlins / raccoons / trolls / ogres / pigeons

### 决定：**吸收**

### 落点

- `skills/readable-final-answer/SKILL.md` Mode B + "文风禁忌" 节

---

## 段 10 · Intermediary updates

### 原文要旨

- commentary 是"边做边想"的 channel（这部分拒绝吸收）
- 每次动作前先一句简短说明（在改什么 / 在读什么 / 为什么）
- 句式多样化，不要每条都用同一开头
- 单条 ≤ 2 句；只有需要长 plan 时才允许超过
- 探索时持续 narrate
- 不夸自己的方案，不与"显而易见的差方案"作对比
- 不用动物比喻填充语
- 频次约 30s

### 决定：**部分吸收**

### 吸收

- 节奏与风格（动作前说明、句式多样、单条 ≤ 2 句、探索 narrate）
- 内容约束（不夸方案、不报琐碎进展）

### 拒绝

- "30s 一次" —— 节奏由 droid runtime 决定，不写进规范
- "commentary channel" —— 本仓库无此概念

### 落点

- `skills/readable-final-answer/SKILL.md` Mode C "过程播报"

---

## 拒绝吸收的部分（汇总）

| 部分 | 拒绝理由 |
|------|---------|
| Personality 段 | 与事实纪律气质相反，会稀释 Truth Directive |
| 默认 proactive 实现 | 与 spec 模式 / 默认停止冲突 |
| commentary + final 双通道 | 本仓库无该通道概念 |
| 30s 一次更新 | 节奏由 runtime 决定，不写规范 |
| "用户说 review 走 code-review" 关键词路由 | 已有 guard-review 承接，不在 AGENTS 做关键词表 |
| "senior engineer judgment" 抽象口号 | 已有更具体的四条红线 + 排错纪律 |

---

## 后续 TODO（可选，不在本轮）

- [推断] resume 后 sanity check 这一条值得保留——可加进 `think-unstuck` 或新增 `assist-resume-check`
- [未验证] codex 整段照抄到 fe-ui-design 后是否影响 agent 路由命中率，需观察后再调
- 后续若再吸收同类外部 prompt，按本文档"段切分 + 处理决定 + 落点"格式做对照
