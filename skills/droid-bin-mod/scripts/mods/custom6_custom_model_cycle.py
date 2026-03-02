#!/usr/bin/env python3
"""custom6: [替代 mod6] Ctrl+N 只在 custom model 间切换 (0 bytes)

与 mod6 功能相同，实现不同:
- 使用 _find_at_or_near 容错定位
- 通过 early_return 参数适配不同函数签名
- 支持双参数 fn(H,A) 签名 (v0.62.1+)
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
    """通用修改: 在函数入口覆盖参数为 customModels, 移除 validateModelAccess

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

    old_start = fn_name.encode() + b'(' + param + param2 + b'){if(' + param + b'.length===0)'
    new_start = (fn_name.encode() + b'(' + param + param2 + b'){' + param +
                 b'=this.customModels.map(m=>m.id);if(' + param + b'.length===0)')
    extra = len(new_start) - len(old_start)

    old_check = m_check.group(0)
    pad = len(old_check) - extra
    if pad < 4:
        raise ValueError(f"{fn_name} 填充空间不足: {pad} < 4")
    new_check = b'/*' + b' ' * (pad - 4) + b'*/'

    assert len(old_start) + len(old_check) == len(new_start) + len(new_check), \
        f"字节不匹配: {len(old_start)}+{len(old_check)} != {len(new_start)}+{len(new_check)}"

    start_offset = _find_at_or_near(data, old_start, m_start.start(), name=f"{fn_name} old_start")
    check_offset = _find_at_or_near(
        data, old_check, region_start + m_check.start(), name=f"{fn_name} old_check")

    data = data[:check_offset] + new_check + data[check_offset + len(old_check):]
    data = data[:start_offset] + new_start + data[start_offset + len(old_start):]

    sig = f"({param.decode()}{param2.decode()})" if param2 else f"({param.decode()})"
    print(f"{fn_name}{sig}: {param.decode()}=this.customModels... (+{extra}), "
          f"validateModelAccess → comment (-{extra}), net 0 bytes")
    return data


data = patch_cycle_fn(data, 'peekNextCycleModel', rb'null')
data = patch_cycle_fn(data, 'cycleSpecModeModel', rb'this\.getSpecModeModel\(\)')

try:
    data = patch_cycle_fn(data, 'peekNextCycleSpecModeModel', rb'null')
except ValueError as e:
    print(f"peekNextCycleSpecModeModel 跳过: {e}")

assert len(data) == original_size, f"大小变化 {len(data) - original_size:+d}"
save_droid(data)
print("custom6 完成")
