--Написать запрос, который посчитает сумму продаж по 100му магазину за 1 января 2013 года.


with
t1 as (
    select art, max(price) as max_price
    from price
    group by art
),
t2 as (
    select *
    from sales
    where datetime::date = '2013-01-01'
        and shop = 100
)

select t2.shop, sum(t2.quantity * t1.max_price) as total_sales
from t2
join t1
    using(art)
GROUP BY t2.shop


