from dotenv import load_dotenv
from flask import Flask, request, jsonify
from simple_bot import gemini_bot
import requests
import os

load_dotenv()
app = Flask(__name__)

# Vonage credentials
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_PHONE_NUMBER = "16513141214"

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
        return None

@app.route('/webhooks/inbound-sms', methods=['POST'])
def inbound_sms():
    try:
        # Get SMS data from Vonage webhook
        data = request.form.to_dict()
        
        from_number = data.get('msisdn')
        message_text = data.get('text')
        
        print(f"📨 Received SMS from {from_number}: {message_text}")
        # print(f"Raw webhook data: {data}")
        print('Sending to AI...')

        ai_response = gemini_bot(message_text)
        print(f'AI response: {ai_response}')

        # Send "hello world" response using direct HTTP
        result = send_sms(from_number, ai_response)
        
        if result and result.get('messages') and result['messages'][0]['status'] == '0':
            print("✅ Response sent successfully!")
        else:
            print(f"❌ Error sending SMS: {result}")
            
    except Exception as e:
        print(f"❌ Error in webhook: {e}")
    
    return jsonify({"status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Vonage SMS Webhook Server"}), 200

if __name__ == '__main__':
    print("🚀 Starting SMS webhook server...")
    print(f"📱 Using Vonage number: {VONAGE_PHONE_NUMBER}")
    app.run(debug=True, host='0.0.0.0', port=5000)