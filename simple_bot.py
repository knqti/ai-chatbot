import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_api = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=gemini_api)

messages = []

while True:
    user_input = input('User: ')
    messages.append(user_input)

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=messages
    )
    print(response.text)
    messages.append(response.text)

    # print(messages)    

