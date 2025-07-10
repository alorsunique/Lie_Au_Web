# This script should orchestrate the calling of the daily components
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

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


if __name__ == "__main__":
    # Five minute sleep to let the computer connect to internet
    time.sleep(300)


    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    daily_run_check_json_path = daily_report_dir / "run_perform_check.json"

    # Get current datetime
    datetime_object = datetime.fromtimestamp(time.time())

    current_year = datetime_object.year
    current_month = datetime_object.month
    current_day = datetime_object.day
    current_hour = datetime_object.hour

    # Declare hours when function should run
    run_time_list = [0, 6, 12,13, 18]

    # Format the hours to be datetime objects
    formatted_run_time_list = []

    for entry in run_time_list:
        run_time_object = datetime(current_year, current_month, current_day, entry)
        formatted_run_time_list.append(run_time_object)

    # Importing the things to be run
    from Daily_Report import kpop_comeback_tracker
    from Daily_Report import kpop_comeback_reader
    from Daily_Report import weather_test
    from Daily_Report import daily_report


    def scheduled_set_function_call():
        kpop_comeback_tracker.main()
        kpop_comeback_reader.main()
        weather_test.main()
        daily_report.main()


    # Determine the index of the hour floored
    index = 0

    for entry in formatted_run_time_list:
        if datetime_object >= entry:
            index += 1

    print(f'Previous scheduled run time: {formatted_run_time_list[index - 1]}')

    # Check if the run_perform_check file exists
    # If not, this will create the file
    # It will also call the function
    if not daily_run_check_json_path.exists():
        print(f'No previous recorded detected.\nCreating record for {formatted_run_time_list[index - 1]}')

        run_status_dict = {
            'year': current_year,
            'month': current_month,
            'day': current_day,
            'time': run_time_list[index - 1]
        }
        with open(daily_run_check_json_path, 'w', encoding='utf-8') as run_check_json:
            json.dump(run_status_dict, run_check_json)

        scheduled_set_function_call()

    # If run_perform_check file exists, check the data stored in the file
    else:
        with open(daily_run_check_json_path, 'r', encoding='utf-8') as run_check_json:
            run_status_dict = json.load(run_check_json)

        loaded_year = run_status_dict['year']
        loaded_month = run_status_dict['month']
        loaded_day = run_status_dict['day']
        loaded_hour = run_status_dict['time']

        # If date of last run is different to current day, will update the file
        # Also call the function
        if loaded_year != current_year or loaded_month != current_month or loaded_day != current_day:
            print(f'Day mismatch detected.\nCreating record for {formatted_run_time_list[index - 1]}')

            os.remove(daily_run_check_json_path)

            run_status_dict = {
                'year': current_year,
                'month': current_month,
                'day': current_day,
                'time': run_time_list[index - 1]
            }
            with open(daily_run_check_json_path, 'w', encoding='utf-8') as run_check_json:
                json.dump(run_status_dict, run_check_json)

            scheduled_set_function_call()

        # If the day is correct, checks if the last previous valid time has been run
        else:
            # Here, the current hour should be floored
            # Rounding down is done in the index part
            if run_time_list[index - 1] > loaded_hour:
                print(f'Hour mismatch detected.\nCreating record for {formatted_run_time_list[index - 1]}')
                os.remove(daily_run_check_json_path)

                run_status_dict = {
                    'year': current_year,
                    'month': current_month,
                    'day': current_day,
                    'time': run_time_list[index - 1]
                }
                with open(daily_run_check_json_path, 'w', encoding='utf-8') as run_check_json:
                    json.dump(run_status_dict, run_check_json)

                scheduled_set_function_call()

            else:
                print(f"Run performed for {run_time_list[index - 1]}")

    # This is the part where it can loop since the checks have been made
    # In the loop, index is not subtracted by 1 since it is looking forward
    # Compared to before where the previous time should be recorded
    while True:
        if index == len(formatted_run_time_list):
            print("All runs for the day done. Creating list for next day runs")

            next_day_formatted_run_time_list = []

            # Adding a day to the entries
            for entry in formatted_run_time_list:
                next_day_entry = entry + timedelta(days=1)
                next_day_formatted_run_time_list.append(next_day_entry)

            formatted_run_time_list = next_day_formatted_run_time_list.copy()

            print(formatted_run_time_list)

            index = 0

        print(f'Index: {index}')
        datetime_object = datetime.fromtimestamp(time.time())
        print(f'Current time: {datetime_object}')
        print(f'Next target time: {formatted_run_time_list[index]}')

        to_sleep_time_object = formatted_run_time_list[index] - datetime_object
        to_sleep_time = to_sleep_time_object.total_seconds()
        print(f'Will sleep for {to_sleep_time} seconds.\nWake up time: {formatted_run_time_list[index]}')

        time.sleep(to_sleep_time)
        os.remove(daily_run_check_json_path)

        run_status_dict = {
            'year': current_year,
            'month': current_month,
            'day': current_day,
            'time': run_time_list[index]
        }
        with open(daily_run_check_json_path, 'w', encoding='utf-8') as run_check_json:
            json.dump(run_status_dict, run_check_json)

        # Run the function again
        scheduled_set_function_call()

        index += 1
