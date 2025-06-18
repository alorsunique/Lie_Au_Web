# This script should check if the Azure OpenAI API is still working

import os
from pathlib import Path

from openai import AzureOpenAI


# Main flow
if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    # Open the text file containing the API details
    api_detail_path = resources_dir / "API Key.txt"

    with open(api_detail_path, "r") as api_detail:
        api_detail_list = api_detail.read().splitlines()

    # Importing the API details
    API = api_detail_list[0]
    endpoint = api_detail_list[1]
    version = api_detail_list[2]
    deployment_name = api_detail_list[3]

    # Initializes the client
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=API,
        api_version=version,
    )

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

    # Read the month comeback
    file_name = "month_comeback.txt"

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

    user_prompt = "Those are the comebacks for the month"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )



    # Read the month comeback
    file_name = "next_day_comeback.txt"

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

    user_prompt = "Those are the comebacks for the next few days"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )



    user_prompt = "Provide a summary. Keep the summary a paragraph at most. Put the most urgent things first"

    # Appends the user prompt
    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # Requests for a response from the model
    response = client.chat.completions.create(
        model=deployment_name,
        messages=message_list,
    )

    # Get the actual message content from the response
    response_message = response.choices[0].message
    response_message_content = response_message.content

    print(f"\nResponse: {response_message.content}\n")

    daily_text = "daily_text.txt"

    # Open the file in write mode and write the string to it
    with open(daily_text, 'w', encoding='utf-8') as daily_text_file:
            daily_text_file.write(response_message_content)
