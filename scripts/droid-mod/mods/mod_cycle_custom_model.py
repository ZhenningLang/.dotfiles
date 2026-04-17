#!/usr/bin/env python3
"""mod-cycle-custom-model: Ctrl+N 预览/切换只在 custom models 间循环

涉及三处 patch:

1. TW (关键): Ctrl+N 真正接的 3-行预览组件 NlL 的 model 列表来自
   `tw=Yd()`，Yd() 返回 factory 模型 id。把这里换成
   `tw=wR().getCustomModels().map(m=>m.id)`，Ctrl+N 预览与循环就只
   在 custom 间发生。这一处 +31 bytes（通过 mT1/iT1 的 padding 抵消）。

2. mT1 (basic ModelSelector 模态): 工厂区 header/recommended/toggle/
   hidden/customHeader 一大块压缩成只 push custom，+0 bytes，保留
   /* spaces */ padding 作为补偿区。

3. iT1 (tabbed/mission ModelSelector 模态): 同 mT1 策略，+0 bytes。

整体 net: +31 bytes；mT1+iT1 padding (~1030B) 足够在 comp_universal
里抵消本 mod 与 mod-unlock-max-custom-effort (+72B) 的总需求。

兼容性: 仅针对 v0.103.x 的 React useMemo 变量命名；升级后 regex 不中即
fail fast，不会静默跑错。脚本幂等：检测到已应用标记即跳过。
"""
import re
import sys

sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid

NAME = 'mod-cycle-custom-model'

# ---------- mT1 (basic ModelSelector) ----------
# 原始变量: JH=items, p=recommended factory, n=hidden factory, g=custom,
#           M=policy, N=expand state, K=t(i18n)
MT1_PAT = re.compile(
    rb'JH\.push\(\{type:"header",label:K\(\"common:modelSelector\.factoryModelsHeader\"\)\}\);'
    rb'let PH=p\.map\(\(UH\)=>\{let QH=fF\(UH,M\);return\{type:"model",id:UH,disabled:!QH\.allowed\}\}\),'
    rb'MH=n\.map\(\(UH\)=>\{let QH=fF\(UH,M\);return\{type:"model",id:UH,disabled:!QH\.allowed\}\}\),'
    rb'CH=g\.map\(\(UH\)=>\{let QH=fF\(UH\.id,M,UH\);return\{type:"model",id:UH\.id,disabled:!QH\.allowed\}\}\);'
    rb'if\(JH\.push\(\.\.\.PH\),n\.length>0\)JH\.push\(\{type:"toggle-builtins",expanded:N,hiddenCount:n\.length\}\);'
    rb'if\(N\)JH\.push\(\.\.\.MH\);'
    rb'if\(CH\.length>0\)JH\.push\(\{type:"sep"\}\),'
    rb'JH\.push\(\{type:"header",label:K\(\"common:modelSelector\.customModelsHeader\"\)\}\),'
    rb'JH\.push\(\.\.\.CH\);'
)
MT1_CORE = (
    b'JH.push(...g.map((UH)=>{let QH=fF(UH.id,M,UH);'
    b'return{type:"model",id:UH.id,disabled:!QH.allowed}}));'
)

# ---------- iT1 (tabbed ModelSelector, mission-aware) ----------
# 原始变量: JT=items, sH=recommended factory, rH=hidden factory, xH=custom,
#           YH=policy, kH=expand state, bH=isMissionOrchestrator
IT1_PAT = re.compile(
    rb'JT\.push\(\{type:"header",label:bH\?t\(\"common:missionModelPicker\.recommendedHeader\"\):'
    rb't\(\"common:modelSelector\.factoryModelsHeader\"\)\}\);'
    rb'let GR=sH\.map\(\(ER\)=>\{let WR=fF\(ER,YH\);return\{type:"model",id:ER,disabled:!WR\.allowed\}\}\),'
    rb'uR=rH\.map\(\(ER\)=>\{let WR=fF\(ER,YH\);return\{type:"model",id:ER,disabled:!WR\.allowed\}\}\),'
    rb'eT=xH\.map\(\(ER\)=>\{let WR=fF\(ER\.id,YH,ER\);return\{type:"model",id:ER\.id,disabled:!WR\.allowed\}\}\);'
    rb'if\(JT\.push\(\.\.\.GR\),rH\.length>0\)JT\.push\(\{type:"sep"\}\),'
    rb'JT\.push\(\{type:"toggle-builtins",expanded:kH,hiddenCount:rH\.length\}\);'
    rb'if\(kH\)JT\.push\(\.\.\.uR\);'
    rb'if\(eT\.length>0\)JT\.push\(\{type:"sep"\}\),'
    rb'JT\.push\(\{type:"header",label:t\(\"common:modelSelector\.customModelsHeader\"\)\}\),'
    rb'JT\.push\(\.\.\.eT\);'
)
IT1_CORE = (
    b'JT.push(...xH.map((ER)=>{let WR=fF(ER.id,YH,ER);'
    b'return{type:"model",id:ER.id,disabled:!WR.allowed}}));'
)

# ---------- TW (关键: Ctrl+N 预览 widget 的 model 列表来源) ----------
# 在 NlL 组件外层，tw 被定义为 tw=Yd() 后传给 availableModels=tw。
# Yd() 返回 factory 模型 id 列表；替换成 custom-only。
TW_OLD = b'tw=Yd()'
TW_NEW = b'tw=wR().getCustomModels().map(m=>m.id)'  # +31 bytes
TW_ANCHOR = b',tw=Yd(),$_=!wR().hasAnyAvailableModel(tw),'  # 唯一定位 anchor


def is_already_applied(data: bytes) -> bool:
    return MT1_CORE in data and IT1_CORE in data and TW_NEW in data


def patch_selector(data: bytes, pat: re.Pattern, core: bytes, label: str) -> bytes:
    m = pat.search(data)
    if not m:
        raise ValueError(f'{label}: pattern not found')

    old = m.group(0)
    wrapper = 4  # "/*" + "*/"
    pad_len = len(old) - len(core) - wrapper
    if pad_len < 0:
        raise ValueError(
            f'{label}: new core ({len(core)}B) + wrapper ({wrapper}B) 超过 old 长度 ({len(old)}B)'
        )

    new = core + b'/*' + b' ' * pad_len + b'*/'
    assert len(new) == len(old), (len(new), len(old))
    data = data[:m.start()] + new + data[m.end():]
    print(
        f'{NAME} {label}: {len(old)}B → core {len(core)}B + padding {pad_len}B '
        f'(+0 bytes, padding 可供 comp_universal 消费)'
    )
    return data


def patch_tw(data: bytes) -> bytes:
    """将 Ctrl+N 预览组件用的 model 列表从 factory 改为 custom-only。

    +31 bytes (不在本 patch 内部补偿，由 mT1/iT1 的 padding 统一通过
    comp_universal 抵消)。
    """
    if TW_NEW in data:
        print(f'{NAME} tw=Yd() → custom: 已应用')
        return data

    count = data.count(TW_ANCHOR)
    if count != 1:
        raise ValueError(
            f'tw=Yd() anchor match count={count}, expected 1 — droid 版本可能变了'
        )

    new_anchor = TW_ANCHOR.replace(TW_OLD, TW_NEW, 1)
    data = data.replace(TW_ANCHOR, new_anchor, 1)
    print(
        f'{NAME} tw=Yd() → custom: {len(TW_OLD)}B → {len(TW_NEW)}B '
        f'({len(TW_NEW) - len(TW_OLD):+d} bytes)'
    )
    return data


def main() -> None:
    data = load_droid()
    if is_already_applied(data):
        print(f'{NAME} 已应用，跳过')
        return

    original_size = len(data)
    try:
        # mT1 / iT1 是 +0 字节（内部 padding），先应用以便生成补偿空间
        if MT1_CORE not in data:
            data = patch_selector(data, MT1_PAT, MT1_CORE, 'mT1 (basic selector)')
        else:
            print(f'{NAME} mT1 (basic selector): 已应用')
        if IT1_CORE not in data:
            data = patch_selector(data, IT1_PAT, IT1_CORE, 'iT1 (tabbed selector)')
        else:
            print(f'{NAME} iT1 (tabbed selector): 已应用')

        # tw=Yd() → custom: +31 字节，由 comp_universal 从上面的 padding 里抵消
        data = patch_tw(data)
    except ValueError as exc:
        print(f'{NAME} 失败: {exc}')
        sys.exit(1)

    delta = len(data) - original_size
    save_droid(data)
    print(f'{NAME} 完成 ({delta:+d} bytes)')


if __name__ == '__main__':
    main()
