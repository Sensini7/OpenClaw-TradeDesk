#!/usr/bin/env bash
# ============================================================================
# assemble-config.sh — Merge JSON config fragments into openclaw.json
# ============================================================================
# Reads DEPLOY_* environment variables to select which fragments to merge.
# Uses jq for deep merge; falls back to Node.js if jq is unavailable.
#
# Usage:  DEPLOY_CHANNELS=telegram,discord DEPLOY_AUTH_MODE=token ... ./assemble-config.sh
# Output: ~/.openclaw/openclaw.json (chmod 600)
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"
OUTPUT="${HOME}/.openclaw/openclaw.json"

# ── Defaults (match workflow_dispatch defaults) ──────────────────────────────
DEPLOY_CHANNELS="${DEPLOY_CHANNELS:-telegram}"
DEPLOY_GATEWAY_BIND="${DEPLOY_GATEWAY_BIND:-loopback}"
DEPLOY_AUTH_MODE="${DEPLOY_AUTH_MODE:-token}"
DEPLOY_SESSION_SCOPE="${DEPLOY_SESSION_SCOPE:-per-channel-peer}"
DEPLOY_DM_POLICY="${DEPLOY_DM_POLICY:-pairing}"
DEPLOY_MEMORY_PROVIDER="${DEPLOY_MEMORY_PROVIDER:-ollama}"
DEPLOY_WEBHOOKS="${DEPLOY_WEBHOOKS:-false}"
DEPLOY_OTEL_EXPORTER="${DEPLOY_OTEL_EXPORTER:-none}"
DEPLOY_INSTALL_METHOD="${DEPLOY_INSTALL_METHOD:-installer}"

# Workspace root: /root for bare metal, /home/node for Docker
if [ "${DEPLOY_INSTALL_METHOD}" = "docker" ]; then
  WORKSPACE_ROOT="/home/node/.openclaw/workspace"
else
  WORKSPACE_ROOT="${HOME}/.openclaw/workspace"
fi
export WORKSPACE_ROOT

# ── Deep merge function ──────────────────────────────────────────────────────
# Try jq first (fast, native), fall back to Node.js (guaranteed on OC servers)
if command -v jq &>/dev/null; then
  deep_merge() {
    # Merge two JSON files: $1 = base, $2 = overlay → stdout
    jq -s '
      def deepmerge(a; b):
        a as $a | b as $b |
        if ($a | type) == "object" and ($b | type) == "object" then
          ($a | keys_unsorted) + ($b | keys_unsorted) | unique |
          map(. as $k |
            if ($a | has($k)) and ($b | has($k)) then
              { ($k): deepmerge($a[$k]; $b[$k]) }
            elif ($b | has($k)) then
              { ($k): $b[$k] }
            else
              { ($k): $a[$k] }
            end
          ) | add // {}
        elif ($b | type) == "array" and ($a | type) == "array" then
          $a + $b
        else
          $b
        end;
      deepmerge(.[0]; .[1])
    ' "$1" "$2"
  }
else
  echo "WARN: jq not found, using Node.js fallback for JSON merge"
  deep_merge() {
    node -e "
      const fs = require('fs');
      const a = JSON.parse(fs.readFileSync('$1', 'utf8'));
      const b = JSON.parse(fs.readFileSync('$2', 'utf8'));
      function merge(target, source) {
        for (const key of Object.keys(source)) {
          if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])
              && target[key] && typeof target[key] === 'object' && !Array.isArray(target[key])) {
            merge(target[key], source[key]);
          } else if (Array.isArray(target[key]) && Array.isArray(source[key])) {
            target[key] = target[key].concat(source[key]);
          } else {
            target[key] = source[key];
          }
        }
        return target;
      }
      console.log(JSON.stringify(merge(a, b), null, 2));
    "
  }
fi

# ── Helper: merge a fragment into the accumulator ────────────────────────────
ACCUM=$(mktemp)
merge_fragment() {
  local fragment="$1"
  if [ ! -f "$fragment" ]; then
    echo "WARN: Fragment not found: $fragment (skipping)"
    return
  fi
  echo "  + $(basename "$(dirname "$fragment")")/$(basename "$fragment")"
  local tmp=$(mktemp)
  deep_merge "$ACCUM" "$fragment" > "$tmp"
  mv "$tmp" "$ACCUM"
}

# ── Build config ─────────────────────────────────────────────────────────────
echo "==> Assembling openclaw.json from fragments..."

# Start with base + agents
cp "${CONFIG_DIR}/base.json" "$ACCUM"
merge_fragment "${CONFIG_DIR}/agents.json"

# Merge each enabled channel
IFS=',' read -ra CHANNELS <<< "$DEPLOY_CHANNELS"
for channel in "${CHANNELS[@]}"; do
  channel=$(echo "$channel" | tr -d ' ')
  merge_fragment "${CONFIG_DIR}/channels/${channel}.json"
done

# Merge gateway bind mode
merge_fragment "${CONFIG_DIR}/gateway/${DEPLOY_GATEWAY_BIND}.json"

# Merge auth mode
merge_fragment "${CONFIG_DIR}/auth/${DEPLOY_AUTH_MODE}.json"

# Merge session scope
merge_fragment "${CONFIG_DIR}/session/${DEPLOY_SESSION_SCOPE}.json"

# Merge memory provider
merge_fragment "${CONFIG_DIR}/memory/${DEPLOY_MEMORY_PROVIDER}.json"

# Merge webhooks
if [ "$DEPLOY_WEBHOOKS" = "true" ]; then
  merge_fragment "${CONFIG_DIR}/webhooks/enabled.json"
else
  merge_fragment "${CONFIG_DIR}/webhooks/disabled.json"
fi

# Merge telemetry
merge_fragment "${CONFIG_DIR}/telemetry/${DEPLOY_OTEL_EXPORTER}.json"

# ── Post-processing ──────────────────────────────────────────────────────────

# Replace ${WORKSPACE_ROOT} placeholder with actual path
if command -v jq &>/dev/null; then
  jq --arg wr "$WORKSPACE_ROOT" '
    walk(if type == "string" then gsub("\\$\\{WORKSPACE_ROOT\\}"; $wr) else . end)
  ' "$ACCUM" > "${ACCUM}.tmp" && mv "${ACCUM}.tmp" "$ACCUM"
else
  sed -i "s|\${WORKSPACE_ROOT}|${WORKSPACE_ROOT}|g" "$ACCUM"
fi

# ── Write output ─────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$OUTPUT")"
mv "$ACCUM" "$OUTPUT"
chmod 600 "$OUTPUT"

echo "==> Config assembled: $OUTPUT"
echo "    Channels: ${DEPLOY_CHANNELS}"
echo "    Gateway:  ${DEPLOY_GATEWAY_BIND} / Auth: ${DEPLOY_AUTH_MODE}"
echo "    Session:  ${DEPLOY_SESSION_SCOPE}"
echo "    Memory:   ${DEPLOY_MEMORY_PROVIDER}"
echo "    Webhooks: ${DEPLOY_WEBHOOKS}"
echo "    OTEL:     ${DEPLOY_OTEL_EXPORTER}"
