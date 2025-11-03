--Задача 1

--create table orders (
--    created_date date ,
--    store_id string ‚
--    order_id string,
--    client_id string,
--    order_sum float
--)
--
--create table cities (
--    store_id string,
--    city string
--)

--вывести id заказов клиента с наибольшей суммой заказов
--- среди клиентов, совершивших первый заказ до июля 2024 г. в городе Москва

with
t as (
    select o.*, c.city
    from orders o
    join cities c
        using (store_id)
),
first_order as (
select client_id
from
    (select client_id, city, created_date,
            row_number() over(partition by client_id  order by created_date, order_id) as rn
    where o.created_date < date '2024-07-01') as t1
where rn=1
      and c.city = 'Москва'
),
client_total_sum as (
    select client id,
            sum(order_sum) over(partition by client_id) as client_total_sum
    from t
    where client id in (select client_id from first_order)
),
max_total_sum as (
    select client_id, client_total_sum
    from client_total_sum
    order by client_total_sum desc
    limit 1;
)

select client_id, order_id
from t
where client_id in (select client id from max_total_sum)
order by order_id




--Задача 2
--
--АВС анализ позволяет оценить наиболее важные товары с точки зрения их вклада в выручку компании.
--В категорию "А" попадают самые значимые товары, продажи которых составляют 80% от общей выручки,
--в категорию "В" - 15%, в категорию "с" - 5%. Необходимо вывести id товаров категории "А"
--за последние 4 недели.
--
--create table orders_art (
--    created_date date,
--    order_id string ,
--    art_id string,
--    qnty float,
--    price float)


with
t as (
    select *
    from orders_art
    where created_date >= current_date - interval '4 weeks'
),
art_revenue as (
    select art_id,
            sum(qnty*price) as art_revenue
    from t
    group by art_id
),
cum_revenue as (
    select  art_id, art_revenue,
            sum(art_revenue) over() as total_revenue,
            sum(revenue) over (order by revenue desc, art_id ) as cum_revenue
            --накопленная выручка включая текущий товар.

    from art_revenue
)

select art_id
from cum_revenue
where cum_revenue * 1.0 / nullif(total_rev, 0) <= 0.80
order by revenue desc, art_id;