import os

import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}"
}

response = requests.get(
    "https://api.hubspot.com/crm/pipelines/2026-09/order",
    headers=headers,
    timeout=19,
)

print("Status: ", response.status_code)
print(response.text)

