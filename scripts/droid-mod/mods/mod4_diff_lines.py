#!/usr/bin/env python3
"""mod4: Edit diff/输出截断行数 20→99 (0 bytes)

目标: iTT() 函数的默认行数参数
  function iTT(H, T=VAR1, R=VAR2) { ... if(A.length>T) D=A.slice(0,T) ... }
  var VAR1=20, VAR2=2000

锚点: var VAR=20,VAR=2000 (值 20+2000 组合定位，不受混淆影响)
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

data = load_droid()

pat = rb'var (' + V + rb')=(20|99),(' + V + rb')=2000'
matches = list(re.finditer(pat, data))

if not matches:
    print("mod4 失败: 未找到 var VAR=20,VAR=2000 模式")
    sys.exit(1)

if len(matches) > 1:
    print(f"mod4 失败: 找到 {len(matches)} 处匹配，无法确定")
    sys.exit(1)

m = matches[0]
var_name = m.group(1)
current_val = int(m.group(2))

if current_val == 99:
    print("mod4 已应用，跳过")
    sys.exit(0)

old = m.group(0)
new = b'var ' + var_name + b'=99,' + m.group(3) + b'=2000'
data = data[:m.start()] + new + data[m.start() + len(old):]
save_droid(data)
print(f"mod4 diff行数: {var_name.decode()}=20 → {var_name.decode()}=99 (+0 bytes)")
print("mod4 完成")
