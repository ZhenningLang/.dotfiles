#!/usr/bin/env python3
"""mod3: 输出预览行数 → 99 行 (同时解决 mod5)

支持两种模式:
  legacy:  VAR=4,VAR2=5,VAR3=200  → VAR=99,...  (+1 byte, 需要补偿)
  v0.73+:  VAR=VAR2?8:4 (near exec-preview) → VAR=99||4  (+0 bytes)
"""
import sys
import re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

data = load_droid()

# 检查是否已应用
if b'=99||4' in data or re.search(V + rb'=99,' + V + rb'=5,' + V + rb'=200', data):
    print("mod3 已应用，跳过")
    sys.exit(0)

# 策略1: v0.73+ 模式 — VAR=VAR2?8:4 (near exec-preview, ternary)
ep_pos = data.find(b'exec-preview')
ternary_pat = re.compile(rb'(' + V + rb')=(' + V + rb')\?8:4')
if ep_pos > 0:
    for m in ternary_pat.finditer(data):
        dist = ep_pos - m.start()
        if 0 < dist < 3000:
            old = m.group(0)
            new = m.group(1) + b'=99||4'
            data = data[:m.start()] + new + data[m.end():]
            save_droid(data)
            print(f"mod3 输出行数: {old} → {new} (+0 bytes)")
            print("mod3 完成 (v0.73+ 模式, 同时解决 mod5)")
            sys.exit(0)

# 策略2: legacy 模式 — VAR=4,VAR2=5,VAR3=200
legacy_pat = rb'(' + V + rb')=4,(' + V + rb')=5,(' + V + rb')=200'
match = re.search(legacy_pat, data)
if match:
    var1, var2, var3 = match.group(1), match.group(2), match.group(3)
    old = match.group(0)
    new = var1 + b'=99,' + var2 + b'=5,' + var3 + b'=200'
    data = data.replace(old, new, 1)
    save_droid(data)
    print(f"mod3 输出行数: {var1.decode()}=4 → {var1.decode()}=99 (+1 byte)")
    print("mod3 完成 (legacy 模式, 同时解决 mod5, 需要补偿 -1 byte)")
    sys.exit(0)

print("mod3 失败: 未找到输出行数配置")
print("  尝试: strings ~/.local/bin/droid | grep exec-preview")
sys.exit(1)
