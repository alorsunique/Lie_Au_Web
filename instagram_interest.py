import time
from pathlib import Path

import numpy as np
import pandas as pd
from selenium import webdriver

follow_dir = Path("D:\Projects\PycharmProjects Resources\Piplup Resources\Follow")
interest_file = follow_dir / "ricardo_guinto_Interest.xlsx"

interest_list = []

import_dataframe = pd.read_excel(interest_file)
for index, row in import_dataframe.iterrows():
    account_string = row.iloc[0]
    if not pd.isna(account_string):
        account_split = account_string.split()
        interest_list.append(account_split[1])

driver = webdriver.Firefox()

while True:
    continue_input = input(f"Input: ")
    if continue_input.lower() == "y":
        break

print(len(interest_list))

for account in interest_list:
    driver.execute_script("window.open('', '_blank');")

    driver.switch_to.window(driver.window_handles[-1])

    website_url = f"https://www.instagram.com/{account}"
    driver.get(website_url)

    sleep_time = np.random.randint(15, 30)
    print(f"Sleeping for {sleep_time}")
    time.sleep(sleep_time)
