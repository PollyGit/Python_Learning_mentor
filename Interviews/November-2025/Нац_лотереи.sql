--1

with
orders_filtered as (
    select order_id, ord_datetime, ord_an
    from orders
    where ord_datetime >= '2024-08-05'
        and ord_datetime < '2024-08-05' + interval '7 days'
)

select distinct
    a.an_id, a.an_name, a.an_price
from orders_filtered o
inner join analysis a
    on o.ord_an = a.an_id;


--2
with
t as (
    select o.order_id, o.ord_datetime, o.ord_an, a.an_group_id
    from orders o
    inner join analysis a
        on o.ord_an = a.an_id
)
by_month as (
select an_group_id,
        date_trunc('month', ord_datetime)::date as month,
        count(*) as month_cnt
from t
group by an_group_id, date_trunc('month', ord_datetime)
)

select an_group_id, month_cnt, month,
    sum(month_cnt) over(partition by an_group_id order by month) as cum_cnt
from by_month
order by an_group_id, month;














--