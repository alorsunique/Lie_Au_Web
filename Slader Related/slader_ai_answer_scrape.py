import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# Function to run Playwright with your existing browser profile
def run_playwright(link, browser, link_count):
    print(f"Link: {link_count + 1}")
    page = browser.new_page()
    page.goto(link)

    time.sleep(10)
    print("Time Waiting: 10")

    page.wait_for_load_state("load")

    # Get the HTML content
    html_content = page.content()

    page.close()

    link_count += 1

    return html_content, link_count

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

    out_going_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/User/AppData/Local/Google/Chrome/User Data",  # Adjust path as needed
            headless=False,  # Set to False so you can see the browser window
            channel="chrome"  # Use the installed Chrome browser, not Chromium
        )

        link_count = 0

        for link in link_list:
            html_content, link_count = run_playwright(link, browser, link_count)

            soup = BeautifulSoup(html_content, "lxml")  # Creates soup object
            question_section = soup.find("section", class_="question__markdown")

            # Extract the question text from the 'data-latex' attribute
            if question_section:
                question_text = question_section.get("data-latex")
                print("Extracted Question:", question_text)
            else:
                print("Question not found.")

            solution_list_soup = soup.find_all('section', class_='solutions-list')

            ai_answer_soup = solution_list_soup[0].find_all('article', class_='solution')

            print(len(ai_answer_soup))

            actual_solution_list = []

            for i, entry in enumerate(ai_answer_soup, start=1):

                latex_blocks = entry.find_all("div", class_="react-result-cell")

                latex_expressions = []
                for latex_block in latex_blocks:
                    latex = latex_block.get("data-latex")
                    if latex:
                        latex_expressions.append(latex)

                actual_solution_list.append(repr(latex_expressions))

            print(actual_solution_list)
            out_going_data.append([question_text] + actual_solution_list[:3])

        browser.close()

    df = pd.DataFrame(out_going_data, columns=['Question', 'Solution List 1', 'Solution List 2', 'Solution List 3'])

    # Save the DataFrame to an Excel file
    output_path = resources_dir / "QuestionAnswer.xlsx"
    if output_path.exists():
        os.remove(output_path)
    df.to_excel(output_path, index=False)

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session End Time: {current_time}")
    print(f"Total Session Run Time: {finish_time - start_time}")
