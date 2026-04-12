# Thesis Tracker

Your backlog stops being a notes app. It becomes a database.

## File location

`./theses/_tracker.csv`

## Schema

```csv
ticker,company,added_date,verdict,verdict_date,one_liner,next_review_date,notes
LMAT,LeMaitre Vascular,2026-04-12,DEEP_DIVE,2026-04-12,"Niche peripheral vascular medical devices, biological tissue moat",2026-05-12,"Q1 earnings 5/8"
MIPS,MIPS AB,2026-04-12,PARK,2026-04-12,"Helmet brain protection licensing royalty model",2026-07-12,"Wait for Q2 royalty trend"
WHATEVER,Acme Co,2026-04-10,KILL,2026-04-10,"Roll-up with declining organic growth and rising debt",,"Don't revisit"
```

## Update rules

**On every skill run:**

1. Check if ticker exists in `_tracker.csv`
2. If new: append new row
3. If exists:
   - Update `verdict`, `verdict_date`, `one_liner`, `notes` with latest
   - Add a row to `./theses/[TICKER]/history.csv` so prior verdicts aren't lost: `date,verdict,one_liner,notes`
   - Recalculate `next_review_date` per rules below

## next_review_date rules

| Verdict | Default review |
|---|---|
| KILL | empty (don't revisit) |
| PARK | +90 days, or earlier if user specified an "X" trigger |
| DEEP_DIVE | +30 days (force a follow-up) |

If the report mentions a specific upcoming catalyst (earnings date, contract expiry, FDA decision), set `next_review_date` to that date instead.

## Folder structure

```
./theses/
├── _tracker.csv              ← master index
├── LMAT/
│   ├── report.md
│   ├── model.xlsx
│   ├── notebooklm.md
│   └── history.csv           ← prior verdicts
├── MIPS/
│   ├── report.md
│   ├── model.xlsx
│   ├── notebooklm.md
│   └── history.csv
└── ...
```

## How to query the tracker

The tracker is just CSV — Emily can open it in Excel, or you can answer questions like:

- "What's in DEEP_DIVE right now?" → filter `verdict == "DEEP_DIVE"`
- "What's due for review this week?" → filter `next_review_date` between today and +7 days
- "How many names did I kill last month?" → count `verdict == "KILL"` where `verdict_date` in last 30 days

When the user asks "what's in my pipeline?" or similar, read `_tracker.csv` and answer from it. Don't make up names.

## Implementation note

Use the `tracker_upsert.py` script in `scripts/` for atomic updates. It handles:
- Upsert logic (append or update)
- History archiving to `./theses/[TICKER]/history.csv`
- Automatic `next_review_date` calculation per verdict type
- Atomic file writes (temp file → rename)

```bash
python3 scripts/tracker_upsert.py --ticker LMAT --company "LeMaitre Vascular" \
    --verdict DEEP_DIVE --one-liner "Niche peripheral vascular devices" \
    --notes "Q1 earnings 5/8"
```
