#!/usr/bin/env python3
"""mod-expand-diff-lines: Edit diff/输出截断行数 → 99 (0 bytes)

两个截断路径:
  1. gBT 文本截断: var VAR=20,VAR=2000 (旧版，v0.93 及以前)
  2. bRD viewport tier 截断: bRD={xs:N,sm:N,md:N,lg:N} (v0.94+)

两个都尝试修改，适配新旧版本。
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

NAME = 'mod-expand-diff-lines'

data = load_droid()
changed = False

# === 路径1: gBT 文本截断 var VAR=20,VAR=2000 ===
pat1 = rb'var (' + V + rb')=(20|99),(' + V + rb')=2000'
matches1 = list(re.finditer(pat1, data))
if len(matches1) == 1:
    m = matches1[0]
    if int(m.group(2)) == 20:
        old = m.group(0)
        new = b'var ' + m.group(1) + b'=99,' + m.group(3) + b'=2000'
        data = data[:m.start()] + new + data[m.start() + len(old):]
        print(f"gBT 文本截断: {m.group(1).decode()}=20 → 99 (+0 bytes)")
        changed = True
    else:
        print("gBT 文本截断: 已是 99，跳过")
elif not matches1:
    print("gBT 文本截断: 未找到（可能已移除），跳过")
else:
    print(f"gBT 文本截断: 找到 {len(matches1)} 处，跳过")

# === 路径2: bRD viewport tier 截断 ===
pat2 = re.compile(rb'bRD=\{xs:(\d+),sm:(\d+),md:(\d+),lg:(\d+)\}')
m2 = pat2.search(data)
if m2:
    md_val, lg_val = int(m2.group(3)), int(m2.group(4))
    if md_val < 99 or lg_val < 99:
        old = m2.group(0)
        new = (b'bRD={xs:' + m2.group(1) + b',sm:' + m2.group(2) +
               b',md:99,lg:99}')
        assert len(new) == len(old), f"长度不匹配: {len(old)} vs {len(new)}"
        data = data[:m2.start()] + new + data[m2.start() + len(old):]
        print(f"bRD viewport: md:{md_val}→99, lg:{lg_val}→99 (+0 bytes)")
        changed = True
    else:
        print("bRD viewport: 已是 99，跳过")
else:
    print("bRD viewport: 未找到，跳过")

if not changed:
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

save_droid(data)
print(f"{NAME} 完成")
