import os
import time
from pathlib import Path

import bs4

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

print(resources_dir)

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By





search_query = input("Enter your Google Images search query: ")
search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"


driver_options = Options()
driver_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=driver_options)
driver.get(search_url)

input_pause = input(f"Input anything to resume: ")

image_url_list = set()

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class': "H8Rx8c"})

print(len(containers))

display_thumbnails = driver.find_elements(By.CLASS_NAME, "H8Rx8c")

print(len(display_thumbnails))

max_url_count = 10

for thumbnail in display_thumbnails:
    print(f"Thumbnail: {thumbnail}")

    try:
        thumbnail.click()
        time.sleep(4)
    except:
        continue

    #image_container = driver.find_elements(By.CLASS_NAME, "sFlh5c pT0Scc iPVvYb")
    #page_html = driver.page_source
    #pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    #image_container = pageSoup.findAll('div', {'class': "p7sI2 PUxBg"})

    #print(pageSoup)

    #print(len(image_container))
    #print(type(image_container))
    # Sva75c > div.A8mJGd.NDuZHe.OGftbe-N7Eqid-H9tDt > div.LrPjRb > div.AQyBn > div.tvh9oe.BIB1wf > c-wiz > div > div > div > div > div.v6bUne > div.p7sI2.PUxBg > a > img.sFlh5c.pT0Scc.iPVvYb
    image_container = driver.find_elements(By.CSS_SELECTOR, ".sFlh5c.pT0Scc.iPVvYb")

    print(image_container)

    for content in image_container:

        if content.get_attribute('src') and 'http' in content.get_attribute('src'):
            print(f"Found Image")
            image_url_list.add(content.get_attribute('src'))

        if len(image_url_list) >= max_url_count:
            break



    time.sleep(2)

    if len(image_url_list) >= max_url_count:
        break

print(image_url_list)

