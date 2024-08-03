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

with open("kumersu_resource_path.txt", "r") as kumersu_resources_text:
    kumersu_resources_dir = Path(str(kumersu_resources_text.readline()).replace('"', ''))

with open("kumersu_key.txt", "r") as key_text:
    key_content = [line.strip() for line in key_text.readlines()]

print(key_content)
base_link = key_content[0]

url = str(input("URL: "))

reqs = requests.get(url)  # Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')

article_list = soup.findAll('article', class_='post-card post-card--preview')

post_link_list = []

for article in article_list:

    links = article.findAll('a')
    for link in links:
        final_link = base_link + link.get('href')
        print(f"Link found: {link.get('href')}")
        post_link_list.append(final_link)

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

post_link_list_length = len(post_link_list)
count = 0

for post in post_link_list:
    time.sleep(1.25)

    count += 1

    print(f"Working on link {count} / {post_link_list_length}")

    new_soup = BeautifulSoup(requests.get(post).text, 'html.parser')

    try:
        user_name = str(new_soup.find('a', class_='post__user-name').text).strip()

        user_name_dir = kumersu_resources_dir / user_name

        if not user_name_dir.exists():
            os.makedirs(user_name_dir)

        date_published = str(new_soup.find('div', class_='post__published').text).strip()
        date_published = date_published.replace(":", '')
        date_published = date_published.replace("-", '')

        post_title = str(new_soup.find('h1', class_='post__title').text).strip()
        post_text_content = str(new_soup.find('div', class_='post__content').text).strip()

        image_links = new_soup.findAll('a', class_='fileThumb')
        downloadable_image_links = []

        for link in image_links:
            raw_link = link.get('href')

            if raw_link.lower().endswith(image_extensions):
                downloadable_image_links.append(raw_link)

        inner_count = 0
        downloable_length = len(downloadable_image_links)


        if downloable_length > 0:

            post_dir = user_name_dir / date_published

            if not post_dir.exists():
                os.mkdir(post_dir)

            info_text_path = post_dir / "Info.txt"
            if info_text_path.exists():
                os.remove(info_text_path)

            formatted_info = f"Title\n{post_title}\nContent\n{post_text_content}"

            print(post_title)

            with open(info_text_path, 'w', encoding='utf-8') as writer:
                writer.write(formatted_info)

            for image_link in downloadable_image_links:
                time.sleep(2.5)

                inner_count += 1

                print(f"Attempting inner link {inner_count} / {downloable_length}")

                parsed_url = urlparse(image_link).path.replace("/", '')

                try:
                    image_path = post_dir / parsed_url
                    if not image_path.exists():
                        image = Image.open(requests.get(image_link, stream=True).raw)

                        if image.mode != 'RGB':
                            image = image.convert('RGB')

                        image.save(image_path, format='JPEG', quality=100)
                    else:
                        print(f"Skipping")

                except requests.exceptions.RequestException as error:
                    print(f"Cannot Fetch: {image_link}: {error}")

                except Exception as error:
                    print(f"Cannot Process: {image_link}: {error}")
    except:
        print(f"Error")