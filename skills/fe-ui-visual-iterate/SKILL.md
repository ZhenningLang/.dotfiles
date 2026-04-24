---
name: fe-ui-visual-iterate
description: 当需要对照参考图反复迭代 UI 视觉效果、或持续对比当前界面与目标样式差异时使用；用 agent-browser 自动截图并按固定差异表对比参考图，小步迭代直到视觉收敛。
argument-hint: <目标页面 URL|组件名|参考图路径>
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(scripts/ui-visual-capture.sh:*)
---

# UI Visual Iterate

对照参考图反复调 UI。每轮结束前必须贴截图 + 固定差异表，不允许"我觉得差不多了"。

## 核心循环

```
Declare → Capture → Diff → Change → Re-capture → 直到差异表全列"接近"
```

一轮只动 1-2 个维度，不把所有差异一次全改，避免改完不知道谁在起作用。

## 1. Declare（前置声明，不声明不进循环）

动手前必须用下表先把目标锁死：

| 字段 | 示例 | 说明 |
|---|---|---|
| 目标 URL | `https://tagent.ordo.global/campaign/xxx` | 要调的页面 |
| 组件/区域 | 表头下拉 / 侧边栏 / 某 modal | 本轮聚焦范围，其它不动 |
| 参考图 | `/Users/.../reference.png` | 用户给的样式目标 |
| Viewport | `1280x900` | 固定，避免响应式干扰 |
| 语言/主题 | `zh-CN` / `light` | i18n 和 theme 是视觉差异常见来源 |
| 认证方式 | profile / state / 无 | 参考 `agent-browser` 的 auth 选项 |
| 本轮只动 | 例：面板宽度 + 圆角 | 只挑 1-2 个维度 |

缺任何一项就问用户或读代码补齐，不要凭感觉开工。

## 2. Capture（自动截图）

用仓库脚本：

```
bash scripts/ui-visual-capture.sh <url> [out_dir] \
  [--viewport 1280x900] [--selector ".dropdown-panel"] [--wait networkidle] \
  [--profile ~/.xxx] [--state ./auth.json]
```

脚本会输出固定 Markdown 表（页面截图 / 元素截图 / DOM snapshot / meta）。把这段表原样贴进本轮报告。

## 3. Diff（固定差异表，强制输出）

看参考图 vs 当前截图，逐条填：

```markdown
## 视觉差异（Round N）

| 维度 | 参考图 | 当前 | 差异程度 | 下一步 |
|---|---|---|---|---|
| 面板宽度 | ~320px 宽松 | ~240px 偏窄 | 偏窄 | +padding / +min-width |
| 圆角 | rounded-xl 明显卡片感 | rounded 太硬 | 接近但偏硬 | rounded-xl |
| 阴影 | 柔和大面积 | 细黑线 | 偏生硬 | shadow-lg + 柔化 |
| 内边距 | p-3 宽松 | p-0.5 贴边 | 差异大 | p-3 |
| item 高度/密度 | ~40px | ~28px 太挤 | 偏密 | py-2 + leading |
| hover/checked 态 | 浅灰整行高亮 | 仅文字变色 | 差异大 | 整行 bg-gray-50 |
| 字号/字重 | text-sm 常规 | text-xs 偏小 | 偏小 | text-sm |
| 色彩 | 白底 + 浅灰边 | 白底 + 深灰边 | 边框偏重 | border-gray-200 |
| i18n 文案 | 全中文 | `AE/AR/AZ` 未翻译 | 未通过 | 走 formatter |
```

差异程度四档：`接近` / `偏小偏大/偏轻偏重` / `差异大` / `未通过（功能/i18n）`。

## 4. Change（小步改，只动 1-2 条）

挑表里优先级最高的 1-2 行改代码，**其它维度这一轮不动**。审美准则必须遵守：

- 细节规范（圆角、阴影、间距、色彩、typography、交互状态）见 `/fe-ui-design`
- 反模式（glassmorphism、纯黑白、渐变文字、卡片嵌套卡片）也在 `/fe-ui-design`

## 5. Re-capture（重新截图 + 重新填表）

改完立即再跑一次 `ui-visual-capture.sh`，贴新截图，重填差异表。

不允许跳过这一步用"我改了应该行"代替。

## 6. 停止条件

只有满足任一条件才停：

- 差异表所有维度都是 `接近`
- 用户显式说 OK / 这个状态可以
- 剩余差异是参考图本身的设计取舍（非本轮目标），转为 backlog

声称"已经接近参考图"但差异表里还有 `偏/差异大/未通过` = 不接受。

## 每轮输出模板（强制）

```markdown
## Round N

### Declare
（前置声明表）

### Capture
（ui-visual-capture.sh 输出的产物表原样贴入）

### Diff
（视觉差异表）

### Change
- 本轮只改：xxx, yyy
- 文件：`path/to/Component.tsx`（行号）
- 代码变化（核心片段，≤ 20 行）

### Next
- 本轮解决：... (参见 Diff 表)
- 还剩：... (留给 Round N+1)
```

## 与相邻 skill 的边界

| 关注点 | 去哪个 skill |
|---|---|
| 审美原则、反模式、typography/color/spacing 细则 | `/fe-ui-design` |
| 浏览器打开、点击、表单、认证、DOM 取值底层 | `/agent-browser` |
| 交付前验证（lint/test/build） | `/guard-verify` |
| 多文件视觉重构、跨组件影响面 | 先 `/think-context-map` 再回本 skill |
| 连续 2 轮差异表没收敛 | `/think-unstuck` |

本 skill 不做：像素 diff、visual regression baseline、Percy/Chromatic 的替代。那些是 CI 级工具；本 skill 是 inner-loop。

## Gotchas

- 像素 diff 对业务 UI 价值低；差异识别靠 agent 看图 + 固定维度表格
- 不固定 viewport / 语言 / 登录态，每轮截图会有系统性漂移，差异表就不可信
- 一轮改超过 2 个维度，后面很难归因谁在起作用；要克制
- hover/focus/checked 态不主动触发就截不到；`agent-browser` 需要 `hover`/`click` 后再截
- 只对着截图调样式容易漏 i18n、空状态、错误态；差异表最后一行专门留给功能性缺陷
- 对齐参考图 ≠ 好设计；参考图本身可能违反 `/fe-ui-design`，发现冲突要提醒用户
- 认证 state/profile 文件含 session token，只本地用，`.gitignore`
- 参考图可能是 dribbble 风格炫技，拿来当标准前先做一次 AI slop 自检（见 `/fe-ui-design`）

## 关联技能

- 审美细则 → `/fe-ui-design`
- 浏览器底层 → `/agent-browser`
- 迭代收敛后要交付 → `/guard-verify` → `/guard-ship`
- 视觉涉及多组件重构 → `/think-context-map` → `/dev-refactor`
- 连续 2 轮没收敛 → `/think-unstuck`
