import os
from pathlib import Path

from openai import AzureOpenAI

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
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

    system_prompt = """
    You are an expert and helpful assistant. Please help the user as best as you can
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
        model=deployment_name,
        messages=message_list,
    )

    response_message = response.choices[0].message

    print(f"Response: {response_message.content}")
