# OpenClaw TradeDesk — 6-Agent AI Trading Signal Pipeline

A fully automated trading intelligence system built on [OpenClaw](https://openclaw.ai), using 6 specialized AI agents that coordinate through shared files on disk to produce daily forex/commodity trading signals delivered via Telegram.

Built by [Axidion](https://axidion.org).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TRADER (Telegram)                         │
│                         ↕                                    │
│                   Commander 👑                               │
│              Chief of Desk · Sonnet 4.5                      │
│         (Telegram interface + coordination)                  │
│                         │                                    │
│    ┌────────────────────┼────────────────────┐              │
│    ↓                    ↓                    ↓              │
│  Scout 🔭          Oracle 📊           Trigger ⚡          │
│  Haiku 4.5         Sonnet 4.5          Sonnet 4.5          │
│  Market Intel      Strategy Filter     Signal Gen           │
│    │                    │                    │              │
│    │              Sentinel 🛡️                │              │
│    │              Haiku 4.5                  │              │
│    │              Risk Manager               │              │
│    │                    │                    │              │
│    └────────────────────┼────────────────────┘              │
│                         ↓                                    │
│                   Herald 📲                                  │
│                   Haiku 4.5                                  │
│              Telegram Briefing                               │
└─────────────────────────────────────────────────────────────┘
```

### Pipeline Flow

```
Scout → intel/DAILY-INTEL.md
     → Oracle → intel/PLAYS.md
          → Trigger → intel/SIGNALS.md
               → Sentinel → intel/VETTED.md
                    → Herald → Telegram
```

No APIs between agents. No message queues. No orchestration framework. **Just files on disk.** Each agent writes its output to the shared `intel/` directory. The next agent reads it as input. Simple, debuggable, auditable.

---

## Agents

| Agent | Model | Cost (MTok) | Role |
|-------|-------|-------------|------|
| **Commander 👑** | Sonnet 4.5 | $3/$15 | Coordinator — talks to trader on Telegram, delegates to team, enforces quality |
| **Scout 🔭** | Haiku 4.5 | $1/$5 | Market research — browses finviz, Yahoo Finance, Google Finance for live prices and news |
| **Oracle 📊** | Sonnet 4.5 | $3/$15 | Strategy filter — matches intel against trader's 9 breakout-retest rules |
| **Trigger ⚡** | Sonnet 4.5 | $3/$15 | Signal generator — creates exact entry/SL/TP levels with R:R calculations |
| **Sentinel 🛡️** | Haiku 4.5 | $1/$5 | Risk manager — position sizing formulas, R:R filtering, daily loss limits |
| **Herald 📲** | Haiku 4.5 | $1/$5 | Telegram reporter — formats briefing, sends private + academy versions |

**Estimated cost**: ~$1.80/month per daily pipeline run. With ad-hoc Telegram interactions via Commander, ~$5-10/month total.

---

## Directory Structure

```
~/.openclaw/workspace/
├── SOUL.md                    # Commander identity and coordination logic
├── AGENTS.md                  # Pipeline orchestration rules
├── USER.md                    # Master trader profile (real data)
├── HEARTBEAT.md               # Self-healing cron health monitor
├── IDENTITY.md                # TradeDesk AI brand identity
├── TOOLS.md                   # Global tool reference
├── BOOTSTRAP.md               # First-run onboarding script
├── MEMORY.md                  # Commander long-term memory
├── openclaw.json.example      # Full config template (secrets stripped)
│
├── agents/
│   ├── scout/                 # 8 core files per agent:
│   │   ├── SOUL.md            #   Identity, principles, data sources with URLs
│   │   ├── AGENTS.md          #   Team awareness and pipeline position
│   │   ├── USER.md            #   Role-scoped trader data (instruments, sources)
│   │   ├── TOOLS.md           #   Available tools and file paths (intel/ symlink)
│   │   ├── IDENTITY.md        #   Display name and emoji
│   │   ├── HEARTBEAT.md       #   Health check config
│   │   ├── BOOTSTRAP.md       #   Boot instructions
│   │   ├── MEMORY.md          #   Long-term memory reference
│   │   └── memory/            #   Daily session notes (auto-generated)
│   ├── oracle/                #   (same 8 files + memory/)
│   ├── trigger/               #   (same 8 files + memory/)
│   ├── sentinel/              #   (same 8 files + memory/)
│   └── herald/                #   (same 8 files + memory/)
│
├── intel/                     # Shared pipeline directory (symlinked into each agent)
│   ├── DAILY-INTEL.md         # Scout → market research with live prices
│   ├── PLAYS.md               # Oracle → strategy-filtered setups
│   ├── SIGNALS.md             # Trigger → exact entry/SL/TP/RR signals
│   ├── VETTED.md              # Sentinel → risk-checked with position sizing
│   ├── BRIEFING.md            # Herald → formatted Telegram briefing
│   └── data/                  # Structured JSON snapshots
│       └── YYYY-MM-DD.json    #   Daily data for deduplication
│
├── memory/                    # Commander session memory
├── skills/                    # Custom skills (future)
└── scripts/                   # Setup and configuration scripts
```

### The 8 Core Files (Per Agent)

The original guide specified only `SOUL.md` and `AGENTS.md`. During setup, we discovered agents need **8 files** to function properly in the OpenClaw dashboard:

| File | Purpose |
|------|---------|
| `SOUL.md` | Agent identity, principles, and detailed instructions |
| `AGENTS.md` | Team awareness — who does what in the pipeline |
| `USER.md` | Role-scoped trader data (each agent gets different data) |
| `TOOLS.md` | Available tools and file paths (intel/ symlink noted) |
| `IDENTITY.md` | Display name and emoji for dashboard |
| `HEARTBEAT.md` | Health check schedule and stale-output detection |
| `BOOTSTRAP.md` | First-run onboarding conversation script |
| `MEMORY.md` | Long-term memory reference and patterns |

---

## Key Design Decisions (Learned During Setup)

### 1. Tool Permission System

OpenClaw's `"profile": "minimal"` gives agents almost no tools by default (just `session_status`). Each agent needs explicit tool grants via `"alsoAllow"`. **This was the #1 issue during setup** — Scout could browse the web but couldn't write files because `read`/`write` weren't in the minimal profile.

| Agent | Profile | Additional Tools |
|-------|---------|-----------------|
| Commander | `full` | Everything (all 23 tools) |
| Scout | `minimal` | `read`, `write`, `edit`, `exec`, `browser`, `web_search`, `web_fetch`, `memory_search`, `memory_get` |
| Oracle | `minimal` | `read`, `write`, `edit`, `exec`, `memory_search`, `memory_get` |
| Trigger | `minimal` | `read`, `write`, `edit`, `exec`, `memory_search`, `memory_get` |
| Sentinel | `minimal` | `read`, `write`, `edit`, `exec`, `memory_search`, `memory_get` |
| Herald | `minimal` | `read`, `write`, `edit`, `exec`, `memory_search`, `memory_get`, **`message`** |

Herald is the only sub-agent with the `message` tool — it's the only one that sends to Telegram.

### 2. Intel Directory Symlinks

Sub-agents have their workspace at `agents/{name}/` but the pipeline writes to `intel/` at the workspace root. **Agents can't write to paths outside their workspace.** The fix: symlink `intel/` into each agent's workspace:

```bash
for agent in scout oracle trigger sentinel herald; do
  ln -sf ~/.openclaw/workspace/intel ~/.openclaw/workspace/agents/$agent/intel
done
```

Now every agent can read/write `intel/DAILY-INTEL.md` using a relative path from their own workspace.

### 3. Scout's Data Sources

The original guide said "browse finviz.com" but didn't provide specific URLs for forex quotes. **Finviz only has stock/ETF quotes, not forex pairs.** Scout's SOUL.md now contains a 3-step data collection strategy:

**Step 1 — Prices (fetch FIRST):**
- Gold: `https://finviz.com/quote.ashx?t=GLD` (GLD ETF as XAUUSD proxy)
- DXY: `https://finviz.com/quote.ashx?t=UUP` (UUP ETF as DXY proxy)
- Forex: `https://finance.yahoo.com/quote/EURUSD=X/` (and USDJPY=X, GBPUSD=X, etc.)
- Fallbacks: `xe.com`, `google.com/finance/quote/EUR-USD`, `investing.com`

**Step 2 — News:** `https://finviz.com/news.ashx`

**Step 3 — Calendar:** `https://www.forexfactory.com/calendar`

### 4. Herald's Channel Enforcement

During the first automated pipeline run, Herald (Haiku model) attempted to send via WhatsApp instead of Telegram. **Smaller models can guess wrong about tool parameters.** Herald's SOUL.md now contains a `CRITICAL` section:

```
ALWAYS use channel=telegram when sending messages.
NEVER use whatsapp, discord, or any other channel.
```

The cron job message also explicitly states `channel=telegram, NOT whatsapp`.

### 5. Private vs Public Briefing Separation

Herald produces two versions of the briefing:

| Content | Private (Trader) | Public (Academy Channel) |
|---------|-----------------|-------------------------|
| Signals with entry/SL/TP | Yes | Yes |
| Position sizes (lots) | Yes | **Stripped** |
| Dollar risk amounts | Yes | **Stripped** |
| Account size | Yes | **Stripped** |
| Sentinel calculations | Yes | **Stripped** |
| R:R ratios | Yes | Yes |
| Setup thesis | Yes | Yes |
| Risk management reminders | Yes | Yes (emphasized) |

The academy channel has ~19,686 subscribers — they see professional analysis without portfolio details.

### 6. Position Sizing Formulas (Sentinel)

Sentinel uses different formulas for forex pairs vs Gold:

**Forex (standard lots):**
```
position_size_lots = (account_size × risk_pct) / (stop_distance_pips × pip_value)
```

**Gold (XAUUSD):**
```
position_size_lots = (account_size × risk_pct) / (stop_distance_points × 10)
```

Gold pip value = $10 per pip per standard lot. Gold typically has wider stops (200-400 pips on swings), so lot sizes are automatically smaller.

### 7. Cron Delivery Mode

OpenClaw cron jobs default to `"delivery": {"mode": "announce"}` which tries to post a summary to a chat session. **On first run, this fails with "cron delivery target is missing"** because there's no active chat session. Fix: set `--no-deliver` on all cron jobs. Herald handles its own Telegram delivery via the `message` tool.

---

## Prerequisites

- **OS**: Linux (Ubuntu 22.04+) or WSL2 (Ubuntu 24.04)
- **Node.js**: 22+ (`nvm install 22` or `fnm install 22`)
- **Anthropic API Key**: From [console.anthropic.com](https://console.anthropic.com)
- **Telegram Bot**: Created via [@BotFather](https://t.me/BotFather) — name it "TradeDesk AI"
- **Telegram User ID**: From [@userinfobot](https://t.me/userinfobot)
- **Telegram Channel ID**: Add bot to channel as admin, forward a message to @userinfobot

---

## Setup Guide

### Step 1: Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

During onboarding:
- Auth: Anthropic API key
- Model: `anthropic/claude-sonnet-4-5-20250929`
- Channels: skip (configure later)

### Step 2: Clone This Repo

```bash
mv ~/.openclaw/workspace ~/.openclaw/workspace-default
git clone https://github.com/Sensini7/OpenClaw-TradeDesk.git ~/.openclaw/workspace
cd ~/.openclaw/workspace
```

### Step 3: Configure Credentials

```bash
cp openclaw.json.example ~/.openclaw/openclaw.json
nano ~/.openclaw/openclaw.json
```

Replace these placeholders:

| Placeholder | Replace With |
|-------------|-------------|
| `YOUR_KEY_HERE` | Anthropic API key (`sk-ant-api03-...`) |
| `YOUR_BOT_TOKEN_HERE` | Bot token from @BotFather |
| `YOUR_TELEGRAM_USER_ID` | Your numeric Telegram user ID |

Also update the gateway auth token if needed (or keep the default).

### Step 4: Update Trader Profile

Edit `USER.md` (master) and each `agents/*/USER.md` with your trader's:
- Instruments and watchlist
- Strategy rules
- Risk parameters (account size, max risk %, etc.)
- Telegram chat ID and channel ID
- Signal format preferences

### Step 5: Create Intel Symlinks

```bash
cd ~/.openclaw/workspace
for agent in scout oracle trigger sentinel herald; do
  ln -sf ~/.openclaw/workspace/intel agents/$agent/intel
done
```

### Step 6: Restart Gateway and Verify

```bash
openclaw gateway restart
openclaw gateway status           # RPC probe: ok
openclaw channels status --probe  # Telegram: running
openclaw agents list              # All 6 agents visible
```

### Step 7: Test Pipeline Manually (End-to-End)

Run each agent in sequence and verify output:

```bash
# 1. Scout — fetches market data
openclaw agent --agent scout \
  --message "Run morning research. Read SOUL.md and USER.md. Fetch prices for all watchlist instruments. Write to intel/DAILY-INTEL.md and intel/data/YYYY-MM-DD.json."
cat intel/DAILY-INTEL.md  # Verify prices are NOT [UNAVAILABLE]

# 2. Oracle — filters against strategy
openclaw agent --agent oracle \
  --message "Read intel/DAILY-INTEL.md. Filter against strategy rules. Write to intel/PLAYS.md."
cat intel/PLAYS.md

# 3. Trigger — generates signals
openclaw agent --agent trigger \
  --message "Read intel/PLAYS.md. Generate signals with entry/SL/TP/RR. Write to intel/SIGNALS.md."
cat intel/SIGNALS.md

# 4. Sentinel — applies risk checks
openclaw agent --agent sentinel \
  --message "Read intel/SIGNALS.md. Apply position sizing and risk limits. Write to intel/VETTED.md."
cat intel/VETTED.md

# 5. Herald — sends Telegram briefing
openclaw agent --agent herald \
  --message "Read intel/VETTED.md and intel/DAILY-INTEL.md. Format briefing. Send using message tool with channel=telegram to chat ID YOUR_CHAT_ID."
```

### Step 8: Set Up Cron Jobs

```bash
# Scout — 6:00 AM ET (11:00 UTC)
openclaw cron add --name "scout-morning" --agent scout \
  --cron "0 11 * * 1-5" --tz "UTC" --exact --no-deliver \
  --timeout-seconds 180 \
  --message "Run your morning research sweep. Read your SOUL.md, USER.md, and TOOLS.md. Research all watchlist instruments (Gold/XAUUSD first). Write report to intel/DAILY-INTEL.md and data to intel/data/YYYY-MM-DD.json."

# Oracle — 6:15 AM ET (11:15 UTC)
openclaw cron add --name "oracle-filter" --agent oracle \
  --cron "15 11 * * 1-5" --tz "UTC" --exact --no-deliver \
  --timeout-seconds 180 \
  --message "Run strategy analysis. Read SOUL.md, USER.md, TOOLS.md, then intel/DAILY-INTEL.md. Filter against strategy rules. Write to intel/PLAYS.md."

# Trigger — 6:25 AM ET (11:25 UTC)
openclaw cron add --name "trigger-signals" --agent trigger \
  --cron "25 11 * * 1-5" --tz "UTC" --exact --no-deliver \
  --timeout-seconds 180 \
  --message "Run signal generation. Read SOUL.md, USER.md, TOOLS.md, then intel/PLAYS.md. Generate exact signals with entry/SL/TP/RR. Write to intel/SIGNALS.md."

# Sentinel — 6:30 AM ET (11:30 UTC)
openclaw cron add --name "sentinel-risk" --agent sentinel \
  --cron "30 11 * * 1-5" --tz "UTC" --exact --no-deliver \
  --timeout-seconds 180 \
  --message "Run risk check. Read SOUL.md, USER.md, TOOLS.md, then intel/SIGNALS.md and intel/DAILY-INTEL.md. Apply position sizing, R:R filters, risk limits. Write to intel/VETTED.md."

# Herald — 6:35 AM ET (11:35 UTC)
openclaw cron add --name "herald-briefing" --agent herald \
  --cron "35 11 * * 1-5" --tz "UTC" --exact --no-deliver \
  --timeout-seconds 120 \
  --message "Run briefing. Read SOUL.md, USER.md, TOOLS.md, then intel/VETTED.md and intel/DAILY-INTEL.md. Format briefing. Send using message tool with channel=telegram to chat ID YOUR_CHAT_ID. IMPORTANT: channel=telegram, NOT whatsapp."
```

Verify:
```bash
openclaw cron list
```

### Step 9: Test Telegram Bot

Message your bot: **"Who are you?"**

Commander should respond identifying itself and listing all 5 sub-agents.

---

## Cron Schedule

Weekdays only (Mon-Fri). Staggered so each agent's output is ready before the next runs.

| Agent | ET (EST) | UTC | WAT (Cameroon) | EDT (Mar-Nov) |
|-------|----------|-----|-----------------|----------------|
| Scout | 6:00 AM | 11:00 | 12:00 PM | 11:00 AM WAT |
| Oracle | 6:15 AM | 11:15 | 12:15 PM | 11:15 AM WAT |
| Trigger | 6:25 AM | 11:25 | 12:25 PM | 11:25 AM WAT |
| Sentinel | 6:30 AM | 11:30 | 12:30 PM | 11:30 AM WAT |
| Herald | 6:35 AM | 11:35 | 12:35 PM | 11:35 AM WAT |

> When the US switches to EDT (March-November), Cameroon time shifts 1 hour earlier since UTC stays the same but ET moves to UTC-4.

---

## Trader Profile

Currently configured for a forex/commodities swing trader:

- **Channel**: @axidiontradedeskmvp (~19,686 subscribers)
- **Academy**: FN Forex Academy (Douala & Buea, Cameroon + Dubai)
- **Primary Instrument**: XAUUSD (Gold)
- **Watchlist**: USDJPY, EURUSD, GBPUSD, USDCAD, GBPJPY, AUDUSD
- **Strategy**: Breakout-retest with trend confirmation (9 strict rules)
- **Risk**: 1% per trade, 3% max daily loss, 3 max concurrent
- **R:R Target**: 1:4 to 1:6 on swings, 1:2 minimum intraday
- **Broker**: Exness
- **Signal Format**: `BUY GOLD SL: 4457 TP: 4474 TP2:4479` (variable punctuation)

To customize for a different trader, update `USER.md` (master) and each agent's scoped `agents/*/USER.md`.

---

## Scripts

Setup scripts used during initial configuration (in `scripts/`):

| Script | Purpose |
|--------|---------|
| `setup-workspace.py` | Creates initial workspace files (SOUL.md, AGENTS.md for all agents) |
| `update-config.py` | Registers 6 agents in openclaw.json with model assignments |
| `fix-agents.py` | Adds MEMORY.md, IDENTITY.md, TOOLS.md for sub-agents (dashboard showed MISSING) |
| `complete-agent-files.py` | Creates USER.md, HEARTBEAT.md, BOOTSTRAP.md — completing the 8-file set |
| `populate-real-data.py` | Fills all USER.md files with real trader profile data from Supabase |
| `fix-tool-profiles.py` | Fixes minimal + alsoAllow permissions (Scout couldn't write files) |
| `fix-tools-paths.py` | Updates TOOLS.md to use `intel/` (symlinked) instead of `../../intel/` |
| `fix-scout-sources.py` | Adds Yahoo Finance, Google Finance, ForexFactory URLs for live forex quotes |
| `add-telegram.py` | Configures Telegram bot token and Commander binding in openclaw.json |
| `fix-herald-channel.py` | Adds explicit `channel=telegram` rule (Herald tried WhatsApp) |
| `update-herald-user.py` | Updates Herald's USER.md with real Telegram chat/channel IDs |

---

## Monitoring

```bash
# Check all cron jobs and their last status
openclaw cron list

# Check a specific job's run history
openclaw cron runs --id <job-id>

# Manually trigger a job (for testing)
openclaw cron run <job-id>

# Check gateway health
openclaw gateway status

# Check Telegram connection
openclaw channels status --probe

# View today's logs
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Read pipeline output
cat ~/.openclaw/workspace/intel/DAILY-INTEL.md
cat ~/.openclaw/workspace/intel/PLAYS.md
cat ~/.openclaw/workspace/intel/SIGNALS.md
cat ~/.openclaw/workspace/intel/VETTED.md
cat ~/.openclaw/workspace/intel/BRIEFING.md
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Scout returns `[UNAVAILABLE]` prices | SOUL.md missing forex URLs or web_fetch blocked | Verify SOUL.md has Yahoo Finance URLs; check `web_fetch` is in agent's `alsoAllow` |
| Herald sends via WhatsApp | Haiku model guessed wrong channel parameter | Update SOUL.md with `CRITICAL: ALWAYS use channel=telegram`; update cron message |
| Cron shows `"delivery target is missing"` | Default announce mode needs an active chat | Run `openclaw cron edit <id> --no-deliver` |
| Agent can't read/write files | `minimal` profile doesn't include file tools | Add `read`, `write`, `edit`, `exec` to agent's `alsoAllow` in openclaw.json |
| Gateway timeout on `cron run` | CLI timeout is 30s but agent takes 60-180s | Job is still running — check `openclaw cron list` after 2-3 minutes |
| Telegram "No response generated" | WSL2 network latency to Telegram API | Retry — WSL NAT layer adds latency. Not an issue on a real VPS |
| Dashboard shows MISSING files | Agent workspace missing one of the 8 core files | Run `scripts/complete-agent-files.py` to create all missing files |
| Intel files empty after Scout runs | Symlink not created for agent's intel/ directory | Run: `ln -sf ~/.openclaw/workspace/intel agents/scout/intel` |

---

## Production Deployment (VPS)

This setup runs on WSL for development. To deploy to a production VPS:

1. Provision an EC2 instance (minimum `t3.medium` / 4GB RAM)
2. Install Node.js 22+ and OpenClaw
3. Clone this repo to `~/.openclaw/workspace/`
4. Copy your `openclaw.json` with real credentials
5. Create intel symlinks
6. Set up cron jobs
7. Enable Tailscale for SSH access (never expose port 22)

On a VPS, the gateway runs 24/7 as a systemd service — no WSL networking quirks, no need to keep a laptop open.

---

## License

MIT

---

**Built with [OpenClaw](https://openclaw.ai) + [Anthropic Claude](https://anthropic.com) by [Axidion](https://axidion.org)**
