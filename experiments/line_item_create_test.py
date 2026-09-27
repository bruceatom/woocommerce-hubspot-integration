import os
import json

import requests
from dotenv import load_dotenv


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

LINE_ITEMS_URL = (
    "https://api.hubapi.com/crm/objects/2026-09/line_items"
)

ORDER_ID = "646363341805"

headers = {
    "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}",
    "Content-Type": "application/json",
}


# ============================================================
# 2. LOAD SAMPLE LINE ITEM
# ============================================================

with open("sample_data/order.json") as file:
    data = json.load(file)

first_item = data["order"]["line_items"][0]


# ============================================================
# 3. TRANSFORM LINE ITEM
# ============================================================

hubspot_item = {
    "name": first_item["name"],
    "quantity": first_item["quantity"],
    "price": first_item["unit_price"],
}


# ============================================================
# 4. CREATE AND ASSOCIATE LINE ITEM
# ============================================================

payload = {
    "properties": hubspot_item,
    "associations": [{
        "to": {
            "id": ORDER_ID
        },
        "types": [{
            "associationCategory": "HUBSPOT_DEFINED",
            "associationTypeId": 514,
        }],
    }],
}

response = requests.post(
    LINE_ITEMS_URL,
    headers=headers,
    json=payload,
    timeout=10,
)


# ============================================================
# 5. RESULT
# ============================================================

print("Status:", response.status_code)
print("Response:", response.text)
