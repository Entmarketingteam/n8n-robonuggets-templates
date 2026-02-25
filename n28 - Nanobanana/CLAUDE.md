# n28 — Nanobanana (RoboNuggets)

## What This Is
Image creation and AI analysis agent using PromptRobo. Two variants covering 3 use cases each — standard and Pro.

## Files
- `(Template) Nanobanana 1 - 3 Use Cases by RoboNuggets _ n28.json` — Standard variant (20 nodes)
- `(Template) Nanobanana Pro - 3 Use Cases by RoboNuggets _ n28.json` — Pro variant

## Workflow Summary (Nanobanana 1, 20 nodes)
Nodes: `PromptRobo AI Agent` → `Create Image` → `Get Image` → `Wait` → `Switch` → `Download Img` → `Analyze Img` → `Get Img Path` → `Bot ID`
- PromptRobo agent generates or refines image prompts
- Creates image via image generation API
- Downloads and analyzes the result
- Switch handles 3 different use case branches

## How to Use
1. Import desired variant into n8n
2. Configure credentials: OpenAI (or PromptRobo), image generation API, Telegram Bot (for Bot ID node)
3. n28 is the base layer for R49 (MCP wrappers) — set up n28 before importing R49

## Notes
- n28 must be active before R49 MCP wrappers will work
- Pro variant likely has higher quality settings or additional use case branches
