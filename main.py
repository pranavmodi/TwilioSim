from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json
import uvicorn
from asgiref.wsgi import WsgiToAsgi

# Load environment variables
load_dotenv()

# Get environment variables
BOTPRESS_WEBHOOK_URL = os.getenv('BOTPRESS_WEBHOOK_URL')
BOTPRESS_BOT_ID = os.getenv('BOTPRESS_BOT_ID')

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://studio.botpress.cloud"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def send_to_botpress(message, user_id="simulator_user", conversation_id="default_conversation"):
    """Simulate sending a message to Botpress"""
    botpress_payload = {
        "message": message,
        "conversationId": conversation_id,
        "userId": user_id,
        "payload": {
            "type": "text",
            "text": message,
            "metadata": {}
        }
    }

    try:
        botpress_response = requests.post(
            BOTPRESS_WEBHOOK_URL,
            json=botpress_payload,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        if botpress_response.status_code != 200:
            return f"Error: Botpress returned status code {botpress_response.status_code}"

        if not botpress_response.content:
            return "Error: Empty response from Botpress"

        botpress_data = botpress_response.json()
        
        # Get the response from Botpress
        if isinstance(botpress_data, list) and botpress_data:
            bot_reply = botpress_data[0].get('text', 'Sorry, I could not process your request.')
        else:
            bot_reply = botpress_data.get('text', 'Sorry, I could not process your request.')
        
        return bot_reply

    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Invalid JSON response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@app.route("/api/message", methods=['POST'])
def api_message():
    """API endpoint to receive messages and respond via Botpress"""
    data = request.json
    message = data.get('message', '')
    user_id = data.get('user_id', 'simulator_user')
    conversation_id = data.get('conversationId', 'default_conversation')

    print(f"\nReceived from Botpress: {message}")
    print(f"ConversationId: {conversation_id}")

    # Get response from Botpress
    bot_response = send_to_botpress(message, user_id, conversation_id)
    
    print(f"Sending to Botpress: {bot_response}")
    
    # Return response with conversationId
    return jsonify({
        "response": bot_response,
        "conversationId": conversation_id,
        "user_id": user_id
    })

def main():
    print("\nBotpress Conversation Simulator")
    print("Type 'quit' to exit")
    print("-" * 30)

    while True:
        # Get user input
        user_message = input("\nYou: ")
        
        if user_message.lower() == 'quit':
            break

        # Get response from Botpress
        bot_response = send_to_botpress(user_message, conversation_id="cli_conversation")
        
        # Display bot response
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    port = 50000
    print(f"\nStarting server on http://0.0.0.0:{port}")
    print(f"API endpoint available at http://0.0.0.0:{port}/api/message")
    print("\nTo access this from the internet, use your server's public IP address or domain name")
    print("-" * 30)
    
    # Convert WSGI app to ASGI
    asgi_app = WsgiToAsgi(app)
    
    # Run Uvicorn server with ASGI app
    uvicorn.run(asgi_app, host="0.0.0.0", port=port, log_level="info")
