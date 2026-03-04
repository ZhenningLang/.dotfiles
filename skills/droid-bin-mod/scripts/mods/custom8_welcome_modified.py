#!/usr/bin/env python3
"""custom8: Welcome 页面橙色 + "Modified" 版本标记 (+65 bytes)

全部欢迎页文字 → 橙色 (hex #FFA500)
版本号 → "vX.Y.Z Modified"

+65 bytes，需要 comp_universal.py 补偿。
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

COLOR = b'color:"#FFA500"'
COLOR_C = COLOR + b','

data = load_droid()
total_diff = 0

if re.search(rb'color:"#FFA500",children:"v\d+\.\d+\.\d+ Modified"', data):
    print("custom8 已应用，跳过")
    sys.exit(0)

# 锚点: 版本文本 (唯一，含硬编码版本号)
ver_m = re.search(rb'dimColor:!0,children:"(v\d+\.\d+\.\d+)"', data)
if not ver_m:
    print("custom8 失败: 未找到版本文本")
    sys.exit(1)
anchor = ver_m.start()
ver = ver_m.group(1).decode()

reps = []  # (位置, 旧, 新, 名称)

# 1. Logo (锚点前 ~100B): bold:!0, → bold:!0,color:"orange",
pat = re.compile(rb'(bold:!0,)(children:' + V + rb'\},void)')
for m in pat.finditer(data):
    if 0 < anchor - m.start() < 300:
        reps.append((m.start(), m.group(0),
                      m.group(1) + COLOR_C + m.group(2), "Logo"))
        break

# 2. 版本: dimColor:!0 → color:"orange", 加 " Modified"
old_v = ver_m.group(0)
new_v = COLOR_C + f'children:"{ver} Modified"'.encode()
reps.append((anchor, old_v, new_v, "版本"))

# 3. 标语 (锚点后 ~160B): italic:!0, → italic:!0,color:"orange",
pat = re.compile(rb'(italic:!0,)(children:' + V + rb')')
for m in pat.finditer(data):
    if 0 < m.start() - anchor < 500:
        reps.append((m.start(), m.group(0),
                      m.group(1) + COLOR_C + m.group(2), "标语"))
        break

# 4. 操作提示 (锚点后 ~290B): {children:VAR} → {color:"orange",children:VAR}
pat = re.compile(rb'\.jsxDEV\(' + V + rb',\{(children:' + V + rb')\},void')
for m in pat.finditer(data):
    if 200 < m.start() - anchor < 800:
        old = m.group(0)
        new = old.replace(b'{' + m.group(1), b'{' + COLOR_C + m.group(1), 1)
        reps.append((m.start(), old, new, "提示"))
        break

# 5. 文件夹 (锚点后 ~440B): dimColor:!0 → color:"orange"
pat = re.compile(rb'(dimColor:!0)(,children:\["Current folder: ")')
m = pat.search(data)
if m and 0 < m.start() - anchor < 1000:
    reps.append((m.start(), m.group(0), COLOR + m.group(2), "文件夹"))

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
print("custom8 完成")
