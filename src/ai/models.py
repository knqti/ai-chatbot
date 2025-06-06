from google import genai
from google.genai import types
import os

def gemini_2_0_flash(inbound_msg: str, instructions: str='') -> str:
    '''Google Gemini 2.0 Flash model.
    
    Args:
        inbound_msg: User inbound message to the AI
        instructions: Initial instructions for the AI (ie, /src/instructions)

    Returns:
        AI response in string format
    '''
    gemini_api = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=gemini_api)

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        config=types.GenerateContentConfig(
            system_instruction=instructions
        ),
        contents=inbound_msg
    )
    return response.text
