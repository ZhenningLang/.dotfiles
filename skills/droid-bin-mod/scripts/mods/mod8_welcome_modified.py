#!/usr/bin/env python3
"""mod8: Welcome/Header 页面橙色 + "Modified" 版本标记

修改三个目标:
  1. rID 函数 (旧 Welcome 页面, JSX): 文字橙色 + 版本号 "Modified"
  2. header 函数 (新 canvas header): 版本号追加 " Modified"
  3. dim-bold 样式 (canvas style table): 颜色改为橙色 (#FFA500)

路径2 产生字节增量，需要 comp_universal.py 补偿。路径3 为 0 bytes。
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

COLOR = b'color:"#FFA500"'
COLOR_C = COLOR + b','

data = load_droid()
total_diff = 0

# 检查是否已应用
welcome_done = bool(re.search(rb'color:"#FFA500",children:"v\d+\.\d+\.\d+ Modified"', data))
header_done = bool(re.search(rb'"v\d+\.\d+\.\d+ Modified","dim-bold"', data))
style_done = b'"dim-bold":{color:"#FFA500"' in data

if welcome_done and header_done and style_done:
    print("mod8 已应用，跳过")
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
if not header_done:
    hdr_m = re.search(rb'V\("(v\d+\.\d+\.\d+)"\),"(v\d+\.\d+\.\d+)","dim-bold"\)', data)
    if not hdr_m:
        print("警告: 未找到 header 版本文本")
    else:
        ver = hdr_m.group(1).decode()
        old = hdr_m.group(0)
        new = f'V("{ver} Modified"),"{ver} Modified","dim-bold")'.encode()
        reps.append((hdr_m.start(), old, new, "Header 版本"))

# === 路径3: dim-bold 样式颜色 → 橙色 (0 bytes) ===
if not style_done:
    # UH.text.secondary (17B) → "#FFA500"/*    */ (17B), 0 bytes 变化
    style_old = b'"dim-bold":{color:UH.text.secondary,'
    style_new = b'"dim-bold":{color:"#FFA500"/*    */,'
    if style_old in data:
        pos = data.find(style_old)
        reps.append((pos, style_old, style_new, "dim-bold 样式"))
    else:
        print("警告: 未找到 dim-bold 样式定义")

if not reps:
    print("mod8 失败: 没有找到任何可修改的目标")
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
print("mod8 完成")
