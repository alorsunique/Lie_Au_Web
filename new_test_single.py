import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("test_resource_path.txt", "r") as test_resources_text:
    test_resources_dir = Path(str(test_resources_text.readline()).replace('"', ''))

with open("test_key.txt", "r") as key_text:
    key_content = [line.strip() for line in key_text.readlines()]

print(key_content)
base_link = key_content[0]

url = str(input("URL: "))

reqs = requests.get(url)  # Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')

print(soup)

aside_setting = soup.findAll('li', class_='aside-setting__views-item')
print(f"------------")

publish_date = aside_setting[1].text.strip()
print(publish_date)



category_block = soup.find_all('div', class_='aside-setting__chapter')

model_block = category_block[-1]

model_list = []
model_setting = model_block.find_all('a', class_='aside-setting__models-link')

for potential_model in model_setting:
    model_list.append(potential_model.text.strip())

print(model_list)

image_link_list = []

box_massage_big = soup.find_all('div', class_='box-massage')[0]

links = box_massage_big.find_all('a',class_='box-massage__card-link slideshowGalleryImage')

for link in links:
    image_link_list.append(link.get('href'))

for link in image_link_list:
    image = Image.open(requests.get(link, stream=True).raw)
    image.show()