from dotenv import load_dotenv
from src.ai.guardrails import base_guide
from src.ai.models import gemini_2_0_flash

load_dotenv()

def test_bot():
    messages = []

    while True:
        user_input = input('User: ')    
        messages.append(user_input)
        response = gemini_2_0_flash(
            inbound_msg=messages,
            instructions=base_guide
        )
        print(f'AI: {response}')
        messages.append(response)

if __name__ == '__main__':
    test_bot()
