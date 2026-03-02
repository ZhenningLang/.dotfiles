---
name: sync-upstream
description: 同步 upstream 仓库更新到当前 fork。当用户提到同步/合并 upstream、拉取上游更新时触发。
---

# Sync Upstream

将 upstream 仓库的更新 rebase 合并到当前 fork。

## 配置

| 项 | 值 |
|---|---|
| origin | 用户的 fork（push/pull） |
| upstream | `https://github.com/notdp/.dotfiles`（只 fetch） |

## 执行流程

### 1. 检查 upstream remote

```bash
cd ~/.dotfiles
git remote -v
```

如果没有 upstream remote：

```bash
git remote add upstream https://github.com/notdp/.dotfiles
```

### 2. Fetch upstream

```bash
git fetch upstream
```

### 3. 分析分叉状态

```bash
# merge-base
BASE=$(git merge-base HEAD upstream/main)

# 本地独有提交
echo "=== 本地提交 ==="
git log --oneline $BASE..HEAD

# upstream 新提交
echo "=== Upstream 新提交 ==="
git log --oneline $BASE..upstream/main

# 预测冲突文件
echo "=== 两边都修改的文件 ==="
comm -12 <(git diff --name-only $BASE..HEAD | sort) <(git diff --name-only $BASE..upstream/main | sort)
```

**展示分析报告给用户，确认后继续。**

### 4. Rebase

```bash
git rebase upstream/main
```

### 5. 冲突解决策略

冲突类型及处理方式：

| 类型 | 处理 |
|---|---|
| DU（upstream 删除，本地修改）| 通常 `git rm`，跟随 upstream |
| UU（双方修改）| 对比内容，优先 upstream 结构，保留本地独有功能 |
| AA（双方新增）| 对比内容，如果是同一功能取更完善的版本 |

**核心原则**：upstream 提供基础结构，本地提交是个性化定制（如颜色偏好、额外配置）。

逐文件解决后：

```bash
git add <resolved-files>
git rebase --continue
```

### 6. Push

```bash
git push --force-with-lease origin main
```

## 回滚

如果 rebase 出问题：

```bash
git rebase --abort
```

如果已 push 但想回退：

```bash
git reflog  # 找到 rebase 前的 commit
git reset --hard <commit>
git push --force-with-lease origin main
```
