import pandas as pd # type: ignore
import mysql.connector # type: ignore
import re
import os

# UPDATE PASSWORD ONLY
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Suitcase.1418',  # CHANGE THIS
    'database': 'fleximart'
}

def main():
    conn = None
    try:
        # Connect & create DB
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS fleximart")
        conn.close()
        
        # Reconnect to fleximart
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Connected")
        
        # SINGLE statements (no multi=True)
        cursor.execute("DROP TABLE IF EXISTS order_items")
        cursor.execute("DROP TABLE IF EXISTS orders") 
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS customers")
        
        cursor.execute("""
            CREATE TABLE customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                city VARCHAR(50),
                registration_date DATE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE products (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INT DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                order_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT NOT NULL,
                order_date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                KEY(customer_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE order_items (
                order_item_id INT PRIMARY KEY AUTO_INCREMENT,
                orderid INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                KEY(order_id), KEY(product_id)
            )
        """)
        conn.commit()
        print("✅ Tables created")

        # Load 10 customers manually (from raw CSV sample)
        customers_data = [
            ('Rahul', 'Sharma', 'rahul@gmail.com', '9876543210', 'Bangalore', '2023-01-15'),
            ('Priya', 'Patel', 'priya@yahoo.com', '919988776655', 'Mumbai', '2023-02-20'),
            ('Amit', 'Kumar', 'amit@gmail.com', '9765432109', 'Delhi', '2023-03-10'),
            ('Sneha', 'Reddy', 'sneha@gmail.com', '9123456789', 'Hyderabad', '2023-04-15'),
            ('Vikram', 'Singh', 'vikram@outlook.com', '09988112233', 'Chennai', '2023-05-22'),
            ('Anjali', 'Mehta', 'anjali@gmail.com', '9876543210', 'Bangalore', '2023-06-18'),
            ('Ravi', 'Verma', 'ravi@gmail.com', '919876501234', 'Pune', '2023-07-25'),
            ('Pooja', 'Iyer', 'pooja@gmail.com', '9123456780', 'Bangalore', '2023-08-15'),
            ('Karthik', 'Nair', 'karthik@yahoo.com', '9988776644', 'Kochi', '2023-09-30'),
            ('Deepa', 'Gupta', 'deepa@gmail.com', '09871234567', 'Delhi', '2023-10-12')
        ]
        
        for data in customers_data:
            cursor.execute("INSERT INTO customers (firstname, lastname, email, phone, city, registrationdate) VALUES (%s,%s,%s,%s,%s,%s)", data)
        conn.commit()
        print("✅ 10 customers loaded")

        # Load 10 products
        products_data = [
            ('Samsung Galaxy S21', 'Electronics', 45999.00, 150),
            ('Nike Running Shoes', 'Fashion', 3499.00, 80),
            ('Apple MacBook Pro', 'Electronics', 85000.00, 45),
            ('Levis Jeans', 'Fashion', 2999.00, 120),
            ('Sony Headphones', 'Electronics', 1999.00, 200),
            ('Organic Almonds', 'Groceries', 899.00, 100),
            ('HP Laptop', 'Electronics', 52999.00, 60),
            ('Adidas T-Shirt', 'Fashion', 1299.00, 150),
            ('Basmati Rice 5kg', 'Groceries', 650.00, 300),
            ('Puma Sneakers', 'Fashion', 4599.00, 70)
        ]
        
        for data in products_data:
            cursor.execute("INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s,%s,%s,%s)", data)
        conn.commit()
        print("✅ 10 products loaded")

        # Load 15 orders + items (creates data for queries)
        sales_data = [
            (1, '2024-01-15', 45999, 'Electronics', 1, 'Completed'),
            (2, '2024-01-16', 2999, 'Fashion', 2, 'Completed'),
            (1, '2024-01-18', 85000, 'Electronics', 1, 'Pending'),
            (3, '2024-01-20', 650, 'Groceries', 3, 'Completed'),
            (4, '2024-01-22', 1999, 'Electronics', 1, 'Completed'),
            (1, '2024-01-25', 45999, 'Electronics', 1, 'Completed'),
            (5, '2024-01-28', 1299, 'Fashion', 2, 'Cancelled'),
            (6, '2024-02-01', 899, 'Groceries', 5, 'Completed'),
            (7, '2024-02-05', 52999, 'Electronics', 1, 'Completed'),
            (8, '2024-02-08', 4599, 'Fashion', 1, 'Completed'),
            (1, '2024-02-12', 45999*2, 'Electronics', 2, 'Completed'),  # High spend
            (2, '2024-02-15', 3499*3, 'Fashion', 3, 'Completed'),
            (3, '2024-02-18', 1999*4, 'Electronics', 4, 'Completed'),
            (4, '2024-02-20', 650*10, 'Groceries', 10, 'Completed'),
            (1, '2024-02-25', 85000, 'Electronics', 1, 'Completed')  # Rahul high total
        ]
        
        cust_ids = [1,2,3,4,5,6,7,8,9,10] * 2  # Cycle customers
        prod_ids = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,1]  # Electronics heavy
        
        for i, (cust_idx, date, amount, cat, qty, status) in enumerate(sales_data):
            cust_id = cust_ids[i % len(cust_ids)]
            prod_id = prod_ids[i % len(prod_ids)]
            unit_price = amount / qty if qty else amount
            
            cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (%s,%s,%s,%s)",
                          (cust_id, date, amount, status))
            order_id = cursor.last_row_id
            
            cursor.execute("INSERT INTO order_items (orderid, product_id, quantity, unit_price, subtotal) VALUES (%s,%s,%s,%s,%s)",
                          (order_id, prod_id, qty, unit_price, amount))
        
        conn.commit()
        print("✅ 15 orders + items loaded")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM customers")
        print(f"🎉 Customers: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM orders")
        print(f"🎉 Orders: {cursor.fetchone()[0]}")
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("\n🚀 NOW RUN QUERIES: mysql -u root -p fleximart < business_queries.sql")

if __name__ == "__main__":
    main()
