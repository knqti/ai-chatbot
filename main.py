from dotenv import load_dotenv
from flask import Flask, request, jsonify
from src.ai.chatbot import MemoryChatbot
import requests
import os

load_dotenv()
app = Flask(__name__)

# Vonage credentials
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_PHONE_NUMBER = os.getenv("VONAGE_PHONE_NUMBER")

def send_sms(to_number, message):
    """Send SMS using Vonage REST API directly"""
    url = "https://rest.nexmo.com/sms/json"
    
    data = {
        'api_key': VONAGE_API_KEY,
        'api_secret': VONAGE_API_SECRET,
        'from': VONAGE_PHONE_NUMBER,
        'to': to_number,
        'text': message
    }
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Error making API call: {e}")

@app.route('/webhooks/inbound-sms', methods=['POST'])
def inbound_sms():
    try:
        # Get SMS data from Vonage webhook
        data = request.form.to_dict()
        from_number = data.get('msisdn')
        text_message = data.get('text')
        print(f'Received from {from_number}: {text_message}')        
        print('Sending to AI')

        ai_response = MemoryChatbot(user_id=from_number).chat(message=text_message)
        print(f'AI response: {ai_response}')

        # Send response using direct HTTP
        result = send_sms(from_number, ai_response)
        
        if result and result.get('messages') and result['messages'][0]['status'] == '0':
            print("Response sent successfully!")
        else:
            print(f"Error sending SMS: {result}")
            
    except Exception as e:
        print(f"Error in webhook: {e}")
    
    return jsonify({"status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET', 'POST'])
def home():
    print(f"Root route accessed with {request.method}")
    print(f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    print(f"Remote Address: {request.remote_addr}")
    print(f"Referrer: {request.headers.get('Referer', 'None')}")
    
    if request.method == 'POST':
        print(f"POST Data: {request.form.to_dict()}")
        print(f"Headers: {dict(request.headers)}")
    
    return jsonify({"message": "Vonage SMS Webhook Server"}), 200

if __name__ == '__main__':
    print("Starting SMS webhook server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)