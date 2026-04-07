---
description: 交付（PR 模式或直接发布模式）
argument-hint: <--pr|--publish> [目标分支] [--skip-review]
---

# Ship

## 1. 预检（两种模式共用）

- [ ] 所有测试通过（自动探测并运行 test 命令）
- [ ] lint/typecheck 通过
- [ ] `git status` 无意外文件
- [ ] `git diff --cached` 检查敏感信息（密钥、token、密码）

预检失败则停止，报告问题。

## 2. 解析参数

解析 `$ARGUMENTS`：

- `--pr` → PR 模式（创建 Pull Request）
- `--publish` → 直接发布模式（推送 main + 发布）
- `--skip-review` → 跳过自动 review
- 位置参数作为目标分支（留空则使用仓库默认分支）
- **未指定 `--pr` 或 `--publish` → 询问用户选择模式**

## 3. Review（可跳过）

除非 `--skip-review`，否则自动执行一次 simple review：

- 审查未提交或已提交但未推送的变更
- Critical issues → 阻断交付，要求修复
- Important/Minor → 列出但不阻断，由用户决定

---

## 模式 A：PR 模式（`--pr`）

### A1. 提交与推送

- 如有未提交变更，引导用户 commit（建议 commit message）
- `git push` 到远程

### A2. 创建 PR

- 自动生成 PR 描述：变更摘要、关键修改、测试说明
- `gh pr create --base <目标分支>`（如有 gh CLI）
- 输出 PR URL

### A3. 交付路径选择

如果用户不想创建 PR，提供备选：

| 路径 | 说明 |
|------|------|
| PR | 创建 Pull Request（默认） |
| merge | 在本地合并到目标分支，验证后再 push |
| keep | 保留当前分支，不创建 PR，不合并 |
| discard | 丢弃当前分支上的本次变更（仅在用户明确确认后） |

各路径执行方式：

- **PR**：push 当前分支 → `gh pr create --base <目标分支>`
- **merge**：切到目标分支 → 拉取最新 → 合并当前分支 → 运行验证 → push
- **keep**：只做预检和 review，保留当前分支，输出下一步建议
- **discard**：先展示将被丢弃的变更，用户明确确认后再执行回退/删分支

---

## 模式 B：直接发布模式（`--publish`）

### B1. 安全检查

- 确认当前分支是 main（或目标分支），如果不是则先合并
- `git pull --rebase` 拉取最新
- 再次运行预检确认合并后无问题

### B2. 提交与推送

- 如有未提交变更，引导用户 commit（建议 commit message）
- `git push origin main`（或目标分支）

### B3. 发布

检测项目类型，执行对应发布流程：

| 项目类型 | 检测方式 | 发布动作 |
|---------|---------|---------|
| npm | `package.json` 存在 | 提示 version bump → `npm publish` 或 `pnpm publish` |
| Python | `pyproject.toml` / `setup.py` | 提示 version bump → `python -m build && twine upload` |
| GitHub Release | `.github/` 或通用 | `gh release create` 自动生成 release notes |
| 其他 | 无法检测 | 询问用户发布方式 |

发布步骤：

1. **询问版本号**：展示当前版本，建议 patch/minor/major，等用户确认
2. **更新版本**：修改对应的版本文件
3. **创建 tag**：`git tag v{version}`
4. **推送 tag**：`git push origin v{version}`
5. **执行发布命令**：按检测到的项目类型执行
6. **创建 GitHub Release**（如有 gh CLI）：`gh release create v{version} --generate-notes`
