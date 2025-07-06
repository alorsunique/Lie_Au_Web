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

