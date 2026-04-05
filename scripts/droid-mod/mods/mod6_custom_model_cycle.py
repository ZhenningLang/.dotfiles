#!/usr/bin/env python3
"""mod6: Ctrl+N 在 custom models 间直接切换（不弹 selector）

v0.94+ 中 Ctrl+N 改为打开 inline model selector (YD0)。
本 mod 将 Pz 回调从 toggle selector 改为直接在 customModels 间 cycle。

关键: 需同时调用 K_(switchModel) 做底层切换 + wh() 触发 UI 状态更新

锚点: useCallback + getModelPolicy + S9 toggle + ,[models_var])

字节变化: +3 bytes (139→142)
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid

data = load_droid()

# === Pz 回调 (v0.94+) ===
# 原版: 弹出 inline selector
OLD_PZ = (
    b'Pz=Z9.useCallback(()=>{'
    b'if(D0.length<=1)return;'
    b'let eT=NR().getModelPolicy();'
    b'if(!D0.some((eA)=>RZ(eA,eT).allowed))return;'
    b'S9((eA)=>!eA)'
    b'},[D0])'
)
# 新版: 直接 cycle, K_ 切换 + wh 更新 UI
NEW_PZ = (
    b'Pz=Z9.useCallback(()=>{'
    b'let M=NR().getCustomModels().map(m=>m.id),'
    b'c=yT().getModel(),'
    b'n=M[(M.indexOf(c)+1)%M.length];'
    b'K_(n);wh({modelId:n})'
    b'},[D0])'
)

if NEW_PZ in data:
    print("mod6 已应用，跳过")
    sys.exit(0)

if OLD_PZ not in data:
    pat = re.compile(
        rb'(\w+=\w+\.useCallback\(\(\)=>\{)'
        rb'if\((\w+)\.length<=1\)return;'
        rb'let \w+=NR\(\)\.getModelPolicy\(\);'
        rb'if\(!\2\.some\(\(\w+\)=>RZ\(\w+,\w+\)\.allowed\)\)return;'
        rb'(\w+)\(\(\w+\)=>!\w+\)'
        rb'\},\[\2\]\)'
    )
    m = pat.search(data)
    if not m:
        print("mod6 失败: Pz 回调未找到 (原版和模糊匹配均失败)")
        sys.exit(1)
    OLD_PZ = m.group(0)
    prefix = m.group(1)
    models_var = m.group(2)
    NEW_PZ = (
        prefix
        + b'let M=NR().getCustomModels().map(m=>m.id),'
        + b'c=yT().getModel(),'
        + b'n=M[(M.indexOf(c)+1)%M.length];'
        + b'K_(n);wh({modelId:n})'
        + b'},[' + models_var + b'])'
    )

delta = len(NEW_PZ) - len(OLD_PZ)
data = data.replace(OLD_PZ, NEW_PZ, 1)

assert NEW_PZ in data, "替换失败"
save_droid(data)
print(f"mod6 Pz 回调: selector→direct cycle ({delta:+d} bytes)")
print("mod6 完成")
