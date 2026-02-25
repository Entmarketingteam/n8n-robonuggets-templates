# R49 — MCP Template Pack (RoboNuggets)

## What This Is
n8n MCP (Model Context Protocol) integration pack. Exposes RoboNuggets workflows as MCP tools via n8n Forms, enabling AI agents to trigger them directly.

## Files

### n8n Templates
| File | What it Does |
|------|-------------|
| `MCP - Nanobanana 1 (by RoboNuggets).json` | MCP wrapper for Nanobanana 1 — Form trigger → Nanobanana 1 workflow |
| `MCP - Nanobanana Pro (by RoboNuggets) (1).json` | MCP wrapper for Nanobanana Pro — Form trigger → Nanobanana Pro workflow |
| `MCP - Post to Instagram (by RoboNuggets).json` | MCP wrapper for Instagram posting — Form → Upload media → Instagram via Blotato (3 nodes) |

### Brand Assets
| File | Description |
|------|-------------|
| `brand assets/Aje Brand Book.png` | Aje brand reference/style guide |
| `brand assets/Manon Mini.webp` | Product/model image asset |
| `brand assets/Splendour Dress.webp` | Product image asset |

## How It Works
These are MCP-enabled wrappers — each workflow uses an n8n Form as the entry point, which gets exposed as an MCP tool endpoint. An AI agent (Claude, GPT, etc.) can call the form URL to trigger the underlying workflow.

## How to Use
1. Import all 3 JSON files into n8n
2. Ensure the underlying workflows (Nanobanana 1, Nanobanana Pro) are already imported and active (see n28 templates)
3. Configure Blotato node credentials for the Instagram workflow
4. Activate all 3 MCP workflows
5. Copy the Form webhook URLs — these become your MCP tool endpoints
6. Register the URLs in your MCP client (Claude Desktop, custom agent, etc.)

## Dependencies
- Nanobanana 1 and Nanobanana Pro workflows must be set up first (from n28 pack)
- Blotato n8n node required for Instagram posting (see n12)
- Instagram account connected via Blotato

## Notes
- Brand assets appear to be sample/demo inputs for the image generation workflows
- Part of RoboNuggets R-series — R49 is the MCP bridge layer on top of n28
