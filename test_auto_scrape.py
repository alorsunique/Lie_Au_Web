from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def get_page_html(url):
    # Start a Playwright session
    with sync_playwright() as p:
        # Launch a new browser instance
        browser = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/User/AppData/Local/Google/Chrome/User Data",  # Adjust path as needed
            headless=False,  # Set to False so you can see the browser window
            channel="chrome"  # Use the installed Chrome browser, not Chromium
        )
        # Open a new page
        page = browser.new_page()

        # Go to the specified URL
        page.goto(url)

        time.sleep(10)

        # Wait for the page content to load
        page.wait_for_load_state("load")

        # Get the HTML content
        html_content = page.content()

        # Close the browser



        browser.close()

    return html_content


# Example usage
url = "https://content-tools.quizlet.com/discussion/question/which-of-the-following-are-features-of-2019-gt-rs-nissanbrembo-braking-system-b8c1bd6b/"
html = get_page_html(url)
print(html)

soup = BeautifulSoup(html, "lxml")  # Creates soup object

exercise_soup = soup.find_all('tr', class_='exercise')

count = 0

question_string_list = []
question_string = ""

global_count = 0

for exercise_row in exercise_soup:
    td_soup = exercise_row.find_all('td')
    if str(td_soup[1].text).strip() == "None":



        count += 1
        global_count += 1

        question_number = exercise_row.find('a').text

        question_content = exercise_row.find('textarea', class_='editable-attribute bound').text

        print(question_content)

        question_string += f"Question {question_number}\n{question_content}\n\n\n"

        if count == 5:
            question_string_list.append(question_string)
            question_string = ""
            count = 0

print(global_count)
