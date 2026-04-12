# R53 — Stock Research Agent

Fully autonomous stock research pipeline: Telegram trigger → Claude Code → SEC EDGAR + web research → Markdown report + financial model → Telegram verdict.

## Architecture

```
Telegram "$LMAT"
     ↓
n8n catches it → SSHes to Claude Code → triggers stock-first-pass skill
     ↓
Skill autonomously:
  • Pulls 10-K + 10-Qs + 8-Ks + Form 4s + 13F + DEF 14A from SEC EDGAR
  • Web searches competitors + news + analyst ratings
  • Builds Markdown report + CSV financial model
  • Updates _tracker.csv (atomic rename, no corruption)
     ↓
n8n reads JSON output → posts 1-pager + verdict back to Telegram
     ↓
If DEEP_DIVE verdict → DMs Ethan
```

## Files

| File | Purpose |
|------|---------|
| `R53_Stock_Research_Agent.json` | n8n workflow (import this) — 10 nodes |
| `scripts/sec_edgar.py` | Python helper for SEC EDGAR API (optional, skill can use WebFetch directly) |
| `_tracker.csv` | Research tracker — all tickers researched with verdicts |
| `reports/` | Generated Markdown reports (one per ticker per date) |
| `models/` | Generated CSV financial models (one per ticker per date) |

## Claude Code Skill

The core brain lives at `.claude/commands/stock-first-pass.md` (project-level command).

**Invoke:** `claude -p '/stock-first-pass LMAT'` or from n8n via SSH.

### What it does (7 phases):
1. **CIK Lookup** — Resolves ticker to SEC CIK via EDGAR API
2. **Pull SEC Filings** — 10-K, 10-Q, 8-K, Form 4, 13F, DEF 14A
3. **Web Research** — Competitors, analyst ratings, news, catalysts
4. **Build Report** — Full Markdown report with 10 sections
5. **Build Model** — CSV financial model with 3yr history + 2yr estimates
6. **Update Tracker** — Atomic CSV append (write tmp → rename)
7. **Output JSON** — Structured JSON for n8n to parse and post

### Verdicts:
- **BUY** — Clear opportunity at current levels
- **HOLD** — Good company, not compelling entry
- **PASS** — Not interesting, move on
- **DEEP_DIVE** — Interesting enough for full deep-dive model + thesis

## n8n Workflow Nodes

```
[Telegram Trigger] → [Extract Ticker] → [Send Ack] (parallel)
                                       → [SSH → Claude Code]
                                          → [Parse Claude Output]
                                             → [Success?]
                                                ├─ YES → [Format Message] → [Send Verdict] → [Deep Dive?]
                                                │                                              ├─ YES → [DM Ethan]
                                                │                                              └─ NO  → (done)
                                                └─ NO  → [Send Error]
```

## Setup & Configuration

### 1. n8n Credentials Needed
- **Telegram Bot** — Bot token from @BotFather
- **SSH** — Credentials to the machine running Claude Code CLI

### 2. Doppler Environment Variables
These should be configured in Doppler and available to the Claude Code machine:

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Claude API key for Claude Code |
| `SEC_EDGAR_USER_AGENT` | Custom User-Agent for SEC (optional, has default) |

### 3. Workflow Configuration (replace placeholders)
- `TELEGRAM_BOT_CREDENTIAL_ID` — Your n8n Telegram credential ID
- `SSH_CREDENTIAL_ID` — Your n8n SSH credential ID  
- `ETHAN_TELEGRAM_CHAT_ID` — Ethan's Telegram user ID for deep dive DMs
- `/path/to/n8n-robonuggets-templates` — Actual path to this repo on the Claude Code machine

### 4. SSH Machine Requirements
- Claude Code CLI installed and authenticated (`claude` command available)
- This repo cloned
- Python 3.10+ (for sec_edgar.py helper, optional)
- Internet access to SEC EDGAR and web search

## SEC EDGAR API Notes

- **Rate limit:** 10 req/sec (script enforces 5/sec to be safe)
- **User-Agent required:** SEC blocks requests without a proper User-Agent
- **CIK lookup:** `https://www.sec.gov/files/company_tickers.json`
- **Submissions:** `https://data.sec.gov/submissions/CIK{padded_cik}.json`
- **XBRL facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK{padded_cik}.json`
- **Filings archive:** `https://www.sec.gov/Archives/edgar/data/{cik}/`

## Usage

### From Telegram
Just send `$LMAT` (or any ticker with $ prefix) in the configured Telegram chat.

### Manual CLI
```bash
# Run the skill directly
claude -p '/stock-first-pass LMAT'

# Run just the SEC helper
python3 scripts/sec_edgar.py LMAT --output summary
python3 scripts/sec_edgar.py LMAT --output json --save reports/LMAT_raw.json
```

## Output Example

The skill outputs JSON that n8n parses:
```json
{
  "status": "complete",
  "ticker": "LMAT",
  "verdict": "DEEP_DIVE",
  "confidence": "HIGH",
  "thesis": "Niche medical device company with 80%+ gross margins...",
  "one_pager": "...(Telegram-formatted markdown)...",
  "deep_dive_needed": true
}
```
