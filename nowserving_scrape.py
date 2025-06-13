import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


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



    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    print("Loading Webdriver")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1920, 1080)

    # Load the site to get the pages
    template_url = "https://nowserving.ph/search/?specializations=General%20Medicine&page="
    initial_url = f"{template_url}1"

    last_page_number = get_pagination_list(initial_url, driver)

    doctor_list = []

    count = 0
    while count < last_page_number:
        count += 1
        working_url = f"{template_url}{count}"

        extract_name_base(working_url, driver, doctor_list)

        current_time_value = datetime.now()
        current_time_string = current_time_value.strftime("%H:%M:%S")

        print(f"Doctor List Length: {len(doctor_list)} | Time: {current_time_string}")
