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






def main():
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"

    message_list = []

    system_prompt = '''
        You are a secretary. You will summarize important information for the day so that the user will be updated.
    '''


    # Appends the system prompt
    message_list.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )

    datetime_object = datetime.fromtimestamp(time.time())

    current_month = datetime_object.month
    current_year = datetime_object.year
    current_day = datetime_object.day

    user_prompt = f"Today is {current_year}/{current_month}/{current_day}. The format is YYYY/MM/DD"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )


    # Read the month comeback
    file_name = daily_report_dir / "next_day_comeback.txt"

    # Initialize an empty list to hold the entries
    reconstructed_list = []

    # Open the file in read mode with UTF-8 encoding
    with open(file_name, 'r', encoding='utf-8') as file:
        # Read each line in the file
        for line in file:
            # Strip trailing whitespace/newline characters and append to the list
            reconstructed_list.append(line.strip())

    # Print the reconstructed list
    print("Reconstructed list:", reconstructed_list)

    count = 0
    for entry in reconstructed_list:
        count += 1
        user_prompt = f"Comeback {count} | {entry}"

        # Appends the user prompt
        message_list.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

    user_prompt = "Those are the comebacks for the next 3 days, today included"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # Read the month comeback



    user_prompt = '''
    Provide a summary. Keep the summary a paragraph at most. 
    Put the most urgent things first. For the comeback, highlight only the next day comebacks. Do not give it raw. Format it properly so that it is like a report
    Do not invent new information regarding the comeback
    I just need the summary. Do not offer any other help.
    '''

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )




    # Requests for a response from the model
    # response = client.chat.completions.create(
        # model=deployment_name,
        # messages=message_list,
    # )

    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")

    response: ChatResponse = chat(
        model='gemma3:4b-it-qat',
        messages=message_list,
    )

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")

    # Get the actual message content from the response
    # response_message = response.choices[0].message
    # response_message_content = response_message.content

    response_message = response.message.content

    # print(f"\nResponse: {response_message.content}\n")
    print(f"\nResponse: {response_message}\n")



    daily_text = "daily_text.txt"
    daily_path = daily_report_dir / daily_text



    # Open the file in write mode and write the string to it
    with open(daily_path, 'w', encoding='utf-8') as daily_text_file:
            daily_text_file.write(response_message)


    message_list = []



    system_prompt = '''
            You are a weather reporter. You will summarize the weather for the next few hours
        '''

    # Appends the system prompt
    message_list.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )

    file_name = daily_report_dir / "Output_JSON.json"

    if file_name.exists():
        with open(file_name, "r") as embed_json:
            output_dict = json.load(embed_json)

    print(output_dict)

    user_prompt = f"This is the weather information for today {output_dict}"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    file_name = daily_report_dir / "quarter_Output_JSON.json"

    if file_name.exists():
        with open(file_name, "r") as embed_json:
            output_dict = json.load(embed_json)

    print(output_dict)

    user_prompt = f"This is the weather information for the next few hours {output_dict}. Please parse it accordingly"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    user_prompt = f"With those information provided, create a short but complete response for the weather of the day and in the next few hours. Keep it a paragaph at most"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    print(message_list)

    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")

    response: ChatResponse = chat(
        model='gemma3:4b-it-qat',
        messages=message_list,
    )


    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")

    # Get the actual message content from the response
    # response_message = response.choices[0].message
    # response_message_content = response_message.content

    response_message = response.message.content

    # print(f"\nResponse: {response_message.content}\n")
    print(f"\nResponse: {response_message}\n")



    daily_text = "daily_weather_text.txt"
    daily_path = daily_report_dir / daily_text


    # Open the file in write mode and write the string to it
    with open(daily_path, 'w', encoding='utf-8') as daily_text_file:
            daily_text_file.write(response_message)





    message_list = []

    system_prompt = '''
                You are a secretary. Please summarize the important stuff of the day
            '''

    # Appends the system prompt
    message_list.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )

    daily_text = "daily_text.txt"
    daily_path = daily_report_dir / daily_text

    # Open the file in write mode and write the string to it
    with open(daily_path, 'r', encoding='utf-8') as file:
        daily_text_content = file.read()

    user_prompt = f"{daily_text_content}"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    daily_text = "daily_weather_text.txt"
    daily_path = daily_report_dir / daily_text

    # Open the file in write mode and write the string to it
    with open(daily_path, 'r', encoding='utf-8') as file:
        daily_text_content = file.read()

    user_prompt = f"{daily_text_content}"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    user_prompt = f"Keep it a paragaph at most"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    print(message_list)

    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")

    response: ChatResponse = chat(
        model='gemma3:4b-it-qat',
        messages=message_list,
    )

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")

    # Get the actual message content from the response
    # response_message = response.choices[0].message
    # response_message_content = response_message.content

    response_message = response.message.content

    # print(f"\nResponse: {response_message.content}\n")
    print(f"\nResponse: {response_message}\n")

    daily_text = "complete_summary.txt"
    daily_path = daily_report_dir / daily_text

    # Open the file in write mode and write the string to it
    with open(daily_path, 'w', encoding='utf-8') as daily_text_file:
        daily_text_file.write(response_message)






# Main flow
if __name__ == "__main__":
     main()