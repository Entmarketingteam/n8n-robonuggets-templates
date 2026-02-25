# R28 — LongForm YouTube Creator Agent (RoboNuggets)

## What This Is
n8n agent that processes YouTube long-form content using OpenAI and Google Sheets as a data source/output layer.

## Files
- `R28_LongForm_YouTube_Creator_Agent.json` — n8n workflow export (21 nodes)

## Workflow Summary
Key nodes: `Google Sheets` → `YouTube` → `OpenAI Chat Model` → `Structured Output Parser` → `Wait` → `Switch` → `Error Log`
- Reads creator/video data from Google Sheets
- Fetches YouTube video data
- Processes with OpenAI (structured output)
- Wait/Switch pattern for pacing and branching logic
- Error logging built in

## How to Use
1. Import `R28_LongForm_YouTube_Creator_Agent.json` into n8n
2. Configure credentials: Google Sheets, YouTube Data API, OpenAI
3. Set up your Google Sheet with the expected input columns
4. Activate and run
