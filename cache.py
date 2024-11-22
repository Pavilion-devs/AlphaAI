import os
import google.generativeai as genai
from google.generativeai import caching
from google.generativeai import GenerationConfig
import datetime
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv('api_key')

genai.configure(api_key=GENAI_API_KEY)

text_file_path = "C:/Users/olabo/OneDrive/Desktop/AlphaAI/frontend_contents.txt"

if not os.path.exists(text_file_path):
    raise FileNotFoundError(f"File not found: {text_file_path}")



with open(text_file_path, "r") as file:
    text_content = file.read()

cache = caching.CachedContent.create(
        model='models/gemini-1.5-flash-001',
        display_name='My-evaluations',
        system_instruction=(
            'You are an experienced developer with in-depth knowledge of programming best practices. '
            'Your task is to review the codebase provided and identify areas for improvement, '
            'such as security, maintainability, and error handling issues.'
        ),
        contents=[text_content],
        ttl=datetime.timedelta(minutes=10),
    )

model = genai.GenerativeModel.from_cached_content(cached_content=cache)


GREEN = '\033[92m'
RESET = '\033[0m'

print("Welcome to the code review tool")

while True:
    user_input = input("> ")

    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    response = model.generate_content([user_input], stream=True)

    print(response.usage_metadata)

    for chunk in response:
        if hasattr(chunk, 'finish_reason') and chunk.finish_reason == 3:
            print("The response was blocked due to safety concerns.")
            continue

        if hasattr(chunk, 'text'):
            print(GREEN + chunk.text + RESET)
        else:
            print("No valid text found in chunk")

