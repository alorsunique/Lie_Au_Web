import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup




# request_result = requests.get(
    # url,
    # allow_redirects=True,
    # headers={
        # "User-Agent": "MyResearchBot/1.0"
    # }
# )  # Request the url

# soup = BeautifulSoup(request_result.text, 'html.parser')

# print(soup)

import wikipediaapi
from wikipediaapi._enums import RedirectFilter
import asyncio

# wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

wiki_wiki = wikipediaapi.Wikipedia('JisooIlhada (jisooilhada@gmail.com)', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)










page_list = wiki_wiki.random(filter_redirect=RedirectFilter.NONREDIRECTS, limit=32)

extracted_page_list = []

for count, page in enumerate(page_list):

    extracted_dict = {}

    inner_page = wiki_wiki.page(page)

    # print(f"Page Title: {inner_page.title}")

    # print("Page - Exists: %s" % inner_page.exists())

    title = inner_page.title

    extracted_dict['Article Title'] = title

    summary = inner_page.summary

    extracted_dict['Article Summary'] = summary

    # print(inner_page_summary)

    sections = inner_page.sections

    for section_count, section_entry in enumerate(sections):

        section_title = section_entry.title

        # extracted_dict[f'Section {section_count + 1} Title'] = section_title

        section_text = section_entry.text

        # extracted_dict[f'Section {section_count + 1} Text'] = section_text


    print(f'{count + 1}: {extracted_dict}')

    extracted_page_list.append(extracted_dict)

    # time.sleep(0.25)

    # print(inner_page_sections)

    # results = asyncio.gather(article_pull(page))






    # inner_page = wiki_wiki.page(f'{page.title()}')

    # time.sleep(5)

    # print(f"Article {count}: {inner_page.title}")
    # print(f"{inner_page.text}")

    # time.sleep(5)



from ollama import chat
from ollama import ChatResponse

message_list = []

system_prompt = '''
    You are a helpful assistant.
'''

# Appends the system prompt
message_list.append(
    {
        'role': 'system',
        'content': system_prompt,
    }
)

user_prompt = """
    I will provide articles.
    I will be these in a string version of a Python dictionary.
"""

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)

for extracted_count, extracted_article in enumerate(extracted_page_list):
    message_list.append(
        {
            "role": "user",
            "content": f"Article Count {extracted_count + 1}. {str(extracted_article)}",
        }
    )


user_prompt = """
    I want you to report them to me in a digestible manner so that I get insight on new things every day.
    Think of it as you are writing an article with a lot of random topics.
    Do not skip out on important parts.
    Assume that I have no access to this article so DO NOT say things like "the article says" or "the article covers". 
    Instead, say it to me like I am listening to you talk.
    Do not format it with Markdown or LaTeX. It should just be plaintext.
    Do not make it longer than what is needed.
    Do not add "chapter" marks. Just ensure that the flow is natural. AGAIN DO NOT ADD CHAPTER TITLES OR HEADINGS.
    You can use information from the supplemental articles IF NECESSARY. IF NOT, DO NOT USE THEM.
    Make it an engaging.
    Make it coherent. You are free to change the structure of the sections for best output. 
    You are free to rearrange the order of the articles to maintain cohesiveness and engagement.
    Ensure that the flow as I read the output is coherent.
    No need to do a greeting at the start.
    Figure out a great hook if necessary.
    Ensure that it is written in a manner that keeps the reader engaged throughout the article that you wrote.
    Figure out all the necessary transitions.
    Do not dumb it down as the reader can comprehend what is written.
    No paragraph limit but do not make it longer than what is needed. At most, it should be 8 A4 pages long with 12 font and single spacing.
"""

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)


print(f'\n\n#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*\n\n')

for message in message_list:
    print(message['content'])

print(f'\n\n#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*#$&*\n\n')








now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Message Generation Start Time: {current_time}")

response: ChatResponse = chat(
    model='gemma4:e4b',
    # model = 'gemma3:12b-it-qat ',
    messages=message_list,
    options={
        'num_ctx': 98304  # Set to your desired token limit
    }
)

now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Message Generation End Time: {current_time}")
print(f"Total Run Time: {finish_time - start_time}")

# next_three_day_response = response

# print(response)

message_content = response.message.content

print(message_content)



