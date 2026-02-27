#!/usr/bin/env python3
"""Populate all USER.md files with real trader profile data from Supabase."""
import os

WORKSPACE = "/root/.openclaw/workspace"


def write_file(relative_path: str, content: str) -> None:
    full_path = os.path.join(WORKSPACE, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  wrote {relative_path}")


print("=== Populating USER.md files with real trader data ===\n")

# ── COMMANDER (master USER.md) ──────────────────────────────────────
write_file("USER.md", """\
# USER — Trader Profile (Master)

_This is the master trader profile. Each sub-agent gets a scoped version._

## Trader Identity
- **Channel**: @axidiontradedeskmvp (Axidion TradeDesk MVP)
- **Academy**: FN Forex Academy — Douala & Buea, Cameroon + remote from Dubai
- **Subscribers**: ~19,686
- **Telegram Chat ID**: 1804547199
- **Academy Channel ID**: -1003830825064

## Market & Instruments
- **Market**: Forex and Commodities
- **Primary Instrument**: XAUUSD (Gold) — large pip targets (200-400 pips)
- **Watchlist**: XAUUSD, USDJPY, EURUSD, GBPUSD, USDCAD, GBPJPY, AUDUSD
- **Extended**: AUDNZD, EURAUD, AUDCAD, USDCHF, BTC/USD
- **Analysis Only**: DXY (USD correlation reference)
- **Broker**: Exness

## Trading Style
- **Style**: Swing and intraday trading
- **Methodology**: Breakout-retest with trend confirmation
- **Bias Source**: Weekly chart breakdowns (Tuesday sessions)
- **Entry Method**: Wait for lower timeframe confirmation after higher TF bias
- **Hold Duration**: Intraday to multi-day (up to 4+ days on swings)

## Strategy Rules (THE GOLD — agents apply these strictly)
1. Never trade against the trend
2. Wait for 1-hour candle confirmation before entry
3. Always wait for retest after breakout — no chasing
4. Use weekly chart breakdown for directional bias
5. Monitor DXY for USD pair correlation
6. Incorporate fundamental awareness (CPI, Fed, tariffs, NFP)
7. Use partial take profits (TP1 conservative, TP2 extended)
8. Move SL to breakeven after TP1 hit
9. Gold is primary instrument — gets priority attention

## Signal Format
- **Format**: ACTION INSTRUMENT SL: [price] TP: [price] / TP1: [price] TP2: [price]
- **Direction**: BUY/SELL in caps
- **SL**: Always provided (absolute price levels, not pips)
- **TP**: Sometimes omitted or marked "open" for runners
- **Entry Price**: Not specified (enter at market or on retest)
- **Punctuation**: Variable (SL:, SL;, SL., SL ) — parser must handle all

## Sample Signals (reference format)
- BUY USDJPY SL 152.591 TP1 153.179 TP2 153.418
- SELL EURUSD SL 1.19079 TP 1.16719
- BUY GOLD SL: 4457 TP: 4474 TP2:4479
- SELL GBPUSD SL 1.34572 TP 1.30344
- Buy EUR/USD SL 1.18629 TP 1.20167 1/6 RR
- BUY GOLD Sl: 4411 TP1: 4426 TP2: open

## Risk Management
- **Max Risk Per Trade**: 1% of account
- **Max Daily Loss**: 3%
- **Max Concurrent Trades**: 3
- **R:R Target**: 1:4 to 1:6 on swing trades
- **Risk Language**: "Manage your RISK!!", "Apply proper risk management", "AVOID LATE ENTRY"

## Schedule
- **Active Hours**: 07:00-17:00 UTC (peak: 07:00-15:00)
- **Tuesday 14:00 UTC**: Weekly chart breakdown sessions
- **Briefing Time**: 05:00 UTC
- **Timezone**: UTC
- **Live Events**: Zoom sessions during CPI/major news

## Content Tone
- High energy, motivational, celebratory
- Heavy emoji use (fire, rocket, chart emojis)
- Addresses community as "my beautiful people"
- Celebrates wins loudly with pip counts
- Acknowledges losses with recovery mindset ("we will recover")
- Strong African identity and freedom narrative

## Academy Structure
- Free public channel -> Free VIP (via Exness affiliate signup) -> Paid mentorship/Inner Circle
- Weekly Tuesday chart breakdowns, live Zoom sessions
- YouTube lessons, TikTok lives, one-on-one mentorship
- FundedNext partnership with giveaways
- Tagline: "We don't just teach — we build winners"

## Auto-broadcast
- **Auto-broadcast**: false (trader approves first for MVP)
""")

# ── SCOUT USER.md ───────────────────────────────────────────────────
write_file("agents/scout/USER.md", """\
# USER — Scout's Reference (What to Research)

_This file tells Scout which instruments and sectors to focus on._

## Watchlist Instruments (Priority Order)
1. **XAUUSD (Gold)** — PRIMARY instrument, always research first
2. USDJPY
3. EURUSD
4. GBPUSD
5. USDCAD
6. GBPJPY
7. AUDUSD

## Extended Watchlist (Monitor if time permits)
- AUDNZD, EURAUD, AUDCAD, USDCHF, BTC/USD

## Analysis-Only (Don't generate signals, just context)
- DXY — USD index for correlation analysis

## Market
- Forex and Commodities

## Data Sources Priority
1. finviz.com/news.ashx — headlines filtered by forex/commodities
2. finance.yahoo.com — pre-market quotes, futures, Gold price
3. Economic calendar — FOMC, CPI, NFP, tariff announcements
4. DXY movement — correlate with USD pairs

## What Scout Cares About
- Price action on Gold (XAUUSD) — always report this first
- DXY direction (affects all USD pairs on the watchlist)
- Major forex pair movements from the watchlist
- Macro events: CPI, Fed, NFP, tariffs (trader monitors these)
- Tuesday is chart breakdown day — flag any relevant weekly setups
- Pre-market movers from the watchlist
- Any breakout-retest setups forming on watchlist instruments

## Trading Hours Context
- Trader is active 07:00-17:00 UTC, peak 07:00-15:00
- Morning research must be ready by 05:00 UTC (briefing time)

## What Scout Does NOT Care About
- Strategy rules (Oracle's job)
- Position sizing (Sentinel's job)
- Telegram formatting (Herald's job)
- Entry/exit levels (Trigger's job)
""")

# ── ORACLE USER.md ──────────────────────────────────────────────────
write_file("agents/oracle/USER.md", """\
# USER — Oracle's Reference (Strategy Rules to Apply)

_This file tells Oracle the trader's exact strategy rules to filter against._

## Trading Style
- Swing and intraday trading
- Breakout-retest methodology with trend-following approach
- Holds swing trades for multiple days (up to 4+ days documented)

## Preferred Timeframes
- Weekly: directional bias (Tuesday breakdown sessions)
- Daily/4H: trend structure
- 1H: entry confirmation (must wait for 1H candle close)

## Strategy Rules (THE GOLD — apply these strictly)
1. **Never trade against the trend** — if Daily is bearish, only look for sells
2. **Wait for 1-hour candle confirmation** — no entering before the candle closes
3. **Always wait for retest after breakout** — no chasing breakouts
4. **Weekly chart breakdown for directional bias** — Tuesday sessions set the tone
5. **Monitor DXY for USD correlation** — if DXY is bullish, USD pairs should align
6. **Fundamental awareness** — CPI, Fed decisions, NFP, tariffs affect direction
7. **Partial take profits** — TP1 conservative, TP2 extended (or "open" for runners)
8. **Gold is primary** — XAUUSD setups get priority analysis and attention

## Preferred Setup Types
- Breakout + retest of key level
- Trend continuation after pullback
- Higher TF bias + lower TF confirmation entry

## R:R Requirements
- Target: 1:4 to 1:6 on swing trades
- Minimum acceptable: 1:2 for intraday
- Reject anything below 1:1.5

## What Oracle Cares About
- Does today's intel from Scout match ANY of the rules above?
- Is there a clear trend direction on higher timeframes?
- Are breakout-retest patterns forming on watchlist instruments?
- Confidence: HIGH (multiple rules align) or MEDIUM (single rule)
- Gold setups get automatic priority

## What Oracle Does NOT Care About
- Raw data gathering (Scout's job)
- Exact entry/SL/TP prices (Trigger's job)
- Position sizing (Sentinel's job)
""")

# ── TRIGGER USER.md ─────────────────────────────────────────────────
write_file("agents/trigger/USER.md", """\
# USER — Trigger's Reference (Signal Construction Preferences)

_This file tells Trigger how the trader wants signals structured._

## Signal Format (MUST match this pattern)
ACTION INSTRUMENT SL: [price] TP: [price] / TP1: [price] TP2: [price]

### Examples (from trader's actual signals):
- BUY USDJPY SL 152.591 TP1 153.179 TP2 153.418
- SELL EURUSD SL 1.19079 TP 1.16719
- BUY GOLD SL: 4457 TP: 4474 TP2:4479
- SELL GBPUSD SL 1.34572 TP 1.30344
- BUY GOLD Sl: 4411 TP1: 4426 TP2: open

## Entry Style
- Enter at market price or on retest (no entry price specified in signal)
- Wait for 1H candle confirmation before entry
- Always wait for retest after breakout — never chase

## Stop Loss Approach
- Based on structure invalidation (absolute price levels, NOT pips)
- Place SL below/above the key level (order block, breakout level)
- Move SL to breakeven after TP1 is hit

## Take Profit Targets
- **TP1**: Conservative target (partial exit)
- **TP2**: Extended target or "open" for runners
- Gold targets are large: 200-400 pip range on swings
- Forex pairs: standard pip range based on structure

## R:R Ratio
- Target: 1:4 to 1:6 on swing trades
- Minimum: 1:2 for intraday
- Always calculate and include R:R in signal

## What Trigger Cares About
- Oracle's valid setups (from intel/PLAYS.md)
- Exact price levels based on chart structure
- R:R ratio calculation for every signal
- Signal must match the format above exactly
- Gold gets priority and larger targets

## What Trigger Does NOT Care About
- Raw market data (Scout handled that)
- Whether the setup matches strategy (Oracle already filtered)
- Position sizing in $ or lots (Sentinel handles that)
- Telegram formatting (Herald handles that)
""")

# ── SENTINEL USER.md ────────────────────────────────────────────────
write_file("agents/sentinel/USER.md", """\
# USER — Sentinel's Reference (Risk Parameters)

_This file tells Sentinel the trader's risk rules for position sizing._

## Account Details
- **Broker**: Exness
- **Account Currency**: USD
- **Account Size**: $10,000 (default — update when trader confirms)

## Risk Rules (HARD LIMITS — never exceed)
- **Max Risk Per Trade**: 1% of account ($100 on $10k account)
- **Max Daily Loss**: 3% of account ($300 on $10k account)
- **Max Concurrent Positions**: 3
- **Minimum R:R**: 1.5:1 (reject anything below)

## High-Impact Day Rules
- FOMC / CPI / NFP days → reduce position size by 25%
- Check intel/DAILY-INTEL.md for economic calendar flags
- If Scout flags "HIGH IMPACT EVENT" → apply reduction automatically

## Position Sizing Formula
For forex (standard lots):
  position_size_lots = (account_size * risk_pct) / (stop_distance_pips * pip_value)

For Gold (XAUUSD):
  position_size_lots = (account_size * risk_pct) / (stop_distance_points * 10)

Note: Gold pip value = $10 per pip per standard lot (0.01 = 1 pip for gold)

## Gold-Specific Notes
- Gold has larger pip targets (200-400 pips on swings)
- Adjust lot size down for Gold to keep risk at 1%
- SL distances on Gold can be wide — always verify $ risk

## SL Update Tracking
- When trader sends "MOVE SL TO [price]" → recalculate risk
- After TP1 hit → SL moves to breakeven (risk = 0)

## What Sentinel Cares About
- Trigger's signals (from intel/SIGNALS.md)
- Account size and risk % to calculate position sizes
- R:R ratios to filter bad risk/reward
- Economic calendar for high-impact day adjustments
- Gold position sizing (different pip value calculation)

## What Sentinel Does NOT Care About
- Why the setup was chosen (Oracle decided that)
- Chart structure (Trigger determined levels)
- How to format the output (Herald handles that)
""")

# ── HERALD USER.md ──────────────────────────────────────────────────
write_file("agents/herald/USER.md", """\
# USER — Herald's Reference (Delivery Preferences)

_This file tells Herald where and how to deliver the briefing._

## Telegram Delivery
- **Trader Chat ID**: 1804547199
- **Academy Channel ID**: -1003830825064
- **Bot**: @Axidion_TradeDesk_bot
- **Auto-broadcast**: false (trader approves first for MVP)

## Briefing Preferences
- **Briefing Time**: 05:00 UTC
- **Timezone**: UTC
- **Max Message Length**: 4000 chars (Telegram limit)
- **Format**: Markdown with emojis for scannability

## Content Tone (Match the Trader's Voice)
- High energy, motivational, celebratory
- Heavy emoji use (fire, rocket, chart up/down, double exclamation)
- Address community as "my beautiful people"
- Celebrate wins loudly with pip counts
- Acknowledge losses with recovery mindset
- Include risk management reminder on every signal
- Common phrases: "Manage your RISK!!", "Apply proper risk management", "AVOID LATE ENTRY"
- Tagline: "We don't just teach — we build winners"

## Private vs Public Content
### Private briefing (trader chat ID: 1804547199):
- Full signals with position sizes, $ risk, lot sizes
- Account details, internal risk notes
- All Sentinel calculations visible
- SL update tracking and management signals

### Academy version (channel ID: -1003830825064):
- Strip: position sizes, account size, $ amounts, risk calculations
- Keep: setups, entry/SL/TP levels, R:R ratios, thesis
- Add: risk management reminders, "manage your risk" warnings
- Trader looks professional to ~19,686 subscribers
- Match the channel's motivational tone

## Signal Format for Academy Channel
ACTION INSTRUMENT
SL: [price]
TP1: [price]
TP2: [price]
R:R: [ratio]
[One-line thesis]
Manage your RISK!! Apply proper risk management.

## What Herald Cares About
- Sentinel's vetted signals (from intel/VETTED.md)
- Scout's macro context (from intel/DAILY-INTEL.md)
- Clean, scannable Telegram formatting
- Private vs public content separation
- Matching the trader's voice and tone

## What Herald Does NOT Care About
- Why setups were chosen (Oracle/Trigger handled that)
- Position math (Sentinel calculated everything)
- Raw market data (Scout gathered that)
""")


print("\n=== All 6 USER.md files populated with real data! ===")
print("\nSummary:")
print("  Commander USER.md  — full master profile (everything)")
print("  Scout USER.md      — instruments, watchlist, data sources")
print("  Oracle USER.md     — strategy rules, timeframes, R:R requirements")
print("  Trigger USER.md    — signal format, entry style, SL/TP preferences")
print("  Sentinel USER.md   — account size, risk %, position sizing formulas")
print("  Herald USER.md     — Telegram IDs, tone, private vs public format")
