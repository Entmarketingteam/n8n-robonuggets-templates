# Install Guide — 30 Minutes to Autonomous

For Ethan. Windows-friendly. Do these in order.

## Prerequisites (you already have)

- Claude Code installed and running via `cc` alias
- Doppler configured for `ent-agency-automation`
- n8n cloud at `entagency.app.n8n.cloud`
- A GitHub repo for research (or just create one — see Step 3)

## Step 1 — Install EdgarTools MCP (5 min)

Add to `claude_desktop_config.json` (or your Claude Code MCP config):

```json
{
  "mcpServers": {
    "edgartools": {
      "command": "uvx",
      "args": ["--from", "edgartools[ai]", "edgartools-mcp"],
      "env": {
        "EDGAR_IDENTITY": "Emily Atchley emily@entagency.com"
      }
    }
  }
}
```

Requires `uv`. If not installed:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart Claude Code. Verify with: ask Claude "list the EdgarTools tools you can call" — should return ~13 tools.

## Step 2 — Install the skill (2 min)

The skill lives at `.claude/commands/stock-first-pass.md` in this repo. If using a separate research repo, copy it there:

```powershell
mkdir -p .claude\commands
copy "R53 - Stock Research Agent\.claude\commands\stock-first-pass.md" .claude\commands\
```

Verify: in Claude Code, type `/stock-first-pass LMAT` — should appear as a command.

## Step 3 — Set up the research repo (5 min)

```powershell
cd C:\path\to\your\projects
git init research
cd research
mkdir theses
echo "theses/*/model.xlsx" > .gitignore  # don't version big binary models
echo "ticker,company,added_date,verdict,verdict_date,one_liner,next_review_date,notes" > theses/_tracker.csv
git add . && git commit -m "Init research repo"
```

Push to GitHub under the `Entmarketingteam` org if you want it backed up.

## Step 4 — Test the skill manually (5 min)

```powershell
cd C:\path\to\research
cc
```

Then in Claude Code:
```
first pass on $LMAT
```

Should produce:
- A 1-pager in chat
- `./theses/LMAT/report.md`
- `./theses/LMAT/model.xlsx`
- `./theses/LMAT/notebooklm.md`
- An updated `./theses/_tracker.csv`
- A verdict on its own line

If anything's broken, debug before moving to the bot.

## Step 5 — Stand up the Telegram bot (10 min)

1. **Create the bot:**
   - DM `@BotFather` on Telegram → `/newbot`
   - Name: "ENT Stock First-Pass Bot"
   - Username: `ent_stock_firstpass_bot` (or whatever's available)
   - Save the token

2. **Add token to Doppler:**
   ```bash
   doppler secrets set TELEGRAM_STOCK_BOT_TOKEN=<token> --project ent-agency-automation --config stock-bot
   doppler secrets set EDGAR_IDENTITY="Emily Atchley emily@entagency.com" --project ent-agency-automation --config stock-bot
   doppler secrets set ETHAN_TELEGRAM_ID=<your-tg-id> --project ent-agency-automation --config stock-bot
   ```
   (Get your TG ID from `@userinfobot`)

3. **Import the n8n workflow:**
   - Open n8n cloud → Workflows → Import from File
   - Select `R53_Stock_Research_Agent.json`
   - Replace placeholders, attach Telegram credential, save & activate

4. **Wire the executor:**
   - Easiest: SSH from n8n cloud to your dev machine (Option A in the blueprint)
   - Production: spin a $6/mo DO droplet (Option B), install `claude` + `uvx` + skill + clone the research repo to a persistent volume
   - Long-term: route via Hermes Agent gateway when your migration finishes

5. **Test:** open the bot in Telegram, send `$MIPS`. Should see the 1-pager + verdict come back within 2-3 min.

## Step 6 — Add the daily review cron (3 min, optional but high-leverage)

In n8n, duplicate the workflow → swap Telegram trigger for Cron node (7am daily) → swap "Parse Ticker" for a node that reads `_tracker.csv` and emits any tickers due for review → loop them through the same Trigger Claude Code → Telegram digest at the end.

This is the daily morning briefing that makes PARK verdicts actually useful.

## Troubleshooting

| Symptom | Fix |
|---|---|
| "EdgarTools tools not visible" | Restart Claude Code after editing MCP config; check `uvx` is in PATH |
| "EDGAR rate limited" | Set `EDGAR_IDENTITY` correctly — SEC requires real identity for higher limits |
| "Skill triggers but no files written" | Check working directory — skill writes to `./theses/[TICKER]/` relative to cwd |
| "n8n SSH execute fails" | Need an SSH key pair: generate on n8n side, add public key to dev machine's `~/.ssh/authorized_keys` |
| "Excel model is empty" | EdgarTools `get_company_facts` returned no XBRL — fall back to web scraping or skip the model on that ticker |

## What to skip

- Don't wire LSEG MCP unless you actually have a Refinitiv subscription
- Don't install all 5 of the equity research skills — they overlap. Start with just `stock-first-pass` + EdgarTools. Add more later if you need the 13F flow tracker as a separate workflow.

## After it works

The unlock is the **voice memo path**. Add a Telegram voice-message handler to the n8n flow → Whisper API → text → ticker extraction. Now you can drop a voice memo mid-set ("first pass on Hims, also check ELF Beauty") and have two reports waiting when you walk out of the gym.
