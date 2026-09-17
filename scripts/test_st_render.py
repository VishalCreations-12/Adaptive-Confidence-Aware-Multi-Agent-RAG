from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    page.goto('http://localhost:8501')
    page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=15000)
    page.wait_for_timeout(3000)
    
    text = page.locator("[data-testid='stAppViewContainer']").inner_text()
    print("Container text length:", len(text))
    print("Container text sample:\n", text[:400])
    browser.close()
