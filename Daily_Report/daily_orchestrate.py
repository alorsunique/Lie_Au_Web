# This script should orchestrate the calling of the daily components
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta
import time
import yaml
import os



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
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    daily_run_status_json_path = daily_report_dir / "Run_Status.json"

    # Get current datetime
    datetime_object = datetime.fromtimestamp(time.time())

    current_year = datetime_object.year
    current_month = datetime_object.month
    current_day = datetime_object.day
    current_hour = datetime_object.hour

    # Declare hours where function should run
    run_time_list = [0,6,12,18]
    # Format the hours
    formatted_run_time_list = []

    for entry in run_time_list:
        run_time_object = datetime(current_year,current_month,current_day,entry)
        formatted_run_time_list.append(run_time_object)




    from Daily_Report import kpop_comeback_tracker
    from Daily_Report import kpop_comeback_reader
    from Daily_Report import weather_test
    from Daily_Report import daily_report





    def report_call():
        kpop_comeback_tracker.main()
        kpop_comeback_reader.main()
        weather_test.main()
        daily_report.main()



    count = 0
    index = 0
    while count < len(formatted_run_time_list):
        if datetime_object > formatted_run_time_list[count]:
            index += 1

        count +=1

    index -= 1




    # Check if the run status file exists
    # If not, this will create the file
    # It will also do report_call
    if not daily_run_status_json_path.exists():

        
        print(formatted_run_time_list[index])

        run_status_dict = {
            'year': current_year,
            'month': current_month,
            'day': current_day,
            'time': run_time_list[index]
        }
        with open(daily_run_status_json_path, 'w', encoding='utf-8') as output_json:
            json.dump(run_status_dict, output_json)

        report_call()

    # If run status file exists, check the data stored in the file
    else:
        with open(daily_run_status_json_path, 'r', encoding='utf-8') as output_json:
            run_status_dict = json.load(output_json)

        loaded_year = run_status_dict['year']
        loaded_month = run_status_dict['month']
        loaded_day = run_status_dict['day']
        loaded_hour = run_status_dict['time']

        print(run_status_dict['year'])
        print(run_status_dict['month'])
        print(run_status_dict['day'])

        # If the last run time, as stored in the file, is different to today, update the file
        # Also do the report_call
        if loaded_year != current_year or loaded_month != current_month or loaded_day != current_day:
            print('day mismatch')

            os.remove(daily_run_status_json_path)

            run_status_dict = {
                'year': current_year,
                'month': current_month,
                'day': current_day,
                'time': run_time_list[index]
            }
            with open(daily_run_status_json_path, 'w', encoding='utf-8') as output_json:
                json.dump(run_status_dict, output_json)

            report_call()

        # If the day is correct, this part should check if the last previous valid time has been run
        else:
            # Here, the current hour should be rounded down
            # Rounding down is done in the index part

            if run_time_list[index] > loaded_hour:

                os.remove(daily_run_status_json_path)

                run_status_dict = {
                    'year': current_year,
                    'month': current_month,
                    'day': current_day,
                    'time': run_time_list[index]
                }
                with open(daily_run_status_json_path, 'w', encoding='utf-8') as output_json:
                    json.dump(run_status_dict, output_json)

                report_call()

            else:
                print(f"Run has been made for hour {run_time_list[index]}")


    # This is the part where it can loop since the checks have been made

    # while True:

    print(index)
    print(formatted_run_time_list[index])
    print(datetime_object)

    if index+1 == len(formatted_run_time_list):
        print("Max hour for the day done. Next day list should be created")

        for entry in formatted_run_time_list:
            print(entry)
            print(entry+timedelta(days=1))
    else:


        datetime_object = datetime.fromtimestamp(time.time())
        
























