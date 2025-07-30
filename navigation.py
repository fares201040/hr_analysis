def get_last_whatsapp_message_from_um_thkour_77_existing_browser(
    remote_debugging_port=9222,
):
    """
    Connect to an already open Chrome browser (with remote debugging enabled),
    go to WhatsApp Web, click on 'ام ذكور 77', and print the last message from that chat.
    The Chrome browser must be started with --remote-debugging-port=9222.
    """
    import time

    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright

    ws_endpoint = f"ws://localhost:{remote_debugging_port}/devtools/browser"
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(ws_endpoint)
        except Exception as e:
            print(f"Could not connect to Chrome with remote debugging: {e}")
            return
        # Find an existing page with WhatsApp Web, or open a new one if not found
        context = browser.contexts[0]
        page = None
        for p_ in context.pages:
            if "web.whatsapp.com" in p_.url:
                page = p_
                break
        if not page:
            page = context.new_page()
            page.goto(
                "https://web.whatsapp.com/",
                wait_until="domcontentloaded",
                timeout=90000,
            )
            print(
                "Please scan the QR code if prompted and wait for WhatsApp Web to load..."
            )
            try:
                page.wait_for_selector(
                    'div[title="Search input textbox"], [data-testid="chat-list-search"]',
                    timeout=120000,
                )
            except PlaywrightTimeoutError:
                print("Timeout waiting for WhatsApp Web to load.")
                browser.close()
                return
        # Click on the chat with the exact name 'HRD Staff'
        try:
            chat_selector = "span[title='HRD Staff']"
            page.wait_for_selector(chat_selector, timeout=60000)
            page.click(chat_selector)
        except PlaywrightTimeoutError:
            print("Could not find the chat named 'HRD Staff'.")
            browser.close()
            return
        # Wait for the chat messages to load
        try:
            page.wait_for_selector("div.selectable-text.copyable-text", timeout=30000)
            message_divs = page.query_selector_all("div.message-in, div.message-out")
            last_msg = None
            for div in reversed(message_divs):
                if "message-in" in div.get_attribute("class"):
                    text_div = div.query_selector("div.selectable-text.copyable-text")
                    if text_div:
                        last_msg = text_div.inner_text()
                        break
            if last_msg:
                print(f"Last message from HRD Staff: {last_msg}")
            else:
                print("No message found from HRD Staff.")
        except PlaywrightTimeoutError:
            print("Could not load messages for 'ام ذكور 77'.")
        browser.close()


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


def open_whatsapp_and_keep_browser():
    """
    Open WhatsApp Web in Chrome, wait for manual QR scan, and keep browser/page open for future actions.
    Returns: playwright instance, browser, and page objects for further automation.
    """
    from playwright.sync_api import sync_playwright

    p = sync_playwright().start()
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded", timeout=90000)
    print(
        "Please scan the QR code in the browser, then press Enter here to continue..."
    )
    input()
    # Now you can use 'page' for further actions, e.g., click chat, read messages, etc.
    return p, browser, page


# Example usage for future actions:
# p, browser, page = open_whatsapp_and_keep_browser()
# # ... perform actions with 'page' ...
# browser.close()
# p.stop()


if __name__ == "__main__":
    # navigate_and_sign_in()
    # Example: open WhatsApp Web and keep browser open for future actions
    p, browser, page = open_whatsapp_and_keep_browser()

    # Import TimeoutError at the top of the block
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    # Handle the "A fresh look for WhatsApp" popup with a "Continue" button
    try:
        print("Checking for 'Continue' popup...")
        # This selector targets a button that contains the exact text "Continue"
        continue_button = page.locator('button:has-text("Continue")')
        # Wait for a short period as the popup may not always appear
        continue_button.wait_for(timeout=10000)
        continue_button.click()
        print("Clicked the 'Continue' button on the popup.")
    except PlaywrightTimeoutError:
        # This is not an error, it just means the popup wasn't there.
        print("'Continue' popup did not appear, proceeding...")
    except Exception as e:
        print(f"An unexpected error occurred while handling the popup: {e}")

    # Example: after scanning QR, click on 'HRD Staff' and print last message
    try:
        chat_name = "HRD Staff"
        # Try multiple selectors for the chat search box
        search_box_selectors = [
            'div[data-testid="chat-list-search"]',
            'div[title="البحث عن دردشة أو بدء دردشة جديدة"]',
            'div[title*="بحث"]',
            'input[title*="بحث"]',
            'input[aria-label*="بحث"]',
            'input[role="searchbox"]',
            'input[type="text"]',
        ]
        search_box = None
        for selector in search_box_selectors:
            try:
                print(f"Trying selector: {selector}")
                search_box = page.wait_for_selector(selector, timeout=7000)
                if search_box:
                    print(f"Found search box with selector: {selector}")
                    break
            except PlaywrightTimeoutError:
                continue
        if not search_box:
            print("Could not find the chat search box with any known selector.")
            raise Exception("Chat search box not found")
        search_box.click()
        search_box.fill(chat_name)
        page.wait_for_timeout(2000)  # Wait for search results to appear

        # Click on the chat in the search results
        chat_selector = f"span[title='{chat_name}']"
        page.wait_for_selector(chat_selector, timeout=10000)
        page.click(chat_selector)
        print(f"Clicked on chat: {chat_name}")

        # Wait for chat header to ensure chat is open
        page.wait_for_selector("header", timeout=10000)
        # Wait extra time for messages to load
        page.wait_for_timeout(5000)

        # Now try to get messages
        message_divs = page.query_selector_all("div.message-in, div.message-out")
        if not message_divs:
            print(
                "No messages found in the chat (possibly only media or still loading)."
            )
        else:
            last_msg = None
            for div in reversed(message_divs):
                # Find the last message sent by the other person
                if "message-in" in div.get_attribute("class"):
                    text_div = div.query_selector("div.selectable-text.copyable-text")
                    if text_div:
                        last_msg = text_div.inner_text()
                        break
            if last_msg:
                print(f"Last message from {chat_name}: {last_msg}")
            else:
                print(f"No text message found from {chat_name}.")

    except TimeoutError as e:
        print(f"A timeout error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Keep the browser open for further actions.
    # Uncomment the lines below when you are finished.
    # print("Closing browser...")
    # browser.close()
    # p.stop()
