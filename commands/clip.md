---
description: 复制内容到系统剪贴板
argument-hint: <要复制的内容>
---

将给定内容复制到系统剪贴板。

## 适用场景

- 需要把命令输出、片段文本、URL 或多行内容快速放入剪贴板
- 后续要粘贴到浏览器、编辑器、聊天窗口或其他外部工具

## 命令

- macOS: `printf '%s' 'content' | pbcopy`
- Linux: `printf '%s' 'content' | xclip -selection clipboard`
- Windows: `printf '%s' 'content' | clip`

## 规则

1. 直接执行复制命令，不要只把内容打印出来
2. 使用 `printf '%s'` 而不是 `echo`，避免多出换行
3. 多行内容或特殊字符优先用 heredoc：

   ```bash
   pbcopy <<'EOF'
   content here
   EOF
   ```

4. 执行后明确确认：`Copied`
5. 不要改写原始内容
