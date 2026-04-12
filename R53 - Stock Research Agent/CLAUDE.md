# R53 — Stock Research Agent

Fully autonomous stock research pipeline. Drop a ticker in Telegram, get a KILL/PARK/DEEP_DIVE verdict on your phone.

**Core question:** "Does this name deserve another 5+ hours of my time?" Most names should die at first pass. Killing fast IS the value.

## Architecture

```
Telegram "$LMAT"
     ↓
n8n catches it → SSHes to Claude Code → triggers /stock-first-pass skill
     ↓
Skill autonomously (via EdgarTools MCP + web search):
  1. Resolves ticker → pulls XBRL company facts
  2. Fetches 10-K, 10-Q, 8-K, Form 4, 13F, DEF 14A
  3. Web searches competitors, news, analyst ratings
  4. Builds 1-pager (phone-scannable, in chat)
  5. Writes full report (5 lenses + verdict) → theses/[TICKER]/report.md
  6. Builds Excel financial model → theses/[TICKER]/model.xlsx
  7. Assembles NotebookLM source bundle → theses/[TICKER]/notebooklm.md
  8. Updates thesis tracker (atomic CSV upsert)
  9. Outputs JSON for n8n
     ↓
n8n posts 1-pager + verdict to Telegram
     ↓
If DEEP_DIVE → DMs Ethan with thesis + next questions
```

## Files

| File | Purpose |
|------|---------|
| `R53_Stock_Research_Agent.json` | n8n workflow — import into n8n cloud |
| `scripts/sec_edgar.py` | SEC EDGAR API helper (fallback if EdgarTools MCP unavailable) |
| `scripts/tracker_upsert.py` | Atomic CSV upsert with history archiving |
| `theses/_tracker.csv` | Master thesis tracker — all tickers with verdicts |
| `theses/[TICKER]/` | Per-ticker output (report.md, model.xlsx, notebooklm.md, history.csv) |
| `references/edgartools-cheatsheet.md` | Exact EdgarTools MCP tool calls for each data point |
| `references/thesis-tracker.md` | Tracker schema, update rules, query examples |
| `references/n8n-blueprint.md` | Full n8n architecture + execution options (SSH/DO/Hermes) |
| `references/install.md` | Ethan's 30-minute setup guide (Windows-friendly) |

## Claude Code Skill

The skill lives at `.claude/commands/stock-first-pass.md` (project-level command).

**Invoke:** `/stock-first-pass LMAT` or `first pass on $LMAT`

### Verdicts (pick exactly one):
- **KILL** — doesn't meet bar. Which lens failed? Don't revisit.
- **PARK** — interesting but waiting for X. Set review date + trigger.
- **DEEP_DIVE** — worth 5+ hours. Name the 3 questions to answer next.

If >30% of names get DEEP_DIVE, the bar is too low.

### 4 outputs every run:
1. **1-pager** — phone-scannable, in chat
2. **Full report** — 5 lenses (business/moat, industry, financials, management, risks) + verdict
3. **Excel model** — 4 sheets (historicals, ratios, quick valuation, insiders)
4. **NotebookLM bundle** — verified URLs for deep reading

### Data sources (priority order):
1. EdgarTools MCP (primary — structured XBRL, filings, 13F, Form 4)
2. web_search / web_fetch (competitors, news, non-US names)
3. sec_edgar.py fallback (if MCP unavailable)

## Stack

- **n8n cloud** at `entagency.app.n8n.cloud`
- **Doppler** for secrets (`ent-agency-automation` project, `stock-bot` config)
- **Claude Code CLI** on execution machine
- **EdgarTools MCP** for SEC data
- **Telegram Bot** for input/output

## Quick Start

See `references/install.md` for the full 30-minute setup.

```bash
# Test the skill directly
claude -p '/stock-first-pass LMAT'

# Test the SEC helper
python3 scripts/sec_edgar.py LMAT --output summary

# Test the tracker
python3 scripts/tracker_upsert.py --ticker LMAT --company "LeMaitre Vascular" \
    --verdict DEEP_DIVE --one-liner "Niche vascular devices"
```

## Future Extensions

1. **Daily review cron** — 7am: re-run PARK names past their review date
2. **EdgarTools live monitor** — real-time 8-K/Form 4 alerts on DEEP_DIVE tickers
3. **Weekly digest** — Sunday pipeline summary
4. **Voice memo input** — Whisper → ticker extraction → verdict by end of gym set

## Note on Repo Organization

This system is architected to work as a standalone repo. If/when it graduates from this template library, the portable pieces are:
- `.claude/commands/stock-first-pass.md` (the skill)
- `scripts/` (helper scripts)
- `references/` (documentation)
- `theses/` (output directory + tracker)
- The n8n workflow JSON imports independently
