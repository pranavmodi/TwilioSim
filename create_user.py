import requests
import json

url = "https://chat.botpress.cloud/47d77e43-4218-49f4-9cb4-3ed976c68d9e/users"

payload = {
    "name": "Pranav",
    "pictureUrl": "www.pranavmodi.com",
    "profile": "my profile",
    "id": "prmods"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")


print(response.text)