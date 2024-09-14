import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup

import beibusosu_catalog


def image_resize(image, min_size):
    working_image = image

    horizontal_size = working_image.size[0]
    vertical_size = working_image.size[1]

    min_pixel_size = min(working_image.size)

    if min_pixel_size > min_size:
        rescale_factor = min_pixel_size / min_size
        new_horizontal = int(horizontal_size / rescale_factor)
        new_vertical = int(vertical_size / rescale_factor)
    else:
        new_horizontal = horizontal_size
        new_vertical = vertical_size

    print(f"Source: {(horizontal_size, vertical_size)} | To Save: {(new_horizontal, new_vertical)}")

    rescaled_image = working_image.resize((new_horizontal, new_vertical), Image.LANCZOS)
    working_image.close()
    return rescaled_image


def main_image_box_download(url, resources_dir, catalog_file, override):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    try:
        left_top_box = soup.findAll('li', class_='aside-setting__views-item')
        publish_date = left_top_box[1].text.strip()
        print(f"Publish Date: {publish_date}")
        publish_date_object = datetime.strptime(publish_date, "%Y-%m-%d")

        left_middle_box = soup.find_all('div', class_='aside-setting__chapter')
        model_soup = left_middle_box[-1]

        model_dict = beibusosu_catalog.catalog_read(catalog_file)

        model_list = []
        found_model = model_soup.find_all('a', class_='aside-setting__models-link')
        for model in found_model:
            model_list.append(model.text.strip())

        copy_model_list = model_list.copy()
        for copy_model in copy_model_list:
            if not copy_model in model_dict:
                beibusosu_catalog.add_model(catalog_file, copy_model, 0)
                if not override:
                    model_list.remove(copy_model)
            else:
                if not model_dict[copy_model] == 1 and not override:
                    model_list.remove(copy_model)

        print(f"Final Model List: {model_list}")

        for model in model_list:
            model_dir = resources_dir / model

            if not model_dir.exists():
                os.makedirs(model_dir)

        main_image_box = soup.find_all('div', class_='box-massage')[0]

        lead_image_link_soup = main_image_box.find_all('a', class_='box-massage__card-link')
        # image_link_soup = main_image_box.find_all('a', class_='box-massage__card-link slideshowGalleryImage')

        source_site_text = main_image_box.find('a', class_='box-massage__head').get_text(strip=True)
        source_site_text = source_site_text.replace("Watch Full Scene at", "").strip()
        source_site_text = source_site_text.replace(" ", "_")

        print(source_site_text)

        image_link_list = []

        for link in lead_image_link_soup:
            image_link_list.append(link.get('href'))

        # for link in image_link_soup:
        # image_link_list.append(link.get('href'))

        image_link_list_length = len(image_link_list)

        count = 0
        total_requested_size = 0
        for image_link in image_link_list:

            mod_time = publish_date_object + count * timedelta(seconds=1)
            mod_time_string = mod_time.strftime("%Y%m%d_%H%M%S")

            count += 1
            print(f"{count}/{image_link_list_length} | Working: {image_link}")

            parsed_url = urlparse(image_link).path.replace("/", '')
            output_name = f"{source_site_text}_{mod_time_string}_{parsed_url}"

            try:
                absent_condition = False

                for model in model_list:
                    model_dir = resources_dir / model
                    image_path = model_dir / output_name

                    if not image_path.exists():
                        absent_condition = True

                if absent_condition:
                    print("Missing copy")
                    time.sleep(1)

                    image_size = requests.head(image_link).headers.get('Content-Length', 0)
                    print(f"Requested Size: {float(image_size) / (1024 * 1024)} MB")
                    total_requested_size += float(image_size)

                    image = Image.open(requests.get(image_link, stream=True).raw)

                    if image.mode != 'RGB':
                        image = image.convert('RGB')

                    to_save_image = image_resize(image, 1080)

                    for model in model_list:
                        model_dir = resources_dir / model
                        image_path = model_dir / output_name

                        if not image_path.exists():

                            to_save_image.save(image_path, format='JPEG', quality=85)
                        else:
                            print(f"{image_link} | Already downloaded for {model}")

                        os.utime(image_path, (mod_time.timestamp(), mod_time.timestamp()))

                else:
                    print("All models involved cleared")

            except requests.exceptions.RequestException as error:
                print(f"Cannot Fetch: {image_link}: {error}")

            except Exception as error:
                print(f"Cannot Process: {image_link}: {error}")

        print(f"Set Total Requested Size: {total_requested_size / (1024 * 1024)} MB")
        return total_requested_size
    except:
        print("Elements not found")


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

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
    total_requested_size = 0

    total_requested_size = main_image_box_download(url, beibusosu_resources_dir, catalog_path, override)

    print(f"Final Size: {total_requested_size / (1024 * 1024)} MB")
