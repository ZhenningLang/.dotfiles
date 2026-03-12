#!/usr/bin/env python3
"""mod4: diff显示行数 20→99 行 (0 bytes)

支持两种模式:
  legacy:  var VAR=20,VAR2,   (后跟裸变量声明)
  v0.73+:  var VAR=20,VAR2="  (后跟字符串赋值, near "\\u23BF Interrupted")
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

data = load_droid()
original_size = len(data)

# 锚点: "\u23BF Interrupted" (比 "Interrupted" 更精确, 避免误匹配)
int_pos = data.find(b'\\u23BF Interrupted')

# 检查是否已应用
if int_pos > 0:
    region = data[max(0, int_pos - 200):int_pos]
    if re.search(rb'var ' + V + rb'=99,', region):
        print("mod4 已应用，跳过")
        sys.exit(0)

# 策略1: v0.73+ — var VAR=20, near "\u23BF Interrupted"
if int_pos > 0:
    region = data[max(0, int_pos - 200):int_pos]
    m = re.search(rb'var (' + V + rb')=20,', region)
    if m:
        abs_pos = max(0, int_pos - 200) + m.start()
        old = b'var ' + m.group(1) + b'=20,'
        new = b'var ' + m.group(1) + b'=99,'
        data = data[:abs_pos] + new + data[abs_pos + len(old):]
        save_droid(data)
        print(f"mod4 diff行数: {old} → {new} (+0 bytes, v0.73+)")
        print("mod4 完成")
        sys.exit(0)

# 策略2: legacy — var VAR=20,VAR2, (后跟裸变量声明)
legacy_pat = rb'var (' + V + rb')=20,(' + V + rb'),'
match = re.search(legacy_pat, data)
if match:
    old = match.group(0)
    new = b'var ' + match.group(1) + b'=99,' + match.group(2) + b','
    data = data.replace(old, new, 1)
    if len(data) != original_size:
        print(f"警告: 大小变化 {len(data) - original_size:+d} bytes")
    save_droid(data)
    print(f"mod4 diff行数: {old} → {new} (+0 bytes, legacy)")
    print("mod4 完成")
    sys.exit(0)

print("mod4 失败: 未找到 diff 行数配置")
print("  尝试: strings ~/.local/bin/droid | grep -E 'var [A-Za-z]+=20,'")
sys.exit(1)
