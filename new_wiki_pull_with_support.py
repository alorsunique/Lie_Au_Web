import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
from PIL import Image
from bs4 import BeautifulSoup


import wikipediaapi
from wikipediaapi._enums import RedirectFilter
import asyncio

# wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

wiki_wiki = wikipediaapi.Wikipedia('JisooIlhada (jisooilhada@gmail.com)', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)



page_list = wiki_wiki.random(filter_redirect=RedirectFilter.NONREDIRECTS, limit=32)

supplemental_page_list = []

extracted_page_list = []

for main_article_count, page in enumerate(page_list):

    extracted_dict = {}

    inner_page = wiki_wiki.page(page)

    title = inner_page.title

    extracted_dict['Article Title'] = title

    summary = inner_page.summary

    extracted_dict['Article Summary'] = summary

    sections = inner_page.sections

    print(f'{main_article_count + 1}: {extracted_dict}')

    extracted_page_list.append(extracted_dict)

    links = inner_page.links

    for link_count, link in enumerate(links):

        supplemental_dict = {}

        print(f'Main Article Count: {main_article_count + 1} | Link Count {link_count+1}: {link}')

        link_title = link.title()

        # print(f'Link Title: {link_title}')

        if (
            link_title.lower().startswith('template talk:' )
            or link_title.lower().startswith('template:')
            or link_title.lower().startswith('wikipedia:')
            or link_title.lower().startswith('help:')
        ):
            # print('Excluded')
            pass
        else:

            in_text_bool = False

            for keys in extracted_dict.keys():

                print('################################################################')

                print(f'Article Number: {main_article_count + 1} | Current Key: {keys} | Link Compare: {link_title}')

                print('%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#%&^#')

                if link_title.lower() in extracted_dict[keys].lower():

                    print(link_title.lower())

                    print(extracted_dict[keys].lower())

                    in_text_bool = True

                print('################################################################\n\n')

            if in_text_bool:

                reference_page = wiki_wiki.page(link)
                # print("Page - Exists: %s" % reference_page.exists())

                if reference_page.exists():
                    supplemental_dict[f'Article Count {main_article_count + 1} Supplement Title'] = reference_page.title
                    supplemental_dict[f'Article Count {main_article_count + 1} Supplement Summary'] = reference_page.summary


                    supplemental_page_list.append(supplemental_dict)








page_list = wiki_wiki.random(filter_redirect=RedirectFilter.NONREDIRECTS, limit=64)

bridge_page_list = []



for main_article_count, page in enumerate(page_list):

    extracted_dict = {}

    inner_page = wiki_wiki.page(page)

    title = inner_page.title

    extracted_dict['Bridge Article Title'] = title

    summary = inner_page.summary

    extracted_dict['Bridge Article Summary'] = summary

    sections = inner_page.sections

    print(f'Bridge {main_article_count + 1}: {extracted_dict}')

    bridge_page_list.append(extracted_dict)























































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
    I will provide bridge articles.
    Take note that these are only for connectivity purposes. THEY ARE NOT SUPPORT OR MAIN ARTICLES.
    Use them if they can help connect main to main or main to support articles.
    I will be sending the bridge articles in a string version of a Python dictionary.
"""

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)


for supplemental_article_count, supplemental_article in enumerate(bridge_page_list):
    message_list.append(
        {
            "role": "user",
            "content": f"Bridge Article {supplemental_article_count+1}. {str(supplemental_article)}\n",
        }
    )




user_prompt = """
    I will provide supplemental articles.
    Take note that these are only SUPPLEMENTAL. THEY ARE NOT MAIN ARTICLES.
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
    I will now provide main articles.
    I will be sending these articles in a string version of a Python dictionary.
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


user_prompt = """
    I want you to transform the collection of articles into a narrative story centered around a main character who actively explores, investigates, and experiences the ideas contained within them.

    The main character should function as the reader’s perspective into the material. Instead of summarizing information, the character should encounter each concept through lived experience, observation, exploration, conversation, or discovery. The articles’ content must be deeply integrated into the unfolding narrative, becoming part of the world the character moves through.
    
    All information should be embedded naturally into the story so that insights emerge through events and progression rather than exposition. The reader should learn by following what the character sees, questions, tests, and uncovers.
    
    Do not refer to “the article,” “the articles,” or any external source framing. Do not describe anything as being summarized or reported. Everything should feel intrinsic to the story’s world.
    
    The output must be plain text only. No Markdown, LaTeX, headings, section breaks, chapter titles, or structural markers of any kind. The narrative must flow continuously and organically.
    
    You are free to reorder, merge, or interweave material from different sources to improve coherence, pacing, thematic resonance, and narrative engagement, as long as all important information is preserved and meaningfully incorporated.
    
    Supplemental material may be included only if it strengthens understanding or narrative depth; otherwise it should be ignored.
    
    The story must have a clear, consistent main character with agency, curiosity, and development over time. This character should actively engage with ideas—questioning them, testing them, connecting them across contexts, and gradually forming a deeper understanding through experience.
    
    Begin with a compelling hook that immediately draws the reader into the character’s journey and stakes. Maintain engagement through strong narrative momentum, meaningful transitions, and evolving discoveries.
    
    The writing should be intellectually rich and assume a capable reader. Do not simplify concepts unnecessarily; instead, integrate complexity naturally into the character’s understanding and experiences.
    
    There is no length limit. The response should be as long as necessary to fully and coherently explore and integrate all material in depth, and no longer.
"""


user_prompt = """
    I want you to transform the collection of articles into a narrative story centered around a main character who actively explores, investigates, and experiences the ideas contained within them.
    
    The main character should function as the reader’s perspective into the material. Instead of summarizing information, the character should encounter each concept through lived experience, observation, exploration, conversation, experimentation, or discovery. The articles’ content must be deeply integrated into the unfolding narrative, becoming part of the world the character moves through.
    
    All information should be embedded naturally into the story so that insights emerge through events and progression rather than exposition. The reader should learn by following what the character sees, questions, tests, debates, and uncovers.
    
    Do not refer to “the article,” “the articles,” or any external source framing. Do not describe anything as being summarized or reported. Everything should feel intrinsic to the story’s world.
    
    The output must be plain text only. No Markdown, LaTeX, headings, section breaks, chapter titles, or structural markers of any kind. The narrative must flow continuously and organically.
    
    You are free to reorder, merge, or interweave material from different sources to improve coherence, pacing, thematic resonance, and narrative engagement, as long as all important information is preserved and meaningfully incorporated.
    
    Supplemental material may be included only if it strengthens understanding or narrative depth; otherwise it should be ignored.
    
    The story must have a clear, consistent main character with agency, curiosity, and development over time. This character should actively engage with ideas—questioning them, testing them, connecting them across contexts, and gradually forming a deeper understanding through experience.
    
    Begin with a compelling hook that immediately draws the reader into the character’s journey and stakes. Maintain engagement through strong narrative momentum, meaningful transitions, evolving discoveries, and recurring threads that connect seemingly unrelated topics.
    
    The writing should be intellectually rich and assume a capable reader. Do not simplify concepts unnecessarily; instead, integrate complexity naturally into the character’s understanding and experiences.
    
    Explore ideas thoroughly. When a topic is important, spend the necessary time examining its implications, nuances, competing perspectives, historical context, technical details, and real-world consequences through the narrative. Favor depth over brevity.
    
    The story must be at least 10,000 words long. Treat 10,000 words as a minimum target, not a maximum. If the material requires more space to be explored properly, continue beyond 10,000 words. Do not compress, rush, or omit important information merely to reduce length.
    
    However, do not add filler, repetition, redundant scenes, or unnecessary dialogue solely to increase word count. Every scene, conversation, observation, and narrative development should contribute meaningfully to understanding the material or advancing the story.
    
    The response should ultimately be as long as necessary to fully and coherently integrate all source material in depth, while remaining engaging, purposeful, and narratively cohesive.
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
    # model = 'gemma3:4b',
    # model = 'gemma3:12b-it-qat ',
    messages=message_list,
    options={
        'num_predict': 16384,
        # 'num_predict': -1,
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




print(f"\n\n\n\n")


thinking_content = response.message.thinking

print(thinking_content)


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




