Section 1: Schema Overview

FACT TABLE: fact_sales
Grain: One row per product per order line item
Business Process: Sales transactions

Measures (Numeric Facts):
- quantity_sold: Number of units sold
- unit_price: Price per unit at time of sale
- discount_amount: Discount applied
- total_amount: Final amount (quantity × unit_price - discount)

Foreign Keys:
- date_key → dim_date
- product_key → dim_product
- customer_key → dim_customer

DIMENSION TABLE: dim_date
Purpose: Date dimension for time-based analysis
Type: Conformed dimension
Attributes:
- date_key (PK): Surrogate key (integer, format: YYYYMMDD)
- full_date: Actual date
- day_of_week: Monday, Tuesday, etc.
- month: 1-12
- month_name: January, February, etc.
- quarter: Q1, Q2, Q3, Q4
- year: 2023, 2024, etc.
- is_weekend: Boolean

[Continue for dim_product and dim_customer]



DIMENSION TABLE: dim_product
Purpose: Product hierarchy for category/subcategory performance analysis.

Attributes:
- `product_key`: PK (INT AUTO_INCREMENT)
- `product_id`: Source system ID (VARCHAR(20))
- `product_name`: Product description (VARCHAR(100))
- `category`: 'Electronics', 'Apparel' (VARCHAR(50))
- `subcategory`: 'Smartphones', 'Laptops' (VARCHAR(50))
- `unit_price`: Average selling price (DECIMAL(10,2))

DIMENSION TABLE: dim_customer
Purpose: Customer segmentation and geographic analysis.

Attributes:
- `customer_key`: PK (INT AUTO_INCREMENT)
- `customer_id`: Source ID (VARCHAR(20))
- `customer_name`: Full name (VARCHAR(100))
- `city`: Residence city (VARCHAR(50))
- `state`: Residence state (VARCHAR(50))
- `customer_segment`: 'High Value', 'Medium', 'Low' (VARCHAR(20))

Section 2: Design Decisions

1. Why you chose this granularity (transaction line-item level)
    Line-item granularity (one row per product per order line) enables granular product-level analytics while supporting higher-level summaries. Orders often contain multiple products across categories (e.g., electronics + apparel), requiring separate fact rows for accurate revenue attribution per item. This atomic grain captures quantity_sold, total_amount precisely, powering Query 2's top-10 products and inventory tracking—impossible at coarser order-level grain which mixes categories.

2. Why surrogate keys instead of natural keys
    Surrogate keys (integer PKs) replace natural keys (VARCHAR product_id/customer_id) for performance and flexibility. They enable fast joins (INT vs. string), change data capture (SCD Type 2 via new surrogate), and decoupling from source systems. Slowly changing dimensions like product price updates create new product_key rows without breaking FK integrity.

3.How this design supports drill-down and roll-up operations
    Star schema supports drill-down/roll-up via conformed dimensions. Start at year totals (roll-up), drill to quarter→month→day using dim_date hierarchy. Cross-slice by dim_product.category or dim_customer.city simultaneously (Query 1). Aggregations use simple GROUP BY—no complex joins needed, delivering sub-second OLAP performance for FlexiMart executives.


Section 3: Sample Data Flow

Source Transaction: 
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: ₹50,000


Becomes in Data Warehouse:

fact_sales: {
    sale_key: 28415
    date_key: 20240115
    product_key: 5
    customer_key: 12
    quantity_sold: 2
    unit_price: 50000.00
    discount_amount: 0.00
    total_amount: 100000.00
}:

dim_date:{
    date_key: 20240115
    full_date: 2024-01-15
    day_of_week: Monday
    month: 1
    month_name: January
    quarter: Q1
    year: 2024
    is_weekend: FALSE
}

dim_product:{
    product_key: 5
    product_id: P001
    product_name: Laptop
    category: Electronics
    subcategory: Computers
    unit_price: 50000.00
}

dim_customer: {
    customer_key: 12
    customer_id: C001
    customer_name: John Doe
    city: Mumbai
    state: Maharashtra
    customer_segment: High Value
}

