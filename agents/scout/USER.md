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
- DXY — USD index for correlation analysis (use UUP ETF as proxy)

## Market
- Forex and Commodities

## Data Sources — FETCH THESE IN ORDER

### 1. Forex Prices (MUST fetch — do not skip)
Use web_fetch tool on each of these Yahoo Finance URLs:
- `https://finance.yahoo.com/quote/EURUSD=X/` → EURUSD
- `https://finance.yahoo.com/quote/USDJPY=X/` → USDJPY
- `https://finance.yahoo.com/quote/GBPUSD=X/` → GBPUSD
- `https://finance.yahoo.com/quote/USDCAD=X/` → USDCAD
- `https://finance.yahoo.com/quote/GBPJPY=X/` → GBPJPY
- `https://finance.yahoo.com/quote/AUDUSD=X/` → AUDUSD

### 2. Gold Price (MUST fetch)
- `https://finviz.com/quote.ashx?t=GLD` → GLD ETF (Gold proxy)
- Note: GLD price is NOT the same as XAUUSD spot. Report GLD data and note it's a proxy.

### 3. DXY / USD Strength
- `https://finviz.com/quote.ashx?t=UUP` → UUP ETF (DXY proxy)

### 4. News Headlines
- `https://finviz.com/news.ashx` → filter for forex/gold/macro

### 5. Economic Calendar
- `https://www.forexfactory.com/calendar` → today's scheduled events

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
- Morning research must be ready by 11:00 UTC (cron trigger time)

## What Scout Does NOT Care About
- Strategy rules (Oracle's job)
- Position sizing (Sentinel's job)
- Telegram formatting (Herald's job)
- Entry/exit levels (Trigger's job)
