# Tinker 🛠️

> **The Autonomous AI Action-Bot that GETS THINGS DONE.**

Tinker is a powerful, platform-agnostic AI agent that lives in your chat app (Discord, iMessage). Unlike standard chatbots that just *talk*, Tinker *acts*. It can browse the web, scrape data, fill forms, and summarize content, all while maintaining conversation context and remembering your preferences.

Designed to be **free to host**, open-source, and privacy-focused.

---

## ✨ Features

-   **🧠 Autonomous Agent**: Uses ReAct (Reasoning + Acting) pattern to solve complex tasks.
-   **🌐 Browser Automation**: Built-in Playwright engine to navigate, Click, Type, and Scrape the web.
-   **💬 Multi-Platform**:
    -   **Discord**: Rich text responses, file attachments.
    -   **iMessage**: Native macOS integration (Blue bubble power!).
-   **💾 Memory System**:
    -   **Short-term**: Remembers thread context.
    -   **Long-term**: Stores user preferences locally (SQLite).
-   **🛡️ Safety First**:
    -   Rate Limiting (5 reqs/10min).
    -   Domain Blocklist (Banking/High-risk sites).
-   **💸 $0 Cost**: Optimized for Free Tier Groq API and self-hosting.

## 🛠️ Tech Stack

-   **Python 3.11**
-   **LLM**: Llama3-70b via Groq API (Free Tier)
-   **Browser**: Playwright (Headless Chromium)
-   **Database**: SQLite (Local)
-   **Platforms**: `discord.py`, `sqlite3` (iMessage)

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   [Groq API Key](https://console.groq.com/) (Free)
-   **For Discord**: A Discord Bot Token [Guide](https://discord.com/developers/applications)
-   **For iMessage**: A macOS device (Local run only)

### 1. Installation

Clone the repo and set up the environment:

```bash
git clone https://github.com/yourusername/tinker.git
cd tinker

# Create virtual env
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium
```

### 2. Configuration

Create a `.env` file in the root directory:

```ini
# Required
GROQ_API_KEY=gsk_...
DISCORD_TOKEN=...

# Optional
ENABLE_IMESSAGE=false # Set to true on macOS to enable iMessage
```

### 3. Running Tinker

**Run Locally:**

```bash
python src/main.py
```

You should see logs indicating Tinker has connected to Discord (and iMessage if enabled).

---

## 📖 Usage Guide

Mention `@Tinker` in your Discord server or DM via iMessage.

### 🔍 Web Search & Research
> "@Tinker find the cheapest RTX 4090 on Amazon"
> "@Tinker what are the top HN posts today? Summarize them."

### 📝 Form Filling & Actions
> "@Tinker go to example.com/signup and sign me up with email test@test.com"

### 🧠 Memory
> "@Tinker remember that I live in San Francisco"
> (Later) "@Tinker what is the weather like where I live?"

---

## ☁️ Deployment (Cloud)

Tinker is configured for one-click deployment on **Render.com**.

1.  Fork this repository.
2.  Sign up for [Render](https://render.com).
3.  Create a new **Background Worker**.
4.  Connect your repo.
5.  Add Environment Variables (`DISCORD_TOKEN`, `GROQ_API_KEY`).
6.  Deploy!

*Note: iMessage support is NOT available in cloud deployments as it requires physical macOS hardware.*

---

## 🔒 Safety & limitations

-   **Rate Limit**: 5 requests per 10 minutes per user to prevent abuse.
-   **Blocklist**: Tinker will refuse to navigate to major banking or social login sites for security.
-   **Cookies**: Tinker does not persist cookies across sessions for privacy.

## 📄 License

MIT
