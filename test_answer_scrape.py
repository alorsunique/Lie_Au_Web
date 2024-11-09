import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from openai import AzureOpenAI

from bs4 import BeautifulSoup

# Function to run Playwright with your existing browser profile
def run_playwright(link, browser):
    # Set up Playwright to use your existing user profile



    # Open the page (same URL you want to automate)
    page = browser.new_page()
    page.goto(link)

    time.sleep(15)

    # Wait for the button to become visible

    page.wait_for_load_state("load")

    # Get the HTML content
    html_content = page.content()


    page.close()

    # Give some time for the action to complete (adjust as necessary)

    # Close the browser

    return html_content



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

    api_key_text_path = resources_dir / "API Key.txt"

    with open(api_key_text_path, "r") as api_key_text:
        api_info_list = api_key_text.read().splitlines()


    API = api_info_list[0]
    endpoint = api_info_list[1]
    version = api_info_list[2]
    deployment_name = api_info_list[3]

    system_prompt = """
        You are an expert across several scientific fields, with a specialty in Physics. You will review a solution made by an instructor to see if it makes sense.

        The question will be provided to you as well as the solution. The question and solution are written in LaTeX. You will check if the solution makes sense.
        Also you need to make sure that the computations are done properly. 
        
        If the solution requires a figure, that should automatically be a no as you aim to minimize the use of figures.
        
        You will respond with 'Valid Solution' if the solution is valid. If it invalid, please respond with the corrected solution.
        """



    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="C:/Users/User/AppData/Local/Google/Chrome/User Data",  # Adjust path as needed
            headless=False,  # Set to False so you can see the browser window
            channel="chrome"  # Use the installed Chrome browser, not Chromium
        )

        for link in link_list:
            html_content = run_playwright(link, browser)

            soup = BeautifulSoup(html_content, "lxml")  # Creates soup object

            #print(soup)

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

            for i, entry in enumerate(ai_answer_soup, start=1):
                # Find all div elements with the 'react-result-cell' class within each solution block
                latex_blocks = entry.find_all("div", class_="react-result-cell")

                latex_expressions = []
                for latex_block in latex_blocks:
                    latex = latex_block.get("data-latex")
                    if latex:
                        latex_expressions.append(latex)

                print(latex_expressions)

                string_latex = str(latex_expressions)

                client = AzureOpenAI(
                    azure_endpoint=endpoint,
                    api_key=API,
                    api_version=version,
                )

                message_list = [
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                ]

                message_list.append(
                    {
                        "role": "user",
                        "content": f"The question is {question_text}. The solution provided is {string_latex}",
                    }
                )

                response = client.chat.completions.create(
                    model=deployment_name,
                    messages=message_list,
                )

                response_message = response.choices[0].message

                print(response_message.content)

        browser.close()
