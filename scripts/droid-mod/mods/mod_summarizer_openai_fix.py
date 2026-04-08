#!/usr/bin/env python3
"""mod-summarizer-openai-fix: summarizer compress 对 OpenAI custom model 改走 Chat Completions (+28 bytes)"""
import re
import sys

sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import V, load_droid, save_droid

NAME = "mod-summarizer-openai-fix"

data = load_droid()
original_size = len(data)

if b'provider==="openai"&&!1)return(' in data:
    print(f"{NAME} 已应用，跳过")
    sys.exit(0)

pattern = (
    rb'(provider==="openai"\)return\(await new ' + V + rb'\(\{apiKey:' + V
    + rb'\.apiKey,baseURL:' + V + rb'\.baseUrl,organization:null,project:null,defaultHeaders:'
    + V + rb'\.extraHeaders\}\)\.responses\.create\(\{model:' + V + rb',input:' + V
    + rb',store:!1,instructions:' + V + rb',max_output_tokens:' + V
    + rb'\}\)\)\.output_text;if\(' + V + rb'&&)('
    + V + rb'\.provider==="generic-chat-completion-api"\)\{)'
)

matches = list(re.finditer(pattern, data))
if not matches:
    print(f"{NAME} 失败: 未找到 summarizer openai+generic 路径")
    sys.exit(1)
if len(matches) > 1:
    print(f"警告: 找到 {len(matches)} 处匹配，使用第1处")

m = matches[0]
g1 = m.group(1)
g2 = m.group(2)

var_match = re.match(V, g2)
if not var_match:
    print(f"{NAME} 失败: 无法提取 generic 条件变量名")
    sys.exit(1)
var_name = var_match.group(0)

new_g1 = g1.replace(b'provider==="openai")', b'provider==="openai"&&!1)')
new_g2 = (
    b'(' + var_name + b'.provider==="generic-chat-completion-api"||'
    + var_name + b'.provider=="openai")){'
)

old_full = g1 + g2
new_full = new_g1 + new_g2
delta = len(new_full) - len(old_full)

assert delta == 28, f"预期 +28 bytes，实际 {delta:+d}"

data = data.replace(old_full, new_full, 1)
assert len(data) == original_size + 28, f"大小异常: {len(data) - original_size:+d} bytes"

save_droid(data)
print(f"{NAME} 完成 ({delta:+d} bytes)")
