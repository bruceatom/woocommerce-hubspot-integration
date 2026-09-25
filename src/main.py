import json

from transforms import transform_customer, transform_order

from hubspot_client import (
    create_hubspot_contact,
    find_hubspot_contact_by_email,
)


# ============================================================
# 1. INTEGRATION WORKFLOW
# ============================================================

def main():
    # 1.1 Load source data
    with open("sample_data/order.json") as file:
        data = json.load(file)

    # 1.2 Separate source business objects
    customer = data["customer"]
    order = data["order"]

    # 1.3 Transform source data
    hubspot_customer = transform_customer(customer)
    hubspot_order = transform_order(order)

    print("Transformed customer:", hubspot_customer)
    print("Transformed order:", hubspot_order)

    # 1.4 Find existing Contact
    existing_contact = find_hubspot_contact_by_email(
        hubspot_customer["email"]
    )

    # 1.5 Reuse existing Contact or create a new Contact
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
# 2. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
