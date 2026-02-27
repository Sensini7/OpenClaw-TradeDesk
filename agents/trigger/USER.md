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
