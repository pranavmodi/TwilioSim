from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json
import uvicorn
from asgiref.wsgi import WsgiToAsgi
import time
import threading

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
    print("\nSending message to Botpress...")
    print("Waiting for response...")
    
    botpress_payload = {
        "conversationId": conversation_id,
        "payload": {
            "message": message,
            "userId": user_id,
            "type": "text",
            "text": message,
            "metadata": {}
        }
    }

    print("\nSending request to Botpress:")
    print(f"URL: {BOTPRESS_WEBHOOK_URL}")
    print("Payload:")
    print(json.dumps(botpress_payload, indent=2))
    print("-" * 50)

    try:
        botpress_response = requests.post(
            BOTPRESS_WEBHOOK_URL,
            json=botpress_payload,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        print("\nBotpress Response Details:")
        print(f"Status Code: {botpress_response.status_code}")
        print(f"Response Headers: {dict(botpress_response.headers)}")
        print(f"Raw Response Content: {botpress_response.content}")
        print("-" * 50)

        if botpress_response.status_code != 200:
            return f"Error: Botpress returned status code {botpress_response.status_code}", conversation_id

        if not botpress_response.content:
            return "Error: Empty response from Botpress", conversation_id

        botpress_data = botpress_response.json()
        
        # Print the full response for debugging
        print("Botpress Response:")
        print(json.dumps(botpress_data, indent=2))
        print("-" * 50)
        
        # Get the response and conversation ID from Botpress
        if isinstance(botpress_data, list) and botpress_data:
            bot_reply = botpress_data[0].get('text', 'Sorry, I could not process your request.')
            # Try to get conversation ID from response, fallback to provided one
            conversation_id = botpress_data[0].get('conversationId', conversation_id)
        else:
            bot_reply = botpress_data.get('text', 'Sorry, I could not process your request.')
            # Try to get conversation ID from response, fallback to provided one
            conversation_id = botpress_data.get('conversationId', conversation_id)
        
        return bot_reply, conversation_id

    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}", conversation_id
    except json.JSONDecodeError as e:
        return f"Invalid JSON response: {str(e)}", conversation_id
    except Exception as e:
        return f"Unexpected error: {str(e)}", conversation_id

@app.route("/api/message", methods=['POST'])
def api_message():
    """API endpoint to receive messages from Botpress"""
    data = request.json
    message = data.get('message', '')
    conversation_id = data.get('conversationId', 'default_conversation')

    print("\nReceived from Botpress:")
    print(f"Message: {message}")
    print(f"ConversationId: {conversation_id}")
    print("-" * 30)

    # Store conversation ID for later use
    global current_conversation_id
    current_conversation_id = conversation_id
    
    return jsonify({"status": "received"})

def console_input_handler():
    """Handle console input in a separate thread"""
    global current_conversation_id
    
    while True:
        user_message = input("\nYou: ").strip()  # Strip whitespace
        if user_message.lower() == 'quit':
            break
            
        if not user_message:  # Skip empty messages
            continue
            
        if current_conversation_id:
            # Send message to Botpress using the stored conversation ID
            bot_response, _ = send_to_botpress(user_message, conversation_id=current_conversation_id)
            print(f"\nSent to Botpress using ConversationId: {current_conversation_id}")
        else:
            print("\nWaiting for Botpress to start the conversation first...")

if __name__ == "__main__":
    port = 50000
    current_conversation_id = None  # Global variable to store conversation ID
    
    print(f"\nStarting server on http://0.0.0.0:{port}")
    print(f"API endpoint available at http://0.0.0.0:{port}/api/message")
    print("\nWaiting for messages from Botpress...")
    print("-" * 30)
    
    # Start console input handler in a separate thread
    input_thread = threading.Thread(target=console_input_handler, daemon=True)
    input_thread.start()
    
    # Convert WSGI app to ASGI
    asgi_app = WsgiToAsgi(app)
    
    # Run Uvicorn server with ASGI app
    uvicorn.run(asgi_app, host="0.0.0.0", port=port, log_level="info")
