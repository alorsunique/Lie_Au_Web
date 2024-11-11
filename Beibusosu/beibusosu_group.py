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
    project_dir = script_path.parent.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("beibusosu_resource_path.txt", "r") as beibusosu_resources_text:
        beibusosu_resources_dir = Path(str(beibusosu_resources_text.readline()).replace('"', ''))

    catalog_path = beibusosu_resources_dir / "Catalog.xlsx"

    url = str(input("URL: "))
    override_string = str(input("Override Input Y: ")).upper()

    if override_string == "Y":
        override = True
    else:
        override = False

    post_link_list = acquire_card_links(url)
    post_link_length = len(post_link_list)

    count = 0
    total_requested_size = 0
    for link in post_link_list:
        count += 1
        print(f"\nSet {count}/{post_link_length} | Working on set {link}\n")
        try:
            set_size = beibusosu_single.main_image_box_download(link, beibusosu_resources_dir, catalog_path, override)
            total_requested_size += set_size

            print(f"Current Set Requested Size: {total_requested_size / (1024 * 1024)} MB")
        except:
            pass


    print(f"Final Size: {total_requested_size / (1024 * 1024)} MB")
