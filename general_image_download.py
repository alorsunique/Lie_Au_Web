import os
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    download_text_path = resources_dir / "Image Download Set.txt"

    with open(download_text_path, "r") as download_text:
        download_links_list = [line.strip() for line in download_text.readlines()]

    general_download_dir = resources_dir / "General Download"
    if not general_download_dir.exists():
        os.mkdir(general_download_dir)

    for link in download_links_list:
        print(link)
        parsed_url = urlparse(link).path.replace("/", '')
        output_name = f"{parsed_url}"

        image_path = general_download_dir / output_name

        try:
            time.sleep(2)
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
