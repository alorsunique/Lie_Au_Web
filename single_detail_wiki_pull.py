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










page_list = wiki_wiki.random(filter_redirect=RedirectFilter.NONREDIRECTS, limit=1)

extracted_page_list = []

supplemental_page_list = []

for count, page in enumerate(page_list):

    extracted_dict = {}

    inner_page = wiki_wiki.page(page)

    # inner_page = wiki_wiki.page('Ropica unifuscomaculata')

    # inner_page = wiki_wiki.page('Talamarang')


    # inner_page = wiki_wiki.page('James Clerk Maxwell')



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

        extracted_dict[f'Section {section_count+1} Title'] = section_title

        section_text = section_entry.text

        extracted_dict[f'Section {section_count+1} Text'] = section_text


    print(f'{count + 1}: {extracted_dict}')

    extracted_page_list.append(extracted_dict)

    time.sleep(0.25)

    links = inner_page.links

    # for title in sorted(links.keys()):

        # print(title)
        # print(type(title))

        # print("%s: %s" % (title, links[title]))

        # if title.startswith('Template talk:') or title.startswith('Template:') or title.startswith('Wikipedia:'):
            # print('Excluded')


    for keys in extracted_dict.keys():

        print(f'{keys}')
        print(f'{extracted_dict[keys]}')

    print(f'----------------------------------------------------------------')

    for link_count, link in enumerate(links):

        supplemental_dict = {}

        print(f'Link Count {link_count+1}: {link}')
        # print(type(link))

        link_title = link.title()

        print(f'Link Title: {link_title}')

        if (
            link_title.lower().startswith('template talk:' )
            or link_title.lower().startswith('template:')
            or link_title.lower().startswith('wikipedia:')
            or link_title.lower().startswith('help:')
        ):
            print('Excluded')
        else:

            in_text_bool = False

            for keys in extracted_dict.keys():

                print('################################################################')

                print(f'Current Key: {keys}')

                print('%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#')

                if link_title.lower() in extracted_dict[keys].lower():

                    print(link_title.lower())

                    print(extracted_dict[keys].lower())

                    in_text_bool = True

                print('################################################################\n\n\n\n')

            if in_text_bool:

                reference_page = wiki_wiki.page(link)
                print("Page - Exists: %s" % reference_page.exists())

                if reference_page.exists():
                    supplemental_dict['Supplement Title'] = reference_page.title
                    supplemental_dict['Supplement Summary'] = reference_page.summary


                    supplemental_page_list.append(supplemental_dict)




for entry in supplemental_page_list:
    print(str(entry))





# time.sleep(1000)

from ollama import chat
from ollama import ChatResponse

message_list = []

system_prompt = '''
    You are a helpful assistant. You will assist the user in their request.
'''

# Appends the system prompt
message_list.append(
    {
        'role': 'system',
        'content': system_prompt,
    }
)


user_prompt = """
    I will provide supplemental articles.
    Take note that these are only SUPPLEMENTAL. THEY ARE NOT THE MAIN ARTICLE.
    I will be sending the supplemental articles in a string version of a Python dictionary.
"""

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)

for supplemental_article_count, supplemental_article in enumerate(supplemental_page_list):
    message_list.append(
        {
            "role": "user",
            "content": f"Supplemental Article {supplemental_article_count+1}. {str(supplemental_article)}\n",
        }
    )






user_prompt = """
    I will be giving you a Wikipedia article. THIS will be the MAIN ARTICLE.
    I will be sending the MAIN ARTICLE in a string version of a Python dictionary.
"""

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)

for extracted_article in extracted_page_list:
    message_list.append(
        {
            "role": "user",
            "content": f"MAIN ARTICLE: {str(extracted_article)}",
        }
    )





user_prompt = """
    I want you to report the main article to me in a digestible manner.
    Do not skip out on important parts.
    Assume that I have no access to this article so DO NOT say things like "the article says" or "the article covers". 
    Instead, say it to me like I am listening to you talk.
    Do not format it with Markdown or LaTeX. It should just be plaintext.
    Do not make it longer than what is needed.
    Do not add "chapter" marks. Just ensure that the flow is natural. AGAIN DO NOT ADD CHAPTER TITLES OR HEADINGS.
    You can use information from the supplemental articles IF NECESSARY. IF NOT, DO NOT USE THEM.
    Make it an engaging.
    Make it coherent. You are free to change the structure of the sections for best output. 
    Ensure that the flow as I read the output is coherent.
    No need to do a greeting at the start.
    Figure out a great hook if necessary.
    Ensure that it is written in a manner that keeps the reader engaged throughout the article that you wrote.
    Figure out all the necessary transitions.
    Do not dumb it down as the reader can comprehend what is written.
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



