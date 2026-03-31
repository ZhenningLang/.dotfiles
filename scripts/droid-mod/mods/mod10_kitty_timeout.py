#!/usr/bin/env python3
"""mod10: kitty 检测超时 200→999ms (0 bytes)

修复 iTerm2 上 kitty keyboard protocol 竞态条件:
终端响应在 input handler 就绪前到达，导致 escape sequence 泄漏到屏幕、Shift+Enter 失效。
增大超时窗口降低竞态概率。

定位策略: setTimeout(VAR,200) 后 100 字节内有 enableKittyProtocol
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

AFTER_MARKER = b'enableKittyProtocol'
PAT = rb'setTimeout\((' + V + rb'),200\)'

data = load_droid()
original_size = len(data)

# 幂等检查
for m in re.finditer(rb'setTimeout\(' + V + rb',999\)', data):
    after = data[m.end():m.end() + 100]
    if AFTER_MARKER in after:
        print("mod10 已应用，跳过")
        sys.exit(0)

# 定位: setTimeout(VAR,200) 且后 100 字节内有 enableKittyProtocol
target = None
for m in re.finditer(PAT, data):
    after = data[m.end():m.end() + 100]
    if AFTER_MARKER in after:
        target = m
        break

if not target:
    print("mod10 失败: 未找到 confirmKittySupport 中的 setTimeout")
    print("  尝试: strings ~/.local/bin/droid | grep -E 'setTimeout.*200.*kitty'")
    sys.exit(1)

old = target.group(0)
new = b'setTimeout(' + target.group(1) + b',999)'
data = data[:target.start()] + new + data[target.end():]

print(f"mod10 kitty检测超时: {old} → {new} (+0 bytes)")

if len(data) != original_size:
    print(f"警告: 大小变化 {len(data) - original_size:+d} bytes")

save_droid(data)
print("mod10 完成")
