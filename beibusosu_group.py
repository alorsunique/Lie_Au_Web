import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup

import os
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
import time

import requests
from PIL import Image
from bs4 import BeautifulSoup

def inner_link_download(url,resources_dir):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    left_top_box = soup.findAll('li', class_='aside-setting__views-item')
    publish_date = left_top_box[1].text.strip()
    publish_date_object = datetime.strptime(publish_date, "%Y-%m-%d")

    left_middle_box = soup.find_all('div', class_='aside-setting__chapter')
    model_soup = left_middle_box[-1]

    model_list = []
    found_model_soup = model_soup.find_all('a', class_='aside-setting__models-link')
    for potential_model in found_model_soup:
        model_list.append(potential_model.text.strip())

    main_image_box = soup.find_all('div', class_='box-massage')[0]
    image_link_soup = main_image_box.find_all('a', class_='box-massage__card-link slideshowGalleryImage')

    image_link_list = []
    for link in image_link_soup:
        image_link_list.append(link.get('href'))

    count = 0
    for image_link in image_link_list:
        time.sleep(2.5)

        to_add_mod_time = publish_date_object + count * timedelta(seconds=1)
        string_time = to_add_mod_time.strftime("%Y%m%d_%H%M%S")

        parsed_url = urlparse(image_link).path.replace("/", '')

        try:
            image = Image.open(requests.get(image_link, stream=True).raw)

            for model in model_list:

                model_dir = resources_dir / model

                if not model_dir.exists():
                    os.makedirs(model_dir)

                output_name = f"{model}_{string_time}_{parsed_url}"
                image_path = model_dir / output_name

                if image.mode != 'RGB':
                    image = image.convert('RGB')

                if not image_path.exists():
                    image.save(image_path, format='JPEG', quality=100)

                else:
                    print(f"Skipping")

                os.utime(image_path, (to_add_mod_time.timestamp(), to_add_mod_time.timestamp()))

        except requests.exceptions.RequestException as error:
            print(f"Cannot Fetch: {image_link}: {error}")

        except Exception as error:
            print(f"Cannot Process: {image_link}: {error}")

        count += 1


script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("beibusosu_resource_path.txt", "r") as beibosusu_resources_text:
    beibosusu_resources_dir = Path(str(beibosusu_resources_text.readline()).replace('"', ''))


url = str(input("URL: "))

request_result = requests.get(url)  # Request the url
soup = BeautifulSoup(request_result.text, 'html.parser')

card_soup = soup.findAll('a', class_='main-content__card-link')

post_link_list = []

for content in card_soup:
    print(f"Link found: {content.get('href')}")
    post_link_list.append(content.get('href'))

for link in post_link_list:
    print(f"Working {link}")
    inner_link_download(link, beibosusu_resources_dir)

