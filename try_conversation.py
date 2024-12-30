import requests

url = "https://chat.botpress.cloud/48f32c62-4614-469d-b1a4-d05554f064cd/conversations"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-bp-secret": "mypass"
}

response = requests.post(url, headers=headers)

# Print the complete response
print("Status Code:", response.status_code)
print("\nHeaders:")
for key, value in response.headers.items():
    print(f"{key}: {value}")
print("\nResponse Body:")
print(response.text)
