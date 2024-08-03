import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import beibusosu_single


def acquire_card_links(url):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    card_soup = soup.findAll('a', class_='main-content__card-link')

    post_link_list = []

    for content in card_soup:
        print(f"Link found: {content.get('href')}")
        post_link_list.append(content.get('href'))

    return post_link_list


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("beibusosu_resource_path.txt", "r") as beibosusu_resources_text:
        beibosusu_resources_dir = Path(str(beibosusu_resources_text.readline()).replace('"', ''))

    url = str(input("URL: "))

    post_link_list = acquire_card_links(url)

    for link in post_link_list:
        print(f"Working {link}")
        beibusosu_single.main_image_box_download(link, beibosusu_resources_dir)
