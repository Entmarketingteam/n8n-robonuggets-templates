# RoboNuggets Template Index

All RoboNuggets R-series and n-series n8n workflow templates in Downloads.

---

## Folders (have CLAUDE.md — open these dirs in Claude Code)

| Folder | What it Does |
|--------|-------------|
| `R50 - Template Pack/` | Cinematic Adverts System — image/video ad generation pipeline |
| `n29 Templates/` | Content repurposing via Telegram: TikTok→Sora, YT→LI/X, YT Short→Script |

---

## Standalone JSON Workflows

Import directly into n8n — no folder needed.

| File | ID | What it Does |
|------|----|-------------|
| `R28_LongForm_YouTube_Creator_Agent.json` | R28 | YouTube long-form creator agent (Google Sheets + OpenAI) |
| `R35 _ meetRobo.json` | R35 | meetRobo — Slack AI agent with Perplexity search + structured output |
| `Ultimate Extract by RoboNuggets (R46).json` | R46 | Ultimate Extract — pulls analytics from Meta Ads, TikTok, Instagram, YouTube → Google Sheets (42 nodes) |
| `R52 _ Longform AI Explainers System.json` | R52 | Longform AI Explainers — full production system with voice, AI agent, structured output (56 nodes) |
| `n1 - Instagram Infographic Agent by RoboNuggets.json` | n1 | Instagram Infographic Agent — scheduled, uses OpenAI 4o image gen + web search |
| `(Template) Nanobanana 1 - 3 Use Cases by RoboNuggets _ n28.json` | n28 | Nanobanana — image creation + analysis agent (PromptRobo) |
| `(Template) Nanobanana Pro - 3 Use Cases by RoboNuggets _ n28.json` | n28 Pro | Nanobanana Pro variant |
| `RoboNuggets - the new Blotato n8n node (n12).json` | n12 | Blotato n8n node integration |
| `n4___The_Downloader_Agent__tutorial.json` | n4 | Downloader Agent |
| `n4___The_Uploader_Agent__tutorial_.json` | n4 | Uploader Agent |

---

## Unpacked Zips (may need extraction)
- `R49 - Template Pack.zip` — not yet extracted

---

## Quick Notes
- All workflows are n8n exports — import via n8n UI > Workflows > Import from File
- R-series = full production systems (multi-step, 20-56 nodes)
- n-series = nano/focused single-purpose agents (7-20 nodes)
- Most require: OpenAI API, Telegram Bot, and platform-specific credentials
