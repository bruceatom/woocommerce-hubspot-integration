# WooCommerce → HubSpot Integration

A Python integration that synchronizes ecommerce customer and order data into HubSpot while preserving source-system identity and preventing duplicate records.

## Business Problem

Ecommerce order data often needs to reach the CRM without manual re-entry. This project synchronizes:

- customers → HubSpot Contacts;
- purchases → native HubSpot Orders and Line Items;
- buyer/order relationships → HubSpot associations;
- source IDs and run receipts → traceability and operational visibility.

## Sample Scenario

Jane Smith places WooCommerce Order #1042 for $149.99 USD as a gift for her brother Michael.

Jane is the **buyer and billing contact**; Michael is the **shipping recipient**. The distinction is preserved rather than assuming the buyer and recipient are the same person.

## How It Works

```text
WooCommerce Order
        |
        v
Python Integration
        |
        +--> Transform source data
        +--> Find or create Contact
        +--> Find or create Order
        +--> Associate Billing Contact
        +--> Find or create Line Items
        +--> Associate Line Items with Order
        |
        v
Timestamped Run Receipt
```

## Reliability and Design Decisions

- **Duplicate-safe synchronization:** Contacts, Orders, and Line Items are checked before creation.
- **Traceability:** WooCommerce Order IDs are preserved and successful runs leave timestamped receipts.
- **Explicit business semantics:** Source statuses are deliberately mapped to HubSpot stages, and buyer vs. recipient roles remain distinct.
- **Maintainable handoff:** API operations, transformations, orchestration, and receipts are separated; significant choices are documented in `DECISIONS.md`.

The goal is a system another developer or administrator can understand, troubleshoot, and extend—not a black-box script that only its author can maintain.

## Running the Demo

After configuring the Python environment and HubSpot credentials:

```bash
python3 src/main.py
```

The demo processes `sample_data/order.json`, synchronizes it to HubSpot, and records the run locally.
