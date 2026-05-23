import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup
import re


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Beibusosu_Resource_Path.txt", "r") as beibusosu_resources_text:
        beibusosu_resources_dir = Path(str(beibusosu_resources_text.readline()).replace('"', ''))


    for entry in beibusosu_resources_dir.iterdir():
        if entry.is_dir():
            # print(entry)

            for image_file in entry.iterdir():
                # print(image_file)


                match = re.match(r"^(.*_\d{8}_\d{6}_)(galleries.*)$", image_file.name)

                if match:
                    prefix = match.group(1)
                    suffix = match.group(2)

                    print(prefix)
                    print(suffix)

                    new_file_name = f'{prefix}media{suffix}'

                    print(new_file_name)

                    new_path = image_file.parent / new_file_name
                    print(new_path)

                    rename_bool = False

                    if rename_bool:
                        os.rename(image_file, new_path)