#!/usr/bin/env python3
"""Add Telegram channel config and binding to openclaw.json."""
import json
import shutil

CONFIG = "/root/.openclaw/openclaw.json"

# Backup
shutil.copy2(CONFIG, CONFIG + ".pre-telegram.bak")
print(f"Backed up to {CONFIG}.pre-telegram.bak")

with open(CONFIG) as f:
    config = json.load(f)

# Add Telegram channel
config["channels"] = {
    "telegram": {
        "botToken": "7429721533:AAGInnmb_xAOorYHUrCqAfv4Vd3Y4geJJ1A",
        "allowFrom": ["1804547199"]
    }
}

# Add binding: all Telegram messages → Commander
config["bindings"] = [
    {
        "agentId": "commander",
        "match": {"channel": "telegram"}
    }
]

with open(CONFIG, "w") as f:
    json.dump(config, f, indent=2)

print("Telegram configured:")
print("  Bot token: 7429...J1A")
print("  Allowed user: 1804547199")
print("  Channel ID: 3830825064 (stored in Herald's USER.md)")
print("  Binding: all Telegram → Commander 👑")
print("\nNext: restart gateway with 'openclaw gateway restart'")
