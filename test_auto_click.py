import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# Function to run Playwright with your existing browser profile
def run_playwright(link, browser):
    # Set up Playwright to use your existing user profile

    count = 0

    while count < 3:

    # Open the page (same URL you want to automate)
    page = browser.new_page()
    page.goto(link)

    time.sleep(15)

    # Wait for the button to become visible
    page.wait_for_selector("button.upload-ai-solution.unbound", timeout=10000)

    # Click the button
    button = page.query_selector("button.upload-ai-solution.unbound")
    if button:
        button.click()
        print("Button clicked successfully.")
    else:
        print("Button not found.")

    # Give some time for the action to complete (adjust as necessary)

    # Close the browser

    count += 1


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
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

        for link in link_list:
            run_playwright(link, browser)

        browser.close()
