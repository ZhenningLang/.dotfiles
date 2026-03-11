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

# mod2: 命令阈值
if b'command.length>99' in data:
    results['mod2'] = 'modified'
elif b'command.length>50' in data:
    results['mod2'] = 'original'
else:
    results['mod2'] = 'unknown'

# mod3+mod5: 输出行数 (VAR=4/99,VAR2=5,VAR3=200)
if re.search(V + rb'=99,' + V + rb'=5,' + V + rb'=200', data):
    results['mod3'] = 'modified'
    results['mod5'] = 'modified'
elif re.search(V + rb'=4,' + V + rb'=5,' + V + rb'=200', data):
    results['mod3'] = 'original'
    results['mod5'] = 'original'
else:
    results['mod3'] = 'unknown'
    results['mod5'] = 'unknown'

# mod4: diff行数
if re.search(rb'var ' + V + rb'=99,' + V + rb',', data):
    results['mod4'] = 'modified'
elif re.search(rb'var ' + V + rb'=20,' + V + rb',', data):
    results['mod4'] = 'original'
else:
    results['mod4'] = 'unknown'

# mod6: custom model cycle (容错版, 支持单/双参数签名)
def _mod6_detect():
    for fn_name in [b'peekNextCycleModel', b'cycleSpecModeModel', b'peekNextCycleSpecModeModel']:
        for m in re.finditer(fn_name + rb'\(' + V + rb'(?:,' + V + rb')?\)\{', data):
            region = data[m.start():m.start() + 800]
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

# mod8: Welcome 页面橙色 + "Modified" 标记
if re.search(rb'color:"#FFA500",children:"v\d+\.\d+\.\d+ Modified"', data):
    results['mod8'] = 'modified'
elif re.search(rb'dimColor:!0,children:"v\d+\.\d+\.\d+"', data):
    results['mod8'] = 'original'
else:
    results['mod8'] = 'unknown'

# mod9: custom model effort 级别
if b'T.provider=="openai"' in data and b'["off","low","medium","high","max"]' in data:
    results['mod9'] = 'modified'
elif b'supportedReasoningEfforts:L?["off","low","medium","high"]:["none"]' in data:
    results['mod9'] = 'original'
else:
    results['mod9'] = 'unknown'



# 输出
total = 9
mod_count = sum(1 for v in results.values() if v == 'modified')
orig_count = sum(1 for v in results.values() if v == 'original')

print(f"droid 状态:\n")
for name, status in results.items():
    icon = '✓' if status == 'modified' else '○' if status == 'original' else '?'
    label = {'modified': '已修改', 'original': '原版', 'unknown': '未知'}[status]
    note = ' (由 mod3 控制)' if name == 'mod5' else ''
    print(f"  {icon} {name}: {label}{note}")

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
