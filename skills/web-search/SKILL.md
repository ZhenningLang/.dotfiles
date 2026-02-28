---
name: web-search
description: 使用 ddgr 进行网络搜索。当需要搜索网页信息、查找资料、获取最新内容时触发。替代内置 WebSearch 工具。
---

# Web Search via ddgr

内置 WebSearch 工具不可用，使用 ddgr (DuckDuckGo) 命令行工具替代。

## 使用方法

通过 Execute 工具调用 ddgr：

```bash
# 基本搜索（返回 JSON 格式，便于解析）
ddgr --json --np -n 5 "搜索关键词"

# 限定时间范围
ddgr --json --np -n 5 -t w "关键词"   # 最近一周
ddgr --json --np -n 5 -t m "关键词"   # 最近一个月
ddgr --json --np -n 5 -t y "关键词"   # 最近一年

# 限定站点
ddgr --json --np -n 5 -w github.com "关键词"

# 指定地区
ddgr --json --np -n 5 -r cn-zh "关键词"   # 中文结果
ddgr --json --np -n 5 -r us-en "关键词"   # 英文结果
```

## 参数说明

- `--json`: JSON 格式输出，便于解析
- `--np`: 非交互模式（不等待用户输入）
- `-n N`: 返回 N 条结果（最多 25）
- `-t SPAN`: 时间范围 d=天, w=周, m=月, y=年
- `-w SITE`: 限定站点
- `-r REG`: 地区，如 us-en, cn-zh
- `-x`: 显示完整 URL

## 输出格式

JSON 模式返回数组，每个元素包含：
- `title`: 标题
- `url`: 链接
- `abstract`: 摘要

## 注意事项

- 禁止使用内置 WebSearch 工具（已知不可用）
- 搜索英文关键词效果更好
- 如果需要页面详细内容，先用 ddgr 搜索获取 URL，再用 FetchUrl 获取正文
