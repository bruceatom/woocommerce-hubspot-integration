import json
import os

import requests
from dotenv import load_dotenv
from transforms import transform_customer, transform_order


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


# ============================================================
# 3. INTEGRATION WORKFLOW
# ============================================================

def main():
    # 3.1 Load source data
    with open("sample_data/order.json") as file:
        data = json.load(file)

    # 3.2 Separate source business objects
    customer = data["customer"]
    order = data["order"]

    # 3.3 Transform source data
    hubspot_customer = transform_customer(customer)
    hubspot_order = transform_order(order)

    print("Transformed customer:", hubspot_customer)
    print("Transformed order:", hubspot_order)

    # 3.4 Find existing Contact
    existing_contact = find_hubspot_contact_by_email(
        hubspot_customer["email"]
    )

    # 3.5 Reuse existing Contact or create a new Contact
    if existing_contact:
        print(
            "Existing HubSpot contact found:",
            existing_contact["id"],
        )
    else:
        created_contact = create_hubspot_contact(
            hubspot_customer
        )

        print(
            "New HubSpot contact created:",
            created_contact["id"],
        )


# ============================================================
# 4. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
