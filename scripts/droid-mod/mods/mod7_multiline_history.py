#!/usr/bin/env python3
"""mod7: 修复多行历史记录按↓无法返回空输入框 (0 bytes)

问题: _T 函数中，多行文本最后一行按↓调用 onDownArrowAtBottom 并返回 true，
     拦截了外层 handler 的历史导航 (navigateNext)。
修复: 将 V(),!0 替换为等长 (spaces)!1，使 _T 返回 false，让外层处理。
"""
import sys
import re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, replace_one, V

data = load_droid()
original_size = len(data)

modified_pat = rb'\),!0\}if\(' + V + rb'\)return\s+!1\}return!1'
if re.search(modified_pat, data):
    print("mod7 已应用，跳过")
    sys.exit(0)

# Pattern: ),!0}if(V)return V(),!0}return!1
# Replace:                  ^^^^^ → spaces + !1
data, _ = replace_one(
    data,
    rb'\),!0\}if\((' + V + rb')\)return \1\(\),!0\}return!1',
    lambda m: b'),!0}if(' + m.group(1) + b')return ' + b' ' * (len(m.group(1)) + 3) + b'!1}return!1',
    'mod7 多行历史')

if len(data) != original_size:
    print(f"警告: 大小变化 {len(data) - original_size:+d} bytes")

save_droid(data)
print("mod7 完成")
