import os

import requests
from dotenv import load_dotenv


# ============================================================
# 1. HUBSPOT CONFIGURATION AND AUTHENTICATION
# ============================================================

HUBSPOT_CONTACTS_URL = "https://api.hubapi.com/crm/objects/2026-09/contacts"


# 1.1 Build authenticated HubSpot request headers
def get_hubspot_headers():
    load_dotenv()

    service_key = os.getenv("HUBSPOT_SERVICE_KEY")

    return {
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


# ============================================================
# 2. HUBSPOT CONTACT OPERATIONS
# ============================================================

# 2.1 Find an existing Contact by email
def find_hubspot_contact_by_email(email):
    headers = get_hubspot_headers()

    response = requests.get(
        f"{HUBSPOT_CONTACTS_URL}/{email}",
        headers=headers,
        params={"idProperty": "email"},
        timeout=10,
    )

    if response.status_code == 200:
        return response.json()

    if response.status_code == 404:
        return None

    response.raise_for_status()


# 2.2 Create a new Contact
def create_hubspot_contact(customer):
    headers = get_hubspot_headers()

    payload = {
        "properties": customer
    }

    response = requests.post(
        HUBSPOT_CONTACTS_URL,
        headers=headers,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
    
# ==========================================================================
# 3. HUBSPOT ORDER OPERATIONS
# ==========================================================================

HUBSPOT_ORDERS_URL = "https://api.hubspot.com/crm/objects/2026-09/orders"

ORDER_PIPELINE_ID = "14a2e10e-5471-408a-906e-c51f3b04369e"

OPEN_STAGE_ID = "4b27b500-f031-4927-9811-68a0b525cbae"

# 3.1 Find an existing Order by external Order Id

def find_hubspot_order_by_external_id(external_order_id):
    headers = get_hubspot_headers()

    response = requests.get(
        HUBSPOT_ORDERS_URL,
        headers=headers,
        params={
            "properties": "hs_external_order_id,hs_order_name",
            "limit": 100,
        },
        timeout=10,
    )

    response.raise_for_status()

    for order in response.json()["results"]:
        if order["properties"].get("hs_external_order_id") == str(external_order_id):
            return order

    return None

# 3.2 Create a new HubSpot Order

def create_hubspot_order(order):
    headers = get_hubspot_headers()
    
    payload = {
        "properties": {
           "hs_order_name": f"WooCommerce Order #{order['woocommerce_order_id']}",
           "hs_external_order_id": str(order["woocommerce_order_id"]),
           "hs_external_order_status": order["status"],
           "hs_pipeline": ORDER_PIPELINE_ID,
           "hs_pipeline_stage": OPEN_STAGE_ID,
           "hs_total_price": order["total"],
           "hs_currency_code": order["currency"],
           }
   }
       
# ==========================================================================
# 4. HUBSPOT LINE ITEM  OPERATIONS
# ==========================================================================

#4.1 Create Line Item and associate it with an Order

def find_hubspot_line_item_by_name(name):
    headers = get_hubspot_headers()
    
    response = requests.get(
        "https://api.hubapi.com/crm/objects/2026-09/line_items",
        headers=headers,
        params={
             "properties": "name",
             "limit": 100,
        },
        timeout=10
    )
    
    response.raise_for_status()
    
    for line_item in response.json()["results"]:
        if line_item["properties"].get("name") == name:
            return line_item
    
    return None
    
#4.2 Create Line Item and associate it with an Order

def create_hubspot_line_item(line_item, order_id):
    headers = get_hubspot_headers()
           
    payload = {
        "properties": line_item,
        "associations": [{
            "to": {"id": order_id},
            "types": [{
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 514,
            }],
        }],
    }
    
    response = requests.post(
        "https://api.hubapi.com/crm/objects/2026-09/line_items",
        headers=headers,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
