# Claude Code — OpenClaw TradeDesk

## VPS Access

To run commands on the production VPS, use SSH:

```bash
ssh -i ~/.ssh/vps_tradedesk root@vps3296464.trouble-free.net "COMMAND HERE"
```

Example:
```bash
ssh -i ~/.ssh/vps_tradedesk root@vps3296464.trouble-free.net "cat /root/.openclaw/openclaw.json"
ssh -i ~/.ssh/vps_tradedesk root@vps3296464.trouble-free.net "openclaw gateway status"
ssh -i ~/.ssh/vps_tradedesk root@vps3296464.trouble-free.net "openclaw logs --max-bytes 50000"
```

**VPS:** `vps3296464.trouble-free.net`
**User:** `root`
**Key:** `~/.ssh/vps_tradedesk`

## Repository

- GitHub: `Sensini7/OpenClaw-TradeDesk`
- Deploy branch: triggers on push to `main`
- Workflow: `.github/workflows/deploy.yml`
