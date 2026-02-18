# TECHSTACK.md — Tinker
**Constraint:** $0/month, no credit card required for any service.

---

## Overview

Every component in Tinker's stack has a free tier that covers the project's needs. No service below requires a paid plan to build, run, or deploy Tinker.

---

## Stack at a Glance

| Layer | Tool | Why |
|---|---|---|
| Bot interface | **discord.py** or **python-telegram-bot** | Free, open source, no billing |
| LLM (brain) | **Groq API** (free tier) | Fastest free inference; llama-3.3-70b or gemma2-9b |
| Agent framework | **FastMCP** | Lightweight MCP server, tool registry, already used in reference repo |
| Browser automation | **Playwright** (Python) | Better than Selenium; handles SPAs; free |
| Web search | **DuckDuckGo HTML scrape** (duckduckgo-search PyPI) | No API key, no billing, sufficient for most queries |
| Short-term memory | **In-process dict** (Python, keyed by thread ID) | Zero infra needed |
| Long-term memory | **Supabase** (free tier — 500MB PostgreSQL) | Managed Postgres, free forever plan |
| Hosting | **Render** (free web service) | 750 hrs/month free, auto-deploy from GitHub |
| Package management | **uv** (Python) | Faster than pip, free |
| Language | **Python 3.12+** | Unified stack — no TS/Python split like the reference repo |
| Testing | **pytest** | Free, standard |
| CI | **GitHub Actions** (free tier — 2000 min/month) | Runs tests on push |

---

## Detailed Choices

### LLM — Groq API (Free Tier)
- **URL:** https://console.groq.com
- **Free quota:** 14,400 requests/day, 6,000 tokens/min on `llama-3.3-70b-versatile`
- **Why not Ollama?** Render's free tier has no GPU and limited RAM. Groq's hosted inference is faster and free within limits.
- **Fallback:** If Groq is unavailable, fall back to `gemma2-9b` on Groq or `mistral-7b` via OpenRouter free tier.
- **Env var:** `GROQ_API_KEY`

### Browser Automation — Playwright (Python)
- **Why Playwright over Stagehand?** Stagehand is JS-only and requires an external LLM call per action. Playwright is Python-native, lighter, and gives us direct control without extra token spend.
- **Install:** `playwright install chromium --with-deps`
- **Mode:** Headless by default; `PLAYWRIGHT_HEADLESS=false` for local debugging.
- **Key capabilities used:** `page.goto()`, `page.fill()`, `page.click()`, `page.inner_text()`, `page.screenshot()`, `page.wait_for_load_state('networkidle')`

### Bot Interface — Discord.py (primary) / python-telegram-bot (secondary)
- Both are free, battle-tested Python libraries.
- Discord is the default because slash commands and threads are easy to scope.
- Telegram support added via the same agent core — only the listener/reply layer differs.
- **Env vars:** `DISCORD_BOT_TOKEN` or `TELEGRAM_BOT_TOKEN`

### Agent Framework — FastMCP
- Tools are Python functions decorated with `@mcp.tool`.
- The MCP server runs internally — the bot calls tools directly via the MCP Python client, not over HTTP.
- Adding a new tool = one decorated function in `src/tools/`.

### Memory — Supabase (free tier)
- **Free tier:** 500 MB storage, unlimited API calls, 2 projects.
- **Schema:** One table `user_memory` with columns `user_id TEXT PRIMARY KEY`, `preferences JSONB`, `updated_at TIMESTAMP`.
- Thread memory stays in-process (no DB writes per message — reduces latency).
- **Env vars:** `SUPABASE_URL`, `SUPABASE_ANON_KEY`

### Hosting — Render (free web service)
- 750 free hours/month (enough for 1 always-on service).
- Auto-deploys from GitHub main branch.
- Free PostgreSQL available too (alternative to Supabase if preferred).
- Cold start ~30s after 15 min inactivity — acceptable for a bot.
- `render.yaml` is already in the reference repo structure and can be reused.

### Web Search — duckduckgo-search
- PyPI package: `duckduckgo-search`
- No API key, no rate limit signup, returns title + URL + snippet.
- For richer results, Tinker navigates the top URL with Playwright and extracts full text.

---

## Project Structure

```
tinker/
├── src/
│   ├── bot/
│   │   ├── discord_bot.py        # Discord listener & reply
│   │   └── telegram_bot.py       # Telegram listener & reply
│   ├── agent/
│   │   ├── loop.py               # ReAct plan→act→observe loop
│   │   ├── intent.py             # Intent classification via Groq
│   │   └── memory.py             # Thread memory + Supabase long-term
│   ├── tools/
│   │   ├── __init__.py           # Tool registry (FastMCP)
│   │   ├── web_search.py         # DuckDuckGo search tool
│   │   ├── browser.py            # navigate, click, fill, extract, screenshot
│   │   └── summarize.py          # LLM-powered page summarizer
│   └── server.py                 # FastMCP server entry point
├── tests/
│   ├── test_tools.py
│   └── test_agent.py
├── .env.example
├── render.yaml
├── requirements.txt
├── PRD.md
├── TECHSTACK.md
└── README.md
```

---

## Environment Variables

```bash
# LLM
GROQ_API_KEY=your_groq_key_here

# Bot (use one or both)
DISCORD_BOT_TOKEN=your_discord_token
TELEGRAM_BOT_TOKEN=your_telegram_token

# Database
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# Config (optional)
MAX_STEPS=10
RATE_LIMIT_TASKS=5
RATE_LIMIT_WINDOW_SECONDS=600
PLAYWRIGHT_HEADLESS=true
```

---

## Free Tier Limits & Mitigation

| Service | Free Limit | Risk | Mitigation |
|---|---|---|---|
| Groq | 14,400 req/day | High-traffic channels could hit limit | In-process request counter; queue tasks; fall back to OpenRouter |
| Render | 750 hrs/month | Service sleeps after 15 min idle | Use UptimeRobot (free) to ping every 10 min |
| Supabase | 500 MB | Very unlikely to hit with user prefs only | Prune old records if > 10,000 rows |
| GitHub Actions | 2,000 min/month | Fine for small team | Cache pip installs; limit CI to push on main |

---

## What We Dropped vs. the Reference Repo

| Reference Repo Feature | Why Dropped in Tinker |
|---|---|
| TypeScript (Stagehand, iMessage watcher) | Splits the codebase; Stagehand needs paid LLM per action; iMessage is Mac-only |
| Modal.py (serverless GPU) | Has costs beyond free tier; not needed with Groq |
| iMessage / AppleScript watcher | Platform-locked, fragile, requires physical Mac; Discord/Telegram are universal |
| Poke MCP integration | Proprietary, unclear free tier; Discord is better supported |

---

## Getting Started (for Antigravity)

```bash
# 1. Clone and install
git clone <your-repo>
cd tinker
pip install uv
uv pip install -r requirements.txt
playwright install chromium --with-deps

# 2. Copy env vars
cp .env.example .env
# Fill in GROQ_API_KEY and DISCORD_BOT_TOKEN

# 3. Run locally
python src/server.py

# 4. Deploy
# Push to GitHub → Render auto-deploys via render.yaml
```

All free. No credit card. No billing surprises.