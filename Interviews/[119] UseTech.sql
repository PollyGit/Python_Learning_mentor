--1
--Посчитать денежную сумму всех заказов, созданных вчера, в разрезе города.
--Присвоить городам ранк и вывести результат по убыванию.

with
t1 as (
select order_id
from "order"
where status = 'done'
    and create_date::date = current_date - 1
),
t2 as (
select d.city,
        sum(o.qty*o.price) as sum_city
from t1
join delivery d
    using(order_id)
join order_lines o
    using(order_id)
group by d.city
)

select city, sum_city,
    dense_rank() over(order by sum_city desc) as drn
from t2
order by sum_city desc





--