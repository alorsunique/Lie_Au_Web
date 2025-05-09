# Reads the output file

import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from pathlib import  Path



def day_forward(date):
    today = date
    tomorrow = date + timedelta(days=1)
    the_day_after = date + timedelta(days=2)

    print(tomorrow.day)
    print(the_day_after.day)

    day_list = [today, tomorrow,the_day_after]

    return day_list



if __name__ == "__main__":


    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    catalog_file = project_dir / "kpop_output.xlsx"

    df = pd.read_excel(catalog_file)

    print(df)

    select_artist_list = ["i-dle"]

    print(df.loc[df['Artist'].isin(select_artist_list)])

    select_day_list = ['May 2, 2025', 'May 7, 2025', 'May 9, 2025', 'May 19, 2025']

    print(df.loc[df['Day'].isin(select_day_list)])

    print("\n\n\n")

    print(df.loc[(df['Day'].isin(select_day_list)) & (df['Artist'].isin(select_artist_list)) ])

    current_time = time.time()
    print(current_time)

    datetime_object = datetime.fromtimestamp(current_time)
    print(datetime_object)

    print(datetime_object.year)
    print(datetime_object.month)
    print(datetime_object.day)

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


    projected_day_list = day_forward(datetime_object)

    day_string_list = []

    for entry in projected_day_list:
        formatted_day = f"{reverse_month_map[entry.month]} {entry.day}, {entry.year}"

        print(formatted_day)

        day_string_list.append(formatted_day)

    filtered_df = df.loc[(df['Day'].isin(day_string_list)) ]

    print(filtered_df)