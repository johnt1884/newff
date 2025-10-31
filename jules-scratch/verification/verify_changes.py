
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the page
        await page.goto("https://boards.4chan.org/b/")

        # Inject the userscript
        with open('ff.js', 'r') as f:
            script_content = f.read()
        await page.evaluate(script_content)

        # Wait for the settings cog to be visible
        settings_cog = page.locator('#otk-settings-cog')
        await expect(settings_cog).to_be_visible(timeout=30000)

        # Open the settings panel
        await settings_cog.click()

        # Wait for the options window to be visible
        options_window = page.locator('#otk-options-window')
        await expect(options_window).to_be_visible()

        # Check initial state of checkboxes
        clock_checkbox = page.locator('#otk-clock-toggle-checkbox')
        pip_checkbox = page.locator('#otk-pip-mode-checkbox')

        await expect(clock_checkbox).to_be_checked()
        await expect(pip_checkbox).to_be_checked()

        # Find and click the "Reset All Colors to Default" button
        reset_button = page.locator('#otk-reset-all-colors-btn')
        await reset_button.click()

        # The script shows an alert, we need to accept it
        page.on("dialog", lambda dialog: dialog.accept())

        # Wait a moment for the reset to apply
        await page.wait_for_timeout(1000)

        # Verify checkboxes are still checked
        await expect(clock_checkbox).to_be_checked()
        await expect(pip_checkbox).to_be_checked()

        print("Verification successful: Checkboxes remained checked after reset.")

        # Take a screenshot
        await options_window.screenshot(path="jules-scratch/verification/verification.png")
        print("Screenshot taken.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
