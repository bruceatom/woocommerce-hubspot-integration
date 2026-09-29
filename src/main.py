import json

from transforms import (
    transform_customer,
    transform_line_item,
    transform_order,
)

from hubspot_client import (
    create_hubspot_contact,
    create_hubspot_order,
    create_hubspot_line_item,
    find_hubspot_contact_by_email,
    find_hubspot_order_by_external_id,
    find_hubspot_line_item_by_name,
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

    # 1.6 Find existing Order
    existing_order = find_hubspot_order_by_external_id(
        hubspot_order["woocommerce_order_id"]
    ) 
    
   # 1.7 Reuse existing Order or create a new Order
    if existing_order:
        hubspot_order_id = existing_order["id"]
        print(
            "Existing HubSpot Order found:", existing_order["id"],
        )
    else:
        created_order = create_hubspot_order(hubspot_order)
        hubspot_order_id = created_order["id"]

        print(
            "New HubSpot Order created:",
            created_order["id"],
        )
        
    # 1.8 Create and associate Line Items

    for item in order["line_items"]:
       hubspot_line_item = transform_line_item(item)
       
       existing_line_item = find_hubspot_line_item_by_name(
           hubspot_line_item["name"]
       )
       
       if existing_line_item:
           print(
                "Existing HubSpot Line Item found:",
                existing_line_item["id"],
          )
       else:
          create_line_item = create_hubspot_line_item(
              hubspot_line_item,
              hubspot_order_id,
         )
         
# ============================================================
# 2. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
