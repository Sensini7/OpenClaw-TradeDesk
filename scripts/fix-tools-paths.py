#!/usr/bin/env python3
"""Fix TOOLS.md paths — use intel/ directly (symlinked) instead of ../../intel/."""
import os

WORKSPACE = "/root/.openclaw/workspace"


def write_file(relative_path: str, content: str) -> None:
    full_path = os.path.join(WORKSPACE, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  wrote {relative_path}")


print("=== Fixing TOOLS.md paths for all agents ===\n")

write_file("agents/scout/TOOLS.md", """\
# TOOLS — Scout 🔭

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **browser**: Browse finviz.com, Yahoo Finance for market data
- **web_search/web_fetch**: Search and fetch web content
- **memory**: Read/write your memory files

## File Paths (relative to your workspace)
- Read: `USER.md` (your instruments and watchlist)
- Read: `SOUL.md` (your role and rules)
- Write: `intel/DAILY-INTEL.md` (your output — the daily report)
- Write: `intel/data/YYYY-MM-DD.json` (structured data)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)

## Important
- The `intel/` directory is symlinked to the shared workspace intel folder
- All agents can read your output from intel/DAILY-INTEL.md
""")

write_file("agents/oracle/TOOLS.md", """\
# TOOLS — Oracle 📊

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files

## File Paths (relative to your workspace)
- Read: `intel/DAILY-INTEL.md` (Scout's output — your input)
- Read: `USER.md` (strategy rules to apply)
- Read: `SOUL.md` (your role and rules)
- Write: `intel/PLAYS.md` (your output — filtered plays)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)

## Important
- The `intel/` directory is symlinked to the shared workspace intel folder
""")

write_file("agents/trigger/TOOLS.md", """\
# TOOLS — Trigger ⚡

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files

## File Paths (relative to your workspace)
- Read: `intel/PLAYS.md` (Oracle's output — your input)
- Read: `USER.md` (signal format preferences)
- Read: `SOUL.md` (your role and rules)
- Write: `intel/SIGNALS.md` (your output — trade signals)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)

## Important
- The `intel/` directory is symlinked to the shared workspace intel folder
""")

write_file("agents/sentinel/TOOLS.md", """\
# TOOLS — Sentinel 🛡️

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files

## File Paths (relative to your workspace)
- Read: `intel/SIGNALS.md` (Trigger's output — your input)
- Read: `USER.md` (risk parameters and account size)
- Read: `SOUL.md` (your role and rules)
- Write: `intel/VETTED.md` (your output — risk-checked signals)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)

## Important
- The `intel/` directory is symlinked to the shared workspace intel folder
""")

write_file("agents/herald/TOOLS.md", """\
# TOOLS — Herald 📲

## Your Tools
- **read/write**: Read and write files in the workspace
- **exec**: Run shell commands if needed
- **memory**: Read/write your memory files
- **message**: Send Telegram messages to trader and academy channel

## File Paths (relative to your workspace)
- Read: `intel/VETTED.md` (Sentinel's output — your input)
- Read: `intel/DAILY-INTEL.md` (macro context from Scout)
- Read: `USER.md` (Telegram IDs, tone, format preferences)
- Read: `SOUL.md` (your role and rules)
- Write: `memory/YYYY-MM-DD.md` (your daily notes)

## Important
- The `intel/` directory is symlinked to the shared workspace intel folder
""")

print("\nDone! All TOOLS.md files now use intel/ (symlinked) paths.")
