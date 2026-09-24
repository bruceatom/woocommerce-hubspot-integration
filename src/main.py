import json
import os

import requests
from dotenv import load_dotenv


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

def create_hubspot_contact(customer):
    load_dotenv()
    
    service_key = os.getenv("HUBSPOT_SERVICE_KEY")
    
    headers = {
       "Authorization": f"Bear {service_key}",
       "Content-Type": "application/json",
    }
    
    payload = {
        "properties": customer
    }
    
    response = requests.post(
        "https://api.hubapi.com/crm/objects/2026-09/contacts",
        headers=headers,
        json=payload,
        timeout=10,
    )

    print("HubSpot status code: ", response.status_code)
    print("HubSpot response: ", response.json())
    
    #Temporary diagnostic prints to investigate write failure
    print("Request URL:", response.request.url)
    print("Authorization header present:", "Authorization" in response.request.headers)
    print("Request method:", response.request.method)

def main():
    # Load the sample ecommerce data from JSON.
    with open("sample_data/order.json") as file:
         data = json.load(file)
    #Separate the two main business objects
    customer = data["customer"]
    order = data["order"]

    # Transform customer data into HubSpot-style field names
    hubspot_customer = transform_customer(customer)
    hubspot_order = transform_order(order)
    
    print("Transformed customer: ",hubspot_customer)
    print("Transformed order: ",hubspot_order)
    
    create_hubspot_contact(hubspot_customer)
              
if __name__ == "__main__":
    main()
