from google import genai
from google.genai import types
import os

def ai_router(inbound_msg):
    gemini_api = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=gemini_api)

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        config=types.GenerateContentConfig(
            system_instruction='''
                If you're asked about the weather then reply "weather" only.
                Otherwise reply "conversation".
                '''
        ),
        contents=inbound_msg
    )
    return response.text