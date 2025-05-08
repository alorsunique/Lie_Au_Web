# This script utilizes GPT models in deciding which of the three generated solutions is the best answer to the question

import os
from pathlib import Path

import pandas as pd
from openai import AzureOpenAI

if __name__ == "__main__":

    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    output_path = resources_dir / "QuestionAnswer.xlsx"

    api_detail_path = resources_dir / "API Key.txt"

    with open(api_detail_path, "r") as api_detail:
        api_detail_list = api_detail.read().splitlines()

    API = api_detail_list[0]
    endpoint = api_detail_list[1]
    version = api_detail_list[2]
    deployment_name = api_detail_list[3]

    df = pd.read_excel(output_path)

    print(df)

    data_as_lists = []

    # Iterate through each row of the DataFrame
    for _, row in df.iterrows():
        # Convert the row to a list (excluding NaN values)
        row_list = row.dropna().tolist()
        data_as_lists.append(row_list)

    # Print the resulting list of lists

    system_prompt = """
            You are an expert across several scientific fields, with a specialty in Physics. You will review solutions made three different instructors.

            The question will be provided to you first. The solutions are written in LaTeX. The solutions have steps and a result cell at the end but for simplicity, it is sent to you as a string version of a list.
            
            You will check if the solutions makes sense. Also you need to make sure that the computations are done properly.
            
            After going through all three, you will decide the best solution.
            
            The best solution is a solution that does not require additional editing or correction.
            If the solution requires a figure, that should automatically be of lower priority in the selection as you aim to minimize the use of figures.
            Your final response should just be the solution number, such as 'first', 'second', or 'third'. For clarity, also display the actual solution that was provided.
            
            If the best solution still require correction, return the corrected solution in the same format as it was provided.
            """

    for question_answer_set in data_as_lists:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=API,
            api_version=version,
        )

        message_list = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        question = question_answer_set[0]

        answer_first = question_answer_set[1]
        answer_second = question_answer_set[2]
        answer_third = question_answer_set[3]

        message_list.append(
            {
                "role": "user",
                "content": f"The question is the following. {question}.",
            }
        )

        message_list.append(
            {
                "role": "user",
                "content": f"The first solution is the following. {answer_first}.",
            }
        )
        message_list.append(
            {
                "role": "user",
                "content": f"The second solution is the following. {answer_second}.",
            }
        )
        message_list.append(
            {
                "role": "user",
                "content": f"The third solution is the following. {answer_third}.",
            }
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=message_list,
        )

        response_message = response.choices[0].message

        print(f"Question: {question}")

        print(response_message.content)

        print("\n\n\n\n\n----------------------------------------------------------------")
