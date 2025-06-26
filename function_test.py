import os
import re
import ollama

# extract the tool call from the response
def extract_tool_call(text):
    import io
    from contextlib import redirect_stdout

    pattern = r"```tool_code\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        # Capture stdout in a string buffer
        f = io.StringIO()
        with redirect_stdout(f):
            result = eval(code)
        output = f.getvalue()
        r = result if output == '' else output
        return f'```tool_output\n{r}\n```'''
    return None


def convert(amount: float, currency: str, new_currency: str) -> float:
    # demo implementation
    return amount * 0.91231




def add_two_number(first_num: float, second_num: float) -> float:
    return first_num * second_num


instruction_prompt_with_function_calling = '''
At each turn, if you decide to invoke any of the function(s), it should be wrapped with ```tool_code```. 
The python methods described below are imported and available, you can only use defined methods. 
The generated code should be readable and efficient. 
The response to a method will be wrapped in ```tool_output``` use it to call more tools or generate a helpful, friendly response. 
When using a ```tool_call``` think step by step why and how it should be used.

The following Python methods are available:

```python

def add_two_number(first_num: float, second_num: float) -> float:
    """Add the two numbers

    Args:
      first_num: The first number
      second_num: The second number
    """
```

User: {user_message}

If you think a tool should be used, reply with the appropriate ```tool_output```
If no tool is used, please reply normally. Do not include ```tool_output```.
'''



user_input = str(input('User Input: '))

user_prompt = instruction_prompt_with_function_calling.format(user_message=user_input)
response = ollama.generate(model='gemma3:4b-it-qat', prompt=user_prompt)

print(response['response'])
call_response = extract_tool_call(response['response'])
print(call_response)