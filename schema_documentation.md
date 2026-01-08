<!-- schemadocumentation.md - Part 1 Schema Doc -->
# Database Schema Documentation

## Entity-Relationship Description
**ENTITY: customers**  
Purpose: Stores customer information.  
Attributes: customerid (PK), firstname, lastname, email (unique), phone, city, registrationdate.  
Relationships: 1:M with orders.

**ENTITY: products**  
Purpose: Product catalog.  
Attributes: productid (PK), productname, category, price, stockquantity.  
Relationships: 1:M with orderitems.

**ENTITY: orders**  
Purpose: Order headers.  
Attributes: orderid (PK), customerid (FK), orderdate, totalamount, status.  
Relationships: M:1 with customers, 1:M with orderitems.

**ENTITY: orderitems**  
Purpose: Order line items.  
Attributes: orderitemid (PK), orderid (FK), productid (FK), quantity, unitprice, subtotal.

## Normalization (3NF)
The FlexiMart database design achieves Third Normal Form (3NF) by eliminating partial and transitive dependencies while preserving data integrity.

Functional Dependencies:

customerid → firstname, lastname, email, phone, city, registrationdate (customerid fully determines all customer attributes)

orderid → customerid, orderdate, totalamount, status (orderid fully determines order details)

productid → productname, category, price, stockquantity (productid fully determines product details)

orderitemid → orderid, productid, quantity, unitprice, subtotal (orderitemid fully determines line item)

No Partial Dependencies: All non-key attributes depend on the entire primary key, not part of composite keys. For example, in orderitems, quantity depends on complete (orderitemid), not just orderid or productid.

No Transitive Dependencies: Non-key attributes don't depend on other non-key attributes. Customer city depends directly on customerid, not through intermediate attributes like email.

Anomaly Prevention:

Update Anomaly: Change customer phone once in customers table, not across multiple orders

Insert Anomaly: Add new products without requiring sales data

Delete Anomaly: Delete order doesn't lose customer record; delete customer doesn't lose product catalog

3NF Justification: Every non-key attribute depends solely on the primary key (1NF+2NF), and no non-key attribute depends on another non-key attribute. This design ensures data consistency, eliminates redundancy, and supports efficient querying while meeting all business requirements
