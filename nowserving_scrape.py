import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import webbrowser



def get_pagination_list(url, webdriver_instance):
    driver = webdriver_instance
    driver.get(url)

    print("Waiting for page")
    time.sleep(5)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    page_soup = soup.findAll('li', class_='pagination__page-item')

    last_page_soup = page_soup[-1]

    last_page_number = int(last_page_soup.find('a', class_='pagination__page-link-item').text)

    return last_page_number

def extract_name_base(url, webdriver_instance, doctor_list):
    driver = webdriver_instance
    driver.get(url)

    print("Waiting for page")
    time.sleep(5)
    page_source = driver.page_source


    soup = BeautifulSoup(page_source, 'html.parser')

    doctor_name_soup = soup.findAll("div", class_="doctor-name")

    for entry in doctor_name_soup:
        doctor_list.append(entry.text.strip())

    return doctor_list



if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    # Options for Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    print("Loading Webdriver")

    # Loads the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Set the window size to access web version of the page
    driver.set_window_size(1920, 1080)





    # template_url = "https://nowserving.ph/search/?specializations=General%20Medicine&page="
    template_url = str(input("Input template URL: "))[:-1]

    # Load the site to get the pages
    initial_url = f"{template_url}1"
    last_page_number = get_pagination_list(initial_url, driver)
    print(f"Last Page: {last_page_number}")
    max_count = int(input("Input Max Count: "))
    start_count = int(input("Input Start Count: "))


    doctor_list_path = resources_dir / "NowServing Related" / "doctor_list.xlsx"
    if doctor_list_path.exists():
        df = pd.read_excel(doctor_list_path)

        doctor_list = df['Listed_Name'].tolist()
    else:
        doctor_list = []

    initial_doctor_set = set(doctor_list)
    print(f"Initial Length: {len(initial_doctor_set)}")

    count = start_count
    while count < max_count:
        count += 1
        working_url = f"{template_url}{count}"

        doctor_list = extract_name_base(working_url, driver, doctor_list)

        current_time_value = datetime.now()
        current_time_string = current_time_value.strftime("%H:%M:%S")

        print(f"Doctor List Length: {len(doctor_list)} | Time: {current_time_string} | Count: {count}/{max_count}")

    doctor_set = set(doctor_list)

    added_set = doctor_set.difference(initial_doctor_set)
    print(f"Added doctor count: {len(added_set)}")

    trimmed_doctor_list = list(doctor_set)
    sorted_doctor_list = sorted(trimmed_doctor_list)

    out_dict = {"Listed_Name":sorted_doctor_list}
    out_df = pd.DataFrame(out_dict)

    if doctor_list_path.exists():
        os.remove(doctor_list_path)

    out_df.to_excel(doctor_list_path, sheet_name='Doctor Names', index=False)

