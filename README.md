# RoboNuggets n8n Template Library

All RoboNuggets R-series and n-series n8n workflow templates, organized into folders with CLAUDE.md context files.

---

## All 11 Template Packs

| Folder | ID | What it Does | Nodes |
|--------|----|-------------|-------|
| `R28 - LongForm YouTube Creator Agent/` | R28 | YouTube long-form creator agent — Google Sheets input, OpenAI processing, error logging | 21 |
| `R35 - meetRobo/` | R35 | Slack AI agent with Perplexity search + structured output | 7 |
| `R46 - Ultimate Extract/` | R46 | Multi-platform analytics pull — Meta Ads, TikTok, Instagram, YouTube → Google Sheets | 42 |
| `R49 - Template Pack/` | R49 | MCP wrappers for Nanobanana 1, Nanobanana Pro, and Instagram posting via Blotato | 3×2 |
| `R50 - Template Pack/` | R50 | Cinematic Adverts System — image/video ad generation pipeline with scene processing | 46 |
| `R52 - Longform AI Explainers System/` | R52 | Full longform content pipeline — research, scripting, structuring, voice generation | 56 |
| `n1 - Instagram Infographic Agent/` | n1 | Scheduled infographic agent — web research → GPT-4o image gen → Instagram | 16 |
| `n4 - Downloader Uploader Agent/` | n4 | Companion download/upload agents for use in larger media pipelines | — |
| `n12 - Blotato Node/` | n12 | Blotato custom n8n node — required for Instagram posting in R49 and others | — |
| `n28 - Nanobanana/` | n28 | Image creation + analysis agent (PromptRobo) — standard and Pro variants | 20 |
| `n29 Templates/` | n29 | Content repurposing via Telegram: TikTok→Sora video, YT Long→LI/X post, YT Short→Script | 7–16 |

---

## Dependency Map

```
n12 (Blotato)  ←── required by R49 Instagram posting
n28 (Nanobanana) ←── required by R49 MCP wrappers
n4  (Downloader/Uploader) ←── used by n29, R50 pipelines
```

---

## Quick Start

1. Import any `.json` file via n8n UI → **Workflows → Import from File**
2. Configure credentials for the services each workflow uses
3. Open the folder in Claude Code — each has a `CLAUDE.md` with full details

## Credential Requirements by Workflow

| Workflow | Required Credentials |
|----------|---------------------|
| R28 | Google Sheets, YouTube Data API, OpenAI |
| R35 | Slack Bot, OpenAI, Perplexity API |
| R46 | Meta Ads API, TikTok API, Instagram Graph API, YouTube Data API, Google Sheets |
| R49 | Blotato API (+ n28 active) |
| R50 | Image/video generation API |
| R52 | OpenAI, ElevenLabs (voice) |
| n1 | OpenAI (GPT-4o), Instagram Graph API or Blotato |
| n4 | Apify API (`YOUR_APIFY_API_TOKEN` — replace before use) |
| n12 | Blotato API key |
| n28 | OpenAI, Telegram Bot |
| n29 | Telegram Bot, OpenAI, Sora API (workflow 1), LinkedIn + X (workflow 2) |

---

## Notes
- R-series = full production systems (21–56 nodes)
- n-series = focused single-purpose agents (2–20 nodes)
- Each folder has a `CLAUDE.md` — open the folder in Claude Code for full context
