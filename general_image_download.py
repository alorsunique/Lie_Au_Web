import os
import time
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests
from PIL import Image


def excel_create(excel_link_file):
    if not excel_link_file.exists():
        model_list = []
        dataframe = pd.DataFrame(model_list, columns=['Link'])
        dataframe.to_excel(excel_link_file, sheet_name='Links', index=False)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    download_excel_pointer = resources_dir / "IDS_Pointer.txt"

    with open(download_excel_pointer, "r") as download_excel_pointer_text:
        download_excel_path = Path(str(download_excel_pointer_text.readline()).replace('"', ''))

    excel_create(download_excel_path)

    dataframe = pd.read_excel(download_excel_path)

    initial_link_list = dataframe['Link'].tolist()
    initial_link_set = set(initial_link_list)

    sorted_list = sorted(list(initial_link_set))

    general_download_dir = resources_dir / "General Image Download"
    if not general_download_dir.exists():
        os.mkdir(general_download_dir)

    for link in sorted_list:
        print(f"Link: {link}\n")
        print(f"Parsed: {urlparse(link)}\n")
        parsed_url = urlparse(link).path.replace("/", '')
        output_name = f"{parsed_url}"

        image_path = general_download_dir / output_name
        if not image_path.exists():

            try:
                time.sleep(5)
                image = Image.open(requests.get(link, stream=True).raw)

                sourced_image_format = image.format

                if sourced_image_format == 'JPEG':
                    image.save(image_path, format='JPEG', quality=100)
                elif sourced_image_format == 'PNG':
                    image.save(image_path, format='PNG')
                elif sourced_image_format == 'GIF':
                    image.save(image_path, format='GIF', save_all=True)
                elif sourced_image_format == 'WEBP':
                    image.save(image_path, format='WEBP')
                else:
                    image.save(image_path, format=sourced_image_format)

            except requests.exceptions.RequestException as error:
                print(f"Cannot Fetch: {link}: {error}")

            except Exception as error:
                print(f"Cannot Process: {link}: {error}")

        else:
            print("File already exists\n\n")