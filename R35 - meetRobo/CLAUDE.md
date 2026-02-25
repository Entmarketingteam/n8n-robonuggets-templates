# R35 — meetRobo (RoboNuggets)

## What This Is
Slack-triggered AI agent that uses Perplexity for web search and returns structured output. A research assistant that lives in Slack.

## Files
- `R35 _ meetRobo.json` — n8n workflow export (7 nodes)

## Workflow Summary
Nodes: `Slack Trigger` → `meetRobo AI Agent` → `OpenAI Chat Model` + `Perplexity` + `Think` → `Structured Output Parser` → `Slack`
- Triggered by a Slack message/event
- AI agent with access to Perplexity search and a Think node for reasoning
- Returns structured, parsed response back to Slack

## How to Use
1. Import `R35 _ meetRobo.json` into n8n
2. Configure credentials: Slack (Bot Token + Webhook), OpenAI, Perplexity API
3. Set up Slack app with event subscriptions pointing to your n8n webhook
4. Activate — mention the bot or use configured trigger in Slack
