---
name: stock-first-pass
description: Run a fully autonomous 3-step first-pass on any stock or company to decide if it deserves deeper investing research. Use whenever the user mentions a ticker, company name, or stock idea in an investing context — phrases like "look at $TICKER", "what about [Company]", "is X worth a deep dive", "screen this name", "first pass on…", or just drops a ticker symbol with no other context. Pulls real SEC data via EdgarTools MCP, builds a Markdown 1-pager + full report + Excel financial model + NotebookLM source bundle, and updates the thesis tracker. Do not skip this skill just because the request is short — a bare ticker IS the trigger.
---

# Stock First-Pass Workflow (v4 — Autonomous)

**Ticker/Input:** $ARGUMENTS

A repeatable, mostly-autonomous workflow to decide if a stock deserves a real deep dive.
Built for Emily/Ethan's stack: Claude Code, EdgarTools MCP, n8n cloud, Doppler.

## Core principle

Goal: answer one question → **"Does this name deserve another 5+ hours of my time?"**

Most names should die at first pass. Killing fast IS the value.

## Inputs

A ticker, company name, or rough description. If ambiguous, resolve it yourself via web search — don't ask the user to clarify a ticker you can disambiguate.

## Tools to use (in priority order)

1. **EdgarTools MCP** — primary data source. ALWAYS try this first for any US-listed company. Tools you'll use:
   - `get_company_facts(ticker)` → structured XBRL financials
   - `get_filings(ticker, form="10-K", limit=1)` → latest annual
   - `get_filings(ticker, form="10-Q", limit=2)` → recent quarterlies
   - `get_filings(ticker, form="8-K", limit=10)` → recent material events
   - `get_filings(ticker, form="4", limit=20)` → insider transactions
   - `get_13f_holdings(ticker)` → who owns it (smart money signal)
   - `get_filings(ticker, form="DEF 14A", limit=1)` → proxy (comp + ownership)
2. **web_search / web_fetch** — for non-US names, recent news, competitor context, industry primers
3. **SEC EDGAR fallback** — if EdgarTools MCP is not connected, use the Python helper:
   `python3 "R53 - Stock Research Agent/scripts/sec_edgar.py" TICKER --output json`
   Or fetch raw EDGAR API via WebFetch (see references/edgartools-cheatsheet.md)
4. **bash_tool** — for building the Excel model (uses xlsx skill — read `/mnt/skills/public/xlsx/SKILL.md` first if available, else build via Python openpyxl)

If EdgarTools MCP is not connected (check tool list), tell user once, then fall back to web_search / sec_edgar.py and proceed. Don't block.

## Outputs (all four, every time)

### Output 1 — The 1-pager (Markdown, in chat)

Phone-scannable. Use this exact structure:

```
# [TICKER] — [Company Name]
*[One-sentence "what they do" — written for a smart non-expert]*

**The product in plain English**
[2–3 sentences. Physical/visual description. The "yellow safety layer in helmets" / "cow tissue inside humans" test.]

**Who pays them and why**
- Customer: [who literally writes the check]
- Pain solved: [what breaks if this product disappears tomorrow]
- Pricing model: [one-time / recurring / per-unit / royalty / etc.]

**How they make money**
- Revenue mix: [segments + %]
- Geography: [%]
- Gross margin profile: [+ why]

**Why they win (or don't)**
- Edge: [actual moat in one sentence]
- Edge strength: [strong / arguable / weak / none]

**Smart money signal** *(from 13F)*
- Top 3 institutional holders + recent direction (buying / selling / steady)
- Insider activity last 6 months (Form 4 net buys/sells)

**Quick stats** *(from EdgarTools XBRL or SEC EDGAR)*
- Market cap / Revenue (LTM) / Revenue growth / FCF margin / Net cash or debt / Insider ownership %
```

### Output 2 — The full first-pass report (Markdown file)

Save to `./theses/[TICKER]/report.md`. The five lenses are weighted equally:

1. **Business model & moat** — products, customers, pricing, real moat (IP/switching costs/scale/brand/network/regulatory/none), score honestly, name competitors
2. **Industry & competitive dynamics** — market structure, who has share + share-shifts, value chain position, who can squeeze them
3. **Unit economics & financials** — gross margin trend (5 yr from XBRL), operating leverage, FCF conversion, capital intensity, ROIC trend, balance sheet
4. **Management & capital allocation** — who runs it, tenure, comp structure (from DEF 14A), insider ownership %, last 5 yrs of capital allocation (buybacks at what price? M&A multiples? did it work?)
5. **Risks** — top 3 thesis-breakers ranked by probability x severity, with leading indicators

End with **Section 6: First-pass verdict** — exactly one of:
- **KILL** — doesn't meet bar (which lens failed?)
- **PARK** — interesting but waiting for X (name X + revisit trigger)
- **DEEP_DIVE** — worth 5+ hours (the 3 specific questions to answer next)

If >30% of names get DEEP_DIVE, the bar is too low.

### Output 3 — Excel financial model (.xlsx)

Save to `./theses/[TICKER]/model.xlsx`. Read `/mnt/skills/public/xlsx/SKILL.md` first if available.

Build minimum viable model:
- **Sheet 1: Historicals** — 5 yrs revenue, gross profit, EBIT, net income, FCF, shares (from `get_company_facts` XBRL)
- **Sheet 2: Ratios** — gross margin, EBIT margin, FCF margin, ROIC, revenue growth, all by year
- **Sheet 3: Quick valuation** — current EV, EV/Revenue, EV/EBIT, P/FCF — at consensus and at -20%/+20%
- **Sheet 4: Insiders** — net Form 4 transactions last 12 months by name

Don't build a full DCF on first pass — too much time, too much false precision. If verdict = DEEP_DIVE, note "build full DCF in next pass."

**Fallback:** If xlsx skill is unavailable, build as CSV to `./theses/[TICKER]/model.csv` with the same data.

### Output 4 — NotebookLM source bundle

Save to `./theses/[TICKER]/notebooklm.md`. Real, verified URLs only:
1. Latest 10-K (link to SEC filing)
2. Latest earnings call transcript
3. Investor presentation (if exists)
4. 1–2 high-quality independent write-ups (Substack, VIC, SA pro — not fluff)
5. 1 industry primer if niche
6. Company products page if physical/visual

For each: title, URL, why included, est. listen time. No invented links.

## Process

1. **Resolve the name** — confirm ticker. Web search if needed. Don't ask user.
2. **Pull SEC data** — via EdgarTools MCP first, fallback to sec_edgar.py or raw EDGAR API. Get facts, latest 10-K, 4 quarters of 10-Q, recent 8-Ks, last 20 Form 4s, latest 13F, latest DEF 14A.
3. **Web search for context** — competitors, recent news (last 90 days), one independent write-up
4. **Build the 1-pager first** — forces compression. If you can't write the plain-English product line cleanly, search more.
5. **Write the report** to `./theses/[TICKER]/report.md`
6. **Build the Excel model** to `./theses/[TICKER]/model.xlsx`
7. **Assemble NotebookLM bundle** to `./theses/[TICKER]/notebooklm.md`
8. **Update the thesis tracker** — append/update `./theses/_tracker.csv`
9. **Output JSON for n8n** — structured JSON as final output (see below)
10. **Deliver in chat**: 1-pager → file paths → verdict on its own line

## Thesis tracker

Maintain `./theses/_tracker.csv` with columns: `ticker,company,added_date,verdict,verdict_date,one_liner,next_review_date,notes`.

On every run, append or update the row for this ticker. Use atomic file operations:
1. Read existing `_tracker.csv`
2. Write to `_tracker.csv.tmp` with all rows + new/updated row
3. `mv _tracker.csv.tmp _tracker.csv` (atomic rename)

If the ticker already exists, update that row (don't duplicate).

## Output format (in-chat reply)

```
[1-pager content]

---

Files saved:
- ./theses/[TICKER]/report.md
- ./theses/[TICKER]/model.xlsx
- ./theses/[TICKER]/notebooklm.md

Thesis tracker updated: [TICKER] → [VERDICT]

**Verdict: [KILL / PARK / DEEP_DIVE]**
```

## n8n Integration — JSON output

After everything is complete, also output this JSON block as the **final message** so n8n can parse it from SSH stdout:

```json
{
  "status": "complete",
  "ticker": "[TICKER]",
  "company": "[company_name]",
  "verdict": "KILL|PARK|DEEP_DIVE",
  "one_liner": "[one-sentence thesis]",
  "one_pager": "[full 1-pager markdown — keep under 4000 chars for Telegram]",
  "report_path": "./theses/[TICKER]/report.md",
  "model_path": "./theses/[TICKER]/model.xlsx",
  "notebooklm_path": "./theses/[TICKER]/notebooklm.md",
  "deep_dive_needed": true|false,
  "insider_sentiment": "NET_BUY|NET_SELL|NEUTRAL",
  "key_metrics": {
    "revenue_ltm": "",
    "revenue_growth": "",
    "gross_margin": "",
    "fcf_margin": "",
    "net_cash_or_debt": "",
    "insider_ownership_pct": ""
  },
  "next_questions": ["question1 if DEEP_DIVE", "question2", "question3"],
  "next_review_date": "YYYY-MM-DD or null",
  "catalysts": ["catalyst1", "catalyst2"],
  "risks": ["risk1", "risk2"]
}
```

## What NOT to do

- Don't write generic "company overview" — every section serves the deserves-a-deep-dive question
- Don't pad with macro/ESG boilerplate
- Don't fabricate numbers — if XBRL doesn't have it, say "not in filings, verify" and move on
- Don't include unverified URLs in NotebookLM bundle
- Don't hedge the verdict. Pick one.
- Don't ask clarifying questions before v1 — start, user can redirect
- Don't build a full DCF on first pass — that's what DEEP_DIVE is for

## Reference files

- `references/edgartools-cheatsheet.md` — exact MCP tool calls for each data point
- `references/thesis-tracker.md` — tracker schema + update rules
- `references/n8n-blueprint.md` — Telegram → autonomous workflow setup
- `references/install.md` — Ethan's 30-minute setup guide
