# Reads the output file

import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yaml


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


def month_comeback(df, current_datetime_object, artist_list, reverse_month_map):
    # Get current month
    current_month = current_datetime_object.month
    string_month = reverse_month_map[current_month]

    # Masks for artist and month
    mask_artist = df['Artist'].str.lower().isin(artist_list)
    mask_month = df['Day'].str.contains(string_month)

    # Filtered DF
    month_comeback_df = df.loc[mask_artist & mask_month]

    return month_comeback_df


def remain_month_comeback(df, current_datetime_object, artist_list, reverse_month_map):
    # Compute for the datetime of the next month
    if current_datetime_object.month == 12:
        next_month = datetime(current_datetime_object.year + 1, 1, 1)
    else:
        next_month = datetime(current_datetime_object.year, current_datetime_object.month + 1, 1)

    # Subtract a day from datetime of next month
    last_day = next_month - timedelta(days=1)

    # Determines the remaining days of the month
    remaining_day_list = []

    count = 0
    while count <= (last_day - current_datetime_object).days + 1:
        remaining_day_list.append(current_datetime_object + timedelta(days=count))
        count += 1

    # Formats the remaining days to match the string format
    remaining_formatted_day_list = []

    for remaining_day in remaining_day_list:
        formatted_day = f"{reverse_month_map[remaining_day.month]} {remaining_day.day}, {remaining_day.year}"
        remaining_formatted_day_list.append(formatted_day)

    # Masks for artists and remaining days
    mask_artist = df['Artist'].str.lower().isin(valid_artist_list)
    mask_month = df['Day'].isin(remaining_formatted_day_list)

    # Filtered DF
    remain_month_comeback_df = df.loc[mask_artist & mask_month]

    return remain_month_comeback_df


def next_day_comeback(df, current_datetime_object, artist_list, reverse_month_map, next_day_add):
    # Store from now up to the specified max
    day_list = []

    count = 0
    while count <= next_day_add:
        day_list.append(current_datetime_object + timedelta(count))
        count += 1

    remaining_formatted_day_list = []
    for remaining_day in day_list:
        formatted_day = f"{reverse_month_map[remaining_day.month]} {remaining_day.day}, {remaining_day.year}"
        remaining_formatted_day_list.append(formatted_day)

    # Masks for artists and remaining days
    mask_artist = df['Artist'].str.lower().isin(artist_list)
    mask_month = df['Day'].isin(remaining_formatted_day_list)

    # Filtered DF
    next_day_comeback_df = df.loc[mask_artist & mask_month]

    return next_day_comeback_df


# Formats the dataframe to a string
def format_output_string(period_df):
    string_list = []

    for index, row in period_df.iterrows():
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

    return string_list


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
    current_datetime_object = datetime.fromtimestamp(time.time())

    current_month = current_datetime_object.month
    current_year = current_datetime_object.year

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

    month_comeback_df = month_comeback(whole_df, current_datetime_object, valid_artist_list, reverse_month_map)

    remain_month_comeback_df = remain_month_comeback(whole_df, current_datetime_object, valid_artist_list,
                                                     reverse_month_map)

    next_day_add = 3
    next_day_comeback_df = next_day_comeback(whole_df, current_datetime_object, valid_artist_list, reverse_month_map,
                                             next_day_add)

    # For the month
    string_list = format_output_string(month_comeback_df)

    string_text = "month_comeback.txt"
    string_path = daily_report_dir / string_text

    with open(string_path, 'w', encoding='utf-8') as comeback_text:
        for entry in string_list:
            comeback_text.write(entry + '\n')

    # For the remaining of the month
    string_list = format_output_string(remain_month_comeback_df)

    string_text = "remain_month_comeback.txt"
    string_path = daily_report_dir / string_text

    with open(string_path, 'w', encoding='utf-8') as comeback_text:
        for entry in string_list:
            comeback_text.write(entry + '\n')

    # For the next few days
    string_list = format_output_string(next_day_comeback_df)

    string_text = "next_day_comeback.txt"
    string_path = daily_report_dir / string_text

    with open(string_path, 'w', encoding='utf-8') as comeback_text:
        for entry in string_list:
            comeback_text.write(entry + '\n')
