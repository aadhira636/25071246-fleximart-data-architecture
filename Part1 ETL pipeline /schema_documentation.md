<!-- schemadocumentation.md - Part 1 Schema Doc -->
Database Schema Documentation

Entity-Relationship Description
ENTITY: customers
Purpose: Stores customer information.  
Attributes: customer_id (PK), first_name, last_name, email (unique), phone, city, registration_date.  
Relationships: 1:M with orders.

ENTITY: products 
Purpose: Product catalog.  
Attributes: product_id (PK), product_name, category, price, stock_quantity.  
Relationships: 1:M with order_items.

ENTITY: orders 
Purpose: Order headers.  
Attributes: orderid (PK), customer_id (FK), order_date, total_amount, status.  
Relationships: M:1 with customers, 1:M with order_items.

ENTITY: order_items 
Purpose: Order line items.  
Attributes: order_item_id (PK), orderid (FK), product_id (FK), quantity, unit_price, subtotal.

Normalization (3NF)
The FlexiMart database design achieves Third Normal Form (3NF) by eliminating partial and transitive dependencies while preserving data integrity.

Functional Dependencies:

customer_id → first_name, last_name, email, phone, city, registration_date (customer_id fully determines all customer attributes)

order_id → customer_id, order_date, total_amount, status (orderid fully determines order details)

product_id → product_name, category, price, stock_quantity (product_id fully determines product details)

order_item_id → orderid, product_id, quantity, unit_price, subtotal (order_item_id fully determines line item)

No Partial Dependencies: All non-key attributes depend on the entire primary key, not part of composite keys. For example, in order_items, quantity depends on complete (order_item_id), not just orderid or product_id.

No Transitive Dependencies: Non-key attributes don't depend on other non-key attributes. Customer city depends directly on customer_id, not through intermediate attributes like email.

Anomaly Prevention:

Update Anomaly: Change customer phone once in customers table, not across multiple orders

Insert Anomaly: Add new products without requiring sales data

Delete Anomaly: Delete order doesn't lose customer record; delete customer doesn't lose product catalog

3NF Justification: Every non-key attribute depends solely on the primary key (1NF+2NF), and no non-key attribute depends on another non-key attribute. This design ensures data consistency, eliminates redundancy, and supports efficient querying while meeting all business requirements
