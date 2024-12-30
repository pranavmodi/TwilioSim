import requests
import json

def create_conversation():
    url = "https://api.botpress.cloud/v1/chat/conversations"
    headers = {
        "accept": "application/json",
        "authorization": "Bearer bp_pat_huxde1cAuxKFeRQPDjiz2M1D9kAIP3D3MUkW",
        "content-type": "application/json",
        "x-bot-id": "95588c0a-5d3c-4ace-8042-af7c88ee9f12"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print("\nResponse Details:")
        print("Status Code:", response.status_code)
        print("\nResponse Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        
        print("\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating conversation: {e}")
        return None

if __name__ == "__main__":
    result = create_conversation()
    if result:
        print("Conversation created successfully:")
        print(result)
