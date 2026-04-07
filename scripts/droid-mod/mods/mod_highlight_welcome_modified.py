#!/usr/bin/env python3
"""mod-highlight-welcome-modified: Welcome/Header 页面橙色 + "Modified" 版本标记

修改三个目标:
  1. rID 函数 (旧 Welcome 页面, JSX): 文字橙色 + 版本号 "Modified"
  2. header 函数 (新 canvas header): 版本号追加 " Modified"
  3. dim-bold 样式 (canvas style table): 颜色改为橙色 (#FFA500)

路径2 产生字节增量，需要 comp_universal.py 补偿。路径3 为 0 bytes。
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
welcome_done = bool(re.search(rb'color:"#FFA500",children:"v\d+\.\d+\.\d+ Modified"', data))
header_done = bool(re.search(rb'"v\d+\.\d+\.\d+ Modified","dim-bold"', data))
style_done = b'"dim-bold":{color:"#FFA500"' in data

if welcome_done and header_done and style_done:
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

reps = []  # (位置, 旧, 新, 名称)

# === 路径1: rID 函数 (旧 Welcome 页面) ===
if not welcome_done:
    ver_m = re.search(rb'dimColor:!0,children:"(v\d+\.\d+\.\d+)"', data)
    if not ver_m:
        print("警告: 未找到 rID 版本文本 (dimColor)，可能已被移除")
    else:
        anchor = ver_m.start()
        ver = ver_m.group(1).decode()

        # 1a. Logo: bold:!0, → bold:!0,color:"orange",
        pat = re.compile(rb'(bold:!0,)(children:' + V + rb'\},void)')
        for m in pat.finditer(data):
            if 0 < anchor - m.start() < 300:
                reps.append((m.start(), m.group(0),
                              m.group(1) + COLOR_C + m.group(2), "Welcome Logo"))
                break

        # 1b. 版本: dimColor:!0 → color:"orange", + " Modified"
        old_v = ver_m.group(0)
        new_v = COLOR_C + f'children:"{ver} Modified"'.encode()
        reps.append((anchor, old_v, new_v, "Welcome 版本"))

        # 1c. 标语: italic:!0, → italic:!0,color:"orange",
        pat = re.compile(rb'(italic:!0,)(children:' + V + rb')')
        for m in pat.finditer(data):
            if 0 < m.start() - anchor < 500:
                reps.append((m.start(), m.group(0),
                              m.group(1) + COLOR_C + m.group(2), "Welcome 标语"))
                break

# === 路径2: header 函数 (新 canvas header) ===
# v0.94+ 有 if/else 两个分支都显示版本号，需要全部替换
if not header_done:
    VER = rb'v\d+\.\d+\.\d+'
    # 找所有 "vX.Y.Z","dim-bold") — 替换为 "vX.Y.Z Modified","dim-bold")
    hdr_pat = re.compile(rb'"(' + VER + rb')","dim-bold"\)')
    for m in hdr_pat.finditer(data):
        ver = m.group(1).decode()
        old = m.group(0)
        new = f'"{ver} Modified","dim-bold")'.encode()
        reps.append((m.start(), old, new, f"Header 版本 @{m.start()}"))
    # 同时替换 V("vX.Y.Z") 中的字符串（居中计算用）
    vfn_pat = re.compile(rb'V\("(' + VER + rb')"\)')
    for m in vfn_pat.finditer(data):
        ver = m.group(1).decode()
        old = m.group(0)
        new = f'V("{ver} Modified")'.encode()
        reps.append((m.start(), old, new, f"Header V() @{m.start()}"))
    if not any("Header" in r[3] for r in reps):
        print("警告: 未找到 header 版本文本")

# === 路径3: dim-bold 样式颜色 → 橙色 (0 bytes) ===
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

# === 路径4: logo 样式颜色 → 橙色 (0 bytes) ===
logo_done = b'logo:{color:"#FFA500"' in data
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
