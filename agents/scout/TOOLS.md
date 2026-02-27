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
