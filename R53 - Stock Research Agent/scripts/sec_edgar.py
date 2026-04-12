#!/usr/bin/env python3
"""
SEC EDGAR Filing Fetcher for Stock Research Agent (R53)

Pulls filings from SEC EDGAR's public API with proper rate limiting.
Used as a helper for the Claude Code stock-first-pass skill.

Usage:
    python3 sec_edgar.py TICKER [--filings 10-K,10-Q,8-K,4,13F,DEF14A]
    python3 sec_edgar.py LMAT
    python3 sec_edgar.py LMAT --filings 10-K,10-Q --output json

Environment:
    SEC_EDGAR_USER_AGENT: Override default User-Agent (optional)

Rate Limiting:
    SEC EDGAR allows 10 requests/second. This script enforces 5/sec to be safe.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

EDGAR_BASE = "https://data.sec.gov"
EDGAR_ARCHIVES = "https://www.sec.gov/Archives/edgar/data"
EDGAR_BROWSE = "https://www.sec.gov/cgi-bin/browse-edgar"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

USER_AGENT = os.environ.get(
    "SEC_EDGAR_USER_AGENT",
    "RoboNuggets-Research/1.0 (research@robonuggets.com)"
)

FILING_TYPES = ["10-K", "10-Q", "8-K", "4", "SC 13F", "DEF 14A"]

# Rate limiting
_last_request_time = 0.0
_min_interval = 0.2  # 5 requests/sec max


def _rate_limit():
    """Enforce SEC EDGAR rate limits."""
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < _min_interval:
        time.sleep(_min_interval - elapsed)
    _last_request_time = time.time()


def fetch_url(url: str) -> dict | str:
    """Fetch a URL with proper headers and rate limiting."""
    _rate_limit()
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {url}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL error for {url}: {e.reason}", file=sys.stderr)
        return None


def ticker_to_cik(ticker: str) -> tuple[str, str, str]:
    """
    Look up CIK from ticker symbol.
    Returns (cik_padded, company_name, ticker_confirmed).
    """
    data = fetch_url(TICKERS_URL)
    if not data or not isinstance(data, dict):
        raise ValueError(f"Failed to fetch ticker list from SEC")

    ticker_upper = ticker.upper()
    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker_upper:
            cik = str(entry["cik_str"])
            cik_padded = cik.zfill(10)
            return cik_padded, entry.get("title", ""), entry.get("ticker", ticker_upper)

    raise ValueError(f"Ticker '{ticker}' not found in SEC EDGAR")


def get_submissions(cik_padded: str) -> dict:
    """Fetch company submissions (filing history) from EDGAR."""
    url = f"{EDGAR_BASE}/submissions/CIK{cik_padded}.json"
    data = fetch_url(url)
    if not data:
        raise ValueError(f"Failed to fetch submissions for CIK {cik_padded}")
    return data


def extract_filings(submissions: dict, form_types: list[str], max_per_type: int = 10) -> dict:
    """
    Extract filing metadata from submissions JSON.
    Returns dict: { form_type: [filing_info, ...] }
    """
    results = {ft: [] for ft in form_types}
    recent = submissions.get("filings", {}).get("recent", {})

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    cik = str(submissions.get("cik", "")).zfill(10)

    for i, form in enumerate(forms):
        for ft in form_types:
            if form == ft or (ft == "4" and form == "4") or (ft == "SC 13F" and "13F" in form):
                if len(results[ft]) >= max_per_type:
                    continue
                accession = accessions[i] if i < len(accessions) else ""
                accession_clean = accession.replace("-", "")
                primary_doc = primary_docs[i] if i < len(primary_docs) else ""
                filing_url = f"{EDGAR_ARCHIVES}/{cik}/{accession_clean}/{primary_doc}" if primary_doc else ""
                index_url = f"{EDGAR_ARCHIVES}/{cik}/{accession_clean}/{accession}-index.htm"

                results[ft].append({
                    "form": form,
                    "date": dates[i] if i < len(dates) else "",
                    "accession": accession,
                    "primary_doc": primary_doc,
                    "description": descriptions[i] if i < len(descriptions) else "",
                    "filing_url": filing_url,
                    "index_url": index_url,
                })

    return results


def get_company_facts(cik_padded: str) -> dict:
    """Fetch XBRL company facts (structured financial data) from EDGAR."""
    url = f"{EDGAR_BASE}/api/xbrl/companyfacts/CIK{cik_padded}.json"
    return fetch_url(url)


def extract_financials(facts: dict) -> dict:
    """Extract key financial metrics from XBRL company facts."""
    if not facts:
        return {}

    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    metrics = {}

    # Map of XBRL tags to human-readable names
    tag_map = {
        "Revenues": "revenue",
        "RevenueFromContractWithCustomerExcludingAssessedTax": "revenue",
        "SalesRevenueNet": "revenue",
        "NetIncomeLoss": "net_income",
        "EarningsPerShareDiluted": "eps_diluted",
        "EarningsPerShareBasic": "eps_basic",
        "GrossProfit": "gross_profit",
        "OperatingIncomeLoss": "operating_income",
        "CostOfGoodsAndServicesSold": "cogs",
        "CostOfRevenue": "cogs",
        "Assets": "total_assets",
        "Liabilities": "total_liabilities",
        "StockholdersEquity": "stockholders_equity",
        "LongTermDebt": "long_term_debt",
        "CashAndCashEquivalentsAtCarryingValue": "cash",
        "CommonStockSharesOutstanding": "shares_outstanding",
        "OperatingExpenses": "opex",
        "NetCashProvidedByUsedInOperatingActivities": "operating_cash_flow",
        "PaymentsToAcquirePropertyPlantAndEquipment": "capex",
    }

    for xbrl_tag, metric_name in tag_map.items():
        if xbrl_tag in us_gaap:
            units = us_gaap[xbrl_tag].get("units", {})
            # Get USD values (or shares for per-share metrics)
            for unit_type in ["USD", "USD/shares", "shares"]:
                if unit_type in units:
                    entries = units[unit_type]
                    # Filter to annual (10-K) filings and get most recent
                    annual = [e for e in entries if e.get("form") == "10-K"]
                    annual.sort(key=lambda x: x.get("end", ""), reverse=True)

                    if metric_name not in metrics:
                        metrics[metric_name] = []

                    for entry in annual[:5]:  # Last 5 years
                        metrics[metric_name].append({
                            "period_end": entry.get("end", ""),
                            "value": entry.get("val"),
                            "form": entry.get("form", ""),
                            "fiscal_year": entry.get("fy"),
                        })
                    break

    return metrics


def build_output(ticker: str, cik: str, company: str, submissions: dict,
                 filings: dict, financials: dict) -> dict:
    """Build structured output for Claude Code consumption."""
    company_info = {
        "ticker": ticker,
        "cik": cik,
        "company_name": company,
        "sic": submissions.get("sic", ""),
        "sic_description": submissions.get("sicDescription", ""),
        "state": submissions.get("stateOfIncorporation", ""),
        "fiscal_year_end": submissions.get("fiscalYearEnd", ""),
        "website": "",
        "phone": "",
    }

    # Get website/phone from submissions
    addresses = submissions.get("addresses", {})
    if isinstance(addresses, dict):
        business = addresses.get("business", {})
        if isinstance(business, dict):
            company_info["phone"] = business.get("phone", "")

    for url_entry in submissions.get("website", submissions.get("websites", [])):
        if isinstance(url_entry, str):
            company_info["website"] = url_entry
            break

    return {
        "company": company_info,
        "filings": {k: v for k, v in filings.items()},
        "financials": financials,
        "fetched_at": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch SEC EDGAR data for a stock ticker")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., LMAT)")
    parser.add_argument("--filings", default=",".join(FILING_TYPES),
                        help="Comma-separated filing types to fetch")
    parser.add_argument("--max-per-type", type=int, default=10,
                        help="Max filings per type (default: 10)")
    parser.add_argument("--output", choices=["json", "summary"], default="json",
                        help="Output format")
    parser.add_argument("--save", help="Save output to this file path")
    args = parser.parse_args()

    ticker = args.ticker.upper().replace("$", "")
    form_types = [f.strip() for f in args.filings.split(",")]

    print(f"Looking up {ticker} on SEC EDGAR...", file=sys.stderr)

    # Step 1: Ticker → CIK
    cik_padded, company_name, ticker_confirmed = ticker_to_cik(ticker)
    print(f"Found: {company_name} (CIK: {cik_padded})", file=sys.stderr)

    # Step 2: Get submissions
    submissions = get_submissions(cik_padded)

    # Step 3: Extract filing metadata
    filings = extract_filings(submissions, form_types, args.max_per_type)
    for ft, entries in filings.items():
        print(f"  {ft}: {len(entries)} filings found", file=sys.stderr)

    # Step 4: Get XBRL financial data
    print("Fetching XBRL financial data...", file=sys.stderr)
    facts = get_company_facts(cik_padded)
    financials = extract_financials(facts)
    print(f"  Extracted {len(financials)} financial metrics", file=sys.stderr)

    # Step 5: Build output
    output = build_output(ticker_confirmed, cik_padded, company_name,
                          submissions, filings, financials)

    output_json = json.dumps(output, indent=2, default=str)

    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        with open(args.save, "w") as f:
            f.write(output_json)
        print(f"Saved to {args.save}", file=sys.stderr)

    if args.output == "json":
        print(output_json)
    elif args.output == "summary":
        print(f"\n{'='*60}")
        print(f"  {ticker_confirmed} — {company_name}")
        print(f"  CIK: {cik_padded} | SIC: {submissions.get('sicDescription', 'N/A')}")
        print(f"{'='*60}")
        for ft, entries in filings.items():
            if entries:
                latest = entries[0]
                print(f"\n  Latest {ft}: {latest['date']}")
                print(f"    URL: {latest['filing_url']}")
        if financials:
            print(f"\n  Financial Metrics Available:")
            for metric, values in financials.items():
                if values:
                    latest = values[0]
                    print(f"    {metric}: {latest['value']:,.0f} (FY ending {latest['period_end']})")


if __name__ == "__main__":
    main()
