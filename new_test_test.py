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

main_content = soup.findAll('a', class_='main-content__card-link')

post_link_list = []

for content in main_content:


    print(f"Link found: {content.get('href')}")
    post_link_list.append(content.get('href'))
