#!/usr/bin/env python3
"""mod-cycle-custom-model: Ctrl+N 在 custom models 间直接切换（不弹 selector）"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

NAME = 'mod-cycle-custom-model'
STABLE_INSERT = b'=this.customModels.map(m=>m.id);'
DIRECT_CALLBACK_MARKER = (
    b'GR().getCustomModels().map((gA)=>gA.id).filter((gA)=>!gA.includes("["));'
    b'if(RR.length<=1)return;'
)
ID_LIST_CALLBACK_MARKER = b'.filter(g=>!g.includes("[")),o=VT();RR[1]&&'
STABLE_TARGETS = (
    b'peekNextCycleModel',
    b'peekNextCycleSpecModeModel',
    b'cycleSpecModeModel',
)

ORIGINAL_CALLBACK_PAT = re.compile(
    rb'(?P<prefix>(?P<cb>\w+)=(?P<react>\w+)\.useCallback\(\(\)=>\{)'
    rb'if\((?P<models>\w+)\.length<=1\)return;'
    rb'let (?P<policy>\w+)=(?P<service>\w+)\(\)\.getModelPolicy\(\);'
    rb'if\(!(?P=models)\.some\(\((?P<item>\w+)\)=>(?P<access>\w+)\((?P=item),(?P=policy)\)\.allowed\)\)return;'
    rb'(?P<toggle>\w+)\(\((?P<state>\w+)\)=>!(?P=state)\)'
    rb'\},\[(?P<dep>\w+)\]\)'
    rb'(?=,(?P<handler>\w+)=\w+\.useCallback\(async\((?P<handler_arg>\w+)\)=>\{)'
)
BROKEN_CALLBACK_PAT = re.compile(
    rb'(?P<prefix>(?P<cb>\w+)=(?P<react>\w+)\.useCallback\(\(\)=>\{)'
    rb'let (?P<br>\w+)=\w+\(\)\.peekNextCycleModel\(Y8A\(\),VT\(\)\.hasSpecModeModel\(\)\?VT\(\)\.getSpecModeModel\(\):VT\(\)\.getModel\(\)\);'
    rb'if\((?P=br)\)(?P<handler>\w+)\((?P=br)\.modelId\)'
    rb'\},\[(?P<dep>\w+)\]\)'
)
CURRENT_BROKEN_CALLBACK_PAT = re.compile(
    rb'(?P<prefix>(?P<cb>\w+)=(?P<react>\w+)\.useCallback\(\(\)=>\{)'
    rb'let (?P<br>\w+)=\w+\(\)\.peekNextCycleModel\('
    rb'(?P<dep>\w+),\w+\(\)\.hasSpecModeModel\(\)\?\w+\(\)\.getSpecModeModel\(\):null\);'
    rb'if\((?P=br)\)(?P<handler>\w+)\((?P=br)\.modelId\)'
    rb'\},\[(?P=dep)\]\)'
)


def is_direct_callback_patched(data):
    return DIRECT_CALLBACK_MARKER in data or ID_LIST_CALLBACK_MARKER in data


def revert_stable_function_patch(data):
    reverted = 0
    for fn_name in STABLE_TARGETS:
        entry_pat = re.compile(
            fn_name + rb'\((?P<param>' + V + rb')(?:,' + V + rb')?\)\{(?P=param)'
            + re.escape(STABLE_INSERT) + rb'if\((?P=param)\.length===0\)'
        )
        m_entry = entry_pat.search(data)
        if not m_entry:
            continue

        old_entry = m_entry.group(0)
        param = m_entry.group('param')
        new_entry = old_entry.replace(param + STABLE_INSERT, b'', 1)

        region_start = m_entry.start()
        region = data[region_start:region_start + 600]
        m_comment = re.search(
            rb'/\*\s*\*/(?=try\{let ' + V + rb'=PJ\((?P<loop>' + V + rb')\);)',
            region,
        )
        if not m_comment:
            raise ValueError(f"{fn_name.decode()} 稳定函数补丁回滚失败: validate 注释未找到")

        loop_var = m_comment.group('loop')
        old_check = m_comment.group(0)
        new_check = b'if(!this.validateModelAccess(' + loop_var + b').allowed)continue;'

        check_offset = region_start + m_comment.start()
        data = data[:check_offset] + new_check + data[check_offset + len(old_check):]

        entry_offset = data.find(old_entry, max(0, region_start - 10), region_start + len(old_entry) + 10)
        if entry_offset == -1:
            raise ValueError(f"{fn_name.decode()} 稳定函数补丁回滚失败: 入口未重新定位")
        data = data[:entry_offset] + new_entry + data[entry_offset + len(old_entry):]

        reverted += 1
        print(f"{fn_name.decode()}: 回滚稳定函数补丁")

    return data, reverted


def build_direct_callback(prefix, handler, dep, models_expr):
    return (
        prefix
        + b'let RR=' + models_expr + b'.filter(g=>!g.includes("[")),o=VT();'
        + b'RR[1]&&' + handler
        + b'(RR[RR.indexOf(o.hasSpecModeModel()&&o.getSpecModeModel()||o.getModel())+1]||RR[0])'
        + b'},[' + dep + b'])'
    )


def patch_callback_to_direct(data):
    if is_direct_callback_patched(data):
        print(f"{NAME} 已应用，跳过")
        return data, False

    for label, pattern in (
        ('修复当前 lw 错误回调', CURRENT_BROKEN_CALLBACK_PAT),
        ('修复旧错误回调', BROKEN_CALLBACK_PAT),
        ('替换原版 selector 回调', ORIGINAL_CALLBACK_PAT),
    ):
        m = pattern.search(data)
        if not m:
            continue
        old = m.group(0)
        models_expr = (
            m.group('models')
            if 'models' in m.groupdict() and m.group('models') is not None
            else m.group('dep')
            if label == '修复当前 lw 错误回调'
            else b'Y8A()'
        )
        new = build_direct_callback(m.group('prefix'), m.group('handler'), m.group('dep'), models_expr)
        data = data.replace(old, new, 1)
        print(f"{NAME} {label} ({len(new) - len(old):+d} bytes)")
        return data, True

    raise ValueError("Ctrl+N 回调未找到")


def main():
    data = load_droid()
    try:
        data, reverted = revert_stable_function_patch(data)
        data, patched = patch_callback_to_direct(data)
    except ValueError as exc:
        print(f"{NAME} 失败: {exc}")
        sys.exit(1)

    if not reverted and not patched:
        return

    save_droid(data)
    print(f"{NAME} 完成")


if __name__ == '__main__':
    main()
