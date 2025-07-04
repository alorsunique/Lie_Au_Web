import os
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import kumersu_single


def forward_link_creator(url, webdriver_instance):
    driver = webdriver_instance
    driver.get(url)

    print("Waiting for page")
    time.sleep(5)
    page_source = driver.page_source

    # reqs = requests.get(url)  # Request the url
    # soup = BeautifulSoup(reqs.text, 'html.parser')

    soup = BeautifulSoup(page_source, 'html.parser')

    paginator_block_list = soup.findAll('div', class_='paginator')
    paginator_block_top_soup = paginator_block_list[0]

    paginator_top_small = paginator_block_top_soup.findAll('small')[0].text

    paginator_small_split = paginator_top_small.split(" ")
    starting_post_number = int(paginator_small_split[1]) - 1
    max_post_number = int(paginator_small_split[-1])

    if '?o=' in url:
        base_group_url, o_value = url.split('?o=')
    else:
        base_group_url = url

    forward_link_list = []

    while starting_post_number < max_post_number:
        modified_url = f"{base_group_url}?o={starting_post_number}"
        starting_post_number += 50
        print(modified_url)
        forward_link_list.append(modified_url)

    return forward_link_list


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("Kumersu_Resource_Path.txt", "r") as kumersu_resources_text:
        kumersu_resources_dir = Path(str(kumersu_resources_text.readline()).replace('"', ''))

    with open("Kumersu_Key.txt", "r") as key_text:
        key_content = [line.strip() for line in key_text.readlines()]

    print(key_content)
    base_link = key_content[0]

    url = str(input("URL: "))

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    print("Loading Webdriver")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    forward_link_list = forward_link_creator(url, driver)

    for forward_url in forward_link_list:
        base_group_url, o_value = forward_url.split('?o=')

        print(f"Working on the following forward: {forward_url}")

        driver.get(forward_url)

        print("Waiting for page")
        time.sleep(5)
        page_source = driver.page_source

        # reqs = requests.get(url)  # Request the url
        # soup = BeautifulSoup(reqs.text, 'html.parser')

        soup = BeautifulSoup(page_source, 'html.parser')

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

            print(f"\n{o_value} | Set {count} / {post_link_list_length} | Working on post {post}\n")

            valid_post_list = kumersu_single.revision_check(post, driver)

            for valid_post in valid_post_list:
                # kumersu_single.article_box_download(post, kumersu_resources_dir, driver)
                kumersu_single.article_box_download(valid_post, kumersu_resources_dir, driver)

    driver.quit()
