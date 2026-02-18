from playwright.async_api import async_playwright
import asyncio

class BrowserManager:
    _instance = None
    _playwright = None
    _browser = None
    _context = None
    _page = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = BrowserManager()
            await cls._instance._start()
        return cls._instance

    async def _start(self):
        self._playwright = await async_playwright().start()
        # Launch headless by default
        self._browser = await self._playwright.chromium.launch(headless=True)
        self._context = await self._browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self._page = await self._context.new_page()

    @classmethod
    async def close(cls):
        if cls._instance:
            if cls._instance._context:
                await cls._instance._context.close()
            if cls._instance._browser:
                await cls._instance._browser.close()
            if cls._instance._playwright:
                await cls._instance._playwright.stop()
            cls._instance = None

    DOMAIN_BLOCKLIST = [
        "facebook.com",
        "twitter.com",
        "instagram.com",
        "linkedin.com",
        "bankofamerica.com",
        "chase.com",
        "wellsfargo.com",
        "paypal.com"
    ]

    async def navigate(self, url: str) -> str:
        """Navigates to the specified URL."""
        if not self._page:
            await self._start()
        try:
            # Check Blocklist
            for domain in self.DOMAIN_BLOCKLIST:
                if domain in url:
                    return f"Error: Navigation to {domain} is blocked for safety reasons."

            # Ensure protocol
            if not url.startswith('http'):
                url = 'https://' + url
            
            await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
            title = await self._page.title()
            return f"Navigated to {url}. Title: {title}"
        except Exception as e:
            return f"Error navigating to {url}: {e}"

    async def click(self, selector: str) -> str:
        """Clicks an element matching the selector."""
        if not self._page:
            return "Error: Browser not started. Navigate first."
        try:
            await self._page.click(selector, timeout=5000)
            return f"Clicked element: {selector}"
        except Exception as e:
            return f"Error clicking {selector}: {e}"

    async def fill_form(self, selector: str, value: str) -> str:
        """Fills a form field matching the selector with the given value."""
        if not self._page:
            return "Error: Browser not started. Navigate first."
        try:
            await self._page.fill(selector, value, timeout=5000)
            return f"Filled {selector} with '{value}'"
        except Exception as e:
            return f"Error filling {selector}: {e}"

    async def extract_text(self, selector: str = "body") -> str:
        """Extracts text from the element matching the selector (defaults to body)."""
        if not self._page:
            return "Error: Browser not started. Navigate first."
        try:
            if selector == "body":
                # For body, try to get readable content or innerText
                text = await self._page.inner_text("body")
                # Simple truncation to avoid huge outputs
                return text[:2000] + ("..." if len(text) > 2000 else "")
            else:
                text = await self._page.inner_text(selector, timeout=5000)
                return text
        except Exception as e:
            return f"Error extracting text from {selector}: {e}"

    async def screenshot(self) -> str:
        """Takes a screenshot of the current page."""
        if not self._page:
            return "Error: Browser not started."
        try:
            # Save to a temporary path (or return bytes? For now, simplistic path)
            path = "screenshot.png"
            await self._page.screenshot(path=path)
            return f"Screenshot saved to {path} (local)"
        except Exception as e:
            return f"Error taking screenshot: {e}"

# Tool wrappers
browser = BrowserManager()

async def navigate(url: str) -> str:
    """Navigates the browser to the specified URL."""
    inst = await BrowserManager.get_instance()
    return await inst.navigate(url)

async def click(selector: str) -> str:
    """Clicks an element on the current page matching the CSS selector."""
    inst = await BrowserManager.get_instance()
    return await inst.click(selector)

async def fill_form(selector: str, value: str) -> str:
    """Fills a form input matching the selector with the given text value."""
    inst = await BrowserManager.get_instance()
    return await inst.fill_form(selector, value)

async def extract_text(selector: str = "body") -> str:
    """Extracts text content from the current page. Optional: provide a CSS selector."""
    inst = await BrowserManager.get_instance()
    return await inst.extract_text(selector)

async def screenshot() -> str:
    """Takes a screenshot of the current page."""
    inst = await BrowserManager.get_instance()
    return await inst.screenshot()
