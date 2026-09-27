import os

import requests
from dotenv import load_dotenv


# ============================================================
# 1. AUTHENTICATION
# ============================================================

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}",
}


# ============================================================
# 2. TEST RECORDS
# ============================================================

ORDER_ID = "646363341805"
LINE_ITEM_ID = "222845703105"


# ============================================================
# 3. ASSOCIATE ORDER -> LINE ITEM
# ============================================================

url = (
    f"https://api.hubapi.com/crm/objects/2026-09/orders/"
    f"{ORDER_ID}/associations/line_items/{LINE_ITEM_ID}/513"
)

response = requests.put(
    url,
    headers=headers,
    timeout=10,
)


# ============================================================
# 4. RESULT
# ============================================================

print("Status:", response.status_code)
print("Response:", response.text)
