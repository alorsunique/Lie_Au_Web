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




def profile_scrape(url, webdriver):
    pass

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    doctor_list_path = resources_dir / "NowServing Related" / "doctor_list.xlsx"
    if doctor_list_path.exists():
        df = pd.read_excel(doctor_list_path)

        doctor_list = df['Listed_Name'].tolist()
    else:
        doctor_list = []

    print(doctor_list)

    clean_list = []

    for entry in doctor_list:
        entry_split = entry.split(' ')

        print(entry_split)

        if 'Dr.' in entry_split:
            entry_split.remove('Dr.')

        print(entry_split)

        output = '-'.join(entry_split)

        print(output)

        test_url = f"https://seriousmd.com/doc/{output}"

        webbrowser.open(test_url)

        time.sleep(3)