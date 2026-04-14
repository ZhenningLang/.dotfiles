#!/usr/bin/env python3
"""mod-highlight-welcome-modified: Welcome/Header 页面橙色高亮

修改三个目标:
  1. dim-bold 样式 (canvas style table): 颜色改为橙色 (#FFA500)
  2. logo 样式: 颜色改为橙色 (#FFA500)

全部修改均保持 0 bytes。
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

NAME = 'mod-highlight-welcome-modified'
COLOR = b'color:"#FFA500"'
COLOR_C = COLOR + b','

data = load_droid()
total_diff = 0

# 检查是否已应用
style_done = b'"dim-bold":{color:"#FFA500"' in data
logo_done = b'logo:{color:"#FFA500"' in data

if style_done and logo_done:
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

reps = []  # (位置, 旧, 新, 名称)

# === 路径1: dim-bold 样式颜色 → 橙色 (0 bytes) ===
if not style_done:
    style_pat = re.compile(rb'"dim-bold":\{color:(' + V + rb')\.text\.secondary,')
    style_m = style_pat.search(data)
    if style_m:
        var_name = style_m.group(1)
        old_val = var_name + b'.text.secondary'
        new_val = b'"#FFA500"' + b'/' + b'*' + b' ' * (len(old_val) - 13) + b'*' + b'/'
        if len(new_val) != len(old_val):
            new_val = b'"#FFA500"' + b' ' * (len(old_val) - 9)
        style_old = b'"dim-bold":{color:' + old_val + b','
        style_new = b'"dim-bold":{color:' + new_val + b','
        pos = style_m.start()
        reps.append((pos, style_old, style_new, "dim-bold 样式"))
    else:
        print("警告: 未找到 dim-bold 样式定义")

# === 路径2: logo 样式颜色 → 橙色 (0 bytes) ===
if not logo_done:
    logo_pat = re.compile(rb'logo:\{color:(' + V + rb'\.headerLogo),')
    logo_m = logo_pat.search(data)
    if logo_m:
        old_val = logo_m.group(1)
        new_val = b'"#FFA500"' + b' ' * (len(old_val) - 9)
        logo_old = b'logo:{color:' + old_val + b','
        logo_new = b'logo:{color:' + new_val + b','
        reps.append((logo_m.start(), logo_old, logo_new, "logo 样式"))
    else:
        print("警告: 未找到 logo 样式定义")

if not reps:
    print(f"{NAME} 失败: 没有找到任何可修改的目标")
    sys.exit(1)

# 从高位到低位替换，避免偏移影响
reps.sort(key=lambda x: x[0], reverse=True)

for pos, old, new, name in reps:
    diff = len(new) - len(old)
    idx = data.find(old, max(0, pos - 10))
    if idx == -1:
        print(f"警告: {name} 未找到，跳过")
        continue
    data = data[:idx] + new + data[idx + len(old):]
    total_diff += diff
    print(f"{name}: ({diff:+d} B)")

print(f"\n总计: {total_diff:+d} bytes")
save_droid(data)
print(f"{NAME} 完成")
