#!/usr/bin/env python3
"""mod-cycle-custom-model: Ctrl+N 在 custom models 间直接切换（不弹 selector）"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid

NAME = 'mod-cycle-custom-model'

data = load_droid()

CURRENT_MARKERS = (
    b'peekNextCycleModel(Y8A(),VT().hasSpecModeModel()?VT().getSpecModeModel():VT().getModel())',
    b'if(BR)g2(BR.modelId)},[OC])',
)

if all(marker in data for marker in CURRENT_MARKERS):
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

BROKEN_MARKERS = (
    b'peekNextCycleModel(Y8A(),VT().hasSpecModeModel()?VT().getSpecModeModel():VT().getModel())',
    b'if(BR)g2(BR.modelId)},[g2])',
)

if all(marker in data for marker in BROKEN_MARKERS):
    data = data.replace(BROKEN_MARKERS[1], CURRENT_MARKERS[1], 1)
    save_droid(data)
    print(f"{NAME} 修复依赖数组: [g2] → [OC] (+0 bytes)")
    print(f"{NAME} 完成")
    sys.exit(0)

pat = re.compile(
    rb'(?P<prefix>(?P<cb>\w+)=(?P<react>\w+)\.useCallback\(\(\)=>\{)'
    rb'if\((?P<models>\w+)\.length<=1\)return;'
    rb'let (?P<policy>\w+)=(?P<service>\w+)\(\)\.getModelPolicy\(\);'
    rb'if\(!(?P=models)\.some\(\((?P<item>\w+)\)=>(?P<access>\w+)\((?P=item),(?P=policy)\)\.allowed\)\)return;'
    rb'(?P<toggle>\w+)\(\((?P<state>\w+)\)=>!(?P=state)\)'
    rb'\},\[\w+\]\)'
    rb'(?=,(?P<handler>\w+)=\w+\.useCallback\(async\((?P<handler_arg>\w+)\)=>\{)'
)
m = pat.search(data)
if not m:
    print(f"{NAME} 失败: Ctrl+N selector 回调未找到")
    sys.exit(1)

old = m.group(0)
groups = m.groupdict()
prefix = groups["prefix"]
handler = groups["handler"]
new = (
    prefix
    + b'let BR=GR().peekNextCycleModel(Y8A(),VT().hasSpecModeModel()?VT().getSpecModeModel():VT().getModel());'
    + b'if(BR)' + handler + b'(BR.modelId)'
    + b'},[' + groups["models"] + b'])'
)

delta = len(new) - len(old)
data = data.replace(old, new, 1)

assert new in data, "替换失败"
save_droid(data)
print(f"{NAME} Ctrl+N 回调: selector→direct cycle ({delta:+d} bytes)")
print(f"{NAME} 完成")
