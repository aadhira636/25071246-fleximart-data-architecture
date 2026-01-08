-- Query 1: Customer Purchase History
-- Business Question: Generate a detailed report showing each customer's name, email, total number of orders placed, and total amount spent. Include only customers who have placed at least 2 orders and spent more than ₹5,000. Order by total amount spent in descending order.
-- Expected to return customers with 2+ orders and >5000 spent

SELECT
        CONCAT(c.firstname, ' ', c.lastname) AS customername, c.email,
        COUNT(DISTINCT o.orderid) AS totalorders, SUM(oi.subtotal) AS totalspent
        FROM customers c
        JOIN orders o ON c.customerid = o.customerid
        JOIN orderitems oi ON o.orderid = oi.orderid
        GROUP BY c.customerid, c.firstname, c.lastname, c.email
        HAVING totalorders >= 2 AND totalspent > 5000
        ORDER BY totalspent DESC;


-- Query 2: Product Sales Analysis
-- Business Question: For each product category, show the category name, number of different products sold, total quantity sold, and total revenue generated. Only include categories that have generated more than ₹10,000 in revenue. Order by total revenue descending.
-- Expected to return categories with >10000 revenue

SELECT
        p.category,
        COUNT(DISTINCT p.productid) AS numproducts,
        SUM(oi.quantity) AS totalquantitysold,
        SUM(oi.subtotal) AS totalrevenue
    FROM products p
    JOIN orderitems oi ON p.productid = oi.productid
    GROUP BY p.category
    HAVING totalrevenue > 10000
    ORDER BY totalrevenue DESC;


-- Query 3: Monthly Sales Trend
-- Business Question: Show monthly sales trends for the year 2024. For each month, display the month name, total number of orders, total revenue, and the running total of revenue (cumulative revenue from January to that month).
-- Expected to show monthly and cumulative revenue

SELECT
    MONTHNAME(o.orderdate) AS monthname,
    COUNT(o.orderid) AS totalorders,
    SUM(o.totalamount) AS monthlyrevenue,
    SUM(SUM(o.totalamount)) OVER (ORDER BY MONTH(o.orderdate)) AS cumulativerevenue
FROM orders o
WHERE YEAR(o.orderdate) = 2024
GROUP BY MONTH(o.orderdate), monthname
ORDER BY MONTH(o.orderdate);

