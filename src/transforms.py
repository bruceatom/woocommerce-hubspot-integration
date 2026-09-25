# ===============================================================================================
# 1. CUSTOMER TRANSFORMATION
# ===============================================================================================

#1.1 Convert source customer fields into HubSpot field names
def transform_customer(customer):
    return {
        "firstname": customer["first_name"],
        "lastname": customer["last_name"],
        "email": customer["email"],
        "phone": customer["phone"],
        }
        
        
# ==========================================================================================
# 2. ORDER TRANSFORMATION
# ==========================================================================================

#2.1 Convert source order fields to integration order fields
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
        
                
