# This script should check if the Azure OpenAI API is still working

import os
from pathlib import Path

from openai import AzureOpenAI

from ollama import chat
from ollama import ChatResponse

import yaml
from datetime import datetime, timedelta
import time


import json


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












def reconstruct_comeback_list(file_name):
    # Initialize an empty list to hold the entries
    reconstructed_list = []

    # Open the file in read mode with UTF-8 encoding
    with open(file_name, 'r', encoding='utf-8') as file:
        # Read each line in the file
        for line in file:
            # Strip trailing whitespace/newline characters and append to the list
            reconstructed_list.append(line.strip())

    return reconstructed_list














def append_working_message_list(working_message_list, working_reconstructed_list):
    count = 0
    for entry in working_reconstructed_list:
        count += 1
        user_prompt = f"Comeback {count} | {entry}"

        # Appends the user prompt
        working_message_list.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )
    
    return working_message_list















def kpop_report(datetime_object, next_day_comeback_path, remain_month_comeback_path, input_model):
    message_list = []

    system_prompt = '''
        You are a KPop enthusiast. You can process information from comeback tables and create interesting reports from those.
        You will also help the user in their query.
    '''

    # Appends the system prompt
    message_list.append(
        {
            'role': 'system',
            'content': system_prompt,
        }
    )

    current_month = datetime_object.month
    current_year = datetime_object.year
    current_day = datetime_object.day

    user_prompt = f"Today is {current_year}/{current_month}/{current_day}. The format is YYYY/MM/DD"

    message_list.append(
        {
            "role": "system",
            "content": user_prompt,
        }
    )

    # Next three day

    next_three_day_message_list = message_list.copy()

    reconstructed_list = reconstruct_comeback_list(next_day_comeback_path)

    next_three_day_message_list = append_working_message_list(next_three_day_message_list, reconstructed_list)

    user_prompt = "Those are the comebacks for the next 3 days, today included"

    next_three_day_message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    user_prompt = '''
        Provide a summary. Keep the summary a paragraph at most. 
        Put the most urgent comeback first.
        Do not give it raw. Format it properly so that it is like a report.
        DO NOT INVENT NEW INFORMATION. Use what was given as they are factual.
        I just need the summary. DO NOT offer any other help.
        The summary should be speakable or in natural language.
        I should be able to get the complete idea just by listening to the message if it was spoken to me.
    '''

    next_three_day_message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")

    response: ChatResponse = chat(
        model=input_model,
        messages=next_three_day_message_list,
    )

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")

    next_three_day_response = response


    # Remaining of the month






    remain_month_message_list = message_list.copy()

    reconstructed_list = reconstruct_comeback_list(remain_month_comeback_path)

    remain_month_message_list = append_working_message_list(remain_month_message_list, reconstructed_list)

    user_prompt = "Those are the comebacks for the remaining days of the month, today included"

    remain_month_message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    user_prompt = '''
        Provide a summary. Keep the summary a paragraph at most. 
        Put the most urgent comeback first.
        Do not give it raw. Format it properly so that it is like a report.
        DO NOT INVENT NEW INFORMATION. Use what was given as they are factual.
        I just need the summary. DO NOT offer any other help.
        The summary should be speakable or in natural language.
        I should be able to get the complete idea just by listening to the message if it was spoken to me.
    '''

    remain_month_message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")

    response: ChatResponse = chat(
        model=input_model,
        messages=remain_month_message_list,
    )

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")

    remain_month_response = response

    return next_three_day_response, remain_month_response









































def main():
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    datetime_object = datetime.fromtimestamp(time.time())
    model_choice = 'gemma3:4b-it-qat'

    next_day_comeback_path = daily_report_dir / 'next_day_comeback.txt'
    remain_month_comeback_path = daily_report_dir / 'remain_month_comeback.txt'

    next_day_respone, remain_month_response = kpop_report(datetime_object, next_day_comeback_path, remain_month_comeback_path, model_choice)

    next_day_message = next_day_respone.message.content
    remain_month_message = remain_month_response.message.content

    print(next_day_message)
    print(remain_month_message)

    report_next_day_comeback_path = daily_report_dir / 'report_next_day_comeback.txt'
    report_remain_month_comeback_path = daily_report_dir / 'report_remain_month_comeback.txt'

    if report_next_day_comeback_path.exists():
        os.remove(report_next_day_comeback_path)

    with open(report_next_day_comeback_path, 'w', encoding='utf-8') as written_report:
        written_report.write(next_day_message)

    if report_remain_month_comeback_path.exists():
        os.remove(report_remain_month_comeback_path)

    with open(report_remain_month_comeback_path, 'w', encoding='utf-8') as written_report:
        written_report.write(remain_month_message)

    




# Main flow
if __name__ == "__main__":
     main()