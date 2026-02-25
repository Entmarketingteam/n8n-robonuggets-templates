# R46 — Ultimate Extract (RoboNuggets)

## What This Is
Multi-platform analytics extraction workflow. Pulls data from Meta Ads, TikTok, Instagram, YouTube, and YouTube Shorts and appends it all to Google Sheets.

## Files
- `Ultimate Extract by RoboNuggets (R46).json` — n8n workflow export (42 nodes)

## Workflow Summary
Platforms covered: `Meta Ads` · `TikTok` · `Instagram` · `YouTube` · `YouTube Shorts`
Pattern per platform: fetch data → `Edit Fields` (normalize) → `Append row in sheet` (Google Sheets)
- 42 nodes total — one pipeline per platform, unified output schema
- Useful for creator reporting, brand deal recaps, agency dashboards

## How to Use
1. Import `Ultimate Extract by RoboNuggets (R46).json` into n8n
2. Configure credentials for each platform: Meta Ads API, TikTok API, Instagram Graph API, YouTube Data API
3. Configure Google Sheets credential + set your target sheet/tab IDs in each append node
4. Run manually or put on a schedule

## ENT Agency Use Case
- Pull creator analytics across all platforms into one Google Sheet for brand reporting
- Feed into the LTK dashboard or Airtable for unified creator performance tracking
