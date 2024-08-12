import os
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    slader_questions_dir = resources_dir / "Slader"
    if slader_questions_dir.exists():
        shutil.rmtree(slader_questions_dir)
    os.mkdir(slader_questions_dir)

    local_HTML_path = Path(str(input("Local Path: ")).replace('"', ''))

    with open(local_HTML_path, 'r', errors="ignore") as local_HTML:
        content = local_HTML.read()  # Reads the local HTML file
        soup = BeautifulSoup(content, "lxml")  # Creates soup object

    exercise_soup = soup.find_all('tr', class_='exercise')

    count = 0

    question_string_list = []
    question_string = ""

    for exercise_row in exercise_soup:
        td_soup = exercise_row.find_all('td')
        if str(td_soup[1].text).strip() == "None":

            count += 1

            question_number = exercise_row.find('a').text

            question_content = exercise_row.find('textarea', class_='editable-attribute bound').text
            question_string += f"Question {question_number}\n{question_content}\n\n\n"

            if count == 5:
                question_string_list.append(question_string)
                question_string = ""
                count = 0

    if not question_string == "":
        question_string_list.append(question_string)

    save_count = 0
    for entry in question_string_list:
        save_count += 1
        output_path = slader_questions_dir / f"Question Set {save_count}.txt"
        with open(output_path, "w") as writer:
            writer.write(entry)
