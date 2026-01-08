Section A: Limitations of RDBMS

    Explain why the current relational database would struggle with:

    1. Products having different attributes (e.g., laptops have RAM/processor, shoes have size/color)
        ANS:  Laptops require RAM, processor, storage while shoes need size, color, material. RDBMS forces a single products table with sparse columns (most NULL) or complex Entity-Attribute-Value (EAV) tables that destroy query performance and violate normalization. Joins across EAV tables for filtering become exponentially slow.

    2. Frequent schema changes when adding new product types
        ANS: Adding smartwatches (with heart_rate_sensor, battery_life) or furniture (with dimensions, weight_capacity) requires ALTER TABLE operations on production databases containing millions of rows. This causes downtime, locks tables, and cascades through foreign key constraints in order_items.

    3. Storing customer reviews as nested data
        ANS:  Storing reviews as separate normalized tables requires expensive multi-table JOINs for product details. A single product page needs 3-4 joins (products → order_items → orders → reviews) versus MongoDB's single document read with embedded reviews array.

Section B: NoSQL Benefits

    Explain how MongoDB solves these problems using:

    1. Flexible schema (document structure)
        ANS: Each product document has its own attributes without rigid table columns. Laptops store {ram: "8GB", processor: "M2"} while shoes contain {size: 9, color: "Black"} in the same products collection. No ALTER TABLE migrations needed – add heart_rate_sensor to smartwatches instantly.

    2. Embedded documents (reviews within products)
        ANS: Customer reviews nest directly: {name: "Samsung Galaxy", reviews: [{user: "U001", rating: 5}, {user: "U002", rating: 4}]}. Single document read loads product + all reviews vs. RDBMS 4-table JOIN. Product page renders 10x faster.

    3. Horizontal scalability
        ANS: Sharding distributes products across multiple servers by category or product_id. Add capacity linearly without downtime, unlike RDBMS vertical scaling limits. FlexiMart handles Black Friday traffic spikes seamlessly.

Section C: Trade-offs

    What are two disadvantages of using MongoDB instead of MySQL for this product catalog?

        1. Limited ACID Transactions: MongoDB provides document-level ACID but lacks multi-document transactions (pre-v4.0) or complex cross-collection consistency guarantees. Updating inventory across products and orders risks race conditions during concurrent checkouts, requiring application-level compensation logic versus MySQL's robust transaction isolation.

        2. Complex Relational Queries: No native JOINs forces denormalization or multiple queries. Product sales reports spanning products, reviews, orders require application stitching or $lookup (slow) versus MySQL's efficient multi-table JOIN. Analytics/reporting suffers compared to normalized relational designs.