SELECT item, SUM(total_spent) AS total_revenue
FROM sales
GROUP BY item
ORDER BY total_revenue DESC
LIMIT 5;

SELECT item, SUM(quantity) AS total_quantity
FROM sales
GROUP BY item
ORDER BY total_quantity DESC
LIMIT 5;

SELECT month, month_name, SUM(total_spent) AS month_revenue
FROM sales
GROUP BY month, month_name
ORDER BY month_revenue DESC;

SELECT month, month_name, AVG(total_spent) AS avg_revenue
FROM sales
GROUP BY month, month_name
ORDER BY avg_revenue DESC;

SELECT location, SUM(total_spent) AS location_revenue
FROM sales
GROUP BY location
ORDER BY location_revenue DESC;

SELECT day_name, SUM(total_spent) AS day_revenue
FROM sales
GROUP BY day_name
ORDER BY day_revenue DESC
LIMIT 1;