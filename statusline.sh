#!/bin/bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
CWD=$(echo "$input" | jq -r '.cwd')
SID=$(echo "$input" | jq -r '.session_id // empty')
SHORT_SID="${SID:0:8}"
IS_CC=$(echo "$input" | jq -e '.context_window' >/dev/null 2>&1 && echo 1 || echo 0)

SHORT_CWD="${CWD/#$HOME/~}"
COLS=$(stty size </dev/tty 2>/dev/null | awk '{print $2}')
[ -z "$COLS" ] && COLS=120

SEP='\033[0m · '
OSC_START='\033]8;;'
OSC_END='\033\\'

# --- Factory usage + plan (stale-while-revalidate, 600s TTL) ---
USAGE_CACHE="/tmp/droid_statusline_usage"
USAGE_STR=""
_fetch_usage() {
  local tok tmp
  tok=$(python3 -c "import json; print(json.loads(open('$HOME/.factory/auth.encrypted').read())['access_token'])" 2>/dev/null) || return
  tmp="${USAGE_CACHE}.tmp.$$"
  curl -s --max-time 5 --noproxy api.factory.ai "https://api.factory.ai/api/organization/subscription/schedule" \
    -H "Authorization: Bearer $tok" \
    -H "Content-Type: application/json" -H "X-Factory-Client: cli" \
    -o "$tmp" 2>/dev/null
  if [ -s "$tmp" ] && head -c1 "$tmp" | grep -q '{'; then
    mv -f "$tmp" "$USAGE_CACHE"
  else
    rm -f "$tmp"
  fi
}
if [ -f "$USAGE_CACHE" ] && [ -s "$USAGE_CACHE" ]; then
  CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$USAGE_CACHE" 2>/dev/null || echo 0) ))
  [ "$CACHE_AGE" -ge 600 ] && _fetch_usage &
else
  _fetch_usage
fi
if [ -f "$USAGE_CACHE" ] && [ -s "$USAGE_CACHE" ]; then
  USAGE_DATA=$(cat "$USAGE_CACHE")
  USED=$(echo "$USAGE_DATA" | jq -r '.usage.standard.orgTotalTokensUsed // 0' 2>/dev/null)
  TOTAL=$(echo "$USAGE_DATA" | jq -r '.usage.standard.totalAllowance // 0' 2>/dev/null)
  END_MS=$(echo "$USAGE_DATA" | jq -r '.usage.endDate // 0' 2>/dev/null)
  PLAN=$(echo "$USAGE_DATA" | jq -r '.schedule[0].plan.name // empty' 2>/dev/null)
  # extract short plan name: "Factory Pro Plan" -> "Pro"
  SHORT_PLAN=$(echo "$PLAN" | sed -E 's/Factory ([A-Za-z]+) Plan/\1/')
  if [ "$TOTAL" -gt 0 ] 2>/dev/null; then
    USED_M=$(awk "BEGIN{printf \"%.1f\", $USED/1000000}")
    TOTAL_M=$(awk "BEGIN{printf \"%.0f\", $TOTAL/1000000}")
    PCT=$(awk "BEGIN{printf \"%.0f\", $USED/$TOTAL*100}")
    if [ "$PCT" -ge 80 ]; then
      USAGE_CLR="38;5;174"
    elif [ "$PCT" -ge 60 ]; then
      USAGE_CLR="38;5;222"
    else
      USAGE_CLR="38;5;114"
    fi
    # days until renewal
    RENEW=""
    if [ "$END_MS" -gt 0 ] 2>/dev/null; then
      NOW_S=$(date +%s)
      END_S=$((END_MS / 1000))
      DAYS_LEFT=$(( (END_S - NOW_S) / 86400 ))
      RENEW=" ${DAYS_LEFT}d"
    fi
    BILLING_URL="https://app.factory.ai/settings/billing"
    USAGE_STR=" · ${OSC_START}${BILLING_URL}${OSC_END}\033[38;5;243m${SHORT_PLAN}\033[0m \033[${USAGE_CLR}m${USED_M}/${TOTAL_M}M\033[0m\033[38;5;243m${RENEW}\033[0m${OSC_START}${OSC_END}"
  fi
fi

if [ "$IS_CC" = "0" ]; then
  right_col=$((COLS - ${#SHORT_CWD}))
  DIR_LINK="\033[${right_col}G${OSC_START}vscode://file${CWD}${OSC_END}\033[1;38;5;66m${SHORT_CWD}\033[0m${OSC_START}${OSC_END}"
else
  DIR_LINK="${SEP}${OSC_START}vscode://file${CWD}${OSC_END}\033[1;38;5;66m${SHORT_CWD}\033[0m${OSC_START}${OSC_END}"
fi

if git -C "$CWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BRANCH=$(git -C "$CWD" --no-optional-locks branch --show-current 2>/dev/null)

  # stale-while-revalidate PR cache
  REPO_ROOT=$(git -C "$CWD" --no-optional-locks rev-parse --show-toplevel 2>/dev/null)
  REPO_NAME=$(basename "$REPO_ROOT" 2>/dev/null)
  SAFE_BRANCH=$(echo "$BRANCH" | tr '/' '_')
  CACHE_FILE="/tmp/droid_statusline_pr_${REPO_NAME}_${SAFE_BRANCH}"
  PR_STR=""
  PR_VIS=""

  if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0) ))
    if [ "$CACHE_AGE" -ge 300 ]; then
      (cd "$REPO_ROOT" && gh pr view --json number,url -q '.number,.url' > "$CACHE_FILE" 2>/dev/null || echo "none" > "$CACHE_FILE") &
    fi
  else
    (cd "$REPO_ROOT" && gtimeout 2 gh pr view --json number,url -q '.number,.url' > "$CACHE_FILE" 2>/dev/null) || echo "none" > "$CACHE_FILE"
  fi
  if [ -f "$CACHE_FILE" ]; then
    PR_NUM=$(head -1 "$CACHE_FILE")
    PR_URL=$(tail -1 "$CACHE_FILE")
    if [ -n "$PR_NUM" ] && [ "$PR_NUM" != "none" ]; then
      PR_STR=" · \033[38;5;146mPR ${OSC_START}${PR_URL}${OSC_END}#${PR_NUM}${OSC_START}${OSC_END}\033[0m"
      PR_VIS=" · PR #${PR_NUM}"
    fi
  fi

  STATS=$({ git -C "$CWD" --no-optional-locks diff --numstat 2>/dev/null; git -C "$CWD" --no-optional-locks diff --cached --numstat 2>/dev/null; } | awk '{a+=$1; d+=$2} END {print a+0, d+0}')
  ADD=${STATS% *}
  DEL=${STATS#* }

  SID_STR=""
  [ -n "$SHORT_SID" ] && SID_STR=" · \033[38;5;243m${SHORT_SID}\033[0m"

  if [ "$IS_CC" = "0" ]; then
    if [ "$ADD" -gt 0 ] || [ "$DEL" -gt 0 ]; then
      printf "\033[1;38;5;214m%s\033[0m%b · \033[1;38;5;146m%s\033[0m%b \033[1;38;5;114m+%s \033[1;38;5;174m-%s\033[0m%b${DIR_LINK}" "$MODEL" "$SID_STR" "$BRANCH" "$PR_STR" "$ADD" "$DEL" "$USAGE_STR"
    else
      printf "\033[1;38;5;214m%s\033[0m%b · \033[1;38;5;146m%s\033[0m%b%b${DIR_LINK}" "$MODEL" "$SID_STR" "$BRANCH" "$PR_STR" "$USAGE_STR"
    fi
  else
    printf "${OSC_START}vscode://file${CWD}${OSC_END}\033[1;38;5;66m%s\033[0m${OSC_START}${OSC_END}${SEP}\033[1;38;5;146m%s\033[0m${SEP}\033[1;38;5;214m%s\033[0m" "$SHORT_CWD" "$BRANCH" "$MODEL"
  fi
else
  SID_STR=""
  [ -n "$SHORT_SID" ] && SID_STR=" · \033[38;5;243m${SHORT_SID}\033[0m"
  printf "\033[1;38;5;214m%s\033[0m%b%b${DIR_LINK}" "$MODEL" "$SID_STR" "$USAGE_STR"
fi
