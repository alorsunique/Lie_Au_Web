import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup
from PIL import ImageSequence

import re



def collect_download_link(url, aidoru_key):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    left_link_list = []
    left_link_dict = {}

    item_soup = soup.findAll('div', class_='item')

    for item in item_soup:


        details_left_soup = item.find('div', class_='post-details-left')
        details_left_link_holder = details_left_soup.find('a')

        left_post_title = details_left_link_holder.get_text(strip=True)

        # print(left_post_title)

        working_link = f"{aidoru_key}{details_left_link_holder.get('href')}"

        post_number = details_left_link_holder.get('href').split('/')[-2]

        # print(f'Post Number: {post_number}')

        left_link_list.append(working_link)

        post_date_soup = item.find('div', class_='post-date')

        post_date_hold = post_date_soup.get("data-date")
        post_date_split = post_date_hold.split()

        date_info = post_date_split[0].replace('-', '')
        time_info = post_date_split[1].replace(':', '')

        post_date = f'{date_info}_{time_info}'

        # print(post_date)

        left_link_dict[working_link] = [post_date, post_number, left_post_title]



    return left_link_list, left_link_dict


def get_media_link(url, left_link_info):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    time_info = left_link_info[0]
    post_number_info = left_link_info[1]
    title_info = left_link_info[2]

    media_link_list = []
    front_title = ''

    try:
        post_media_soup = soup.find('div', class_='post-media')

        tag_block_soup = soup.find('div', class_='pb-block pb-block-tags')

        tags_soup = tag_block_soup.findAll('a')


        tag_list = []

        for tag in tags_soup:
            allowed_characters = re.compile(r'^[A-Za-z0-9_-]+$')

            if allowed_characters.match( tag.get_text() ):
                tag_list.append(tag.get_text())

        tag_string = ''

        if len(tag_list) > 0:
            tag_string = '_'.join(tag_list)

        # print(tag_string)

        front_title = f'{time_info}_{post_number_info}[_]{title_info}[_]{tag_string}'

        # print(front_title)




        # Find all images
        media_entry_soup = post_media_soup.findAll('a', class_='post-media-item')

        for entry in media_entry_soup:
            format_link = entry.get('href')

            working_link = f'https:{format_link}'

            media_link_list.append(working_link)

        # Find all videos
        media_entry_soup = post_media_soup.findAll('div', class_='post-media-item')

        for entry in media_entry_soup:

            video_soup = entry.find('video', class_='post-video')

            video_source_soup = video_soup.find('source', type='video/mp4')

            if video_source_soup and video_source_soup.has_attr("src"):
                # print(video_source_soup)

                try_source = video_source_soup.get("src")

                if len(try_source) == 0:
                    try_source = video_source_soup.get("data-src")

                working_link = f'https:{try_source}'

                media_link_list.append(working_link)

        print(media_link_list)

    except:
        print(f'Locked Content')

    return media_link_list, front_title







def download_media(url, front_title, save_path):
    """
    Downloads jpg/png/webp/gif/mp4 while preserving animation.
    save_path must include filename + extension.
    """

    parsed_url = urlparse(url).path.replace("/", '')

    output_name = f'{front_title}[_]{parsed_url}'

    output_path = save_path / output_name

    print(output_path)

    if not output_path.exists():



        # time.sleep(1)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        with requests.get(url, stream=True, headers=headers, timeout=30) as r:
            r.raise_for_status()

            content_type = r.headers.get("Content-Type", "").lower()

            # ---- VIDEO (MP4) ----
            if "video/mp4" in content_type or save_path.suffix == ".mp4":
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                return

            # ---- ANIMATED FORMATS (RAW SAVE) ----
            if any(ext in content_type for ext in ["image/webp", "image/gif"]):
                # Raw byte write preserves animation 100%
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return

            # ---- STATIC IMAGES (JPG / PNG) ----
            image = Image.open(r.raw)

            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")

            image.save(output_path)

        # os.utime(output_path, (mod_time.timestamp(), mod_time.timestamp()))

    else:
        print('Downloaded Already')






































if __name__ == '__main__':
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("AidoruSawaru_Resource_Path.txt", "r") as aidorusawaru_resources_text:
        aidorusawaru_resources_dir = Path(str(aidorusawaru_resources_text.readline()).replace('"', ''))

    with open("AidoruSawaru_Key.txt", "r") as key_text:
        key_content = [line.strip() for line in key_text.readlines()]



    while True:
        print("\n--------------------------------\n")

        print("0. Exit Loop")
        print("1. Single Page")
        print("2. Page Range")

        choice = str(input("Choice: "))

        if choice == "0":
            break





        elif choice == "1":

            url = str(input("URL: "))

            aidoru_key = key_content[0]

            left_link_list, left_link_dict = collect_download_link(url, aidoru_key)

            for entry in left_link_list:

                print(entry)

                left_link_info = left_link_dict[entry]

                media_link_list, front_title = get_media_link(entry, left_link_info)

                for entry in media_link_list:
                    download_media(entry, front_title, aidorusawaru_resources_dir)

        elif choice == "2":

            lower_bound = int(input("Lower Bound: "))
            upper_bound = int(input("Upper Bound: "))
            mid_tag = str(input('Mid Tag: '))


            count = lower_bound

            while count <= upper_bound:



                aidoru_key = key_content[0]

                if mid_tag == '':

                    working_url = f'{aidoru_key}/page/{count}/'

                else:
                    working_url = f'{aidoru_key}/{mid_tag}/page/{count}/'


                left_link_list, left_link_dict = collect_download_link(working_url, aidoru_key)

                for entry in left_link_list:

                    print(entry)

                    left_link_info = left_link_dict[entry]

                    media_link_list, front_title = get_media_link(entry, left_link_info)

                    for entry in media_link_list:
                        download_media(entry, front_title, aidorusawaru_resources_dir)

                count += 1


        else:
            print("Did not catch that")









