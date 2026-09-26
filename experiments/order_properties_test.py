import os

import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}"
}

response = requests.get(
    "https://api.hubapi.com/crm/properties/2026-09/orders",
    headers=headers,
    timeout=10,
)

print("Status: ", response.status_code)

if response.status_code == 200:
    for prop in response.json()["results"]:
        if prop.get("label") in {
           "Name",
           "Pipeline",
           "Pipeline Stage",
           "Total Amount",
       }:
           print(
               prop.get("label"),
               "=>",
               prop.get("name"),
           )
print("/nProperties containing 'stage:':")

for prop in response.json()["results"]:
    if "stage" in prop.get("label", "").lower():
        print(
            prop.get("label"),
            "=>",
            prop.get("name"),
            )
           

else:
     print(response.text)
