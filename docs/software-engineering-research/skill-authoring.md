# Skill Authoring Guide

本文档规定本仓库 `skills/*/SKILL.md` 的编写约束。违反触发语义硬约束的 skill 无法通过 `scripts/verify_skills.py`。

其它推荐项（结构模板、输入输出格式）放在本文档后续节（由 PR2 补充）和 `skill-patterns.md`。

---

## 1. frontmatter 触发语义（硬约束）

### 1.1 规范

frontmatter 的 `description` 字段必须分两段，以触发词开头：

```
<触发词> <场景描述段>；<能力描述段>
```

三个组成部分的职责：

| 组成 | 写什么 | 不写什么 |
|---|---|---|
| 触发词 | 固定前缀（见 1.2），让 agent 能做路由决策 | 自由措辞 |
| 场景描述段 | 代码状态、任务性质、情境特征 | "用户是否明示请求"、"用户要求 X" |
| 能力描述段 | skill 做什么、输出什么 | 详细操作步骤（放 SKILL.md 正文） |

**分段符号**：中文场景用 `；`，英文场景用 `.` 或 `;`。

### 1.2 允许的触发词（四选一）

```
Use when ...
Invoke when ...
用于 ... 时
当 ... 时使用
```

`scripts/verify_skills.py` 校验 `description` 以上述 4 种前缀之一开头（允许前导空白）。

**不接受**的写法：

- `<skill 名>。<描述>`（如 `代码重构。支持分支比较...`）
- `<能力描述>。<触发条件>`（触发条件放后面）
- `Run after ...`（不在白名单）
- `After <某事件>, use ...`（不在白名单）

### 1.3 场景化 vs 用户行为化（关键硬约束）

`description` 描述**何时该被调用的客观场景**，不描述**"用户是否明示请求"**。

这一条是硬约束，因为：

- "用户要求 X 时使用" 会让 agent 把自主判断让渡给用户的显式措辞
- agent 在日常工作中应能基于代码状态、任务性质**自主决定**是否调用 skill
- 能让 skill 在 `commands/*.md` 路由、agent 隐式选择、用户显式触发三种场景下一致生效

#### 正反对比

| ❌ 用户行为化 | ✅ 场景化 |
|---|---|
| `用户要求重构、简化、清理重复时使用` | `当代码出现重复、结构债、可读性下降或需要调整模块边界时使用` |
| `用户要求 review、审查代码变更时使用` | `当存在未 review 的代码变更或需要在合并前把关时使用` |
| `用户要求提交、发布时使用` | `当改动已完成、需要创建 PR 或推送到远端时使用` |
| `用户要求技术选型时使用` | `当实现前需要技术选型、方案对比或可行性评估时使用` |
| `用户要求了解项目结构时使用` | `当接手陌生仓库、需要分析代码结构或梳理依赖关系时使用` |
| `用户要求安全审查时使用` | `当改动触及认证、授权、数据处理或外部依赖边界时使用` |

#### 允许保留"用户触发"的例外

只有当触发**本质上**依赖用户主观判断（而不是客观代码状态）时，可以在能力描述段提到"用户可触发"，但**触发词段仍必须是场景**：

```
✅ 当对话进展停滞、agent 路径漂移或需要结构化排查时使用；也接受用户手动触发。
```

### 1.4 豁免机制（trigger-exempt）

当一条 skill **改写后会丢失原 description 携带的关键语义**（如时序感、外部依赖契约、原 prompt 触发词法），允许在 `skills/catalog.json` 中标注豁免：

```json
{
  "name": "react-doctor",
  "path": "skills/react-doctor",
  "domain": "ui",
  "role": "brand-exception",
  "trigger-exempt": true
}
```

豁免规则：

- `trigger-exempt: true` 时，`verify_skills.py` 跳过对该 skill 的触发前缀校验
- 仅用于改写会丢失原信息的真实情况，不是逃避规范的口子
- 必须在 `commit message` 或仓库说明里写清豁免理由
- `role: brand-exception` 的外挂 skill（如 `agent-browser`、`hive`）默认豁免（无需显式标 `trigger-exempt`）

当前已知豁免案例：

| skill | 理由 |
|---|---|
| `agent-browser` | 外挂 brand-exception，由上游维护 |
| `hive` | 外挂 brand-exception，由上游维护 |
| `react-doctor` | 原 `Run after making React changes ...` 的"after"时序感无法用 4 种触发词无损表达 |

### 1.4 能力描述段约束

- 压缩到一行内，不展开步骤
- 可以标注"与 X skill 的边界"，但必须放能力描述段，不放触发段
- 例：`当改动涉及多文件或影响面不明时使用；改动前画文件地图 + 风险 checklist（与 think-map 的区别是它聚焦仓库全局，本 skill 聚焦单次任务）`

---

## 2. 检查清单（提交前自检）

- [ ] description 以 4 种触发前缀之一开头
- [ ] 触发段描述"场景/代码状态/任务性质"，不含"用户要求 X"
- [ ] 有 `；` 或 `.` 分隔触发段和能力段
- [ ] 能力段压缩成一行，不展开步骤
- [ ] 与其它 skill 有职责边界时已在能力段标注
- [ ] `python3 scripts/verify_skills.py` 通过

---

## 3. 自动校验

`scripts/verify_skills.py` 在启动时读取每个 skill 的 `description`，校验触发前缀合规。不合规时：

```
DESCRIPTION TRIGGER PREFIX VIOLATION: <skill-name> description must start with one of:
  - Use when ...
  - Invoke when ...
  - 用于 ... 时
  - 当 ... 时使用
got: "..."
```

校验规则不检查场景化 vs 用户行为化（这部分由人工 review 把关），只检查前缀词法。

---

## 4. 后续节（PR2 补充）

- 结构模板：3 个 SKILL.md 正文骨架（动作型 / 工作流型 / 反向提问型）
- 输入输出模板：`{{var}}` 占位符约定 + 固定输出表格模式
- 完整样例：见 `skill-patterns.md`
