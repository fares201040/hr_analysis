from playwright.sync_api import sync_playwright


def navigate_and_sign_in():
    """
    Navigate to render.com and click the 'Sign In' button using Playwright (Edge).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()
        page.goto("https://render.com", wait_until="domcontentloaded", timeout=60000)
        # Wait for the Sign In link to be visible
        page.wait_for_selector("text=Sign In", timeout=30000)
        page.click("text=Sign In")
        page.wait_for_url("https://dashboard.render.com/login", timeout=30000)
        browser.close()
        # Do not close the browser so it remains open for manual interaction


if __name__ == "__main__":
    navigate_and_sign_in()
