# EdgarTools MCP Cheatsheet

Exact tool calls to grab everything needed for a first-pass. Run these in this order.

## 1. Company facts (XBRL — your financial spine)

```
get_company_facts(ticker="LMAT")
```

Returns structured XBRL: revenue, COGS, gross profit, OpInc, NetInc, FCF, shares outstanding, all by year/quarter. This is the source of truth for everything in the financials section. **Use this before scraping the 10-K text.**

## 2. Latest annual report

```
get_filings(ticker="LMAT", form="10-K", limit=1)
→ then .obj() on the result to get parsed sections
```

Pull these sections specifically:
- `Item 1` (Business) → product description, segments, competition
- `Item 1A` (Risk Factors) → for risks section, but be skeptical (boilerplate-heavy)
- `Item 7` (MD&A) → management's narrative on performance
- `Item 7A` (Quantitative risks) → currency, rates, commodity exposure

## 3. Recent quarterlies

```
get_filings(ticker="LMAT", form="10-Q", limit=2)
```

Use for: most recent quarter's revenue + segment trends. Compare to year-ago for growth.

## 4. Recent material events

```
get_filings(ticker="LMAT", form="8-K", limit=10)
```

Scan items reported. Flag: M&A, executive departures, guidance changes, restatements, lawsuits.

## 5. Insider transactions (Form 4)

```
get_filings(ticker="LMAT", form="4", limit=20)
```

For each: who, role, transaction code (P=open market buy, S=sale, A=award, M=option exercise, F=tax withholding). **Only P (and large open-market buys at non-trivial size) are real signal.** Awards and tax-withholding sales are noise.

Net it out: in last 12 months, did insiders deploy real cash to buy on the open market?

## 6. Institutional holdings (13F)

```
get_13f_holdings(ticker="LMAT")
```

Tier the holders (this matters):
- **Tier 1 (3.0–3.5x weight)**: Berkshire, Baupost, Pershing Square, Greenlight, Third Point, ValueAct, named superinvestors
- **Tier 2 (1.5–2.0x)**: Active fundamental funds (Capital Group, T. Rowe, Wellington, Fidelity active)
- **Tier 3 (0.5–1.0x)**: Active quants, hedge funds without strong public records
- **Tier 4 (0.0–0.5x)**: Index funds (Vanguard, BlackRock, State Street) — ignore, mechanical

Look at QoQ change for Tier 1 and Tier 2 — that's the smart money signal.

## 7. Proxy statement

```
get_filings(ticker="LMAT", form="DEF 14A", limit=1)
```

Pull:
- Executive comp table → are they paid for stock price, EPS, revenue, ROIC?
- Insider ownership table → CEO/founder skin in the game
- Director independence + tenure

Comp structure is the cheat code for "what will management actually do."

## 8. Live monitoring (optional, for watchlist names)

```
edgar_monitor(tickers=["LMAT", "MIPS"], forms=["8-K", "4"])
```

Real-time feed. Wire this into n8n if you want push alerts on watchlist filings.

## When EdgarTools fails

- **Foreign issuer (no SEC filings)**: fall back to web_search + fetch IR page directly
- **Recently IPO'd / no XBRL history**: use S-1 instead of 10-K (`form="S-1"`)
- **MCP not connected**: tell user once, fall back to web_search, proceed

## Data quality flags to surface in the report

- Revenue down for 3+ consecutive quarters
- Gross margin compression > 200bps YoY
- FCF negative while reported earnings positive
- Insider net selling > $5M in last 6 months with no offsetting buys
- Tier 1 holder reduced position > 25% QoQ
- 8-K "departure of principal officer" in last 12 months
- Auditor change in last 24 months

Any of these = call it out explicitly in the verdict. They don't auto-kill, but they shift the burden of proof.
