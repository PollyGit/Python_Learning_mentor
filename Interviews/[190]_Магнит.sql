--# 1
--
--# Посчитать в одном запросе:
--# количество купленных товаров по дням,
--# размер аудитории (кол-во уникальных пользователей по дням),
--# полученную таблицу отсортировать по дате

select date, count(item_id), count(distinct user_id)
from orders
group by date
order by date


--# 2
--# Вывести список пользователей, купивших item id 1 и 3 (купил и товар 1, и товар 3),
--# но не купивших товар 2

with
item_2 as (
    select distinct user_id
    from orders
    where item_id == 2
),
item_1 as (
    select distinct user_id
    from orders
    where item_id = 1
),
item_3 as (
    select distinct user_id
    from orders
    where item_id = 3
),
item_1_3 as (
    select user_id
    from item_1
    where user_id in ( select user_id from item_3 )
)

select user_id
from item_1_3
where user_id not in ( select user_id from item_2 )


-- or
-- Вывести список пользователей, купивших item id 1 и 3
-- но не купивших товар 2

SELECT user_id
FROM orders
WHERE item_id = 1

INTERSECT

SELECT user_id
FROM orders
WHERE item_id = 3

EXCEPT

SELECT user_id
FROM orders
WHERE item_id = 2;


-- or
select user_id
from (
    select user_id,
           count(distinct case when item_id = 1 then 1 end) as has_1,
           count(distinct case when item_id = 3 then 1 end) as has_3,
           count(distinct case when item_id = 2 then 1 end) as has_2
    from orders
    where item_id in (1, 2, 3)
    group by user_id
) t
where has_1 = 1 and has_3 = 1 and has_2 = 0;


--# 3
--Посчитать среднее количество дней между первым и вторым заказом у пользователей

with
rn_table as (
    select *,
            row_number() over(partition by user_id order by date) as rn_orders
    from (
        select distinct user_id, order_id, date
        from orders) as t1
    ),
detect_date as (
    select user_id,
            max(date) filter (where rn_orders = 2) as second_date,
            max(date) filter (where rn_orders = 1) as first_date
    from rn_table
    group by user_id
    having count(*) >= 2
)

select avg(second_date - first_date) as avg_days
from detect_date

