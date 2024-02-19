import os
from pathlib import Path

resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    pass

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())

if entry_list[0]:
    resources_dir = Path(str(entry_list[0]).replace('"', ''))
    print(f"Resources Directory: {resources_dir}")

    if not resources_dir.exists():
        os.mkdir(resources_dir)
else:
    print(f"No directory")
