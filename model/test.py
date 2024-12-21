import base64
from VLMManager import VLMManager
import requests

with open(r"pleasework.jpg", "rb") as f:
    imgbytes = f.read()

vlm = VLMManager()
count = vlm.identify(imgbytes, ['empty chair'], [176, 435, 1245, 754])


# post to server
# hit to IP Address: 192.168.12.179:5000
# hit at /api/model as POST request 


# Define the endpoint
url = "http://192.168.12.179:5000/api/model"

# Example payload (replace with your data)
payload = {
    "SectorID": "1.2",
    "empty": f"{count}",
}

# Headers (optional, if required by the API)
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
if response.ok:
    print("Response:", response.json())
else:
    print("Failed to send request. Status code:", response.status_code)
    print("Response:", response.text)


#RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
