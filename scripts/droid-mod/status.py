#!/usr/bin/env python3
"""检查 droid 当前状态：原版/已修改/部分修改，以及 settings.json 配置"""
import json
import re
from pathlib import Path

droid = Path.home() / '.local/bin/droid'
V = rb'[A-Za-z_$][A-Za-z0-9_$]*'

with open(droid, 'rb') as f:
    data = f.read()

results = {}

# mod1: 截断条件
# 用 isTruncated 定位截断函数（不依赖混淆后的函数名）
# 原版: if(!V&&!V)return{text:V,isTruncated:!1}
# 修改: if(!0||!V)return{text:V,isTruncated:!1}
# 补偿后: ;/* ... */return{text:V,isTruncated:!1} (死代码被替换)
if b'if(!0||!' in data:
    results['mod1'] = 'modified'
elif re.search(rb'/\*\s+\*/return\{text:' + V + rb',isTruncated:!1\}', data):
    results['mod1'] = 'modified'  # comp_universal 补偿后形态
elif re.search(rb'if\(!' + V + rb'&&!' + V + rb'\)return\{text:' + V + rb',isTruncated:!1\}', data):
    results['mod1'] = 'original'
else:
    results['mod1'] = 'unknown'

# mod4: diff行数 — 两个截断路径
def _mod4_detect():
    # 路径1: gBT 文本截断 var VAR=(20|99),VAR=2000
    gbt_matches = list(re.finditer(rb'var ' + V + rb'=(20|99),' + V + rb'=2000', data))
    gbt = None
    if len(gbt_matches) == 1:
        gbt = 'modified' if int(gbt_matches[0].group(1)) == 99 else 'original'
    # 路径2: bRD viewport tier
    brd_m = re.search(rb'bRD=\{xs:\d+,sm:\d+,md:(\d+),lg:(\d+)\}', data)
    brd = None
    if brd_m:
        brd = 'modified' if int(brd_m.group(1)) >= 99 and int(brd_m.group(2)) >= 99 else 'original'
    # 只要有一个路径存在且已修改就算 modified
    states = [s for s in [gbt, brd] if s is not None]
    if not states:
        return 'unknown'
    if all(s == 'modified' for s in states):
        return 'modified'
    if any(s == 'modified' for s in states):
        return 'partial'
    return 'original'
results['mod4'] = _mod4_detect()

# mod6: Ctrl+N custom model direct cycle (v0.94+ Pz 回调)
def _mod6_detect():
    # 新版: Pz 回调直接 cycle custom models
    if b'NR().getCustomModels().map(m=>m.id)' in data and (
            b'K_(n);wh({modelId:n})' in data or b'K_(M[' in data or b'yT().setModel(M[' in data):
        return 'modified'
    # 新版原版: Pz 回调弹出 selector
    if b'S9((eA)=>!eA)},[D0])' in data or re.search(
            rb'\w+\(\(\w+\)=>!\w+\)\},\[\w+\]\)', data):
        return 'original'
    # 旧版 mod: cycleModel 中注入 customModels
    for fn_name in [b'peekNextCycleModel', b'cycleSpecModeModel']:
        pos = data.find(fn_name + b'(')
        if pos >= 0:
            region = data[pos:pos + 800]
            if b'=this.customModels.map(m=>m.id)' in region:
                return 'modified'
            if b'validateModelAccess(' in region:
                return 'original'
    return 'unknown'

results['mod6'] = _mod6_detect()

# mod7: 多行历史记录按↓修复
# 修改后: V(),!0 → spaces + !1
mod7_modified = re.search(rb'\),!0\}if\(' + V + rb'\)return\s+!1\}return!1', data)
mod7_original = re.search(rb'\),!0\}if\((' + V + rb')\)return \1\(\),!0\}return!1', data)
if mod7_modified:
    results['mod7'] = 'modified'
elif mod7_original:
    results['mod7'] = 'original'
else:
    results['mod7'] = 'unknown'

# mod8: Welcome/Header 橙色 + "Modified" 标记
welcome_mod = bool(re.search(rb'color:"#FFA500",children:"v\d+\.\d+\.\d+ Modified"', data))
header_mod = bool(re.search(rb'"v\d+\.\d+\.\d+ Modified","dim-bold"', data))
style_mod = b'"dim-bold":{color:"#FFA500"' in data
logo_mod = b'logo:{color:"#FFA500"' in data
# else 分支也需要改 — 检查是否还有未改的版本号
header_orig_remain = bool(re.search(rb',"v\d+\.\d+\.\d+","dim-bold"\)', data))
all_targets = [header_mod, style_mod, logo_mod]
if all(all_targets) and not header_orig_remain:
    results['mod8'] = 'modified'
elif any(all_targets):
    results['mod8'] = 'partial'
elif re.search(rb'dimColor:!0,children:"v\d+\.\d+\.\d+"', data) or re.search(rb',"v\d+\.\d+\.\d+","dim-bold"\)', data):
    results['mod8'] = 'original'
else:
    results['mod8'] = 'unknown'

# mod9: custom model effort 级别
# 紧凑版: 在数组末尾追加 "max" (wUT 自动映射 openai "xhigh")
if re.search(rb'supportedReasoningEfforts:\w+\?\["off","low","medium","high","max"\]:\["none"\]', data):
    results['mod9'] = 'modified'
elif re.search(rb'supportedReasoningEfforts:\w+\?\["off","low","medium","high"\]:\["none"\]', data):
    results['mod9'] = 'original'
else:
    results['mod9'] = 'unknown'

# mod10: kitty keyboard 检测超时
if re.search(rb'setTimeout\(\w+,999\)', data) and b'enableKittyProtocol' in data:
    results['mod10'] = 'modified'
elif re.search(rb'setTimeout\(\w+,200\)', data) and b'enableKittyProtocol' in data:
    results['mod10'] = 'original'
else:
    results['mod10'] = 'unknown'


# 输出
total = len(results)
mod_count = sum(1 for v in results.values() if v == 'modified')
orig_count = sum(1 for v in results.values() if v == 'original')

print(f"droid 状态:\n")
for name, status in results.items():
    icon = '✓' if status == 'modified' else '△' if status == 'partial' else '○' if status == 'original' else '?'
    label = {'modified': '已修改', 'original': '原版', 'unknown': '未知', 'partial': '部分修改'}[status]
    print(f"  {icon} {name}: {label}")

print()
if mod_count == total:
    print("结论: 已修改")
elif orig_count == total:
    print("结论: 原版")
else:
    print(f"结论: 部分修改 ({mod_count}/{total})")

# === settings.json 配置检查 ===
settings_path = Path.home() / '.factory/settings.json'
if not settings_path.exists():
    print(f"\n⚠ settings.json 不存在: {settings_path}")
else:
    try:
        cfg = json.loads(settings_path.read_text())
    except Exception as e:
        print(f"\n⚠ settings.json 解析失败: {e}")
        cfg = None

    if cfg:
        print(f"\nsettings.json 配置检查:\n")
        models = cfg.get('customModels', [])
        if not models:
            print("  ⚠ customModels 为空，未配置任何自定义模型")
        else:
            warnings = []
            for m in models:
                mid = m.get('id', '?')
                name = m.get('displayName', mid)
                provider = m.get('provider', '?')
                effort = m.get('reasoningEffort')
                extra = m.get('extraArgs', {})

                issues = []
                has_mod9 = results.get('mod9') == 'modified'

                # reasoningEffort 优先级:
                #   有值 (low/medium/high/max/xhigh) → Droid 控制，extraArgs 中的 effort 被忽略
                #   none/off → Droid 不发送 thinking/reasoning，extraArgs 接管
                # 后果: extraArgs 有 effort 时，Tab 切到 off/none 本想关闭思考，
                #       但 extraArgs 会接管并重新开启

                if provider == 'anthropic':
                    if not effort:
                        issues.append('缺少 reasoningEffort (建议 "high")')
                    thinking = extra.get('thinking', {})
                    oc = extra.get('output_config', {})
                    removable = []
                    if thinking:
                        removable.append('thinking')
                    if oc.get('effort'):
                        removable.append('output_config.effort')
                    if removable:
                        issues.append(
                            f'extraArgs 中的 {" 和 ".join(removable)} 已不需要'
                            '（Droid 内置 reasoningEffort 已接管）。'
                            '不删后果: Tab 切到 off 时 extraArgs 会接管，思考不会真正关闭')
                elif provider == 'openai':
                    if not effort:
                        issues.append('缺少 reasoningEffort (建议 "high")')
                    reasoning = extra.get('reasoning', {})
                    if reasoning:
                        keep_parts = []
                        if extra.get('text', {}).get('verbosity'):
                            keep_parts.append('text.verbosity')
                        keep_note = '，' + '、'.join(keep_parts) + ' 可保留' if keep_parts else ''
                        issues.append(
                            f'extraArgs 中的整个 reasoning 对象必须移除（包括 summary）'
                            '（responses.create 中 extraArgs 浅展开会覆盖 requestParams.reasoning，'
                            '导致 effort 字段丢失，Tab 切换 Thinking Level 完全无效'
                            + (f'；mod9 已解锁 xhigh' if has_mod9 else '') + '）'
                            + keep_note)

                icon = '✓' if not issues else '⚠'
                print(f"  {icon} {name} [{provider}]")
                if effort:
                    print(f"    reasoningEffort: {effort}")
                if extra:
                    print(f"    extraArgs: {json.dumps(extra, ensure_ascii=False)}")
                for issue in issues:
                    print(f"    ⚠ {issue}")
                    warnings.append((name, issue))

            # missionModelSettings 检查
            mission = cfg.get('missionModelSettings', {})
            model_ids = [m.get('id', '') for m in models]
            if mission:
                print(f"\n  missionModelSettings:")
                wm = mission.get('workerModel', '')
                vm = mission.get('validationWorkerModel', '')
                we = mission.get('workerReasoningEffort', '')
                ve = mission.get('validationWorkerReasoningEffort', '')
                print(f"    Worker:    {wm} ({we})" + (" ⚠ 不在 customModels 中" if wm and wm not in model_ids else ""))
                print(f"    Validator: {vm} ({ve})" + (" ⚠ 不在 customModels 中" if vm and vm not in model_ids else ""))

            if not warnings:
                print("\n  配置正常 ✓")
