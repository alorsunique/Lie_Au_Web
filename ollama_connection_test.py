from ollama import chat
from ollama import ChatResponse


input_string = input(f"Input: ")

response: ChatResponse = chat(model='gemma3:1b-it-qat', messages=[
  {
    'role': 'user',
    'content': input_string,
  },
])



print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)