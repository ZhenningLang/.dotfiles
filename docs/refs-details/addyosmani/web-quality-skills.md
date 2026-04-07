# addyosmani/web-quality-skills

- 上游仓库：`https://github.com/addyosmani/web-quality-skills`
- 本地路径：`/Users/zhenninglang/.dotfiles/refs/addyosmani/web-quality-skills`
- 主分类：**代码质量 / 审查 / 调试**
- 能力标签：`Lighthouse`, `Core Web Vitals`, `Accessibility`, `SEO`, `Best Practices`
- 一句话总结：面向 Web 质量审查与优化的框架无关技能仓库，围绕 Lighthouse、Core Web Vitals、WCAG 2.2、SEO 和现代最佳实践组织。

## 能力概览

- 提供 `web-quality-audit` 总审计 skill，编排 Performance、Accessibility、SEO、Best Practices 四类检查。
- 提供 `performance`、`core-web-vitals`、`accessibility`、`seo`、`best-practices` 五个专项 skill。
- 聚焦 Lighthouse / Core Web Vitals 指标阈值、性能预算、WCAG 2.2 要求与技术 SEO。
- 兼容 React、Vue、Angular、Svelte、Next.js、Nuxt、Astro 和原生 HTML 等多种栈。
- 唯一自动化脚本是 `web-quality-audit/scripts/analyze.sh`，做基础 HTML 静态检查并输出 JSON。
- `accessibility` 和 `core-web-vitals` 带独立 reference 文档，其他 skill 主要把规则直接写在 `SKILL.md`。
- README 明确声明它是非官方集合，核心资产是 markdown skill，不是大型 CLI/运行时项目。

## 资产盘点

- 6 个 skills。
- 1 个 shell 脚本。
- 3 份 reference 文档。
- 2 份 agent 指南文档（`AGENTS.md`、`CLAUDE.md`）。

## 关键文件

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `skills/web-quality-audit/SKILL.md`
- `skills/performance/SKILL.md`
- `skills/core-web-vitals/SKILL.md`
- `skills/accessibility/SKILL.md`
- `skills/seo/SKILL.md`
- `skills/best-practices/SKILL.md`
- `skills/web-quality-audit/scripts/analyze.sh`

## 备注

- 更像“Web 质量审查/优化知识库 + skill 包”，而不是通用型 agent 基础设施。
- `seo` 的范围主要是技术 SEO / 页面结构 / structured data，不覆盖完整内容策略与外链运营。
- 仓库自身无运行时依赖，`CLAUDE.md` 给出的校验方式是可选的 skill 格式验证和 markdown lint。
