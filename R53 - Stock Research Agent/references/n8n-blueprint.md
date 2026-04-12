# n8n Workflow Blueprint: Telegram → Autonomous First-Pass → Verdict

This is the production loop. Drop a ticker in Telegram, get the verdict back. No desk time.

## Architecture

```
[Telegram Bot] → [n8n Webhook] → [Parse ticker] → [Trigger Claude Code]
                                                          ↓
                                        [Skill runs autonomously: SEC pull,
                                         report, model, NotebookLM bundle,
                                         tracker update — all in repo]
                                                          ↓
                                              [Read verdict + 1-pager]
                                                          ↓
                                  [Telegram reply with verdict + file links]
                                                          ↓
                                       [If DEEP_DIVE: also DM to Ethan]
```

## Why this stack

You already have it. n8n cloud at `entagency.app.n8n.cloud`, Doppler for secrets, Claude Code Channels (Telegram) already wired for dev access. The only new thing is one workflow.

## Workflow JSON

The full importable workflow lives at `R53_Stock_Research_Agent.json` in the parent directory. Import that into n8n cloud.

## The Claude Code invocation

The critical line is the `Trigger Claude Code` node. Three options:

### Option A: SSH to Ethan's dev machine (simplest)

```bash
ssh ethan@dev-machine 'cd /repo/research && doppler run -- claude --print -p "/stock-first-pass TICKER" --output-format json'
```

Pros: zero new infra. Cons: Ethan's machine has to be on. Needs SSH key from n8n cloud → dev machine (use Doppler-managed key).

### Option B: Run Claude Code in a DigitalOcean droplet (recommended for prod)

Spin a small droplet:
- Install `claude` CLI
- Install `uvx` and configure EdgarTools MCP
- Mount a persistent volume at `/repo/research` for the `theses/` folder
- Point n8n at it via SSH

This way the bot works even when Ethan's laptop is closed.

### Option C: Hermes Agent gateway (your stated migration target)

Once you've migrated to Hermes, route via Hermes' WhatsApp/Telegram unified gateway. Replace the Telegram Trigger with a Hermes webhook. Cleaner long-term.

## Output contract from skill

The skill emits a JSON block as its final output when invoked with `--output-format json`:

```json
{
  "status": "complete",
  "ticker": "LMAT",
  "company": "LeMaitre Vascular",
  "verdict": "DEEP_DIVE",
  "one_liner": "Niche peripheral vascular medical devices, biological tissue moat",
  "one_pager": "# LMAT — LeMaitre Vascular\n...",
  "files": [
    "./theses/LMAT/report.md",
    "./theses/LMAT/model.xlsx",
    "./theses/LMAT/notebooklm.md"
  ],
  "deep_dive_needed": true,
  "insider_sentiment": "NET_BUY",
  "key_metrics": {
    "revenue_ltm": "",
    "revenue_growth": "",
    "gross_margin": "",
    "fcf_margin": "",
    "net_cash_or_debt": "",
    "insider_ownership_pct": ""
  },
  "next_questions": ["question1", "question2", "question3"],
  "next_review_date": "2026-05-12",
  "catalysts": ["catalyst1", "catalyst2"],
  "risks": ["risk1", "risk2"]
}
```

## Doppler secrets needed

In project `ent-agency-automation`, add to a new config `stock-bot`:

| Secret | Purpose |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` | New bot from BotFather, dedicated to this |
| `EDGAR_IDENTITY` | `Emily Atchley emily@entagency.com` (SEC requires real identity) |
| `ANTHROPIC_API_KEY` | For Claude Code (already exists in your stack) |
| `ETHAN_TELEGRAM_ID` | For DEEP_DIVE alerts |
| `RESEARCH_REPO_PATH` | `/repo/research` or wherever `theses/` lives |

n8n pulls these via `doppler run -- n8n-trigger`.

## Telegram bot setup (5 min)

1. DM `@BotFather` on Telegram → `/newbot` → name it "ENT Stock Bot" or similar
2. Save the token to Doppler as `TELEGRAM_BOT_TOKEN`
3. In n8n cloud, create a new credential "stock-bot" with that token
4. Start the workflow → grab the webhook URL → `/setwebhook` via BotFather (or n8n's Telegram trigger handles this)
5. Test: send `$LMAT` to the bot, watch n8n execute

## Daily / weekly extensions (do these after v4 works)

Once the basic loop runs, layer on:

1. **Daily review trigger** — n8n cron at 7am: read `_tracker.csv`, find rows where `next_review_date <= today`, queue them for re-run, post summary to Telegram
2. **EdgarTools live monitor** — `edgar_monitor` watching all DEEP_DIVE tickers, pushes 8-K and Form 4 filings to Telegram in real time
3. **Weekly digest** — Sunday 8pm: post pipeline state (X in DEEP_DIVE, Y in PARK, Z killed this week)
4. **Voice memo input** — n8n Telegram trigger handles voice messages too — Whisper API → text → ticker extraction. Drop voice memo at the gym, get verdict by the time you finish your set.

That last one is the dream. Drop a voice memo mid-set ("first pass on Hims, also check ELF Beauty") and have two reports waiting when you walk out.
