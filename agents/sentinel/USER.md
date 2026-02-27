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
