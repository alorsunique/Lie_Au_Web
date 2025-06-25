import os
import json
import requests

if __name__ == "__main__":
    # Choose your model (must be already pulled via `ollama pull`)
    model_name = "llama2"  # or "mistral", "gemma", etc.

    system_prompt = """
    You are an expert and helpful assistant. Please help the user as best as you can.
    Keep your response as short as possible.
    """

    user_prompt = input("Enter your prompt: ")

    # Build chat messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Send request to local Ollama server
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model_name,
            "messages": messages,
            "stream": False  # Set to True to stream tokens
        }
    )

    data = response.json()
    print(f"\nResponse: {data['message']['content']}\n")