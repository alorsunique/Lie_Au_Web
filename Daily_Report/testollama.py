import os
from pathlib import Path

from ollama import chat
from ollama import ChatResponse

import yaml
from datetime import datetime, timedelta
import time


message_list = []

system_prompt = '''
    You are a helpful assistant. You will assist the user in their request
'''

# Appends the system prompt
message_list.append(
    {
        'role': 'system',
        'content': system_prompt,
    }
)

user_prompt = "Tell me a fact about butterflies"

message_list.append(
    {
        "role": "user",
        "content": user_prompt,
    }
)

print(message_list)

response: ChatResponse = chat(
        model='gemma3:4b-it-qat',
        messages=message_list,
    )

print(response)

