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
