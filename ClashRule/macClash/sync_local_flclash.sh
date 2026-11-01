#!/bin/zsh
# 本地保存 Direct.yaml / Reject.yaml / FlClashOverride.js 时，0 秒同步到本机 FlClash 缓存（免等 GitHub Raw CDN 缓存）

set -e

RULE_DIR="/Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash"
FLCLASH_DIR="/Users/kqy/Library/Application Support/com.follow.clash"
PROV_BASE="$FLCLASH_DIR/profiles/providers"
SCRIPT_FILE="$FLCLASH_DIR/scripts/375085198477365248.js"

DIRECT_HASH="0bcea73dd8c0f4e7ead3b5a814f6185f"
REJECT_HASH="8852193bb292e95b0578e51a458a4cc1"

# 1. 同步覆写脚本
if [[ -f "$RULE_DIR/FlClashOverride.js" && -d "$FLCLASH_DIR/scripts" ]]; then
  cp -f "$RULE_DIR/FlClashOverride.js" "$SCRIPT_FILE"
fi

# 2. 同步规则集缓存
if [[ ! -d "$PROV_BASE" ]]; then
  exit 0
fi

for prof_dir in "$PROV_BASE"/*(N/); do
  base_name="${prof_dir:t}"
  [[ "$base_name" == .* ]] && continue

  rules_dir="$prof_dir/rules"
  if [[ -d "$rules_dir" && ! -w "$rules_dir" ]]; then
    cp -R "$prof_dir" "${prof_dir}_kqy_tmp"
    mv "$prof_dir" "$PROV_BASE/.root_bak_${base_name}_$$"
    mv "${prof_dir}_kqy_tmp" "$prof_dir"
  fi

  mkdir -p "$rules_dir"
  if [[ -f "$RULE_DIR/Direct.yaml" ]]; then
    cp -f "$RULE_DIR/Direct.yaml" "$rules_dir/$DIRECT_HASH"
  fi
  if [[ -f "$RULE_DIR/Reject.yaml" ]]; then
    cp -f "$RULE_DIR/Reject.yaml" "$rules_dir/$REJECT_HASH"
  fi
done
