import os
import time
from pathlib import Path

from datetime import datetime

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Function to run Playwright with your existing browser profile
def run_playwright(link, browser, link_count):

    print(f"Working on: {link}")
    count = 0

    present_button = True

    while count < 3 and present_button:
        print(f"Link: {link_count + 1} | Run: {count+1}")
        page = browser.new_page()
        page.goto(link)

        # Wait for the button to become visible
        time.sleep(10)
        print("Time Waiting: 10")

        try:
            page.wait_for_selector("button.upload-ai-solution.unbound", timeout=10000)

            print("Button found")

            # Click the button
            button = page.query_selector("button.upload-ai-solution.unbound")
            if button:
                button.click()
                print("Button clicked successfully.")
                time.sleep(10)
                print("Waiting for button to respond. Additional Time Waiting: 10")
            else:
                print("Button not found.")

        except PlaywrightTimeoutError:
            print("Button did not appear on the page within the timeout.")
            present_button = False

        page.close()

        count += 1

    link_count += 1
    return link_count


if __name__ == "__main__":
    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session Start Time: {current_time}")


    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    link_text_path = resources_dir / "Dashboard Links.txt"

    with open(link_text_path, "r") as link_text:
        link_list = link_text.read().splitlines()

    with sync_playwright() as p:

        # Set up Playwright to use your existing user profile
        browser = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/User/AppData/Local/Google/Chrome/User Data",  # Adjust path as needed
            headless=False,  # Set to False so you can see the browser window
            channel="chrome"  # Use the installed Chrome browser, not Chromium
        )

        link_count = 0
        for link in link_list:
            link_count = run_playwright(link, browser, link_count)

        browser.close()

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session End Time: {current_time}")
    print(f"Total Session Run Time: {finish_time - start_time}")