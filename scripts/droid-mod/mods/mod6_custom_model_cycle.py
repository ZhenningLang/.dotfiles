#!/usr/bin/env python3
"""mod6: Ctrl+N 只在非 Copilot custom model 间切换

修改 peekNextCycleModel, cycleSpecModeModel, peekNextCycleSpecModeModel:
- 函数入口覆盖参数为 customModels ID 列表
- validateModelAccess 替换为 /\[/ 检查，跳过 ID 含 [ 的模型（Copilot 模型）

字节变化: 每个函数约 +8 bytes（注入 +33, 检查缩短 -25），总计约 +24 bytes
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

data = load_droid()
original_size = len(data)


def _find_at_or_near(data, needle, expected_offset, *, window=64, name=""):
    if expected_offset < 0:
        raise ValueError(f"{name} offset invalid: {expected_offset}")
    if data[expected_offset:expected_offset + len(needle)] == needle:
        return expected_offset

    start = max(0, expected_offset - window)
    end = min(len(data), expected_offset + window)
    idx = data.find(needle, start, end)
    if idx == -1:
        raise ValueError(f"{name} bytes not found near offset {expected_offset}")
    return idx


def patch_cycle_fn(data, fn_name, early_return):
    """覆盖参数为 customModels ID, 替换 validateModelAccess 为 /\[/ copilot 过滤

    支持单参数 fn(H) 和双参数 fn(H,A) 签名。
    """

    start_pat = (fn_name.encode() + rb'\((' + V + rb')((?:,' + V + rb')?)\)\{if\(\1\.length===0\)'
                 rb'return ' + early_return + rb';')
    m_start = re.search(start_pat, data)
    if not m_start:
        raise ValueError(f"{fn_name} 入口未找到!")
    param = m_start.group(1)
    param2 = m_start.group(2)

    region_start = m_start.start()
    check_pat = rb'if\(!this\.validateModelAccess\((' + V + rb')\)\.allowed\)continue;'
    m_check = re.search(check_pat, data[region_start:region_start + 500])
    if not m_check:
        raise ValueError(f"{fn_name} validateModelAccess 未找到!")

    check_var = m_check.group(1)

    old_start = fn_name.encode() + b'(' + param + param2 + b'){if(' + param + b'.length===0)'
    new_start = (fn_name.encode() + b'(' + param + param2 + b'){' + param +
                 b'=this.customModels.map(m=>m.id);if(' + param + b'.length===0)')
    start_extra = len(new_start) - len(old_start)

    old_check = m_check.group(0)
    new_check_core = b'if(/\\[/.test(' + check_var + b'))continue;'

    space = len(old_check) - start_extra - len(new_check_core)
    if space >= 4:
        new_check = new_check_core + b'/*' + b' ' * (space - 4) + b'*/'
    elif space >= 0:
        new_check = new_check_core + b' ' * space
    else:
        new_check = new_check_core

    net_change = (len(new_start) + len(new_check)) - (len(old_start) + len(old_check))

    start_offset = _find_at_or_near(data, old_start, m_start.start(), name=f"{fn_name} old_start")
    check_offset = _find_at_or_near(
        data, old_check, region_start + m_check.start(), name=f"{fn_name} old_check")

    data = data[:check_offset] + new_check + data[check_offset + len(old_check):]
    data = data[:start_offset] + new_start + data[start_offset + len(old_start):]

    sig = f"({param.decode()}{param2.decode()})" if param2 else f"({param.decode()})"
    print(f"{fn_name}{sig}: customModels.map (+{start_extra}), "
          f"/\\[/ check ({len(new_check_core)}B vs {len(old_check)}B), net {net_change:+d}")
    return data, net_change


total_change = 0
data, ch = patch_cycle_fn(data, 'peekNextCycleModel', rb'null')
total_change += ch
data, ch = patch_cycle_fn(data, 'cycleSpecModeModel', rb'this\.getSpecModeModel\(\)')
total_change += ch

try:
    data, ch = patch_cycle_fn(data, 'peekNextCycleSpecModeModel', rb'null')
    total_change += ch
except ValueError as e:
    print(f"peekNextCycleSpecModeModel 跳过: {e}")

assert len(data) == original_size + total_change, \
    f"大小不匹配: 期望 {original_size + total_change}, 实际 {len(data)}"
save_droid(data)
if total_change:
    print(f"mod6 完成 ({total_change:+d} bytes, 需要补偿)")
else:
    print("mod6 完成 (0 bytes)")
