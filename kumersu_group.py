import os
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import kumersu_single

if __name__ == "__main__":
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

    post_link_list_length = len(post_link_list)
    count = 0

    for post in post_link_list:
        time.sleep(1)

        count += 1

        print(f"\nSet {count} / {post_link_list_length} | Working on post {post}\n")

        kumersu_single.article_box_download(post, kumersu_resources_dir)
