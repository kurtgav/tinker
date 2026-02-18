# Tinker Development Todo List

Based on `eve/PRD.md`.

## M1: Scaffold
- [ ] Initialize git repository
- [ ] Set up Python environment and `requirements.txt`
- [ ] Create Basic Discord Bot
    - [ ] `src/main.py` entry point
    - [ ] Connect to Discord
    - [ ] Handle `@Tinker` mentions (Echo test)

## M2: Basic Agent
- [ ] Implement Intent Router (Groq)
- [ ] Implement Tool System (FastMCP style)
- [ ] Create Tools:
    - [ ] `web_search` (DuckDuckGo)
    - [ ] `summarize_page` (LLM)
- [ ] Implement Agent ReAct Loop
- [ ] Verify basic search/summarize flow

## M3: Browser Tools (Playwright)
- [ ] Setup Playwright
- [ ] Implement Navigation & Interaction Tools:
    - [ ] `navigate`
    - [ ] `click`
    - [ ] `fill_form`
    - [ ] `extract_text`
    - [ ] `screenshot`
- [ ] Handle dynamic pages/SPAs

## M4: Memory
- [ ] Short-term Memory (Thread context, last 10 msgs)
- [ ] Long-term Memory (Supabase)
    - [ ] User preferences storage

## M5: Polish
- [ ] Rate Limiting (5 tasks/10min/user)
- [ ] Domain Blocklist
- [ ] Improved Reply Formatting (Markdown, Attachments)
- [ ] Error Handling

## M6: Deploy
- [ ] Dockerfile
- [ ] Render Deployment Config
- [ ] Documentation (README.md)
