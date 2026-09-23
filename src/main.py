import json


def main():
    with open("sample_data/order.json") as file:
         order = json.load(file)
      
    customer = {
        "firstname": order["billing"]["first_name"],
        "lastname": order["billing"]["last_name"],
        "email": order["billing"]["email"],
        "woocommerce_order_id": order["id"],
        "order_total": order["total"],
        "currency": order["currency"],
    }
     
    print(customer)
              
if __name__ == "__main__":
    main()
