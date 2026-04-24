#!/usr/bin/env bash
# ui-visual-capture.sh — 用 agent-browser 抓取 UI 当前快照（页面截图 + 可选元素截图 + DOM snapshot）
# 用法：
#   bash scripts/ui-visual-capture.sh <url> [out_dir] [--viewport WxH] [--selector CSS] [--wait MODE] [--profile PATH] [--state PATH]
# 输出：
#   stdout 输出固定 Markdown 表，列产物路径，给 agent 直接贴入差异报告
# 行为：
#   - 默认 out_dir=/tmp/visual-qa/<timestamp>，避免污染仓库
#   - 默认 viewport=1280x900，wait=networkidle
#   - 找不到 agent-browser 直接退出 2，并给安装提示
#   - 任何步骤失败立即退出（set -e），让上层感知

set -euo pipefail

if [[ $# -lt 1 ]]; then
  cat >&2 <<EOF
usage: $0 <url> [out_dir] [--viewport WxH] [--selector CSS] [--wait MODE] [--profile PATH] [--state PATH]

required:
  <url>         打开的目标 URL（http(s):// 或 file://）

positional:
  [out_dir]     产物目录，默认 /tmp/visual-qa/<timestamp>

options:
  --viewport    浏览器视口，默认 1280x900
  --selector    要单独截图的 CSS 选择器（如 ".dropdown-panel"），可选
  --wait        加载等待策略，默认 networkidle（agent-browser wait --load 取值）
  --profile     使用持久 profile 路径（agent-browser --profile）
  --state       使用导出的 auth state 文件（agent-browser --state）
EOF
  exit 2
fi

URL="$1"; shift

# 第二个位置参数（不是 -- 开头）当作 out_dir
OUT_DIR=""
if [[ $# -gt 0 && "$1" != --* ]]; then
  OUT_DIR="$1"; shift
fi

VIEWPORT="1280x900"
SELECTOR=""
WAIT_MODE="networkidle"
PROFILE=""
STATE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --viewport) VIEWPORT="$2"; shift 2 ;;
    --selector) SELECTOR="$2"; shift 2 ;;
    --wait)     WAIT_MODE="$2"; shift 2 ;;
    --profile)  PROFILE="$2"; shift 2 ;;
    --state)    STATE="$2"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="/tmp/visual-qa/$(date +%Y%m%d_%H%M%S)"
fi

mkdir -p "$OUT_DIR"

# 找 agent-browser（global 安装 / npx fallback）
AB=""
if command -v agent-browser >/dev/null 2>&1; then
  AB="agent-browser"
elif command -v npx >/dev/null 2>&1; then
  AB="npx -y agent-browser"
else
  cat >&2 <<EOF
ERROR: agent-browser not found.
Install: npm i -g agent-browser  |  brew install agent-browser  |  cargo install agent-browser
Then run: agent-browser install
EOF
  exit 2
fi

# 拼通用前缀（profile / state）
COMMON_FLAGS=()
[[ -n "$PROFILE" ]] && COMMON_FLAGS+=(--profile "$PROFILE")
[[ -n "$STATE"   ]] && COMMON_FLAGS+=(--state "$STATE")

PAGE_PNG="$OUT_DIR/page.png"
ELEM_PNG="$OUT_DIR/element.png"
SNAPSHOT_TXT="$OUT_DIR/snapshot.txt"
META_TXT="$OUT_DIR/meta.txt"

# 1. open + wait + viewport
$AB "${COMMON_FLAGS[@]}" open "$URL" >/dev/null
$AB "${COMMON_FLAGS[@]}" viewport "$VIEWPORT" >/dev/null 2>&1 || true   # 不是所有版本都支持
$AB "${COMMON_FLAGS[@]}" wait --load "$WAIT_MODE" >/dev/null

# 2. 整页截图
$AB "${COMMON_FLAGS[@]}" screenshot "$PAGE_PNG" >/dev/null

# 3. 可选：元素截图
ELEM_LINE=""
if [[ -n "$SELECTOR" ]]; then
  if $AB "${COMMON_FLAGS[@]}" screenshot --selector "$SELECTOR" "$ELEM_PNG" >/dev/null 2>&1; then
    ELEM_LINE="| 元素截图 (\`$SELECTOR\`) | $ELEM_PNG |"
  else
    ELEM_LINE="| 元素截图 (\`$SELECTOR\`) | _capture failed_ |"
  fi
fi

# 4. DOM snapshot
$AB "${COMMON_FLAGS[@]}" snapshot -i > "$SNAPSHOT_TXT" 2>/dev/null || \
  $AB "${COMMON_FLAGS[@]}" snapshot > "$SNAPSHOT_TXT" 2>/dev/null || \
  echo "(snapshot unavailable)" > "$SNAPSHOT_TXT"

# 5. meta
{
  echo "url=$URL"
  echo "viewport=$VIEWPORT"
  echo "wait=$WAIT_MODE"
  echo "selector=${SELECTOR:-<none>}"
  echo "profile=${PROFILE:-<none>}"
  echo "state=${STATE:-<none>}"
  echo "captured_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$META_TXT"

# 输出 Markdown 表
cat <<EOF
## 视觉快照产物

| 产物 | 路径 |
|---|---|
| 页面截图 | $PAGE_PNG |
${ELEM_LINE:+$ELEM_LINE
}| DOM snapshot | $SNAPSHOT_TXT |
| 元数据 | $META_TXT |

- url: \`$URL\`
- viewport: \`$VIEWPORT\`
- wait: \`$WAIT_MODE\`
- selector: \`${SELECTOR:-<none>}\`
EOF
