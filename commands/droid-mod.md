---
description: 修改/检查/恢复 droid 二进制
argument-hint: <status | apply | apply 1,4,8 | restore>
---

对 `~/.local/bin/droid` 二进制执行修改、状态检查或恢复。

脚本位置: `scripts/droid-mod/`

## 子命令

| 命令 | 说明 |
|------|------|
| `status` | 检查当前 droid 各 mod 的应用状态和 settings.json 配置 |
| `apply` | 应用全部 mod（自动备份 → 移除签名 → 逐个应用 → 补偿 → 签名） |
| `apply 1,4,8` | 只应用指定编号的 mod |
| `restore` | 从备份恢复原版 droid |
| `restore 0.90.0` | 恢复指定版本的备份 |
| `restore --list` | 列出所有可用备份 |

## 执行方式

脚本目录通过当前命令文件位置推算: `$(dirname $THIS_COMMAND)/../scripts/droid-mod/`，
即 `~/.dotfiles/scripts/droid-mod/`。

根据 `$ARGUMENTS` 决定子命令，默认为 `status`。

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")/../scripts/droid-mod" 2>/dev/null && pwd || echo "$HOME/.dotfiles/scripts/droid-mod")"

# status
python3 "$SCRIPT_DIR/status.py"

# apply (全部)
python3 "$SCRIPT_DIR/apply.py"

# apply (指定 mod)
python3 "$SCRIPT_DIR/apply.py" 1,4,8

# restore
python3 "$SCRIPT_DIR/restore.py"
python3 "$SCRIPT_DIR/restore.py" 0.90.0
python3 "$SCRIPT_DIR/restore.py" --list
```

## 可用 mod

| # | 说明 | 字节 |
|---|------|------|
| 1 | 命令框 "command truncated. press Ctrl+O" → 隐藏 | 0 |
| 4 | Edit diff/输出截断行数 20 → 99 | 0 |
| 6 | Ctrl+N 跳过 Copilot model（ID 含 `[` 的模型） | ~+27 |
| 7 | 多行历史按↓无法返回空输入框 → 修复 | 0 |
| 8 | Welcome 橙色 + 版本号 "Modified" 标记 | ~+54 |
| 9 | Custom model effort 完整级别（Anthropic=`max`，OpenAI=`xhigh`） | ~+72 |
| 10 | Kitty keyboard 检测超时 200→999ms | 0 |

## 规则

1. 先执行 `status` 确认当前状态再决定下一步
2. `apply` 会自动处理备份、签名、字节补偿，补偿失败会自动恢复
3. 修改后提示用户「新开一个 droid 窗口验证」
4. 不要在 droid 正在运行修改操作时中断
