# Group download of beibusosu

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from cattrs import override

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

    read_df = pd.read_excel(catalog_path)

    workable_df = read_df.loc[ ~read_df['Home Link'].isna() ]


    model_list = workable_df['Model'].tolist()
    home_link_list = workable_df['Home Link'].tolist()

    last_sweep_path = beibusosu_resources_dir / 'Last_Sweep.txt'

    if not last_sweep_path.exists():
        with open(last_sweep_path, "w") as writer:
            writer.close()

    with open(last_sweep_path, 'r') as reader:
        last_entry = reader.read()
        reader.close()

    print(last_entry)


    if not last_entry == '':
        workable_model_list = model_list[model_list.index(last_entry) + 1:].copy()
        workable_home_link_list = home_link_list[model_list.index(last_entry) + 1:].copy()
    else:
        workable_model_list = model_list.copy()
        workable_home_link_list = home_link_list.copy()

    print(workable_model_list)

    count = 0

    while count < len(workable_home_link_list):

        to_process_model = workable_model_list[count]
        to_process_home_link = workable_home_link_list[count]


        to_process_home_link_list = []

        in_count = 0
        break_condition = False

        time.sleep(2)

        while not break_condition:
            in_count += 1
            test_link = f'{to_process_home_link}/page{in_count}.html'
            print(test_link)

            try:
                response = requests.get(test_link)

                soup = BeautifulSoup(response.text, 'html.parser')

                if 'There is no content for this model yet.' in str(soup):
                    break_condition = True
                else:
                    to_process_home_link_list.append(test_link)

            except:
                pass


        to_process_home_link_list.reverse()

        print(to_process_home_link_list)

        time.sleep(2)

        for home_page_link in to_process_home_link_list:
            override = ''
            post_link_list = acquire_card_links(home_page_link)
            post_link_length = len(post_link_list)

            post_link_list.reverse()

            post_count = 0
            total_requested_size = 0

            # Go through each link found in the card section
            for link in post_link_list:
                post_count += 1
                print(f"\nSet {post_count}/{post_link_length} | Working on set {link}\n")
                try:
                    set_size = beibusosu_single.main_image_box_download(link, beibusosu_resources_dir, catalog_path,
                                                                        override)
                    total_requested_size += set_size

                    print(f"Current Set Requested Size: {total_requested_size / (1024 * 1024)} MB")
                except:
                    print("Some error occured")
                    pass

            print(f"Final Size: {total_requested_size / (1024 * 1024)} MB")

        if last_sweep_path.exists():
            os.remove(last_sweep_path)

        is_last = workable_model_list[-1] == to_process_model

        if not is_last:
            with open(last_sweep_path, 'w') as writer:
                # writer.write(account)
                writer.write( workable_model_list[ workable_model_list.index(to_process_model) ] )
                writer.close()

        count += 1