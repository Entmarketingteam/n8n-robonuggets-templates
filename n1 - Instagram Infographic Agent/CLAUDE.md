# n1 — Instagram Infographic Agent (RoboNuggets)

## What This Is
Scheduled n8n agent that auto-generates Instagram infographic posts using OpenAI GPT-4o image generation and web search.

## Files
- `n1 - Instagram Infographic Agent by RoboNuggets.json` — n8n workflow export (16 nodes)

## Workflow Summary
Nodes: `Schedule Trigger` → `Research Agent` (web search) → `Image Prompt Agent` → `Generate Image` (4o) → `Convert Image` → `Captions Agent` → post
- Runs on a schedule (daily/weekly)
- Research agent pulls trending topics via web search
- Separate agents for image prompt and caption writing
- Uses OpenAI 4o image generation
- Converts and formats image for Instagram

## How to Use
1. Import into n8n
2. Configure credentials: OpenAI API (needs GPT-4o image gen access), web search tool
3. Set your schedule in the Schedule Trigger node
4. Configure Instagram posting credentials (Graph API or via Blotato)
5. Customize `Image Style` node with your brand aesthetic

## ENT Agency Use Case
- Auto-generate health/wellness infographics for Beauty Creatine Plus Instagram
- Schedule creator tip content for ENT Agency social
