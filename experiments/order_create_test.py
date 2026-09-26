import os

import requests
from dotenv import load_dotenv

# ==================================================================================================
# 1. AUTHENTICATION
# ==================================================================================================

load_dotenv()

headers = {
     "Authorization": f"Bearer {os.getenv('HUBSPOT_SERVICE_KEY')}",
     "Content-Type": "application/json",
}


# ==================================================================================================
# 2. ORDER CONFIGURATION
# ==================================================================================================

ORDERS_URL = "https://api.hubspot.com/crm/objects/2026-09/orders"

ORDER_PIPELINE_ID = "14a2e10e-5471-408a-906e-c51f3b04369e"

OPEN_STAGE_ID = "4b27b500-f031-4927-9811-68a0b525cbae"

#===================================================================================================
# 3. BUILD TEST ORDER
#===================================================================================================

payload = {
    "properties": {
        "hs_order_name": "WooCommerce Order #1042",
        "hs_external_order_id": "1042",
        "hs_external_order_status": "processing",
        "hs_pipeline": ORDER_PIPELINE_ID,
        "hs_pipeline_stage": OPEN_STAGE_ID,
        "hs_total_price": "149.99",
        "hs_currency_code": "USD",
        }
}

# =================================================================================================
# 4. CREATE ORDER
# =================================================================================================

response = requests.post(
    ORDERS_URL,
    headers=headers,
    json=payload,
    timeout=10,
)

print("Status: ", response.status_code)
print("Response: ", response.text)


