# R50 — Cinematic Adverts System (RoboNuggets)

## What This Is
n8n workflow that generates cinematic-style video ads. Takes input assets (images/video) and prompts, processes them through a scene pipeline, and produces styled ad content.

## Files
- `R50 _ Cinematic Adverts System.json` — Main n8n workflow export (import directly into n8n)
- `Core Inputs/core elements.png` — Reference board for visual elements
- `Core Inputs/core image.jpg` — Base image asset
- `Core Inputs/elements board inputs/1-4.(jpeg/png/jpg)` — Input asset set (4 images)

## Workflow Summary (46 nodes)
Key nodes: `PROMPTS` → `IMAGES` → `VIDEOS` → `Get Scenes` → `Get Project` → scene processing pipeline with logging
- Handles both image and video tracks separately (Split Out → Switch)
- Uses project-based organization (Get Project, Get Project1, Get Scenes)
- Logs results back (Log Images node)

## How to Use
1. Import `R50 _ Cinematic Adverts System.json` into n8n
2. Place your input assets in `Core Inputs/` matching the existing structure
3. Configure credentials in n8n for any connected services
4. Run from the PROMPTS entry node

## Notes
- Input images should match aspect ratios of the sample assets in `elements board inputs/`
- Part of RoboNuggets R-series template packs
