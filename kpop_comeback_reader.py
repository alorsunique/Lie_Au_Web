# Reads the output file

import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def day_forward(date):
    today = date
    tomorrow = date + timedelta(days=1)
    day_after_tomorrow = date + timedelta(days=2)

    day_list = [today, tomorrow, day_after_tomorrow]

    return day_list


if __name__ == "__main__":

    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    # Read the text file containing the valid artist
    artist_list_path = resources_dir / "Artists_List.txt"

    with open(artist_list_path, "r") as artist_text:
        content = artist_text.read()

    content_split = content.split('\n')

    valid_artist_list = []
    for entry in content_split:
        formatted_entry = entry.lower().strip()

        if formatted_entry:
            valid_artist_list.append(formatted_entry)

    # Get the current month and year
    datetime_object = datetime.fromtimestamp(time.time())

    current_month = datetime_object.month
    current_year = datetime_object.year

    catalog_path = resources_dir / f"{current_year}_{str(current_month).zfill(2)}_KPop_Output.xlsx"

    df = pd.read_excel(catalog_path)

    current_time = time.time()
    datetime_object = datetime.fromtimestamp(current_time)

    projected_day_list = day_forward(datetime_object)

    reverse_month_map = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    day_string_list = []
    for entry in projected_day_list:
        formatted_day = f"{reverse_month_map[entry.month]} {entry.day}, {entry.year}"
        day_string_list.append(formatted_day)

    month_comeback_df = df.loc[(df['Artist'].str.lower().isin(valid_artist_list))]

    print(month_comeback_df)

    near_day_comeback_df = df.loc[
        (df['Day'].isin(day_string_list))
        & (df['Artist'].str.lower().isin(valid_artist_list))
        ]

    print(near_day_comeback_df)

    string_list = []

    for index, row in month_comeback_df.iterrows():
        comeback_day = row['Day']

        if pd.isna(row['Time']):
            comeback_time = "Not Specified"
        else:
            comeback_time = row['Time']

        comeback_artist = row['Artist']
        comeback_information = row['Relevant Info Site']

        formatted_string = f"Day: {comeback_day} | Time: {comeback_time} | Artist: {comeback_artist} | Relevant Information: {comeback_information}"

        string_list.append(formatted_string)

    if len(string_list) == 0:
        string_list.append("No relevant comeback for the month")

    print("Comeback for the month")
    print(string_list)

    string_text = "month_comeback.txt"

    # Open the file in write mode and write the string to it
    with open(string_text, 'w', encoding='utf-8') as month_text:
        for entry in string_list:
            month_text.write(entry + '\n')

    string_list = []

    for index, row in near_day_comeback_df.iterrows():
        comeback_day = row['Day']

        if pd.isna(row['Time']):
            comeback_time = "Not Specified"
        else:
            comeback_time = row['Time']

        comeback_artist = row['Artist']
        comeback_information = row['Relevant Info Site']

        formatted_string = f"Day: {comeback_day} | Time: {comeback_time} | Artist: {comeback_artist} | Relevant Information: {comeback_information}"

        string_list.append(formatted_string)

    if len(string_list) == 0:
        string_list.append("No relevant comeback in the next few days")

    print("Comeback for the next few days")
    print(string_list)

    string_text = "next_day_comeback.txt"

    # Open the file in write mode and write the string to it
    with open(string_text, 'w', encoding='utf-8') as next_day_text:
        for entry in string_list:
            next_day_text.write(entry + '\n')
