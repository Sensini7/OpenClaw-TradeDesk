# AGENTS — Oracle Operating Rules

## When Triggered

1. Read `intel/DAILY-INTEL.md` (Scout's output for today)
2. Read `USER.md` from the workspace root for trader's strategy rules
3. For each instrument in Scout's report:
   - Check if the setup matches ANY rule in the trader's strategy
   - If yes: add to Valid Setups with confidence and reasoning
   - If no: add to Filtered Out with the specific reason
4. Write output to `intel/PLAYS.md`

## Confidence Levels

- **HIGH**: Multiple strategy rules align, strong structure, with-trend
- **MEDIUM**: Single rule match, decent structure, needs confirmation
- **WATCH**: Interesting but doesn't fully match — note but don't forward

## Memory
- Write daily notes to `agents/oracle/memory/YYYY-MM-DD.md`
- Track: which setups were approved/rejected and why
