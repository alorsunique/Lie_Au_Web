import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup


def article_box_download(url, resources_dir):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    try:
        username = str(soup.find('a', class_='post__user-name').text).strip()
        username_dir = resources_dir / username

        if not username_dir.exists():
            os.makedirs(username_dir)

        date_published = str(soup.find('div', class_='post__published').text).strip()
        date_published = date_published.replace(":", '')
        date_published = date_published.replace("-", '')
        date_published = date_published.replace(" ", '_')

        time_format = "Published_%Y%m%d_%H%M%S"
        publish_date_object = datetime.strptime(date_published, time_format)

        print(date_published)

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

            post_dir = username_dir / date_published

            if not post_dir.exists():
                os.mkdir(post_dir)

            info_text_path = post_dir / "Info.txt"
            if info_text_path.exists():
                os.remove(info_text_path)

            formatted_info = f"Title\n{post_title}\nContent\n{post_content_text}"

            print(post_title)

            with open(info_text_path, 'w', encoding='utf-8') as writer:
                writer.write(formatted_info)

            for image_link in downloadable_image_links:
                mod_time = publish_date_object + count * timedelta(seconds=1)
                mod_time_string = mod_time.strftime("%Y%m%d_%H%M%S")

                count += 1

                print(f"Attempting inner link | {count} / {downloadable_length}")

                parsed_url = urlparse(image_link).path.replace("/", '')
                output_name = f"{mod_time_string}_{parsed_url}"

                image_path = post_dir / output_name

                if not image_path.exists():
                    try:
                        time.sleep(2)
                        image = Image.open(requests.get(image_link, stream=True).raw)

                        sourced_image_format = image.format

                        if sourced_image_format == 'JPEG':
                            image.save(image_path, format='JPEG', quality=100)
                        elif sourced_image_format == 'PNG':
                            image.save(image_path, format='PNG')
                        elif sourced_image_format == 'GIF':
                            image.save(image_path, format='GIF', save_all=True)
                        elif sourced_image_format == 'WEBP':
                            image.save(image_path, format='WEBP')
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

    article_box_download(url, kumersu_resources_dir)
