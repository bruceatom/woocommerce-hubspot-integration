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
# 2. LOAD SAMPLE LINE ITEMS
# ============================================================

with open("sample_data/order.json") as file:
    data = json.load(file)

line_items = data["order"]["line_items"]


# ============================================================
# 3. TRANSFORM AND SEND LINE ITEMS
# ============================================================

for item in line_items:
    hubspot_item = {
        "name": item["name"],
        "quantity": item["quantity"],
        "price": item["unit_price"],
    }

    payload = {
        "properties": hubspot_item,
        "associations": [{
            "to": {"id": ORDER_ID},
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

    print(item["name"], "=>", response.status_code)
