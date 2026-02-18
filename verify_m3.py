import asyncio
from src.tools.browser import navigate, click, fill_form, extract_text, screenshot, BrowserManager

async def test_browser_tools():
    print("Testing M3 Browser Tools...")
    
    # Test 1: Navigation
    print("\n[1] Testing Navigation...")
    url = "https://example.com"
    result = await navigate(url)
    print(f"Result: {result}")
    assert "Navigated to" in result
    assert "Example Domain" in result

    # Test 2: Extraction
    print("\n[2] Testing Text Extraction...")
    text = await extract_text("h1")
    print(f"H1 Text: {text}")
    assert "Example Domain" in text
    
    body_text = await extract_text()
    print(f"Body Text Sample: {body_text[:50]}...")
    assert "This domain is for use" in body_text

    # Test 3: Click (Clicking the link "More information...")
    print("\n[3] Testing Click...")
    click_result = await click("a")
    print(f"Click Result: {click_result}")
    assert "Clicked element" in click_result
    
    # Allow some time for navigation
    await asyncio.sleep(2)
    new_text = await extract_text("h1")
    print(f"New H1 Text: {new_text}")
    # The link goes to iana.org, title should change
    
    # Test 4: Screenshot
    print("\n[4] Testing Screenshot...")
    shot_result = await screenshot()
    print(f"Result: {shot_result}")
    assert "Screenshot saved" in shot_result

    # Cleanup
    await BrowserManager.close()
    print("\n✅ M3 Verification Passed!")

if __name__ == "__main__":
    asyncio.run(test_browser_tools())
