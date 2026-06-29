import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup
import json


now = datetime.now()
overall_start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Program Start Time: {current_time}")


persona_dir = Path( r"D:\Projects\Resources\Lie_Au_Web Resources\Persona" )



json_list = []

for json_file in persona_dir.rglob('*.json'):
    json_list.append(json_file)

import random

selected_persona = random.choice(json_list)


# selected_persona = json_list[8]

print(selected_persona)

with open(selected_persona, 'r') as open_json:
    persona_data = json.load(open_json)








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

    # inner_page = wiki_wiki.page('Peacocks Crossroads, North Carolina')

    inner_page = wiki_wiki.page('The Origin of Consciousness in the Breakdown of the Bicameral Mind')

    inner_page = wiki_wiki.page('Gang bang')



    inner_page = wiki_wiki.page('Florida Keys')

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
    So everything should be written so that it conveys the same information when spoken aloud.
    Do not format it with Markdown or LaTeX. It should just be plaintext.
    Do not make it longer than what is needed.
    Do not add "chapter" marks. Just ensure that the flow is natural. AGAIN DO NOT ADD CHAPTER TITLES OR HEADINGS.
    You can use information from the supplemental articles IF NECESSARY. IF NOT, DO NOT USE THEM.
    Make it engaging.
    Make it coherent. You are free to change the structure of the sections for best output. 
    Ensure that the flow, as I read the output, is coherent.
    No need to do a greeting at the start.
    Figure out a great hook if necessary.
    Ensure that it is written in a manner that keeps the reader engaged throughout the article that you wrote.
    Figure out all the necessary transitions.
    Do not dumb it down as the reader can comprehend what is written.
"""

user_prompt = """
    I want you to transform the main article into a comprehensive, standalone report.
    
    The report should aim for 12,000 to 15,000 words whenever the source material can support that level of depth. Under no circumstances should the report be shorter than 10,000 words. If necessary, expand explanations, provide historical background, discuss implications, explain causes and effects, analyze evidence, and thoroughly explore important concepts until the required depth is achieved.
    
    Do not skip any important information, arguments, evidence, examples, data points, case studies, nuances, caveats, or conclusions from the article.
    
    Assume that I have no access to the original article. Therefore, NEVER use phrases such as "the article says", "the article mentions", "the article discusses", "according to the article", or similar references. Present all information directly as if you are explaining it to me yourself.
    
    Everything should be written so that it sounds natural when read aloud. The report should feel like a knowledgeable expert speaking directly to an interested listener.
    
    Do not format the output with Markdown, LaTeX, bullet points, numbered lists, headings, subheadings, chapter titles, section titles, or any other structural markers. The output must be plain text only.
    
    Maintain a natural flow throughout the entire report. Use strong transitions between topics so that each idea leads smoothly into the next.
    
    Do not artificially compress information for brevity. Prioritize completeness, depth, clarity, and thoroughness over conciseness.
    
    Explain complex concepts fully. When important context is required to understand a topic, provide that context. When claims are supported by evidence, explain the evidence. When conclusions are reached, explain the reasoning behind them.
    
    Preserve the intellectual depth of the source material. Do not dumb down the content. Assume the reader is intelligent and capable of understanding sophisticated explanations.
    
    You may use information from supplemental articles ONLY when it meaningfully improves understanding, fills critical gaps, provides essential context, clarifies technical points, or helps create a more complete report. If supplemental articles are not necessary, do not use them.
    
    Make the report engaging and compelling to read. Use strong narrative flow, thoughtful pacing, and clear explanations that sustain interest across the entire report.
    
    You are free to reorganize the material if doing so improves clarity, coherence, or readability. However, all important information from the source material must still be included.
    
    Ensure that the final output reads as a single, cohesive, professionally written report rather than a summary. The reader should feel that they have effectively absorbed the full substance of the source material without needing to read the original article.
    
    Do not include greetings, introductions about your process, meta-commentary, summaries of what you are going to do, or conclusions that discuss the existence of the source article. Simply begin the report itself.
"""



user_prompt = """
    I want you to report the main article to me in a digestible manner.
    Do not skip out on important parts.
    Assume that I have no access to this article so DO NOT say things like "the article says" or "the article covers". 
    Instead, say it to me like I am listening to you talk.
    So everything should be written so that it conveys the same information when spoken aloud.
    Do not format it with Markdown or LaTeX. It should just be plaintext.
    Do not make it longer than what is needed.
    Do not add "chapter" marks. Just ensure that the flow is natural. AGAIN DO NOT ADD CHAPTER TITLES OR HEADINGS.
    You can use information from the supplemental articles IF NECESSARY. IF NOT, DO NOT USE THEM.
    Make it engaging.
    Make it coherent. You are free to change the structure of the sections for best output. 
    Ensure that the flow, as I read the output, is coherent.
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

user_prompt = """
    I also want you to write this through the lens of someone else.
    I will be sending a persona with information in the string version of a Python dictionary.
    Write as if you are that person.
    This means that your knowledge is limited based on what that person would most likely know.
    For the MAIN and supplemental articles, just treat them as being accessed by the person through a library for example.
    This means that the person may know that such info exists because of this access but an understanding beyond the main
    and supplemental articles is not given.
"""


message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)

user_prompt = f"""
    The persona that you will be using is the following:
    {str(persona_data)}
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
        'num_predict': 16384,
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




# print(response)

print(f"\n\n\n\n")

input_token_count = response.prompt_eval_count
output_token_count = response.eval_count

total_token_count = input_token_count + output_token_count

model_load_process_time = response.load_duration / 1000000000
input_process_time = response.prompt_eval_duration / 1000000000
output_process_time = response.eval_duration / 1000000000

total_process_time = response.total_duration / 1000000000



print(f'Input Token Count: {input_token_count}')
print(f'Output Token Count: {output_token_count}')
print(f'Total Token Count: {total_token_count}')

print(f'Load Time: {model_load_process_time}')
print(f'Input Time: {input_process_time}')
print(f'Output Time: {output_process_time}')

print(f'Total Time: {total_process_time}')





now = datetime.now()
overall_finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"\n\n\n\nProgram End Time: {current_time}")
print(f"Total Program Run Time: {overall_finish_time - overall_start_time}")

