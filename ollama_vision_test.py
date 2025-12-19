
from ollama import chat
from ollama import ChatResponse

from io import BytesIO
import base64

from datetime import datetime

from PIL import Image

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # or PNG based on your image
    return base64.b64encode(buffered.getvalue()).decode("utf-8")



def query_ollama(prompt, image_base64):

    print("Got Here")

    """Query Ollama with an image and prompt"""

    response = chat(

        model='gemma3:4b-it-qat',

        messages=[{

        'role': 'system',

        'content': prompt,

        'images': [image_base64]

        }]

    )

    return response['message']['content']


if __name__ == "__main__":


    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation Start Time: {current_time}")


    image_path = "skin.jpg"
    loaded_img = Image.open(image_path)

    converted_img = image_to_base64(loaded_img)

    prompt = '''
        I got this on my leg. It feels scaly and becomes itchy if I start itching it first. What could it be?
    '''



    response = query_ollama(prompt,converted_img)

    print(response)

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Message Generation End Time: {current_time}")
    print(f"Total Run Time: {finish_time - start_time}")