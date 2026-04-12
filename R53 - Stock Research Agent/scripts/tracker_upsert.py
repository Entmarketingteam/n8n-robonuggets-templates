#!/usr/bin/env python3
"""
Upsert a thesis row into ./theses/_tracker.csv

Usage:
    python tracker_upsert.py --ticker LMAT --company "LeMaitre Vascular" \
        --verdict DEEP_DIVE --one-liner "Niche peripheral vascular devices" \
        --notes "Q1 earnings 5/8"

Atomic write — safe to interrupt.
"""
import argparse
import csv
import os
import tempfile
from datetime import date, timedelta

TRACKER = "./theses/_tracker.csv"
FIELDS = ["ticker", "company", "added_date", "verdict", "verdict_date",
          "one_liner", "next_review_date", "notes"]

REVIEW_OFFSETS = {
    "KILL": None,
    "PARK": 90,
    "DEEP_DIVE": 30,
}


def calc_next_review(verdict: str, override: str | None) -> str:
    if override:
        return override
    days = REVIEW_OFFSETS.get(verdict)
    if days is None:
        return ""
    return (date.today() + timedelta(days=days)).isoformat()


def upsert(row: dict) -> str:
    os.makedirs("./theses", exist_ok=True)
    rows = []
    found = False

    if os.path.exists(TRACKER):
        with open(TRACKER, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["ticker"] == row["ticker"]:
                    # archive prior verdict
                    archive_history(r)
                    r.update({k: v for k, v in row.items() if v != ""})
                    found = True
                rows.append(r)

    if not found:
        rows.append(row)

    fd, tmp = tempfile.mkstemp(dir="./theses", suffix=".csv", text=True)
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, TRACKER)
    return "updated" if found else "added"


def archive_history(prior: dict) -> None:
    ticker_dir = f"./theses/{prior['ticker']}"
    os.makedirs(ticker_dir, exist_ok=True)
    hist_path = f"{ticker_dir}/history.csv"
    new = not os.path.exists(hist_path)
    with open(hist_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "verdict", "one_liner", "notes"])
        if new:
            w.writeheader()
        w.writerow({
            "date": prior.get("verdict_date", ""),
            "verdict": prior.get("verdict", ""),
            "one_liner": prior.get("one_liner", ""),
            "notes": prior.get("notes", ""),
        })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--company", required=True)
    ap.add_argument("--verdict", required=True, choices=["KILL", "PARK", "DEEP_DIVE"])
    ap.add_argument("--one-liner", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--next-review", default=None,
                    help="ISO date override; defaults applied per verdict")
    args = ap.parse_args()

    today = date.today().isoformat()
    row = {
        "ticker": args.ticker.upper(),
        "company": args.company,
        "added_date": today,
        "verdict": args.verdict,
        "verdict_date": today,
        "one_liner": args.one_liner,
        "next_review_date": calc_next_review(args.verdict, args.next_review),
        "notes": args.notes,
    }
    result = upsert(row)
    print(f"{result}: {row['ticker']} → {row['verdict']}")


if __name__ == "__main__":
    main()
