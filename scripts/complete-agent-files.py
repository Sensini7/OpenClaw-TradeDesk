#!/usr/bin/env python3
"""Create all missing agent files: USER.md, HEARTBEAT.md, BOOTSTRAP.md for each sub-agent."""
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")


def write_file(relative_path: str, content: str) -> None:
    full_path = os.path.join(WORKSPACE, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  wrote {relative_path}")


print("=== Creating agent-specific USER.md files ===\n")

# ── SCOUT USER.md ────────────────────────────────────────────────────
write_file("agents/scout/USER.md", """\
# USER — Scout's Reference (What to Research)

_This file tells Scout which instruments and sectors to focus on._
_Sourced from the master USER.md at workspace root._

## Watchlist Instruments
- [Paste from master USER.md — e.g., EUR/USD, GBP/USD, XAUUSD, NVDA, SPY]

## Sectors to Monitor
- [e.g., forex, indices, tech stocks, commodities]

## Data Sources Priority
1. finviz.com/news.ashx — headlines filtered by instruments above
2. finviz.com/quote.ashx?t=TICKER — per-ticker data
3. finance.yahoo.com — pre-market quotes, futures
4. Economic calendar — FOMC, CPI, NFP, etc.

## What Scout Cares About
- Price action and volume on watchlist tickers
- Macro events that affect the trader's instruments
- Pre-market movers from the watchlist
- News headlines relevant to the trader's sectors

## What Scout Does NOT Care About
- Strategy rules (that's Oracle's job)
- Position sizing (that's Sentinel's job)
- Telegram formatting (that's Herald's job)
- Entry/exit levels (that's Trigger's job)
""")

# ── ORACLE USER.md ───────────────────────────────────────────────────
write_file("agents/oracle/USER.md", """\
# USER — Oracle's Reference (Strategy Rules to Apply)

_This file tells Oracle the trader's exact strategy rules._
_Sourced from the master USER.md at workspace root._

## Trading Style
- [day_trader / swing_trader — from master USER.md]

## Preferred Timeframes
- [e.g., 1H, 4H, Daily — from master USER.md]

## Strategy Rules (THE GOLD — apply these strictly)
[Paste the strategy_rules from master USER.md. These are the
trader's actual rules in their own words. Oracle filters
Scout's intel ONLY against these rules.]

Example rules:
- Looks for liquidity grabs below key levels before going long
- Prefers London session for entries
- Uses order blocks + fair value gaps as entry criteria
- Trades with the daily trend only
- Takes partials at 1:2 RR, lets runners ride to 1:3+

## Setup Types the Trader Uses
- [e.g., FVG + OB confluence, break of structure, liquidity sweep]

## What Oracle Cares About
- Does today's intel from Scout match ANY of the rules above?
- Confidence level: HIGH (multiple rules align) or MEDIUM (single rule)
- Filtered out tickers with specific reasoning

## What Oracle Does NOT Care About
- Raw data gathering (that was Scout's job)
- Exact entry/SL/TP prices (that's Trigger's job)
- Position sizing (that's Sentinel's job)
""")

# ── TRIGGER USER.md ──────────────────────────────────────────────────
write_file("agents/trigger/USER.md", """\
# USER — Trigger's Reference (Signal Construction Preferences)

_This file tells Trigger how the trader wants signals structured._
_Sourced from the master USER.md at workspace root._

## Entry Style
- [e.g., limit orders at key levels, market orders on confirmation]

## Stop Loss Approach
- Based on structure invalidation (not fixed % distance)
- [e.g., below the order block, below the liquidity sweep low]

## Take Profit Targets
- TP1: 1.5-2R (conservative, partial exit)
- TP2: 2.5-3R+ (extended, let-it-ride)
- [Adjust based on trader preference from master USER.md]

## Preferred Timeframes for Entry
- [e.g., 1H for entry refinement, 4H for structure]

## What Trigger Cares About
- Oracle's valid setups (from intel/PLAYS.md)
- Exact price levels based on chart structure
- R:R ratio calculation for every signal
- One-sentence thesis explaining the setup

## What Trigger Does NOT Care About
- Raw market data (Scout handled that)
- Whether the setup matches strategy (Oracle already filtered)
- Position sizing in $ or lots (Sentinel handles that)
- Telegram formatting (Herald handles that)
""")

# ── SENTINEL USER.md ─────────────────────────────────────────────────
write_file("agents/sentinel/USER.md", """\
# USER — Sentinel's Reference (Risk Parameters)

_This file tells Sentinel the trader's risk rules for position sizing._
_Sourced from the master USER.md at workspace root._

## Account Details
- **Account Size**: $[from master USER.md — e.g., 10000]
- **Broker**: [from master USER.md]
- **Account Currency**: USD

## Risk Rules (HARD LIMITS — never exceed)
- **Max Risk Per Trade**: [e.g., 1-2% of account]
- **Max Concurrent Positions**: [e.g., 3]
- **Max Single Position Size**: 20% of account value
- **Minimum R:R**: 1.5:1 (reject anything below)

## High-Impact Day Rules
- FOMC / CPI / NFP days → reduce position size by 25%
- Check intel/DAILY-INTEL.md for economic calendar

## Position Sizing Formula
position_size = (account_size * risk_pct) / stop_distance_in_dollars

## What Sentinel Cares About
- Trigger's signals (from intel/SIGNALS.md)
- Account size and risk % to calculate position sizes
- R:R ratios to filter bad risk/reward
- Economic calendar for high-impact day adjustments

## What Sentinel Does NOT Care About
- Why the setup was chosen (Oracle decided that)
- Chart structure (Trigger determined levels)
- How to format the output (Herald handles that)
""")

# ── HERALD USER.md ───────────────────────────────────────────────────
write_file("agents/herald/USER.md", """\
# USER — Herald's Reference (Delivery Preferences)

_This file tells Herald where and how to deliver the briefing._
_Sourced from the master USER.md at workspace root._

## Telegram Delivery
- **Trader Chat ID**: [from master USER.md — personal DM]
- **Academy Channel ID**: [from master USER.md — public channel]
- **Auto-broadcast**: false (trader approves first for MVP)

## Briefing Preferences
- **Briefing Time**: 7:00 AM ET
- **Timezone**: America/New_York
- **Max Message Length**: 4000 chars (Telegram limit)
- **Format**: Markdown with emojis for scannability

## Private vs Public Content
### Private briefing (trader only):
- Full signals with position sizes, $ risk, lot sizes
- Account details, internal risk notes
- All Sentinel calculations visible

### Academy version (public channel):
- Strip: position sizes, account size, $ amounts, risk notes
- Keep: setups, entry/SL/TP levels, R:R ratios, thesis
- Trader looks professional to subscribers

## What Herald Cares About
- Sentinel's vetted signals (from intel/VETTED.md)
- Scout's macro context (from intel/DAILY-INTEL.md)
- Clean, scannable Telegram formatting
- Private vs public content separation

## What Herald Does NOT Care About
- Why setups were chosen (Oracle/Trigger handled that)
- Position math (Sentinel calculated everything)
- Raw market data (Scout gathered that)
""")


print("\n=== Creating agent-specific HEARTBEAT.md files ===\n")

# ── HEARTBEAT files ──────────────────────────────────────────────────
write_file("agents/scout/HEARTBEAT.md", """\
# HEARTBEAT — Scout 🔭

## Health Check
- Verify `intel/DAILY-INTEL.md` exists and contains today's date
- Verify `intel/data/YYYY-MM-DD.json` exists for today
- If missing and it's after 6:15 AM ET: flag as STALE

## Self-Check
- Can you access finviz.com? Try browsing the news page.
- Can you read USER.md from the workspace root?
- Can you write to intel/DAILY-INTEL.md?

## Outside market hours (after 4:30 PM ET or weekends)
Reply HEARTBEAT_OK
""")

write_file("agents/oracle/HEARTBEAT.md", """\
# HEARTBEAT — Oracle 📊

## Health Check
- Verify `intel/PLAYS.md` exists and contains today's date
- If missing and it's after 6:30 AM ET: flag as STALE
- Check that `intel/DAILY-INTEL.md` (input) also exists

## Self-Check
- Can you read intel/DAILY-INTEL.md?
- Can you read USER.md from the workspace root?
- Can you write to intel/PLAYS.md?

## Outside market hours (after 4:30 PM ET or weekends)
Reply HEARTBEAT_OK
""")

write_file("agents/trigger/HEARTBEAT.md", """\
# HEARTBEAT — Trigger ⚡

## Health Check
- Verify `intel/SIGNALS.md` exists and contains today's date
- If missing and it's after 6:40 AM ET: flag as STALE
- Check that `intel/PLAYS.md` (input) also exists

## Self-Check
- Can you read intel/PLAYS.md?
- Can you write to intel/SIGNALS.md?

## Outside market hours (after 4:30 PM ET or weekends)
Reply HEARTBEAT_OK
""")

write_file("agents/sentinel/HEARTBEAT.md", """\
# HEARTBEAT — Sentinel 🛡️

## Health Check
- Verify `intel/VETTED.md` exists and contains today's date
- If missing and it's after 6:45 AM ET: flag as STALE
- Check that `intel/SIGNALS.md` (input) also exists

## Self-Check
- Can you read intel/SIGNALS.md?
- Can you read USER.md from the workspace root?
- Can you write to intel/VETTED.md?

## Outside market hours (after 4:30 PM ET or weekends)
Reply HEARTBEAT_OK
""")

write_file("agents/herald/HEARTBEAT.md", """\
# HEARTBEAT — Herald 📲

## Health Check
- Verify today's briefing was sent (check memory for send confirmation)
- If not sent and it's after 7:00 AM ET: flag as STALE
- Check that `intel/VETTED.md` (input) exists

## Self-Check
- Can you read intel/VETTED.md?
- Can you read intel/DAILY-INTEL.md?
- Is the Telegram message tool available?

## Outside market hours (after 4:30 PM ET or weekends)
Reply HEARTBEAT_OK
""")


print("\n=== Creating agent-specific BOOTSTRAP.md files ===\n")

# ── BOOTSTRAP files ──────────────────────────────────────────────────
write_file("agents/scout/BOOTSTRAP.md", """\
# BOOTSTRAP — Scout 🔭 First Run

_This file runs on your first session. After completing, it can be deleted._

## Introduction
You are **Scout 🔭**, the Market Intelligence agent for TradeDesk by Axidion.
Your job: research markets, gather data, write structured intel reports.

## First Run Checklist
1. Read your SOUL.md — confirm you understand your role
2. Read USER.md — confirm you know the trader's instruments
3. Verify you can access the browser tool
4. Try browsing https://finviz.com/news.ashx — confirm it loads
5. Write a test file to `intel/DAILY-INTEL.md` with placeholder data
6. Confirm: "Scout 🔭 ready. Instruments loaded. Browser working."

## After Bootstrap
- Your cron job runs at 6:00 AM ET Mon-Fri
- You can also be triggered manually by Commander
- Always write to intel/DAILY-INTEL.md and intel/data/YYYY-MM-DD.json
""")

write_file("agents/oracle/BOOTSTRAP.md", """\
# BOOTSTRAP — Oracle 📊 First Run

_This file runs on your first session. After completing, it can be deleted._

## Introduction
You are **Oracle 📊**, the Strategy Analyst for TradeDesk by Axidion.
Your job: filter Scout's intel against the trader's strategy rules.

## First Run Checklist
1. Read your SOUL.md — confirm you understand your role
2. Read USER.md — confirm you know the trader's strategy rules
3. Verify you can read from intel/DAILY-INTEL.md (Scout's output)
4. Verify you can write to intel/PLAYS.md
5. Confirm: "Oracle 📊 ready. Strategy rules loaded. Pipeline input accessible."

## After Bootstrap
- Your cron job runs at 6:15 AM ET Mon-Fri (after Scout)
- You can also be triggered manually by Commander
- Always write to intel/PLAYS.md
""")

write_file("agents/trigger/BOOTSTRAP.md", """\
# BOOTSTRAP — Trigger ⚡ First Run

_This file runs on your first session. After completing, it can be deleted._

## Introduction
You are **Trigger ⚡**, the Signal Generator for TradeDesk by Axidion.
Your job: convert Oracle's valid plays into exact, actionable trade signals.

## First Run Checklist
1. Read your SOUL.md — confirm you understand your role
2. Read USER.md — confirm you know the trader's entry/SL/TP preferences
3. Verify you can read from intel/PLAYS.md (Oracle's output)
4. Verify you can write to intel/SIGNALS.md
5. Confirm: "Trigger ⚡ ready. Signal format understood. Pipeline input accessible."

## After Bootstrap
- Your cron job runs at 6:25 AM ET Mon-Fri (after Oracle)
- You can also be triggered manually by Commander
- Always write to intel/SIGNALS.md
""")

write_file("agents/sentinel/BOOTSTRAP.md", """\
# BOOTSTRAP — Sentinel 🛡️ First Run

_This file runs on your first session. After completing, it can be deleted._

## Introduction
You are **Sentinel 🛡️**, the Risk Manager for TradeDesk by Axidion.
Your job: calculate position sizes, check R:R ratios, reject bad risk.

## First Run Checklist
1. Read your SOUL.md — confirm you understand your role
2. Read USER.md — confirm you know the account size and risk parameters
3. Verify you can read from intel/SIGNALS.md (Trigger's output)
4. Verify you can write to intel/VETTED.md
5. Test: calculate position size for a $10,000 account, 1% risk, $5 stop distance
   → Expected: 20 shares. Confirm your math is correct.
6. Confirm: "Sentinel 🛡️ ready. Risk parameters loaded. Math verified."

## After Bootstrap
- Your cron job runs at 6:30 AM ET Mon-Fri (after Trigger)
- You can also be triggered manually by Commander
- Always write to intel/VETTED.md
""")

write_file("agents/herald/BOOTSTRAP.md", """\
# BOOTSTRAP — Herald 📲 First Run

_This file runs on your first session. After completing, it can be deleted._

## Introduction
You are **Herald 📲**, the Telegram Reporter for TradeDesk by Axidion.
Your job: format vetted signals into clean Telegram briefings.

## First Run Checklist
1. Read your SOUL.md — confirm you understand your role
2. Read USER.md — confirm you know the Telegram chat ID and format prefs
3. Verify you can read from intel/VETTED.md (Sentinel's output)
4. Verify you can read from intel/DAILY-INTEL.md (macro context)
5. Verify the Telegram message tool is available
6. Confirm: "Herald 📲 ready. Telegram configured. Briefing template loaded."

## After Bootstrap
- Your cron job runs at 6:35 AM ET Mon-Fri (after Sentinel)
- You can also be triggered manually by Commander
- Always read VETTED.md + DAILY-INTEL.md, format, and send via Telegram
""")


print("\n=== All 15 files created! ===")
print("\nSummary:")
print("  5x USER.md    — agent-specific trader data scoped to each role")
print("  5x HEARTBEAT.md — agent-specific health checks")
print("  5x BOOTSTRAP.md — first-run checklists per agent")
