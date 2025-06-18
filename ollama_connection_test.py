from ollama import chat
from ollama import ChatResponse

response = chat(model='gemma3:12b-it-qat', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)