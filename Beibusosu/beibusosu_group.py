# Group download of beibusosu

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import beibusosu_single


# Get the links from the cards
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

    with open("Beibusosu_Resource_Path.txt", "r") as beibusosu_resources_text:
        beibusosu_resources_dir = Path(str(beibusosu_resources_text.readline()).replace('"', ''))

    catalog_path = beibusosu_resources_dir / "Catalog.xlsx"

    workable_group_list = []

    while True:
        print("\n--------------------------------\n")

        print("0. Exit Loop")
        print("1. Add Group")

        choice = str(input("Choice: "))

        if choice == "0":
            break
        elif choice == "1":
            url = str(input("URL: "))
            override_string = str(input("Override Input Y: ")).upper()

            if override_string == "Y":
                override = True
            else:
                override = False

            workable_element = (url, override)
            workable_group_list.append(workable_element)
        else:
            print("Did not catch that")

    for element in workable_group_list:
        url = element[0]
        override = element[1]

        post_link_list = acquire_card_links(url)
        post_link_length = len(post_link_list)

        post_link_list.reverse()

        count = 0
        total_requested_size = 0

        # Go through each link found in the card section
        for link in post_link_list:
            count += 1
            print(f"\nSet {count}/{post_link_length} | Working on set {link}\n")
            try:
                set_size = beibusosu_single.main_image_box_download(link, beibusosu_resources_dir, catalog_path,
                                                                    override)
                total_requested_size += set_size

                print(f"Current Set Requested Size: {total_requested_size / (1024 * 1024)} MB")
            except:
                print("Some error occured")
                pass

        print(f"Final Size: {total_requested_size / (1024 * 1024)} MB")
