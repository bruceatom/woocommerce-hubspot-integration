# Design Decisions

## Customer identity
HubSpot Contacts are matched by email before creation to prevent duplicate Contacts.

## Order identity
WooCommerce Order ID is preserved as the external Order ID. Existing HubSpot Orders 
are checked before creation.

## Buyer vs recipient
The buyer and shipping recepient are not assumed to be the same person. In the sample scenario, Jane Smith buys a gift that is shipped to Michael Smith.

# Buyer association
The purchasing customer is associated with the HubSpot Order as the Billing Contact. Shipping recipients are not automatically
created as Contacts.

## HubSpot objects
Customers map to HubSpot Contacts.
Ecommerce orders map to native HubSpot Orders.
Purchased products will map to HubSpot Line Items.

## Order status
WooCommerce 'processing' maps to the HubSpot "Open" Order status because the order has not yet shipped or been completed.

## Project structure
'main.py' orchestrates the integration
'transforms.py' handles data transformation
'hubspot_client.py' handles HubSpot API operations.
'experiments/' preserves API discovery prototypes. 



