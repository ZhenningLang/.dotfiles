#!/usr/bin/env python3
"""mod-unlock-max-custom-effort: custom model 支持完整 effort 级别 (+6 bytes/处)

问题: custom model 硬编码 supportedReasoningEfforts 为 ["off","low","medium","high"]，
缺少 "max" 级别 (anthropic 的最高级, openai 由 wUT() 自动映射为 "xhigh")。

修改: 在数组末尾追加 "max":
  ["off","low","medium","high"] → ["off","low","medium","high","max"]

wUT() 内置 "max"→"xhigh" 映射，因此 openai 自动正确。
"""
import sys
import re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

NAME = 'mod-unlock-max-custom-effort'

data = load_droid()

OLD = b'["off","low","medium","high"]'
NEW = b'["off","low","medium","high","max"]'

PAT_MOD = re.compile(
    rb'supportedReasoningEfforts:' + V + rb'\?' + re.escape(NEW) + rb':\["none"\]'
)
PAT = re.compile(
    rb'supportedReasoningEfforts:' + V + rb'\?' + re.escape(OLD) + rb':\["none"\]'
)

if PAT_MOD.search(data) and not PAT.search(data):
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

matches = list(PAT.finditer(data))
if not matches:
    print("错误: supportedReasoningEfforts effort 列表未找到")
    sys.exit(1)

total_diff = 0
for m in reversed(matches):
    old = m.group(0)
    new = old.replace(OLD, NEW, 1)
    data = data[:m.start()] + new + data[m.end():]
    diff = len(new) - len(old)
    total_diff += diff

print(f"{NAME}: 共修改 {len(matches)} 处 ({total_diff:+d} bytes)")
save_droid(data)
