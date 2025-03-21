CREATE TABLE public.Order (
    order_row_id SERIAL PRIMARY KEY,
    order_id VARCHAR(50),
    order_date text,
    ship_date text,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    region VARCHAR(50)
);


CREATE TABLE public.OrderDetail (
    order_detail_row_id SERIAL PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    sales NUMERIC(10,5),
    discount NUMERIC(5,2),
    profit NUMERIC(10,5)
);


CREATE TABLE public.Customer (
    customer_row_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20)
);


CREATE TABLE public.Product (
    product_row_id SERIAL PRIMARY KEY,
    product_id VARCHAR(50),
	product_name VARCHAR(255),
    category VARCHAR(50),
    sub_category VARCHAR(50)
);


'''DROP TABLE public.temp_import, public.salesperson, public.return CASCADE;'''

CREATE TABLE public.Return (
    order_id VARCHAR(50),
    returned BOOLEAN
);



CREATE TABLE public.Salesperson (
    region VARCHAR(50) PRIMARY KEY,
    person VARCHAR(100)
);


ALTER TABLE public.Order
ALTER COLUMN order_date TYPE DATE USING TO_DATE(order_date, 'MM/DD/YYYY'),
ALTER COLUMN ship_date TYPE DATE USING TO_DATE(ship_date, 'MM/DD/YYYY');


--return rate by product and region
SELECT o.region, p.category, COUNT(distinct r.order_id ) * 100.0 / COUNT(distinct od.order_id) AS return_rate
FROM public.OrderDetail od
JOIN public.Order o ON od.order_id = o.order_id
JOIN public.Product p ON od.product_id = p.product_id
LEFT JOIN public.Return r ON o.order_id = r.order_id
GROUP BY o.region, p.category
ORDER BY o.region, return_rate DESC;


--first 5 customers who order the most each region
select region, customer_name, total_orders
from(
SELECT o.region, c.customer_name, COUNT(distinct o.order_id) AS total_orders, row_number() over (partition by region order by COUNT(distinct o.order_id) desc) as rk
FROM public.order o
JOIN Customer c ON o.customer_id = c.customer_id
GROUP BY o.region, c.customer_name
ORDER BY o.region, total_orders DESC) a
where rk<=5
;


--first 3 popular products each region
WITH ProductSales AS (
    SELECT o.region, p.product_name, COUNT(distinct od.order_id) AS order_count, row_number() over (partition by region order by COUNT(distinct od.order_id) desc) as rk
    FROM public.OrderDetail od
    JOIN public.Product p ON od.product_id = p.product_id
    JOIN public.Order o ON od.order_id = o.order_id
    GROUP BY o.region, p.product_name)

SELECT region, product_name, order_count
FROM ProductSales
WHERE rk<=3
ORDER BY region;

