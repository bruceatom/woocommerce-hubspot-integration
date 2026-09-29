import os
import requests
from dotenv import load_dotenv

load_dotenv()

CONTACT_ID = "279098318823"
ORDER_ID = "646363341805"
ASSOCIATION_TYPE_ID = 2695

url = (
    f"https://api.hubapi.com/crm/objects/2026-09/contacts/"
    f"{CONTACT_ID}/associations/orders/{ORDER_ID}"
)

headers = {
    "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}",
    "Content-Type": "application/json",
}

payload = [
    {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": ASSOCIATION_TYPE_ID,
    }
]

response = requests.put(
    url,
    headers=headers,
    json=payload,
    timeout=10,
)

print("Status:", response.status_code)
print("Response:", response.text)
