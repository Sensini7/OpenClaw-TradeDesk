#!/usr/bin/env python3
"""Fix missing agent files and update tool profiles in openclaw.json."""
import json
import os
import shutil

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")


def write_file(relative_path: str, content: str) -> None:
    full_path = os.path.join(WORKSPACE, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  wrote {relative_path}")


# ═══════════════════════════════════════════════════════════════════
# PART 1: Create missing files for Commander + all sub-agents
# ═══════════════════════════════════════════════════════════════════

print("=== Creating missing workspace files ===\n")

# Commander MEMORY.md (was missing)
write_file("MEMORY.md", """\
# MEMORY — Commander Long-Term Memory

_Updated automatically. Do not delete — this is your continuity._

## Trader Preferences
- [Will be populated as you learn the trader's habits]

## Pipeline Notes
- [Will be populated as you observe pipeline behavior]

## Lessons Learned
- [Will be populated from daily operations]
""")

# ── Sub-agent files ──────────────────────────────────────────────

AGENTS = {
    "scout": {"emoji": "🔭", "role": "Market Intelligence"},
    "oracle": {"emoji": "📊", "role": "Strategy Analyst"},
    "trigger": {"emoji": "⚡", "role": "Signal Generator"},
    "sentinel": {"emoji": "🛡️", "role": "Risk Manager"},
    "herald": {"emoji": "📲", "role": "Telegram Reporter"},
}

for agent_id, info in AGENTS.items():
    prefix = f"agents/{agent_id}"

    # MEMORY.md
    write_file(f"{prefix}/MEMORY.md", f"""\
# MEMORY — {agent_id.title()} {info['emoji']}

_Auto-updated. This is {agent_id.title()}'s long-term memory._

## Patterns
- [Will be populated from daily operations]

## Issues
- [Track recurring problems here]
""")

    # IDENTITY.md
    write_file(f"{prefix}/IDENTITY.md", f"""\
# IDENTITY — {agent_id.title()} {info['emoji']}

- **Name**: {agent_id.title()}
- **Emoji**: {info['emoji']}
- **Role**: {info['role']}
- **Team**: TradeDesk by Axidion
""")

    # TOOLS.md (agent-specific)
    if agent_id == "scout":
        tools_content = """\
# TOOLS — Scout 🔭

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **browser**: Browse finviz.com, Yahoo Finance for market data
- **web_search/web_fetch**: Search and fetch web content
- **memory**: Read/write your memory files

## File Paths (relative to workspace root)
- Read: `../../USER.md` (trader profile)
- Write: `../../intel/DAILY-INTEL.md` (your output)
- Write: `../../intel/data/YYYY-MM-DD.json` (structured data)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)
"""
    elif agent_id == "herald":
        tools_content = """\
# TOOLS — Herald 📲

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files
- **message**: Send Telegram messages to trader and academy channel

## File Paths (relative to workspace root)
- Read: `../../intel/VETTED.md` (Sentinel's output)
- Read: `../../intel/DAILY-INTEL.md` (macro context)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)
"""
    else:
        # Oracle, Trigger, Sentinel — file-based only
        input_file = {
            "oracle": "../../intel/DAILY-INTEL.md",
            "trigger": "../../intel/PLAYS.md",
            "sentinel": "../../intel/SIGNALS.md",
        }[agent_id]
        output_file = {
            "oracle": "../../intel/PLAYS.md",
            "trigger": "../../intel/SIGNALS.md",
            "sentinel": "../../intel/VETTED.md",
        }[agent_id]
        tools_content = f"""\
# TOOLS — {agent_id.title()} {info['emoji']}

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files

## File Paths (relative to workspace root)
- Read: `{input_file}` (input from previous agent)
- Read: `../../USER.md` (trader profile and rules)
- Write: `{output_file}` (your output)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)
"""

    write_file(f"{prefix}/TOOLS.md", tools_content)


# ═══════════════════════════════════════════════════════════════════
# PART 2: Update openclaw.json with per-agent tool profiles
# ═══════════════════════════════════════════════════════════════════

print("\n=== Updating openclaw.json tool profiles ===\n")

shutil.copy2(CONFIG, CONFIG + ".pre-tools.bak")
print(f"  backed up to {CONFIG}.pre-tools.bak")

with open(CONFIG) as f:
    config = json.load(f)

# Define tool profiles per agent
# "full" = all tools, "minimal" = read/write/exec/memory only
TOOL_PROFILES = {
    "commander": {
        "profile": "full",
        # Commander keeps all 23 tools — needs to coordinate everything
    },
    "scout": {
        "profile": "custom",
        "tools": {
            "read": True,
            "write": True,
            "edit": True,
            "exec": True,
            "browser": True,
            "web_search": True,
            "web_fetch": True,
            "memory_search": True,
            "memory_get": True,
            # Disabled for Scout:
            "message": False,
            "cron": False,
            "gateway": False,
            "nodes": False,
            "canvas": False,
            "agents_list": False,
            "sessions_list": False,
            "sessions_history": False,
            "sessions_send": False,
            "sessions_spawn": False,
            "session_status": False,
            "apply_patch": False,
            "process": False,
            "image": False,
        }
    },
    "oracle": {
        "profile": "custom",
        "tools": {
            "read": True,
            "write": True,
            "edit": True,
            "exec": True,
            "memory_search": True,
            "memory_get": True,
            # Disabled for Oracle:
            "browser": False,
            "web_search": False,
            "web_fetch": False,
            "message": False,
            "cron": False,
            "gateway": False,
            "nodes": False,
            "canvas": False,
            "agents_list": False,
            "sessions_list": False,
            "sessions_history": False,
            "sessions_send": False,
            "sessions_spawn": False,
            "session_status": False,
            "apply_patch": False,
            "process": False,
            "image": False,
        }
    },
    "trigger": {
        "profile": "custom",
        "tools": {
            "read": True,
            "write": True,
            "edit": True,
            "exec": True,
            "memory_search": True,
            "memory_get": True,
            # Disabled:
            "browser": False,
            "web_search": False,
            "web_fetch": False,
            "message": False,
            "cron": False,
            "gateway": False,
            "nodes": False,
            "canvas": False,
            "agents_list": False,
            "sessions_list": False,
            "sessions_history": False,
            "sessions_send": False,
            "sessions_spawn": False,
            "session_status": False,
            "apply_patch": False,
            "process": False,
            "image": False,
        }
    },
    "sentinel": {
        "profile": "custom",
        "tools": {
            "read": True,
            "write": True,
            "edit": True,
            "exec": True,
            "memory_search": True,
            "memory_get": True,
            # Disabled:
            "browser": False,
            "web_search": False,
            "web_fetch": False,
            "message": False,
            "cron": False,
            "gateway": False,
            "nodes": False,
            "canvas": False,
            "agents_list": False,
            "sessions_list": False,
            "sessions_history": False,
            "sessions_send": False,
            "sessions_spawn": False,
            "session_status": False,
            "apply_patch": False,
            "process": False,
            "image": False,
        }
    },
    "herald": {
        "profile": "custom",
        "tools": {
            "read": True,
            "write": True,
            "edit": True,
            "exec": True,
            "memory_search": True,
            "memory_get": True,
            "message": True,  # Herald NEEDS messaging for Telegram
            # Disabled:
            "browser": False,
            "web_search": False,
            "web_fetch": False,
            "cron": False,
            "gateway": False,
            "nodes": False,
            "canvas": False,
            "agents_list": False,
            "sessions_list": False,
            "sessions_history": False,
            "sessions_send": False,
            "sessions_spawn": False,
            "session_status": False,
            "apply_patch": False,
            "process": False,
            "image": False,
        }
    },
}

# Apply tool profiles to each agent in the config
for agent in config["agents"]["list"]:
    agent_id = agent["id"]
    if agent_id in TOOL_PROFILES:
        profile = TOOL_PROFILES[agent_id]
        if profile["profile"] == "full":
            agent["tools"] = {"profile": "full"}
        else:
            agent["tools"] = {
                "profile": "custom",
                "overrides": profile["tools"]
            }
        print(f"  {agent_id}: {profile['profile']} profile applied")

with open(CONFIG, "w") as f:
    json.dump(config, f, indent=2)

print(f"\nDone! Config saved to {CONFIG}")
print("\nTool access summary:")
print("  Commander 👑  → full (23/23 tools)")
print("  Scout 🔭      → custom (read, write, exec, browser, web, memory)")
print("  Oracle 📊     → custom (read, write, exec, memory)")
print("  Trigger ⚡    → custom (read, write, exec, memory)")
print("  Sentinel 🛡️   → custom (read, write, exec, memory)")
print("  Herald 📲     → custom (read, write, exec, memory, message)")
