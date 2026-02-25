# R52 — Longform AI Explainers System (RoboNuggets)

## What This Is
Full production pipeline for creating long-form AI explainer content. Covers research, scripting, structuring, and voice generation in one 56-node workflow.

## Files
- `R52 _ Longform AI Explainers System.json` — n8n workflow export (56 nodes)

## Workflow Summary
Key nodes: `AI Agent by RoboNuggets` → `Model` → `Think` → `Structure` → `Split Out` → `Create Voice`
- AI agent handles research and scripting
- Think node for multi-step reasoning
- Structured output parsing for consistent script format
- Splits content into segments (Split Out)
- Voice generation at the end (Create Voice node)

## How to Use
1. Import `R52 _ Longform AI Explainers System.json` into n8n
2. Configure credentials: OpenAI (or compatible LLM), voice API (ElevenLabs or similar)
3. Provide topic/brief as workflow input
4. Output is a structured script + generated audio

## Notes
- Largest workflow in the R-series at 56 nodes
- Voice node likely requires ElevenLabs API key
