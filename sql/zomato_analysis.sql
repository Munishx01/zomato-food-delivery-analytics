-- Zomato Food Delivery Analytics | SQLite dialect (tables loaded by python/run_sql_validation.py)
-- Tables: orders(order_id, order_timestamp, restaurant_id, cuisine, payment_mode, order_status,
--         item_quantity, order_amount, discount, delivery_fee, packaging_fee, tax, delivery_vehicle_id)
--         restaurants(restaurant_id, restaurant_name, restaurant_type, city, area, primary_cuisine, restaurant_rating)
-- SQLite notes: strftime() for dates; PostgreSQL equivalent is date_trunc('month', ...).

-- 1. KPI summary
SELECT ROUND(SUM(order_amount),2) total_order_amount, SUM(item_quantity) total_items,
       ROUND(SUM(discount),2) total_discount, ROUND(SUM(delivery_fee),2) total_delivery_fee,
       ROUND(SUM(packaging_fee),2) total_packaging_fee, ROUND(SUM(tax),2) total_tax,
       COUNT(DISTINCT order_id) total_orders
FROM orders;

-- 2. Cuisine-wise order amount
SELECT cuisine, ROUND(SUM(order_amount),0) total_amount FROM orders GROUP BY cuisine ORDER BY total_amount DESC;

-- 3. City-wise restaurant count and average rating
SELECT city, COUNT(*) restaurants, ROUND(AVG(restaurant_rating),2) avg_rating
FROM restaurants GROUP BY city ORDER BY restaurants DESC;

-- 4. Monthly distinct delivery vehicles (vehicle count)
SELECT strftime('%Y-%m', order_timestamp) month, COUNT(DISTINCT delivery_vehicle_id) vehicles
FROM orders GROUP BY month ORDER BY month;

-- 5. Payment mode distribution (% of orders)
SELECT payment_mode, COUNT(*) orders,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) pct_orders
FROM orders GROUP BY payment_mode ORDER BY orders DESC;

-- 6. Order status: orders vs item quantity
SELECT order_status, COUNT(*) orders, SUM(item_quantity) items FROM orders GROUP BY order_status;

-- 7. Restaurant-type rating comparison
SELECT restaurant_type, ROUND(AVG(restaurant_rating),2) avg_rating, COUNT(*) restaurants
FROM restaurants GROUP BY restaurant_type ORDER BY avg_rating DESC;

-- 8. Top 10 restaurants by delivered revenue (window RANK)
WITH r AS (
  SELECT s.restaurant_name, s.city, SUM(o.order_amount) revenue
  FROM orders o JOIN restaurants s USING (restaurant_id)
  WHERE o.order_status = 'Delivered' GROUP BY s.restaurant_id)
SELECT RANK() OVER (ORDER BY revenue DESC) rnk, restaurant_name, city, ROUND(revenue,0) revenue
FROM r ORDER BY rnk LIMIT 10;

-- 9. Monthly revenue with month-over-month change (CTE + LAG)
WITH m AS (SELECT strftime('%Y-%m', order_timestamp) month, SUM(order_amount) revenue FROM orders GROUP BY month)
SELECT month, ROUND(revenue,0) revenue,
       ROUND(100.0*(revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month),1) mom_pct
FROM m ORDER BY month;

-- 10. Cancellation rate and average order value
SELECT ROUND(100.0*SUM(CASE WHEN order_status='Cancelled' THEN 1 ELSE 0 END)/COUNT(*),2) cancellation_rate_pct,
       ROUND(SUM(order_amount)/COUNT(DISTINCT order_id),2) avg_order_value
FROM orders;

-- 11. Data-quality checks (all should return 0 on cleaned data)
SELECT COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_ids FROM orders;
SELECT COUNT(*) AS orphan_orders FROM orders o LEFT JOIN restaurants r USING (restaurant_id) WHERE r.restaurant_id IS NULL;
SELECT COUNT(*) AS negative_amounts FROM orders WHERE order_amount < 0 OR discount > order_amount;
