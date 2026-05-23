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



if __name__ == '__main__':
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("AidoruSawaru_Resource_Path.txt", "r") as aidorusawaru_resources_text:
        aidorusawaru_resources_dir = Path(str(aidorusawaru_resources_text.readline()).replace('"', ''))

    with open("AidoruSawaru_Key.txt", "r") as key_text:
        key_content = [line.strip() for line in key_text.readlines()]

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    aidoru_author_list_path = resources_dir / f'Aidoru_Exclude.txt'

    with open(aidoru_author_list_path, "r") as author_list_text:
        author_list = [line.strip() for line in author_list_text.readlines()]

    print(author_list)
    sorted_author_list = sorted(author_list)

    with open(aidoru_author_list_path, 'w') as writer:
        for author in sorted_author_list:
            writer.write("%s\n" % author)

    excluded_author_list = []

    for entry in sorted_author_list:
        excluded_author_list.append(entry.lower())

    to_remove_list = []

    for entry in aidorusawaru_resources_dir.iterdir():
        formatted_year = int(str(entry.name)[0:4])

        if formatted_year < 2024:
            to_remove_list.append(entry)


    for entry in aidorusawaru_resources_dir.iterdir():
        creator_block = str(entry.name).split('[_]')[2]

        for excluded_author in excluded_author_list:

            if excluded_author.lower() in creator_block.lower():
                if entry not in to_remove_list:
                    to_remove_list.append(entry)




    webp_list = []
    mp4_list = []

    for entry in aidorusawaru_resources_dir.rglob('*.webp'):

        formatted_name = ''.join(entry.stem.split('-')[0:-1])

        webp_list.append(formatted_name)

    for entry in aidorusawaru_resources_dir.rglob('*.mp4'):

        formatted_name = ''.join(entry.stem.split('-')[0:-1])

        mp4_list.append(formatted_name)

    common_set = set(webp_list).intersection( set(mp4_list) )

    print(common_set)
    print(len(common_set))

    common_list = sorted( list(common_set) )

    print(common_list)
    print(len(common_list))



    for entry in aidorusawaru_resources_dir.rglob('*.webp'):

        # print(entry)
        # print(str(entry))

        formatted_entry = ''.join(entry.stem.split('-'))

        for common in common_list:

            # print(common)

            if str(common) in formatted_entry:

                # print(entry)

                if entry not in to_remove_list:
                    to_remove_list.append(entry)

    # print(to_remove_list)

    for entry in to_remove_list:
        os.remove(entry)












