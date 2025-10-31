from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Listen for console messages from the page
        page.on("console", lambda msg: print(f"Browser console: {msg.text()}"))

        try:
            # Use a minimal HTML page
            page.goto("data:text/html,<html><body></body></html>")

            with open("ff.js", "r") as f:
                script_content = f.read()

            # Use evaluate to run the script
            page.evaluate(script_content)

            # Wait explicitly for the cog icon to appear before trying to click it
            print("Waiting for settings cog to appear...")
            cog_icon = page.locator('#otk-settings-cog')
            cog_icon.wait_for(state='visible', timeout=10000) # Wait for 10 seconds
            print("Settings cog found. Clicking it.")

            cog_icon.click()

            # Wait for the options window to be visible
            options_window = page.locator('#otk-options-window')
            options_window.wait_for(state='visible', timeout=5000)
            print("Options window is visible.")

            clock_checkbox = page.locator('#otk-clock-toggle-checkbox')
            pip_checkbox = page.locator('#otk-pip-mode-checkbox')

            print(f"Initial clock enabled: {clock_checkbox.is_checked()}")
            print(f"Initial PiP enabled: {pip_checkbox.is_checked()}")

            page.click('#otk-reset-all-colors-btn')

            print(f"After reset clock enabled: {clock_checkbox.is_checked()}")
            print(f"After reset PiP enabled: {pip_checkbox.is_checked()}")

            page.screenshot(path="jules-scratch/verification/verification.png")

            if not clock_checkbox.is_checked():
                raise Exception("Clock checkbox became unchecked after reset")
            if not pip_checkbox.is_checked():
                raise Exception("PiP checkbox became unchecked after reset")

            print("Verification successful: Checkboxes remained checked.")

        except PlaywrightTimeoutError as e:
            print(f"A timeout error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
