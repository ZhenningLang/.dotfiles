# HughYau/qiushi-skill

- 上游仓库：`https://github.com/HughYau/qiushi-skill`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/HughYau/qiushi-skill`
- 主分类：**行为协议 / 提示工程**
- 能力标签：`方法论框架`, `哲学驱动`, `工作流编排`, `多平台分发`, `Hooks`, `Subagents`
- 一句话总结：从毛泽东思想中提炼"实事求是"总原则和九大方法论工具，系统性武装 AI Agent 的分析与决策能力，附带工作流编排、subagent 和多平台插件支持。

## 能力概览

- **总原则层**：`实事求是` 作为全局认识论约束，要求事实驱动、验证闭环、承认未知。
- **哲学基座层**：`矛盾分析法`（抓主要矛盾）、`实践认识论`（实践→认识→再实践螺旋）。
- **工作方法层**：`调查研究`（没有调查就没有发言权）、`群众路线`（从群众中来到群众中去）、`批评与自我批评`（惩前毖后治病救人）。
- **战略战术层**：`持久战略`（战略藐视战术重视）、`集中兵力`（伤十指不如断一指）、`星火燎原`（建根据地不做流寇）、`统筹兼顾`（调动一切积极因素）。
- **工作流编排**：提供三条标准化跨 skill 工作流（新项目启动、复杂问题攻坚、方案迭代优化），定义 skill 调用顺序、步骤间数据传递格式和终止条件。
- **入口路由**：`arming-thought` 作为轻量路由器，session 启动时自动注入，按场景调度下游 skill，避免机械全调用。

## 架构特点

- **三层金字塔**：哲学基座 → 工作方法 → 战略战术，层层递进，上层约束下层。
- **路由式调度**：不在每次对话机械加载全部 skill，而是通过 `arming-thought` 按需调度。
- **工作流编排层**：`workflows` skill 解决"应该先用哪个 skill、怎么衔接"的问题，强制步骤间数据传递。
- **指令优先级**：用户指示 > 宿主平台规则 > qiushi skills，明确作为补充框架而非替代。
- **原著可追溯**：每个 skill 附带 `original-texts.md` 收录毛选原文，保证方法论有据可依。

## 资产盘点

- 11 个 skills（含 `arming-thought` 路由入口 + 9 个方法论 + `workflows` 编排层）。
- 10 个 commands（对应每个 skill 的手动入口）。
- 1 个 agent（`self-critic` 自我批评审查 subagent）。
- 3 个 subagent prompts（`investigation-agent-prompt`、`contradiction-mapper-prompt`、`feedback-synthesizer-prompt`）。
- 3 个 reference guides（`contradiction-types-reference`、`review-checklist`、`phase-assessment-guide`）。
- SessionStart hook（POSIX shell + Windows PowerShell 双版本）。
- 多平台插件配置：`.claude-plugin`、`.cursor-plugin`、`.codex`、`.opencode`。
- 验证脚本：`validate.sh`（macOS/Linux）、`validate.ps1`（Windows）。

## 关键文件

- `skills/arming-thought/SKILL.md` — 总入口路由与实事求是原则
- `skills/workflows/SKILL.md` — 三条标准化工作流定义
- `skills/contradiction-analysis/SKILL.md` — 矛盾分析法，最核心的分析工具
- `agents/self-critic.md` — 自我批评审查 subagent
- `hooks/hooks.json` — SessionStart 自动注入配置
- `.claude-plugin/plugin.json` — Claude Code 插件配置

## 与其他 refs 的对比

| 维度 | qiushi-skill | tanweai/pua | obra/superpowers |
|---|---|---|---|
| 方法论来源 | 毛泽东思想（哲学/方法论） | PUA/PIP 高压激励 | 软件工程纪律 |
| 核心机制 | 路由调度 + 工作流编排 | 行为约束 + 失败升级 | spec→plan→implement→review |
| 侧重点 | 分析问题的思维框架 | 推动执行的行为协议 | 工程流程的阶段管理 |
| skill 粒度 | 9 个独立方法论 + 编排层 | 11 个变体/强度等级 | 5 个核心阶段 |

## 可借鉴的设计

- 工作流编排层的数据传递格式和终止条件设计，可用于自己的 skill 串联。
- 路由式 skill 调度（按场景按需加载）优于全量注入。
- 原著引用文件分离设计，避免 skill 主体过长但保留可追溯性。
- 指令优先级声明（用户 > 宿主 > 本框架）是良好的防冲突实践。

## 备注

- 核心价值是方法论框架与思维工具，不是传统代码库。
- 九大思想武器覆盖从"怎么想问题"到"怎么做事情"的完整链路，与纯行为约束类（如 pua）互补。
- Windows 支持（PowerShell hook）从 v1.2.0 起加入，跨平台覆盖较完整。
