import webbrowser
import time
from PIL import  Image
from urllib.parse import urlparse
from pathlib import Path
import os

import requests
from bs4 import BeautifulSoup

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("key_resource_path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

with open("key.txt", "r") as key_text:
    key_content = [line.strip() for line in key_text.readlines()]



print(key_content)
base_link = key_content[0]
chrome_path = key_content[1]
# Register Chrome

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


url = str(input("URL: "))

reqs = requests.get(url) #Request the url
soup = BeautifulSoup(reqs.text, 'html.parser')



article_list = soup.findAll('article', class_ = 'post-card post-card--preview')

#print(article_list)

link_list = []

for entry in article_list:

    links = entry.findAll('a')

    #print(entry)
    print(f"-------------------------------------------------------------------------------")

    for link in links:

        final_link = base_link + link.get('href')

        print(final_link)

        print(link.get('href'))
        link_list.append(final_link)
    print(f"-------------------------------------------------------------------------------")

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

for entry in link_list:
    print("Hey")
    new_soup = BeautifulSoup(requests.get(entry).text, 'html.parser')
    print(new_soup)

    user_name = str(new_soup.find('a',class_='post__user-name').text).strip()

    print(f"CUNTPISS: {user_name}")

    user_name_dir = resources_dir / user_name

    if not user_name_dir.exists():
        os.mkdir(user_name_dir)

    date_published = str(new_soup.find('div',class_='post__published').text).strip()
    date_published = date_published.replace(":",'')
    date_published = date_published.replace("-",'')

    post_title = str(new_soup.find('h1',class_='post__title').text).strip()
    post_text_content = str(new_soup.find('div',class_='post__content').text).strip()

    print(date_published)
    print(post_title)
    print(post_text_content)

    links = new_soup.findAll('a', class_='fileThumb')

    print(f"Links {links}")

    downloadable_img_links = []

    for link in links:
        raw_link = link.get('href')

        if raw_link.lower().endswith(image_extensions):
            downloadable_img_links.append(raw_link)


    print(downloadable_img_links)

    if len(downloadable_img_links) > 0:

        post_dir = user_name_dir / date_published

        if not post_dir.exists():
            os.mkdir(post_dir)

        info_text_path = post_dir / "Info.txt"
        if info_text_path.exists():
            os.remove(info_text_path)

        formatted_info = f"Title\n{post_title}\nContent\n{post_text_content}"

        with open(info_text_path, 'w', encoding='utf-8') as writer:
            writer.write(formatted_info)


        for image in downloadable_img_links:
            parsed_url = urlparse(image).path.replace("/",'')

            try:
                img = Image.open(requests.get(image, stream=True).raw)
                img.show()

                image_path = post_dir / parsed_url
                img.save(image_path, format='JPEG', quality=100)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching image URL {image}: {e}")
            except Exception as e:
                print(f"Error processing image {image}: {e}")
