--1
--пользователи, купившие 1 и 3, но не 2

with
t as (
    select o.order_id, o.client_id, i.item_id
    from orders o
    join items i
        using(order_id)
)


select client_id
from t
where item_id = '1'

intersect

select client_id
from t
where item_id = '3'

except
select client_id
from t
where item_id = '2'

--
--2. для всех клиентов отобразить ид самого первого заказа

with
rn as (
    select client_id, order_id
    row_number() over(partition by client_id order by created_date) as rn
    from orders
)

select client_id, order_id
from rn
where rn = 1;


--3. для всех клиентов, совершивших первый заказ в г Москва до июля 2024г отобразить ид самого дорогого заказа

with
rn as (
    select o.client_id, o.order_id, o.created_date, s.city,
    row_number() over(partition by o.client_id order by o.created_date) as rn
    from orders o
    join stores s
        using(store_id)
),
first_order_clients as (
    select client_id
    from rn
    where rn = 1
        and created_date < date '2024-07-01'
        and city = 'Moscow'
),
order_totals as (
    select
        o.client_id,
        o.order_id,
        sum(i.item_cnt * i.item_cost) as order_sum
    from orders o
    join items i using (order_id)
    group by o.client_id, o.order_id
)

select client_id, order_id
        max(order_sum) as max_price
from order_totals
group by client_id

--