import os
from pathlib import Path

from openai import AzureOpenAI
import time


def random_fact(LLM_client):
    system_prompt = """
        You are an expert and helpful assistant. Please help the user as best as you can
        """

    message_list = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    user_prompt = "Give me a random fun fact. Limit it to a single paragraph"

    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=message_list,
    )

    response_message = response.choices[0].message.content

    return response_message


def get_next_run_time():
    """Calculate the next time to run the main function at the nearest 10-minute mark, including seconds."""
    current_time = time.time()
    print(current_time)
    print(type(current_time))
    # Get the current minutes and seconds
    minutes = int(time.strftime("%M", time.localtime(current_time)))
    seconds = int(time.strftime("%S", time.localtime(current_time)))

    print(time.localtime(current_time))

    # Calculate how many minutes to add to reach the next 10-minute mark

    print(minutes)
    print(f"Mod mins {minutes//10}")

    next_minutes = ((minutes // 10) + 1) * 10

    print(next_minutes)

    if next_minutes == 60:  # Special case for the top of the hour
        next_run_time = current_time + ((60 - minutes) * 60 - seconds)
    else:
        next_run_time = current_time + ((next_minutes - minutes) * 60 - seconds)

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_run_time)))

    return next_run_time




if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    api_detail_path = resources_dir / "API Key.txt"

    with open(api_detail_path, "r") as api_detail:
        api_detail_list = api_detail.read().splitlines()

    API = api_detail_list[0]
    endpoint = api_detail_list[1]
    version = api_detail_list[2]
    deployment_name = api_detail_list[3]

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=API,
        api_version=version,
    )


    while True:

        print(f"Random Fact: {random_fact(client)}")

        time.sleep(60)