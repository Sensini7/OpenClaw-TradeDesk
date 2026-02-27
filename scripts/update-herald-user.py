#!/usr/bin/env python3
"""Update Herald's USER.md with real Telegram credentials."""
import os

WORKSPACE = "/root/.openclaw/workspace"

herald_user = os.path.join(WORKSPACE, "agents/herald/USER.md")

content = """\
# USER — Herald's Reference (Delivery Preferences)

_This file tells Herald where and how to deliver the briefing._

## Telegram Delivery
- **Trader Chat ID**: 1804547199
- **Academy Channel ID**: -1003830825064
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
"""

with open(herald_user, "w") as f:
    f.write(content)

print("Updated Herald's USER.md with real Telegram IDs:")
print("  Trader Chat ID: 1804547199")
print("  Academy Channel ID: -1003830825064")
print("  (Note: prefixed with -100 for Telegram API supergroup format)")
