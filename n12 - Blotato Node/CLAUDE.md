# n12 — Blotato n8n Node (RoboNuggets)

## What This Is
Custom n8n node integration for Blotato — a social media posting service. Required by R49 (MCP Post to Instagram) and any workflow that posts to Instagram via Blotato.

## Files
- `RoboNuggets - the new Blotato n8n node (n12).json` — n8n workflow/node export

## What Blotato Does
Blotato is a social media API layer that simplifies posting to Instagram, TikTok, and other platforms without managing platform OAuth directly.

## How to Use
1. Import into n8n
2. Get a Blotato API key from blotato.com
3. Add Blotato credential in n8n (API key auth)
4. This node is then available for use in other workflows (R49 Instagram posting, etc.)

## Dependencies
- Required by: `R49 - Template Pack` (MCP Post to Instagram workflow)
- Required by: any workflow using Instagram posting via Blotato
