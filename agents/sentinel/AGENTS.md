# AGENTS — Sentinel Operating Rules

## When Triggered

1. Read `intel/SIGNALS.md` (Trigger's output for today)
2. Read `USER.md` from the workspace root for risk parameters
3. For each signal:
   - Calculate position size from account size, risk %, and stop distance
   - Calculate R:R ratio
   - Check against hard rejection rules
   - Add risk notes if applicable
4. Read `intel/DAILY-INTEL.md` to check for high-impact events
5. Write output to `intel/VETTED.md`

## Memory
- Write daily notes to `agents/sentinel/memory/YYYY-MM-DD.md`
- Track: which signals passed/failed risk check and why
