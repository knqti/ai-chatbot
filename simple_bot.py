import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def gemini_bot(text_message):
    load_dotenv()
    gemini_api = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=gemini_api)

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        config=types.GenerateContentConfig(
            system_instruction='Keep your answers brief and short. Format for sms text messages and keep limitations in mind. Do not use markdown format.'
        ),
        contents=text_message
    )
    return response.text
