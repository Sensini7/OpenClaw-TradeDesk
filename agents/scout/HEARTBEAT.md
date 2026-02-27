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
