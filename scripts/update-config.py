#!/usr/bin/env python3
"""Update openclaw.json with 6-agent TradeDesk configuration."""
import json
import os
import shutil

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

# Backup first
shutil.copy2(config_path, config_path + ".pre-tradedesk.bak")
print(f"Backed up config to {config_path}.pre-tradedesk.bak")

with open(config_path) as f:
    config = json.load(f)

# Update agents section
config["agents"]["defaults"]["workspace"] = "/root/.openclaw/workspace"

config["agents"]["list"] = [
    {
        "id": "commander",
        "name": "Commander 👑",
        "default": True,
        "workspace": "/root/.openclaw/workspace",
        "model": {"primary": "anthropic/claude-sonnet-4-5-20250929"},
        "subagents": {
            "allowAgents": ["scout", "oracle", "trigger", "sentinel", "herald"]
        }
    },
    {
        "id": "scout",
        "name": "Scout 🔭",
        "workspace": "/root/.openclaw/workspace/agents/scout",
        "model": {"primary": "anthropic/claude-haiku-4-5-20251001"}
    },
    {
        "id": "oracle",
        "name": "Oracle 📊",
        "workspace": "/root/.openclaw/workspace/agents/oracle",
        "model": {"primary": "anthropic/claude-sonnet-4-5-20250929"}
    },
    {
        "id": "trigger",
        "name": "Trigger ⚡",
        "workspace": "/root/.openclaw/workspace/agents/trigger",
        "model": {"primary": "anthropic/claude-sonnet-4-5-20250929"}
    },
    {
        "id": "sentinel",
        "name": "Sentinel 🛡️",
        "workspace": "/root/.openclaw/workspace/agents/sentinel",
        "model": {"primary": "anthropic/claude-haiku-4-5-20251001"}
    },
    {
        "id": "herald",
        "name": "Herald 📲",
        "workspace": "/root/.openclaw/workspace/agents/herald",
        "model": {"primary": "anthropic/claude-haiku-4-5-20251001"}
    }
]

# Enable inter-agent communication
if "tools" not in config:
    config["tools"] = {}

config["tools"]["agentToAgent"] = {
    "enabled": True,
    "allow": ["commander", "scout", "oracle", "trigger", "sentinel", "herald"]
}

# Enable browser for Scout
config["browser"] = {
    "enabled": True
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("Updated openclaw.json with 6-agent TradeDesk configuration:")
print("  - Commander 👑 (Sonnet) — default agent, delegates to all")
print("  - Scout 🔭 (Haiku) — market intelligence")
print("  - Oracle 📊 (Sonnet) — strategy filter")
print("  - Trigger ⚡ (Sonnet) — signal generator")
print("  - Sentinel 🛡️ (Haiku) — risk manager")
print("  - Herald 📲 (Haiku) — Telegram reporter")
print("  - Agent-to-agent communication enabled")
print("  - Browser enabled for Scout")
