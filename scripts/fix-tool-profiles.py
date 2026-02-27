#!/usr/bin/env python3
"""Fix agent tool profiles — minimal profile is too restrictive, need read/write/exec."""
import json
import shutil

CONFIG = "/root/.openclaw/openclaw.json"

shutil.copy2(CONFIG, CONFIG + ".pre-toolfix.bak")
print(f"Backed up to {CONFIG}.pre-toolfix.bak")

with open(CONFIG) as f:
    config = json.load(f)

# Fix each agent's tool profile
for agent in config["agents"]["list"]:
    aid = agent["id"]

    if aid == "commander":
        # Commander gets full access (already correct)
        agent["tools"] = {"profile": "full"}
        print(f"  {aid}: full profile")

    elif aid == "scout":
        # Scout needs: read, write, edit, exec, browser, web_search, web_fetch, memory
        agent["tools"] = {
            "profile": "minimal",
            "alsoAllow": [
                "read", "write", "edit", "exec",
                "browser", "web_search", "web_fetch",
                "memory_search", "memory_get"
            ]
        }
        print(f"  {aid}: minimal + read/write/edit/exec/browser/web/memory")

    elif aid == "oracle":
        # Oracle needs: read, write, edit, exec, memory
        agent["tools"] = {
            "profile": "minimal",
            "alsoAllow": [
                "read", "write", "edit", "exec",
                "memory_search", "memory_get"
            ]
        }
        print(f"  {aid}: minimal + read/write/edit/exec/memory")

    elif aid == "trigger":
        # Trigger needs: read, write, edit, exec, memory
        agent["tools"] = {
            "profile": "minimal",
            "alsoAllow": [
                "read", "write", "edit", "exec",
                "memory_search", "memory_get"
            ]
        }
        print(f"  {aid}: minimal + read/write/edit/exec/memory")

    elif aid == "sentinel":
        # Sentinel needs: read, write, edit, exec, memory
        agent["tools"] = {
            "profile": "minimal",
            "alsoAllow": [
                "read", "write", "edit", "exec",
                "memory_search", "memory_get"
            ]
        }
        print(f"  {aid}: minimal + read/write/edit/exec/memory")

    elif aid == "herald":
        # Herald needs: read, write, edit, exec, memory, message (for Telegram)
        agent["tools"] = {
            "profile": "minimal",
            "alsoAllow": [
                "read", "write", "edit", "exec",
                "memory_search", "memory_get",
                "message"
            ]
        }
        print(f"  {aid}: minimal + read/write/edit/exec/memory/message")

with open(CONFIG, "w") as f:
    json.dump(config, f, indent=2)

print(f"\nConfig saved. Restart gateway to apply: openclaw gateway restart")
