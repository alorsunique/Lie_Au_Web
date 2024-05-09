import io
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))


def get_image_url(driver, search_query, thumbnail_selector, image_selector, max_url_count):
    image_url_list = set()

    search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
    driver.get(search_url)

    input_pause = input(f"Input anything to resume: ")

    display_thumbnails = driver.find_elements(By.CLASS_NAME, thumbnail_selector)
    print(f"Elements Found: {len(display_thumbnails)}")

    url_count = 0

    for thumbnail in display_thumbnails:
        print(f"Thumbnail: {thumbnail}")

        try:
            thumbnail.click()
            time.sleep(3)
        except:
            continue

        image_container = driver.find_elements(By.CSS_SELECTOR, image_selector)

        print(f"Image: {image_container}")

        for content in image_container:

            if content.get_attribute('src') and 'http' in content.get_attribute('src'):
                url_count += 1
                print(f"Found Image. Count: {url_count}")
                image_url_list.add(content.get_attribute('src'))

            if len(image_url_list) >= max_url_count:
                break

        if len(image_url_list) >= max_url_count:
            break

    return image_url_list


def download_images(image_url_list, download_dir):
    count = 0
    for entry in image_url_list:
        count += 1

        try:
            image_content = requests.get(entry).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)

            file_path = download_dir / f"image_{count}.jpg"

            with open(file_path, "wb") as f:
                image.save(f, "JPEG")

            print("Success")
        except Exception as e:
            print('Fail -', e)


search_query = input("Enter Search Query: ")
max_url_count = int(input("Enter Max URL Count: "))

current_time = time.time()
start_time = current_time
start_datetime = datetime.fromtimestamp(start_time)

start_datetime_formatted = start_datetime.strftime("%Y%m%d_%H%M%S")

session_dir = resources_dir / "Google Images Downloads" / start_datetime_formatted
if not session_dir.exists():
    os.makedirs(session_dir)

thumbnail_selector = "H8Rx8c"
image_selector = ".sFlh5c.pT0Scc.iPVvYb"

driver_options = Options()
driver_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=driver_options)

url_list = get_image_url(driver, search_query, thumbnail_selector, image_selector, max_url_count)
download_images(url_list, session_dir)
