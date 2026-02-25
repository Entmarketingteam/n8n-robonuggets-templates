# n4 — Downloader & Uploader Agent (RoboNuggets)

## What This Is
Two companion n8n workflows for downloading and uploading content as part of automated media pipelines.

## Files
- `n4___The_Downloader_Agent__tutorial.json` — Downloads media from a URL
- `n4___The_Uploader_Agent__tutorial_.json` — Uploads media to a destination

## How to Use
1. Import both JSON files into n8n
2. These are typically used as sub-workflows called by larger pipelines (e.g., R50 Cinematic Adverts, n29 repurposing workflows)
3. Configure storage credentials as needed (S3, Google Drive, etc.)
4. Can be triggered standalone or chained into other workflows via Execute Workflow nodes

## Notes
- Tutorial versions — may include sticky note annotations explaining each step
- Pair with n29 or R50 for full download → process → upload pipelines
