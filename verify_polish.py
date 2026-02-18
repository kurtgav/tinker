from src.utils.rate_limiter import RateLimiter
from src.tools.browser import navigate, BrowserManager
import asyncio
import time

def test_rate_limiter():
    print("Testing Rate Limiter...")
    limiter = RateLimiter(max_requests=2, period_seconds=60)
    user = "test_user"
    
    assert limiter.is_allowed(user) == True
    assert limiter.is_allowed(user) == True
    assert limiter.is_allowed(user) == False # 3rd request should fail
    print("✅ Rate Limiter functional.")

async def test_blocklist():
    print("\nTesting Domain Blocklist...")
    # BrowserManager is singleton, ensure it's started
    
    url = "https://facebook.com"
    result = await navigate(url)
    print(f"Result for {url}: {result}")
    assert "blocked" in result.lower()
    
    url = "https://example.com"
    result = await navigate(url)
    print(f"Result for {url}: {result}")
    assert "Navigated to" in result
    
    await BrowserManager.close()
    print("✅ Blocklist functional.")

async def main():
    test_rate_limiter()
    await test_blocklist()
    print("\n✅ M5 Polish Verification Passed!")

if __name__ == "__main__":
    asyncio.run(main())
