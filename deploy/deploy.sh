#!/usr/bin/env bash
# ============================================================================
# deploy.sh — OpenClaw-TradeDesk Multi-Variant Deployment Script
# ============================================================================
# Runs on the target server via SSH (called by GitHub Actions deploy.yml).
# All DEPLOY_* and secret env vars must be passed by the caller.
#
# Usage: All environment variables are expected to be set before invocation.
#        See deploy/.env.example for the full list.
# ============================================================================
set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
DEPLOY_DIR="$WORKSPACE/deploy"

# ── 0. Bootstrap PATH (nvm / local bins) ─────────────────────────────────────
echo "==> [0/14] Bootstrapping PATH..."
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 22 2>/dev/null && nvm alias default 22 2>/dev/null || true
export PATH="$HOME/.local/bin:$HOME/.npm/bin:/usr/local/bin:$PATH"

# ── 1. Clone or pull the workspace ───────────────────────────────────────────
echo "==> [1/14] Syncing workspace repo..."
if [ -d "$WORKSPACE/.git" ]; then
  git -C "$WORKSPACE" fetch origin main
  git -C "$WORKSPACE" reset --hard origin/main
else
  if [ -d "$WORKSPACE" ]; then
    BACKUP="${WORKSPACE}-backup-$(date +%Y%m%d%H%M%S)"
    echo "    Existing workspace moved to: $BACKUP"
    mv "$WORKSPACE" "$BACKUP"
  fi
  mkdir -p "$HOME/.openclaw"
  git clone https://github.com/Sensini7/OpenClaw-TradeDesk.git "$WORKSPACE"
fi

# ── 2. Generate ~/.openclaw/.env ─────────────────────────────────────────────
echo "==> [2/14] Writing .env file..."
cat > "$HOME/.openclaw/.env" <<ENVEOF
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN:-}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-}
TELEGRAM_USER_ID=${TELEGRAM_USER_ID:-}
DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN:-}
SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN:-}
SLACK_APP_TOKEN=${SLACK_APP_TOKEN:-}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
WEBHOOK_SECRET=${WEBHOOK_SECRET:-}
WEBHOOK_URL=${WEBHOOK_URL:-}
OPENCLAW_GATEWAY_PASSWORD=${OPENCLAW_GATEWAY_PASSWORD:-}
OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-}
DATADOG_API_KEY=${DATADOG_API_KEY:-}
GRAFANA_PUSH_URL=${GRAFANA_PUSH_URL:-}
ENVEOF
chmod 600 "$HOME/.openclaw/.env"

# ── 3. Assemble openclaw.json from fragments ─────────────────────────────────
echo "==> [3/14] Assembling config from fragments..."
chmod +x "${DEPLOY_DIR}/assemble-config.sh"
bash "${DEPLOY_DIR}/assemble-config.sh"

# ── 4. Write auth-profiles.json ──────────────────────────────────────────────
echo "==> [4/14] Writing auth-profiles.json (global + per-agent)..."
AUTH_JSON=$(cat <<AUTHEOF
{
  "default": {
    "apiKey": "${ANTHROPIC_API_KEY:-}"
  }
}
AUTHEOF
)

# Global auth profile
echo "$AUTH_JSON" > "$HOME/.openclaw/auth-profiles.json"
chmod 600 "$HOME/.openclaw/auth-profiles.json"

# Per-agent auth profiles (agents read from their own dir first)
for agent in commander scout oracle trigger sentinel herald; do
  AGENT_DIR="$WORKSPACE/agents/$agent"
  mkdir -p "$AGENT_DIR"
  echo "$AUTH_JSON" > "$AGENT_DIR/auth-profiles.json"
  chmod 600 "$AGENT_DIR/auth-profiles.json"
done
echo "    Auth profiles written for all 6 agents."

# ── 5. Install OpenClaw binary ───────────────────────────────────────────────
DEPLOY_INSTALL_METHOD="${DEPLOY_INSTALL_METHOD:-installer}"
if [ "$DEPLOY_INSTALL_METHOD" = "installer" ]; then
  if ! command -v openclaw &>/dev/null; then
    echo "==> [5/14] Installing OpenClaw via installer script..."
    ( curl -fsSL https://openclaw.ai/install.sh | CI=1 bash ) 2>&1 || true

    # Re-source nvm for newly installed binary
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm use 22 2>/dev/null || true
    export PATH="$HOME/.local/bin:$HOME/.npm/bin:/usr/local/bin:$PATH"

    if ! command -v openclaw &>/dev/null; then
      echo "ERROR: OpenClaw installation failed — binary not found."
      exit 1
    fi
    echo "    OpenClaw installed: $(openclaw --version 2>/dev/null || echo 'unknown')"
  else
    echo "==> [5/14] OpenClaw already installed: $(openclaw --version 2>/dev/null || echo 'unknown')"
  fi
elif [ "$DEPLOY_INSTALL_METHOD" = "docker" ]; then
  echo "==> [5/14] Skipping binary install (Docker mode)."
fi

# ── 6. Install Ollama (if memory_provider=ollama) ────────────────────────────
DEPLOY_MEMORY_PROVIDER="${DEPLOY_MEMORY_PROVIDER:-ollama}"
if [ "$DEPLOY_MEMORY_PROVIDER" = "ollama" ]; then
  if ! command -v ollama &>/dev/null; then
    echo "==> [6/14] Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
  else
    echo "==> [6/14] Ollama already installed."
  fi

  # Ensure Ollama service is running
  if command -v systemctl &>/dev/null; then
    sudo systemctl enable ollama 2>/dev/null || true
    sudo systemctl start ollama 2>/dev/null || true
  fi

  # Pull the embedding model (idempotent)
  echo "    Pulling nomic-embed-text model..."
  ollama pull nomic-embed-text 2>/dev/null || true
  echo "    Ollama ready with nomic-embed-text."
else
  echo "==> [6/14] Skipping Ollama (memory_provider=${DEPLOY_MEMORY_PROVIDER})."
fi

# ── 7. Create intel/ symlinks ────────────────────────────────────────────────
echo "==> [7/14] Creating intel symlinks..."
for agent in scout oracle trigger sentinel herald; do
  mkdir -p "$WORKSPACE/agents/$agent"
  ln -sf "$WORKSPACE/intel" "$WORKSPACE/agents/$agent/intel"
done

# ── 8. Run openclaw doctor ───────────────────────────────────────────────────
if [ "$DEPLOY_INSTALL_METHOD" = "installer" ]; then
  echo "==> [8/14] Running openclaw doctor --fix..."
  openclaw doctor --fix 2>&1 || true
else
  echo "==> [8/14] Skipping doctor (Docker mode)."
fi

# ── 9. Process management setup ──────────────────────────────────────────────
DEPLOY_PROCESS_MANAGER="${DEPLOY_PROCESS_MANAGER:-native}"
echo "==> [9/14] Process management: ${DEPLOY_PROCESS_MANAGER}"
# Disable any leftover systemd service to avoid conflict with native daemon
if sudo systemctl is-enabled openclaw 2>/dev/null; then
  sudo systemctl stop openclaw 2>/dev/null || true
  sudo systemctl disable openclaw 2>/dev/null || true
  echo "    Disabled systemd openclaw service (using native daemon)."
fi

# ── 10. Docker Compose ───────────────────────────────────────────────────────
if [ "$DEPLOY_PROCESS_MANAGER" = "docker-compose" ]; then
  echo "==> [10/14] Starting Docker Compose..."
  cd "${DEPLOY_DIR}/docker"
  docker compose up -d --build
  cd "$WORKSPACE"
else
  echo "==> [10/14] Skipping Docker Compose."
fi

# ── 11. Nginx reverse proxy ─────────────────────────────────────────────────
DEPLOY_NGINX_PROXY="${DEPLOY_NGINX_PROXY:-false}"
if [ "$DEPLOY_NGINX_PROXY" = "true" ]; then
  echo "==> [11/14] Installing Nginx config..."
  NGINX_TMPL="${DEPLOY_DIR}/nginx/openclaw.conf.tmpl"
  if [ -f "$NGINX_TMPL" ]; then
    export SERVER_NAME="${DEPLOY_SERVER_NAME:-_}"
    envsubst '$SERVER_NAME' < "$NGINX_TMPL" | sudo tee /etc/nginx/sites-available/openclaw.conf > /dev/null
    sudo ln -sf /etc/nginx/sites-available/openclaw.conf /etc/nginx/sites-enabled/openclaw.conf
    sudo nginx -t && sudo systemctl reload nginx
    echo "    Nginx config installed and reloaded."
  else
    echo "    WARN: Nginx template not found at $NGINX_TMPL"
  fi
else
  echo "==> [11/14] Skipping Nginx proxy."
fi

# ── 12. Fix ~/.bashrc PATH ──────────────────────────────────────────────────
echo "==> [12/14] Ensuring PATH in .bashrc..."
if ! grep -q 'NVM_DIR' "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'BASHEOF'

# OpenClaw PATH (added by deploy.sh)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PATH="$HOME/.local/bin:$HOME/.npm/bin:$PATH"
BASHEOF
  echo "    PATH entries added to .bashrc."
else
  echo "    .bashrc already has NVM_DIR."
fi

# ── 13. Restart gateway ─────────────────────────────────────────────────────
echo "==> [13/14] Restarting gateway..."
if [ "$DEPLOY_PROCESS_MANAGER" = "docker-compose" ]; then
  cd "${DEPLOY_DIR}/docker"
  docker compose restart openclaw-gateway
  cd "$WORKSPACE"
  echo "    Docker container restarted."
else
  # Use OpenClaw's native daemon management
  openclaw gateway install 2>/dev/null || \
    openclaw gateway install-daemon 2>/dev/null || true
  if openclaw gateway restart 2>/dev/null; then
    echo "    Gateway restarted."
  else
    openclaw gateway start 2>/dev/null || {
      echo "ERROR: Could not start the OpenClaw gateway."
      exit 1
    }
  fi
fi

# ── 14. Health checks ───────────────────────────────────────────────────────
echo "==> [14/14] Running health checks..."
sleep 5

if [ "$DEPLOY_PROCESS_MANAGER" = "docker-compose" ]; then
  echo "--- Docker status ---"
  cd "${DEPLOY_DIR}/docker"
  docker compose ps
  cd "$WORKSPACE"
fi

if [ "$DEPLOY_INSTALL_METHOD" = "installer" ]; then
  echo "--- Gateway status ---"
  openclaw gateway status 2>/dev/null || echo "    (gateway status unavailable)"

  echo "--- Agent list ---"
  openclaw agents list 2>/dev/null || echo "    (agent list unavailable)"
fi

echo ""
echo "============================================"
echo "  Deployment complete!"
echo "  Channels:  ${DEPLOY_CHANNELS:-telegram}"
echo "  Gateway:   ${DEPLOY_GATEWAY_BIND:-loopback}"
echo "  Auth:      ${DEPLOY_AUTH_MODE:-token}"
echo "  Process:   ${DEPLOY_PROCESS_MANAGER}"
echo "  Memory:    ${DEPLOY_MEMORY_PROVIDER}"
echo "============================================"
