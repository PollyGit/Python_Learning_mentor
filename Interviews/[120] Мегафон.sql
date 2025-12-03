Задача 1 (SQL):
Найдите все ошибки в коде

WITH orders AS (
    SELECT * FROM orders o
    WHERE 1=1
        AND status = 'shipped'
        FND udt = '01-10-2024'
)

SELECT DISTINCT customer, order_id, MAX(DISTINCT end_date) FROM customer c
LEFT JOIN o
ON c.order_id = o.order_id
FULL JOIN customer_list cl
ON c.customer = cl.customer
WHERE 1=1
    OR end_date ='31-12-2999'
    AND c.udt = '01-10-2024'
    AND c.start_date ‹= '31-09-2024
GROUP BY customer DESC


SELECT DISTINCT c.customer, c.order_id, MAX(cl.end_date)
FROM customer c

AND udt = '2024-10-01'

MAX(end_date)

WHERE 1=1
    OR (end_date ='2999-12-31'
    AND c.udt = '2024-10-01'
    AND c.start date ‹= '2024-09-30')

GROUP BY c.customer, c.order_id