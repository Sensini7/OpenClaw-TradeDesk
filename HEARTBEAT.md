# HEARTBEAT — Self-Healing Monitor

## Cron Health Check (run on each heartbeat)

Check if any daily cron jobs have stale output (today's date
not present in the file). If stale, trigger them:

Jobs to monitor:
- Scout Morning (6:00 AM): check intel/DAILY-INTEL.md has today's date
- Oracle (6:15 AM): check intel/PLAYS.md has today's date
- Trigger (6:25 AM): check intel/SIGNALS.md has today's date
- Sentinel (6:30 AM): check intel/VETTED.md has today's date
- Herald (6:35 AM): verify briefing was sent

If a file is missing or stale for today (and it's after the
scheduled time), use `openclaw cron run <jobId> --force`
to re-trigger the agent.

## Outside market hours (after 4:30 PM ET)
Reply HEARTBEAT_OK
