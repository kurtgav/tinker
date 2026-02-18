# PRD — Tinker
**Version:** 0.1  
**Status:** Draft  
**Owner:** You  
**For:** Antigravity (autonomous AI coding agent)

---

## 1. Overview

Tinker is a conversational AI action-bot that listens to messages from a chat platform (Discord or Telegram), understands intent, and autonomously executes real-world tasks — browsing the web, filling forms, scraping data, summarizing pages, and reporting results back to the chat. It is platform-agnostic, memory-aware, and runs entirely on free infrastructure.

Think of it as a group-chat member who can actually *do* things on the internet, not just talk about them.

---

## 2. Problem Statement

Existing chat bots answer questions but can't take actions. Browser automation tools take actions but have no chat interface. Tinker bridges both — triggered by natural language in a conversation, it executes multi-step browser tasks and returns structured results, all within the same chat thread.

---

## 3. Goals

- A user in a Discord/Telegram channel mentions `@Tinker` followed by a task in plain English.
- Tinker parses the intent, breaks it into steps, executes each step (web browsing, form submission, data extraction), and replies with results in the same channel.
- The entire system runs for $0/month on free-tier services.
- Any developer can clone and self-host in under 30 minutes.

---

## 4. Non-Goals

- No paid API dependencies at runtime (no OpenAI billing, no paid proxies).
- No mobile app or dedicated frontend — the chat platform IS the UI.
- No real-time voice or video.
- No storing or processing personally identifiable information (PII).

---

## 5. User Stories

| ID | As a… | I want to… | So that… |
|----|-------|-----------|---------|
| U1 | Discord user | @mention Tinker with a task like "find the cheapest RTX 4090 on Amazon" | it returns me a price comparison without me opening a browser |
| U2 | Group member | Ask Tinker to "sign me up for the Y Combinator newsletter" | it fills the form and confirms completion |
| U3 | Team lead | Ask Tinker to "summarize the top 5 HN posts today" | I get a daily briefing without leaving chat |
| U4 | Developer | Configure Tinker with my own tools via a simple `.py` file | I can extend what Tinker can do without changing core logic |
| U5 | Any user | Ask Tinker a follow-up like "now find a cheaper one on eBay" | Tinker remembers the previous task context in the same thread |

---

## 6. Functional Requirements

### 6.1 Trigger & Parsing
- Tinker activates on `@Tinker <natural language task>` in any channel it is added to.
- A lightweight intent classifier routes the message to the correct agent skill (web search, form fill, scrape, summarize, Q&A).
- If intent is ambiguous, Tinker asks one clarifying question before acting.

### 6.2 Agent Loop
- Tinker uses a `plan → act → observe → reply` loop (ReAct pattern).
- Each plan step is a discrete tool call (browse URL, click element, extract text, fill field, submit, etc.).
- Max steps per task: 10 (configurable). If exceeded, Tinker reports partial results.
- All intermediate steps are logged to a structured JSON file for debugging.

### 6.3 Browser Execution
- Headless browser automation handles all web interactions.
- Tinker can: navigate to URLs, click elements by CSS/XPath/text, fill and submit forms, extract inner text or table data, take a screenshot and attach it to the chat reply.
- JavaScript-heavy SPAs must be handled (wait for network idle, dynamic content).

### 6.4 Memory
- **Short-term (thread memory):** Within a single Discord thread or Telegram reply-chain, Tinker retains the last 10 messages for context. Stored in-process.
- **Long-term (user memory):** User-specific preferences (e.g., "my Amazon region is .co.uk") stored in a free-tier database, keyed by user ID. Recalled at the start of each new task.

### 6.5 Tool Registry
- Tools are decorated Python functions registered via FastMCP (`@mcp.tool`).
- Built-in tools at launch: `web_search`, `navigate`, `click`, `fill_form`, `extract_text`, `screenshot`, `summarize_page`.
- Developers add new tools by adding a decorated function to `src/tools/`.

### 6.6 Reply Formatting
- Plain task results → markdown-formatted reply with a short summary + key data points.
- Long results (>2000 chars) → first 500 chars in chat + full result as a `.txt` attachment or pastebin link.
- Errors → friendly error message + one suggested retry phrasing.

### 6.7 Rate Limiting & Safety
- Per-user: max 5 tasks per 10 minutes.
- Block list of domains Tinker will never navigate to (e.g., login walls, banking sites, adult content).
- Tinker never stores or echoes back credentials, tokens, or anything that looks like a password.

---

## 7. Non-Functional Requirements

| Requirement | Target |
|---|---|
| Task completion latency (p50) | < 15 seconds for single-page tasks |
| Task completion latency (p95) | < 45 seconds for multi-step tasks |
| Uptime | 99% (acceptable on free tier with cold starts) |
| Concurrent task handling | 3 parallel tasks minimum |
| Zero-cost constraint | $0/month hard ceiling |

---

## 8. User Flow

```
User: @Tinker find the best free Figma alternatives

Tinker: Got it! Let me search for that... 🔍

[agent loop: web_search → navigate top results → extract_text → summarize]

Tinker: Here are the top free Figma alternatives I found:
1. **Penpot** — open source, self-hostable, Figma-compatible files
2. **Framer** — free tier, great for prototyping
3. **Lunacy** — free, offline-capable, supports Sketch files
4. **Quant UX** — fully free, no account needed

Want me to open any of these and give you a detailed comparison?
```

---

## 9. Architecture Diagram

```
Discord / Telegram
       │
       │  @Tinker <task>
       ▼
  Bot Listener (discord.py / python-telegram-bot)
       │
       ▼
  Intent Router (LLM call via Groq free tier)
       │
       ▼
  Agent Loop (ReAct — plan, act, observe)
       │
       ├── Tool: web_search (DuckDuckGo scrape, no API key)
       ├── Tool: navigate / click / fill / extract (Playwright)
       ├── Tool: summarize_page (LLM)
       └── Tool: screenshot (Playwright → attach to chat)
       │
       ▼
  Short-term Memory (in-process dict, thread-keyed)
  Long-term Memory (Supabase free tier PostgreSQL)
       │
       ▼
  Reply Formatter → Discord / Telegram reply
```

---

## 10. Milestones

| Milestone | Deliverable | ETA |
|---|---|---|
| M1 — Scaffold | Repo structure, bot connects to Discord/Telegram, echoes messages | Day 1 |
| M2 — Basic agent | Intent parsing, `web_search` + `summarize` tools working | Day 2 |
| M3 — Browser tools | `navigate`, `click`, `extract_text`, `fill_form` via Playwright | Day 3–4 |
| M4 — Memory | Thread memory + Supabase long-term memory | Day 5 |
| M5 — Polish | Rate limiting, error handling, reply formatting, screenshot attach | Day 6 |
| M6 — Deploy | One-click Render deploy, README, env var docs | Day 7 |

---

## 11. Success Metrics

- 80% of plain-language web tasks complete without clarification.
- p50 latency under 15 seconds on the free-tier host.
- Developer can add a new tool in < 10 lines of Python.
- Zero paid services required for a full deployment.

---

## 12. Out of Scope (v1)

- OAuth login flows on behalf of the user
- Scheduling / cron-triggered tasks
- Multiple concurrent browser sessions beyond 3
- Voice/audio input
- Fine-tuned model — use a free hosted LLM only

---

## 13. Prompt for Antigravity

> You are building **Tinker**, an AI action-bot described in this PRD. Use the tech stack defined in `TECHSTACK.md`. Follow all milestones in order. For each milestone, write clean, well-commented code, commit with a descriptive message, and confirm completion before moving to the next. Do not skip steps. Do not use any paid APIs or services. The bot name throughout all code, comments, and UI strings must be **Tinker**. Begin with M1.