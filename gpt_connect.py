import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from openai import AzureOpenAI

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    api_key_text_path = resources_dir / "API Key.txt"



    with open(api_key_text_path, "r") as api_key_text:
        api_info_list = api_key_text.read().splitlines()




    API = api_info_list[0]
    endpoint = api_info_list[1]
    version = api_info_list[2]
    deployment_name = api_info_list[3]

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key = API,
        api_version = version,
    )

    system_prompt = """
    You are an expert across several scientific fields, with a specialty in Physics. You will review a solution made by an instructor to see if it makes sense.
    
    If the solution requires a figure, that should automatically be a no as you aim to minimize the use of figures.
    """

    message_list = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    user_prompt = str(input("Enter your prompt: "))

    message_list.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    response = client.chat.completions.create(
        model = deployment_name,
        messages=message_list,
    )

    response_message = response.choices[0].message

    print(response_message.content)