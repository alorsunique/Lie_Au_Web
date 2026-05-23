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



    creator_list = []

    for entry in aidorusawaru_resources_dir.iterdir():

        # print(entry)
        # title_block = str(entry.name).split('[_]')[1]
        creator_block = str(entry.name).split('[_]')[2]


        creator = creator_block.split('_')[0]

        if creator not in creator_list:
            creator_list.append(creator)

        # print(creator_block)

    sorted_creator_list = sorted(creator_list)

    for creator in sorted_creator_list:
        print(creator)





