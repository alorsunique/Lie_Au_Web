import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def image_resize(image, min_size):
    working_image = image

    horizontal_size = working_image.size[0]
    vertical_size = working_image.size[1]

    min_pixel_size = min(working_image.size)

    if min_pixel_size > min_size:
        rescale_factor = min_pixel_size / min_size
        new_horizontal = int(horizontal_size / rescale_factor)
        new_vertical = int(vertical_size / rescale_factor)
    else:
        new_horizontal = horizontal_size
        new_vertical = vertical_size

    print(f"Source: {(horizontal_size, vertical_size)} | To Save: {(new_horizontal, new_vertical)}")

    rescaled_image = working_image.resize((new_horizontal, new_vertical), Image.LANCZOS)
    working_image.close()
    return rescaled_image


def article_box_download(url, resources_dir, webdriver_instance):
    driver = webdriver_instance
    driver.get(url)

    print("Waiting for page")
    time.sleep(5)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    post_number = str(url).split("/")[-1]

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    try:

        username = str(soup.find('div', class_='post__user').text).strip()
        username_dir = resources_dir / username

        print(f"Username: {username}")

        if not username_dir.exists():
            os.makedirs(username_dir)

        date_published = str(soup.find('div', class_='post__published').text).strip()
        date_published = date_published.replace(":", '')
        date_published = date_published.replace("-", '')
        date_published = date_published.replace(" ", '_')

        time_format = "Published_%Y%m%d"

        publish_date_object = datetime.strptime(date_published, time_format)

        post_title = str(soup.find('h1', class_='post__title').text).strip()
        post_content_text = str(soup.find('div', class_='post__content').text).strip()

        image_link_soup = soup.findAll('a', class_='fileThumb')
        downloadable_image_links = []

        for link in image_link_soup:
            if link.get('href').lower().endswith(image_extensions):
                downloadable_image_links.append(link.get('href'))

        count = 0
        downloadable_length = len(downloadable_image_links)

        if downloadable_length > 0:

            formatted_info = f"\nTitle\n{post_title}\nContent\n{post_content_text}\n"

            print(formatted_info)

            for image_link in downloadable_image_links:
                mod_time = publish_date_object + count * timedelta(seconds=1)
                mod_time_string = mod_time.strftime("%Y%m%d_%H%M%S")

                count += 1

                print(f"Attempting inner link | {count} / {downloadable_length}")

                parsed_url = urlparse(image_link).path.replace("/", '')
                output_name = f"{mod_time_string}_{post_number}_{parsed_url}"

                image_path = username_dir / output_name

                if not image_path.exists():
                    try:
                        time.sleep(5)
                        print(f"Requesting Image")
                        image = Image.open(requests.get(image_link, stream=True).raw)

                        if image.mode != 'RGB':
                            image = image.convert('RGB')

                        sourced_image_format = image.format

                        if sourced_image_format == 'JPEG':
                            to_save_image = image_resize(image, 1080)
                            to_save_image.save(image_path, format='JPEG', quality=85)
                        elif sourced_image_format == 'PNG':
                            to_save_image = image_resize(image, 1080)
                            to_save_image.save(image_path, format='PNG')
                        elif sourced_image_format == 'GIF':
                            image.save(image_path, format='GIF', save_all=True)
                        elif sourced_image_format == 'WEBP':
                            to_save_image = image_resize(image, 1080)
                            to_save_image.save(image_path, format='WEBP')
                        else:
                            image.save(image_path, format=sourced_image_format)

                        os.utime(image_path, (mod_time.timestamp(), mod_time.timestamp()))

                    except requests.exceptions.RequestException as error:
                        print(f"Cannot Fetch: {image_link}: {error}")

                    except Exception as error:
                        print(f"Cannot Process: {image_link}: {error}")
                else:
                    print(f"Already Downloaded: {image_link}")
    except:
        print("Error")


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("kumersu_resource_path.txt", "r") as kumersu_resources_text:
        kumersu_resources_dir = Path(str(kumersu_resources_text.readline()).replace('"', ''))

    with open("kumersu_key.txt", "r") as key_text:
        key_content = [line.strip() for line in key_text.readlines()]

    print(key_content)
    base_link = key_content[0]

    url = str(input("URL: "))

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    print("Loading Webdriver")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    article_box_download(url, kumersu_resources_dir, driver)

    driver.quit()
