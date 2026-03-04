---
name: feishu-api
version: 2.0.0
description: |
  飞书开放平台 API 操作指南。当任务涉及飞书/Lark API 调用时使用：
  读写电子表格、文档操作、通讯录查询、消息发送、日历管理等。
  覆盖认证方式、常用 API 端点、错误处理和限流策略。
---

# 飞书 Open API 操作指南

## 快速开始：获取 Token

项目中已有 `feishu_auth.py` 模块，一行代码获取有效 token：

```python
from feishu_auth import get_user_access_token

token = get_user_access_token()
```

该函数的行为：
1. 本地有有效 token → 直接返回（无网络请求）
2. token 过期但 refresh_token 有效 → 静默刷新（需 `offline_access` 权限）
3. 无 token / 刷新失败 → 自动打开浏览器完成 OAuth 登录

Token 持久化在项目根目录 `.feishu_tokens.json`，已加入 `.gitignore`。

### 环境变量

`feishu_auth.py` 需要两个环境变量（`.env` 或 shell 环境均可）：

```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

### 发起请求

```python
import requests
from feishu_auth import get_user_access_token

token = get_user_access_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json; charset=utf-8",
}
resp = requests.get(
    "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{token}/sheets/query",
    headers=headers,
)
```

### OAuth 流程细节

- 授权 URL：`https://accounts.feishu.cn/open-apis/authen/v1/authorize`
- Token 端点：`https://open.feishu.cn/open-apis/authen/v2/oauth/token`（v2 接口）
- 回调地址：`http://localhost:9752/callback`（需在飞书开发者后台「安全设置 → 重定向 URL」中配置）
- 授权码有效期 5 分钟，只能用一次
- `scope` 参数控制 token 权限范围，按需传入（如 `sheets:spreadsheet`）
- 加上 `offline_access` scope 可获得 `refresh_token`（7 天有效），实现静默刷新

### Token 生命周期

| 凭证 | 有效期 | 过期后 |
|------|--------|--------|
| `access_token` | ~2 小时 | 用 refresh_token 刷新 |
| `refresh_token` | ~7 天 | 重新 OAuth 登录 |
| 授权许可 | 365 天 | 重新 OAuth 登录 |

### 在已有脚本中集成

替换原来手动管理 token 的方式：

```python
# 之前
self.user_access_token = os.getenv('user_access_token')

# 现在
from feishu_auth import get_user_access_token
self.user_access_token = get_user_access_token()
```

不需要手动处理 token 过期，`get_user_access_token()` 内部自动处理。

## 认证方式总览

飞书有三种 access token，按场景选用：

| Token | 场景 | 有效期 | 获取方式 |
|-------|------|--------|---------|
| `user_access_token` | 代表用户操作（推荐） | ~2h | `feishu_auth.py` 自动处理 |
| `tenant_access_token` | 应用身份调用，不涉及用户数据 | ~2h | App ID + App Secret 直接获取 |
| `app_access_token` | 应用身份凭证（较少使用） | ~2h | App ID + App Secret |

### 获取 tenant_access_token

不需要用户授权，适合后台自动化任务：

```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id": "cli_xxx", "app_secret": "xxx"}'
```

注意：tenant_access_token 只能访问应用自身权限范围内的数据，访问用户资源需要额外授权。

## 常用 API 端点

Base URL: `https://open.feishu.cn/open-apis`

### 电子表格

| 操作 | 方法 | 路径 |
|------|------|------|
| 获取 sheet 列表 | GET | `/sheets/v3/spreadsheets/{token}/sheets/query` |
| 获取 sheet 详情（含合并单元格） | GET | `/sheets/v3/spreadsheets/{token}/sheets/{sheet_id}` |
| 读取数据 | GET | `/sheets/v2/spreadsheets/{token}/values/{range}` |
| 写入数据 | PUT | `/sheets/v2/spreadsheets/{token}/values` |
| 批量写入 | POST | `/sheets/v2/spreadsheets/{token}/values_batch_update` |
| 追加数据 | POST | `/sheets/v2/spreadsheets/{token}/values_append` |

读取参数 `valueRenderOption`：
- `FormattedValue` — 格式化值（推荐默认）
- `Formula` — 公式原文（提取 HYPERLINK 等）
- `UnformattedValue` — 原始值

Range 格式：`{sheet_id}!A1:ZZ1000`

写入示例：

```python
requests.put(
    f"{BASE}/sheets/v2/spreadsheets/{spreadsheet_token}/values",
    headers=headers,
    json={
        "valueRange": {
            "range": "sheet_id!A1:B2",
            "values": [["a", "b"], ["c", "d"]]
        }
    }
)
```

### 文档

| 操作 | 方法 | 路径 |
|------|------|------|
| 获取文档元信息 | GET | `/docx/v1/documents/{document_id}` |
| 获取文档内容 | GET | `/docx/v1/documents/{document_id}/blocks` |
| 创建文档 | POST | `/docx/v1/documents` |

### 通讯录

| 操作 | 方法 | 路径 |
|------|------|------|
| 搜索用户 | POST | `/contact/v3/users/search` |
| 获取用户信息 | GET | `/contact/v3/users/{user_id}` |
| 获取部门列表 | GET | `/contact/v3/departments` |
| 通过手机/邮箱查 ID | POST | `/contact/v3/users/batch_get_id` |

### 消息

| 操作 | 方法 | 路径 |
|------|------|------|
| 发送消息 | POST | `/im/v1/messages` |
| 回复消息 | POST | `/im/v1/messages/{message_id}/reply` |
| 获取消息 | GET | `/im/v1/messages/{message_id}` |

### 多维表格 (Bitable)

| 操作 | 方法 | 路径 |
|------|------|------|
| 列出数据表 | GET | `/bitable/v1/apps/{app_token}/tables` |
| 查询记录 | POST | `/bitable/v1/apps/{app_token}/tables/{table_id}/records/search` |
| 新增记录 | POST | `/bitable/v1/apps/{app_token}/tables/{table_id}/records` |

### 云空间

| 操作 | 方法 | 路径 |
|------|------|------|
| 获取文件列表 | GET | `/drive/v1/files` |
| 获取文件元信息 | GET | `/drive/v1/metas/batch_query` |

## 错误处理

### 必须处理的错误码

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| `99991400` | 频率限制 | 读 `x-ogw-ratelimit-reset` 响应头，等待后重试 |
| `99991663` | token 无效 | 调用 `get_user_access_token()` 重新获取 |
| `99991664` | token 过期 | 同上 |
| `99991672` | 权限不足 | 检查应用权限配置 |
| `99991677` | user_access_token 过期 | `feishu_auth.py` 自动处理 |
| `99991679` | 用户未授权该 scope | 检查 OAuth 授权时的 scope 参数 |

### 其他常见错误码

| 错误码 | 含义 |
|--------|------|
| `10003` | 请求参数缺失或错误 |
| `10014` | 应用不可用（被禁用） |
| `1069902` | 无权限访问该资源 |
| `90221` | 数据过大（单批 >10MB） |

### 带自动重新认证的重试模式

```python
import time
from feishu_auth import get_user_access_token

TOKEN_EXPIRED_CODES = {99991663, 99991664, 99991677}

def feishu_request(method, url, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        token = get_user_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.request(method, url, headers=headers, **kwargs)
        data = resp.json()
        code = data.get("code", -1)

        if code == 0:
            return data
        if code == 99991400:  # 限流
            wait = int(resp.headers.get("x-ogw-ratelimit-reset", 5))
            time.sleep(wait)
            continue
        if code in TOKEN_EXPIRED_CODES:
            # 删除本地缓存，下次 get_user_access_token() 会重新获取
            from feishu_auth import TOKEN_FILE
            TOKEN_FILE.unlink(missing_ok=True)
            continue
        raise Exception(f"飞书 API 错误 {code}: {data.get('msg')}")
    raise Exception("飞书 API 重试次数超限")
```

## 限流策略

限流按 **每应用 + 每租户** 计算：

| 等级 | 限制 | 典型 API |
|------|------|---------|
| Level 4 | 1000次/分 & 50次/秒 | 大部分读接口 |
| Level 5 | 1次/秒 | 部分写接口 |
| Level 8 | 20次/秒 | 常见读接口 |

触发限流时 HTTP 429（旧版可能 400），响应体 `code: 99991400`。

响应头：
- `x-ogw-ratelimit-limit` — 窗口期限制
- `x-ogw-ratelimit-reset` — 等待秒数

并发建议：
- 读接口 5-10 QPS
- 写接口 1-3 QPS
- 批量场景用批量 API 替代循环
- 避免整点/半点集中发消息

## 电子表格操作要点

### 合并单元格

飞书 API 返回合并信息格式不统一，需兼容多种结构：
1. 调用 sheet 详情接口获取 `merges` 字段
2. 合并区域只有锚点单元格有值，其余为空
3. 纵向合并需手动填充下方空单元格

### 分批读取大表格

单次读取有行数限制：
1. 每次读取 500-1000 行
2. 通过空行比例判断是否到底（连续空行 >50%）
3. Range 示例：`sheet_id!A1:ZZ1000`，`sheet_id!A1001:ZZ2000`

### HYPERLINK 提取

超链接需额外请求 Formula 模式：
```
GET /sheets/v2/spreadsheets/{token}/values/{range}?valueRenderOption=Formula
```
解析 `=HYPERLINK("url","text")` 提取 URL。

## 注意事项

1. **Token 安全**：不要在前端或日志中暴露 token
2. **分页**：列表接口用 `page_token` + `page_size`，`has_more=true` 表示还有下一页
3. **ID 类型**：用户 ID 有 `open_id`、`union_id`、`user_id` 三种，通过 `user_id_type` 参数指定
4. **富文本**：读表格时优先用 `richTextValues` 保留超链接
5. **飞书内部链接**：`internal-api-drive-stream.feishu.cn` 开头的是内部资源 URL，通常无需处理
6. **Wiki 页面**：Wiki token 可以直接当 spreadsheet token 用于 sheets API（如果该 wiki 是电子表格）

## 参考文档

- 认证：https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/get-access-token
- OAuth v2：https://open.feishu.cn/document/authentication-management/access-token/get-user-access-token
- 刷新 token：https://open.feishu.cn/document/authentication-management/access-token/refresh-user-access-token
- 限流：https://open.feishu.cn/document/server-docs/api-call-guide/frequency-control
- 错误码：https://open.feishu.cn/document/server-docs/api-call-guide/generic-error-code
- API 列表：https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list
