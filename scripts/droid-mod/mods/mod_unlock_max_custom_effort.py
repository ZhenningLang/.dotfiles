#!/usr/bin/env python3
"""mod-unlock-max-custom-effort: custom model 解锁完整 effort 级别 (+72 bytes)"""
import re
import sys

sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

NAME = 'mod-unlock-max-custom-effort'

data = load_droid()

FIRST_CONTEXT = (
    rb'id:(?P<ref>' + V + rb')\.id,displayName:(?P=ref)\.displayName,shortDisplayName:(?P=ref)\.displayName,'
    rb'modelProvider:(?P=ref)\.provider,'
)
SECOND_CONTEXT = (
    rb'id:(?P<ref>' + V + rb')\.model,modelProvider:(?P=ref)\.provider,displayName:(?P<name>' + V + rb'),'
    rb'shortDisplayName:(?P=name),'
)
ORIGINAL_EXPR = rb'supportedReasoningEfforts:(?P<cond>' + V + rb')\?\["off","low","medium","high"\]:\["none"\],defaultReasoningEffort:(?P=ref)\.reasoningEffort'
MAX_ONLY_EXPR = rb'supportedReasoningEfforts:(?P<cond>' + V + rb')\?\["off","low","medium","high","max"\]:\["none"\],defaultReasoningEffort:(?P=ref)\.reasoningEffort'
PROVIDER_EXPR = (
    rb'supportedReasoningEfforts:(?P<cond>' + V + rb')\?(?P=ref)\.provider=="openai"\?'
    rb'\["none","low","medium","high","xhigh"\]:\["off","low","medium","high","max"\]:\["none"\],'
    rb'defaultReasoningEffort:(?P=ref)\.reasoningEffort'
)

FIRST_PATTERNS = {
    'original': re.compile(FIRST_CONTEXT + rb'(?P<expr>' + ORIGINAL_EXPR + rb')'),
    'max-only': re.compile(FIRST_CONTEXT + rb'(?P<expr>' + MAX_ONLY_EXPR + rb')'),
    'provider-aware': re.compile(FIRST_CONTEXT + rb'(?P<expr>' + PROVIDER_EXPR + rb')'),
}
SECOND_PATTERNS = {
    'original': re.compile(SECOND_CONTEXT + rb'(?P<expr>' + ORIGINAL_EXPR + rb')'),
    'max-only': re.compile(SECOND_CONTEXT + rb'(?P<expr>' + MAX_ONLY_EXPR + rb')'),
    'provider-aware': re.compile(SECOND_CONTEXT + rb'(?P<expr>' + PROVIDER_EXPR + rb')'),
}


def build_provider_aware(cond_var: bytes, ref_var: bytes) -> bytes:
    cond = cond_var.decode()
    ref = ref_var.decode()
    return (
        f'supportedReasoningEfforts:{cond}?{ref}.provider=="openai"?'
        f'["none","low","medium","high","xhigh"]:["off","low","medium","high","max"]:["none"],'
        f'defaultReasoningEffort:{ref}.reasoningEffort'
    ).encode()


def build_max_only(cond_var: bytes, ref_var: bytes) -> bytes:
    cond = cond_var.decode()
    ref = ref_var.decode()
    return (
        f'supportedReasoningEfforts:{cond}?["off","low","medium","high","max"]:["none"],'
        f'defaultReasoningEffort:{ref}.reasoningEffort'
    ).encode()


def find_case(patterns):
    for label, pattern in patterns.items():
        match = pattern.search(data)
        if match:
            return label, match
    return None, None


first_label, first_match = find_case(FIRST_PATTERNS)
second_label, second_match = find_case(SECOND_PATTERNS)

if first_label == 'provider-aware' and second_label == 'max-only':
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

if not first_match or not second_match:
    print("错误: custom model effort 列表未找到")
    sys.exit(1)

replacements = [
    (
        first_match.start('expr'),
        first_match.end('expr'),
        first_match.group('expr'),
        build_provider_aware(first_match.group('cond'), first_match.group('ref')),
        f'列表路径: {first_label} → provider-aware',
    ),
    (
        second_match.start('expr'),
        second_match.end('expr'),
        second_match.group('expr'),
        build_max_only(second_match.group('cond'), second_match.group('ref')),
        f'当前模型路径: {second_label} → max-only',
    ),
]

total_diff = 0
for start, end, old, new, label in sorted(replacements, key=lambda item: item[0], reverse=True):
    data = data[:start] + new + data[end:]
    diff = len(new) - len(old)
    total_diff += diff
    print(f"{NAME} {label} ({diff:+d} bytes)")

print(f"{NAME}: 共修改 {len(replacements)} 处 ({total_diff:+d} bytes)")
save_droid(data)
