# n29 Templates — Content Repurposing Pack (RoboNuggets)

## What This Is
3 n8n workflows triggered via Telegram that repurpose existing content into new formats using AI.

## Files & What Each Does

### 1. TikTok → Sora Video
`🔺Send a Tiktok, 🔻get a Sora Vid  _ n29 by RoboNuggets.json`
- Trigger: Send a TikTok URL to a Telegram bot
- Output: Sora-generated video sent back via Telegram
- Nodes: Telegram Trigger → Get Video → Analyze video → Create Sora → Send a video
- 16 nodes total, includes Wait/Switch for error handling

### 2. YouTube Long → LinkedIn or X Post
`🔺Send a YT Long, 🔻get a LI or X post _ n29 by RoboNuggets.json`
- Trigger: Send a YouTube long-form URL to Telegram
- Output: Repurposed post published to LinkedIn and/or X (Twitter)
- Nodes: Telegram Trigger → Analyze video → LinkedIn / Twitter
- 10 nodes total

### 3. YouTube Short → Script
`🔺Send a YT Short, 🔻get a Script _ n29 by RoboNuggets.json`
- Trigger: Send a YouTube Shorts URL to Telegram
- Output: Script sent back via Telegram
- Nodes: Telegram Trigger → Analyze video → Send a text message
- 7 nodes total (simplest of the 3)

## How to Use
1. Import desired workflow(s) into n8n
2. Configure credentials: Telegram Bot, OpenAI (or equivalent), LinkedIn/X (for workflow 2), Sora API (for workflow 1)
3. Set your Telegram bot token in the Telegram Trigger node
4. Activate the workflow — send a URL to your bot to trigger

## Use Cases for ENT Agency
- Repurpose creator content across platforms automatically
- Generate video ads from existing TikTok content (workflow 1)
- Convert long-form creator YouTube videos to social posts for brand partnerships
