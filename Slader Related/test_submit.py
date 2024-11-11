import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Function to run Playwright with your existing browser profile
def run_playwright(link, browser):
    # Set up Playwright to use your existing user profile

    count = 0

    while count < 3:

        # Open the page (same URL you want to automate)
        page = browser.new_page()
        page.goto(link)

        try:
            # Step 1: Click the edit icon to reveal the options
            page.click('.edit-icon')  # Use the selector for the element you want to interact with

            # Step 2: Wait for the "Edit" or "Delete" button to become visible
            page.wait_for_selector('#edit-solution-btn', state='visible', timeout=5000)  # Wait for the edit option

            # Step 3: Click the "Edit" button
            page.click('#edit-solution-btn')  # or '.content-tool-item.delete' for Delete

            print("Successfully clicked the Edit button")

        except PlaywrightTimeoutError:
            print("Timeout: Edit option did not appear after clicking the edit icon.")

        finally:
            time.sleep(10)
            # Close the page to avoid memory leaks
            page.close()


        # Give some time for the action to complete (adjust as necessary)

        # Close the browser

        count += 1


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("../Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    link_text_path = resources_dir / "Dashboard Links.txt"

    with open(link_text_path, "r") as link_text:
        link_list = link_text.read().splitlines()

    print(link_list)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/User/AppData/Local/Google/Chrome/User Data",  # Adjust path as needed
            headless=False,  # Set to False so you can see the browser window
            channel="chrome"  # Use the installed Chrome browser, not Chromium
        )

        link = "https://content-tools.quizlet.com/discussion/question/what-would-the-waveform-of-an-aperiodic-sound-4b336c0a/"
        run_playwright(link, browser)

        browser.close()
