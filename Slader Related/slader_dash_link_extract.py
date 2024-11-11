import os
from pathlib import Path

from bs4 import BeautifulSoup

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    slader_dashboard_point = resources_dir / "Slader_Pointer.txt"
    with open(slader_dashboard_point, "r") as slader_pointer_text:
        local_HTML_path = Path(str(slader_pointer_text.readline()).replace('"', ''))

    with open(local_HTML_path, 'r', errors="ignore") as local_HTML:
        content = local_HTML.read()  # Reads the local HTML file
        soup = BeautifulSoup(content, "lxml")  # Creates soup object

    exercise_soup = soup.find_all('tr', class_='exercise')

    valid_links = []

    for exercise_row in exercise_soup:
        td_soup = exercise_row.find_all('td')

        if str(td_soup[1].text).strip() == "None":

            link_tag = td_soup[0].find('a')
            link = link_tag['href'] if link_tag else None

            if not link == None:
                valid_links.append(link)

    print(valid_links)
    print(len(valid_links))

    link_text_path = resources_dir / "Dashboard Links.txt"

    if link_text_path.exists():
        os.remove(link_text_path)

    max_count = 25
    trimmed_valid_links = valid_links[:max_count]

    with open(link_text_path, 'w') as text_file:
        for link in trimmed_valid_links:
            text_file.write(f"{link}\n")
