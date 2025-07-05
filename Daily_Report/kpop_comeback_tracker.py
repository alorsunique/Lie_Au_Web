# For tracking K POP comebacks
# Data taken from kpopofficial.com

import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup


def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path


# Main function used to track
def track(url, day_of_the_week_list):
    request_result = requests.get(url)  # Request the url
    soup = BeautifulSoup(request_result.text, 'html.parser')

    try:
        inner_global_info_list = []
        day_content_soup = soup.findAll('figure', class_='wp-block-table is-style-stripes')

        for day_content in day_content_soup:
            body_content_soup = day_content.findAll('tbody')
            tr_content_soup = body_content_soup[0].findAll('tr')

            for tr_content in tr_content_soup:
                date = ""
                time = ""
                artist = ""

                td_element = tr_content.findAll('td', class_='has-text-align-right')

                for element in td_element:
                    content = element.get_text(separator=' ').strip()

                    for weekday in day_of_the_week_list:
                        if content.startswith(weekday):
                            content = content[len(weekday):].strip()

                    date_split = content.split("at")

                    try:
                        date = date_split[0].strip()
                    except IndexError:
                        pass

                    try:
                        time = date_split[1].strip()
                    except IndexError:
                        pass

                td_element = tr_content.findAll('td', class_='has-text-align-left')

                for element in td_element:
                    try:
                        artist = element.find('strong').get_text(separator=' ').strip()

                        for strong_tag in element.find_all('strong'):
                            strong_tag.decompose()  # Removes the <strong> tag and its contents

                        content_list = list(element.stripped_strings)
                    except:
                        pass

                if not date == "" and not artist == "":
                    try:
                        print(f"{date} | {time} | {artist} | {content_list}")
                        info_list = [date, time, artist, content_list]
                        inner_global_info_list.append(info_list)
                    except:
                        pass

        return inner_global_info_list

    except:
        pass



# Main
def main():
    # Get the current month and year
    current_datetime_object = datetime.fromtimestamp(time.time())

    current_month = current_datetime_object.month
    current_year = current_datetime_object.year

    month_map = {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december"
    }

    day_of_the_week_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    column_label_list = ["Day", "Time", "Artist", "Relevant Info Site"]

    # URL for current month
    formatted_url = f"https://kpopofficial.com/kpop-comeback-schedule-{month_map[current_month]}-{current_year}/"
    print(f"Formatted URL: {formatted_url}")

    page_info_list = track(formatted_url, day_of_the_week_list)
    df = pd.DataFrame(page_info_list, columns=column_label_list)

    # For next month
    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    formatted_url = f"https://kpopofficial.com/kpop-comeback-schedule-{month_map[next_month]}-{next_year}/"
    print(f"Formatted URL: {formatted_url}")

    page_info_list = track(formatted_url, day_of_the_week_list)
    next_df = pd.DataFrame(page_info_list, columns=column_label_list)

    # Will store the dataframe to an Excel file
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    # Writing for current month
    catalog_path = daily_report_dir / f"{current_year}_{str(current_month).zfill(2)}_KPop_Output.xlsx"
    print(catalog_path)

    if catalog_path.exists():
        os.remove(catalog_path)

    df.to_excel(catalog_path, sheet_name='Comeback', index=False)

    # Writing for next month
    catalog_path = daily_report_dir / f"{next_year}_{str(next_month).zfill(2)}_KPop_Output.xlsx"
    print(catalog_path)

    if catalog_path.exists():
        os.remove(catalog_path)

    next_df.to_excel(catalog_path, sheet_name='Comeback', index=False)






if __name__ == "__main__":
    main()