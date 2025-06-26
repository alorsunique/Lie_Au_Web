# Reads the output file

import time
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd



import yaml

# Get the date for today, tomorrow, and the day after tomorrow
def day_forward(date):
    today = date
    tomorrow = date + timedelta(days=1)
    day_after_tomorrow = date + timedelta(days=2)

    day_list = [today, tomorrow, day_after_tomorrow]

    return day_list



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





def month_comeback(df, current_month, artist_list, reverse_month_map):

    print(current_month)
    print(artist_list)
    print(reverse_month_map)

    string_month = reverse_month_map[current_month]
    print(string_month)

    print(df['Day'])

    mask_artist = df['Artist'].str.lower().isin(valid_artist_list)
    print(mask_artist)
    mask_month = df['Day'].str.contains(string_month)
    print(mask_month)

    month_comeback_df = df.loc[mask_artist & mask_month]

    print(month_comeback_df)



def remain_month_comeback(df, datetime_object, artist_list, reverse_month_map):
    # Compute for the datetime of the next month
    if datetime_object.month == 12:
        next_month = datetime(datetime_object.year + 1, 1, 1)
    else:
        next_month = datetime(datetime_object.year, datetime_object.month + 1, 1)

    # Subtract a day from datetime of next month
    last_day = next_month - timedelta(days=1)

    remaining_day_list = []

    count = 0
    while count <= (last_day-datetime_object).days + 1:
        print(datetime_object + timedelta(days=count))
        remaining_day_list.append(datetime_object + timedelta(days=count))
        count += 1

    # Generate list of remaining days including today
    #remaining_days = [datetime_object + timedelta(days=i)
                      #for i in range((last_day_of_month - datetime_object).days + 1)]

    # Optional: just the date part
    #remaining_dates = [d.date() for d in remaining_days]

    #print(remaining_dates)







# Main
if __name__ == "__main__":
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    # Read the text file containing the valid artist
    artist_list_path = daily_report_dir / "Artists_List.txt"

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

    # For next month
    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    catalog_path = daily_report_dir / f"{current_year}_{str(current_month).zfill(2)}_KPop_Output.xlsx"

    df = pd.read_excel(catalog_path)

    catalog_path = daily_report_dir / f"{next_year}_{str(next_month).zfill(2)}_KPop_Output.xlsx"

    next_df = pd.read_excel(catalog_path)

    whole_df = pd.concat([df, next_df], ignore_index=True)

    # Get tbe next three days
    projected_day_list = day_forward(datetime_object)

    print(projected_day_list)




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

    month_comeback(whole_df, current_month, valid_artist_list, reverse_month_map)

    remain_month_comeback(whole_df, datetime_object, valid_artist_list, reverse_month_map)

    time.sleep(1000)

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
    string_path = daily_report_dir / string_text

    # Open the file in write mode and write the string to it
    with open(string_path, 'w', encoding='utf-8') as month_text:
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
    string_path = daily_report_dir / string_text

    # Open the file in write mode and write the string to it
    with open(string_path, 'w', encoding='utf-8') as next_day_text:
        for entry in string_list:
            next_day_text.write(entry + '\n')
