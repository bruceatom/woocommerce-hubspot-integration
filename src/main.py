import json
import os

import requests
from dotenv import load_dotenv


HUBSPOT_CONTACTS_URL = "https://api.hubapi.com/crm/objects/2026-09/contacts"


def get_hubspot_headers():
    load_dotenv()

    service_key = os.getenv("HUBSPOT_SERVICE_KEY")

    return {
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


def transform_customer(customer):
    return {
        "firstname": customer["first_name"],
        "lastname": customer["last_name"],
        "email": customer["email"],
        "phone": customer["phone"],
    }


def transform_order(order):
    return {
        "woocommerce_order_id": order["id"],
        "status": order["status"],
        "currency": order["currency"],
        "total": order["total"],
        "billing_address": order["billing_address"],
        "shipping_address": order["shipping_address"],
        "line_items": order["line_items"],
    }


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


def main():
    with open("sample_data/order.json") as file:
        data = json.load(file)

    customer = data["customer"]
    order = data["order"]

    hubspot_customer = transform_customer(customer)
    hubspot_order = transform_order(order)

    print("Transformed customer:", hubspot_customer)
    print("Transformed order:", hubspot_order)

    existing_contact = find_hubspot_contact_by_email(
        hubspot_customer["email"]
    )

    if existing_contact:
        print(
            "Existing HubSpot contact found:",
            existing_contact["id"],
        )
    else:
        created_contact = create_hubspot_contact(hubspot_customer)

        print(
            "New HubSpot contact created:",
            created_contact["id"],
        )


if __name__ == "__main__":
    main()
