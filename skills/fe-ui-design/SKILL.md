---
name: fe-ui-design
description: 当需要构建 web 组件、页面或应用界面时使用；提供设计原则、反模式约束和参考文档。
argument-hint: <页面/组件需求|设计目标>
---

# FE UI Design

构建符合设计原则的前端界面，避免 AI 生成的典型视觉问题。

## 四大基础原则

每次生成或修改 UI 时，先用这四条自检：

1. **对齐** — 每个元素都有视觉锚点。文本左对齐、元素沿网格线排列、间距对称。不要随意放置。
2. **对比** — 用 size/weight/color 的明确差异建立层次。标题和正文的大小比至少 1.5:1，差异不够 = 没有层次。
3. **一致** — 间距、颜色、字体、圆角、阴影在整个页面使用统一 token。不造新值。
4. **聚合（Proximity）** — 相关元素靠近，无关元素拉远。用距离表达分组，不依赖边框和卡片。

## Typography

→ 详细参考 [typography](refs/typography.md)

**DO**: 用 modular type scale + fluid sizing (`clamp()`) 建立字号层次
**DO**: 用字重和大小变化创造清晰的视觉层次
**DON'T**: 使用过度泛滥的字体 — Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: 用等宽字体作为"技术感"的偷懒手段
**DON'T**: 在每个标题上方放大圆角图标 — 看起来像模板

## Color

→ 详细参考 [color](refs/color.md)

**DO**: 使用 OKLCH 色彩空间（感知均匀）
**DO**: 给中性色加品牌色微调（tinted neutrals），哪怕 chroma 只有 0.01
**DON'T**: 灰色文字放在彩色背景上 — 用背景色的深色调代替
**DON'T**: 使用纯黑 #000 或纯白 #fff — 永远加一点色调
**DON'T**: 使用 AI 调色盘：cyan-on-dark、紫蓝渐变、霓虹暗底
**DON'T**: 渐变文字做"冲击力" — 装饰性而非功能性
**DON'T**: 默认暗色模式 + 发光强调色 — 不需要真正的设计决策就能"看起来酷"

## Layout & Space

→ 详细参考 [spatial](refs/spatial.md)

**DO**: 使用 4pt 基础间距系统（4, 8, 12, 16, 24, 32, 48, 64px）
**DO**: 用 varied spacing 创造节奏 — 紧密分组 + 宽松分隔
**DO**: 用 `clamp()` 做流体间距
**DON'T**: 把所有东西包在卡片里 — 不是所有内容都需要容器
**DON'T**: 卡片嵌套卡片 — 视觉噪音，扁平化层级
**DON'T**: 相同大小的卡片网格无限重复 — icon + heading + text 的模板
**DON'T**: 全部居中 — 左对齐 + 不对称布局更有设计感
**DON'T**: 到处使用相同间距 — 没有节奏的布局是单调的

## Visual Details

**DON'T**: 到处用 glassmorphism — 模糊效果、玻璃卡片、发光边框缺乏目的性
**DON'T**: 圆角元素 + 一侧粗彩色边框 — 偷懒的强调，几乎从不显得有意
**DON'T**: 用 sparkline 做装饰 — 看起来精致但不传达信息
**DON'T**: 圆角矩形 + 通用阴影 — 安全、无记忆点，典型 AI 输出
**DON'T**: 用 modal 除非真的没有更好的选择

## Motion

→ 详细参考 [motion](refs/motion.md)

**DO**: 用 exponential easing（ease-out-quart/quint/expo）做自然减速
**DO**: 对高度动画使用 `grid-template-rows` 而非直接动画 `height`
**DON'T**: 动画 layout 属性（width, height, padding, margin）— 只用 transform + opacity
**DON'T**: 使用 bounce 或 elastic easing — 过时且俗气，真实物体平滑减速

## Interaction

→ 详细参考 [interaction](refs/interaction.md)

**DO**: 每个交互元素设计 8 种状态（default/hover/focus/active/disabled/loading/error/success）
**DO**: 设计有意义的空状态 — 不只是"暂无内容"
**DON'T**: 不要把每个按钮都做成 primary — 用 ghost、text link、secondary 建立层级
**DON'T**: 重复用户已能看到的信息

## Responsive

→ 详细参考 [responsive](refs/responsive.md)

**DO**: 用 container queries 做组件级响应式
**DON'T**: 在移动端隐藏关键功能 — 适配界面，不要截肢

## UX Writing

→ 详细参考 [ux-writing](refs/ux-writing.md)

**DO**: 按钮文案用「动词 + 名词」— "保存更改" 而非 "确定"
**DO**: 错误信息回答三个问题：发生了什么？为什么？怎么修？

## AI Slop Test

**关键质量检查**：如果你把这个界面展示给人，说"AI 做的"，他们会立刻相信吗？如果会，那就是问题。

回顾上面所有 DON'T — 它们是 2024-2025 年 AI 生成作品的指纹。

## Gotchas

- 不要把 dribbble 风格装饰当成设计质量；先保证层次、对齐、一致和可用性
- 不要为了“高级感”默认上暗色、玻璃、渐变、发光；没有信息价值的视觉效果只会显得廉价
- 组件单看顺眼不代表页面成立；必须从整体节奏、信息层级和状态覆盖重新检查
- 设计约束不是只审美化输出，落地时要和可访问性、响应式、实现成本一起判断
