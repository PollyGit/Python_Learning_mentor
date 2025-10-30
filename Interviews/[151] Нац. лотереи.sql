--Есть таблица анализов Analysis:
--an_id - ID анализа
--an_name - название анализа
--an_cost - себестоимость анализа
--an_price - розничная цена анализа
--an_group_id - группа анализов
--
--Есть таблица групп анализов Groups:
--gr_id - ID группы
--gr_name - название группы
--gr_temp - температурный режим хранения.
--
--Есть таблица заказов Orders:
--ord_id - ID заказа
--ord_datetime - дата и время заказа
-- ord_an - ID анализа
--
--1. Вывести название и цену для всех анализов, которые продавались 5 августа 2024 и всю следующую неделю

with
orders_7d as (
    select distinct ord_an
    from orders
    where ord_datetime::date between '2024-08-05' and '2024-08-05' + interval '6 days'
    -- interval '6 days' чтоб ровно неделя была с 5 по 11
)

select a.an_id, a.an_name, a.an_price
from orders_7d as o
join analysis as a
    on o.ord_an = a.an_id

--  or
select distinct a.an_name, a.an_price
from orders o
join analysis a
     on a.an_id = o.ord_an
where ord_datetime >= timestamp '2024-08-05 00:00:00'
  and ord_datetime <  timestamp '2024-08-05 00:00:00' + interval '7 days'
order by a.an_name;


--2  Нарастающим итогом рассчитать, как увеличивалось количество проданных тестов каждый месяц каждого года с
--разбивкой по группе


select count(ord_an) over(partition by date_trunс('month', ord_datetime) order by ord_datetime) as count_month
from orders


with
order_month as (
    select date_trunс('month', o.ord_datetime)::date as date_month,
            a.an_group_id as group_id,
            count(*) as count_month
    from orders o
    join analysis a
        on a.an_id = o.ord_an
    --group by o.date_trunс('month', ord_datetime)::date, a.an_group_id
    group by 1,2
)

select g.gr_name, o.date_month, o.count_month,
        sum(o.count_month) over(partition by date_part('year', o.date_month) order by o.date_month
                                rows between unbounded preceding and current row) as count_year
from order_month o
join groups g
    on o.group_id = g.gr_id
order by g.gr_id, o.date_month;



--3
--Есть таблица балансов клиентов
--ClientBalance:
--client_id - идентификатор клиента;
--client name - ФИО клиента
--client_balance_date -дата баланса клиента
--client_balance_value - значение баланса клиента
--В данной таблице в какой-то момент времени появились полные дубли. Предложите способ для избавления от них без создания новой таблицы

-- это выбрать уникальные строки
select *
from
    (select *,
        row_number() over (partition by client_id, client name,client_balance_date, client_balance_value) as rn
    from ClientBalance) as t1
where rn = 1;


-- а чтобы удалить дубли:

with dups as (
  select ctid,
         row_number() over (
           partition by client_id, "client name", client_balance_date, client_balance_value
           order by ctid
         ) as rn
  from clientbalance
)
delete from clientbalance cb
using dups d
where cb.ctid = d.ctid
  and d.rn > 1;

-- или
-- удалить дубли вариант 2

delete from clientbalance a
using clientbalance b
where a.client_id = b.client_id
  and a.client_name = b.client_name
  and a.client_balance_date = b.client_balance_date
  and a.client_balance_value = b.client_balance_value
  and a.ctid > b.ctid;  -- удаляем дубликаты, оставляя одну запись

 -- или

 with dups as (
  select ctid,
         row_number() over (
           partition by client_id, "client name", client_balance_date, client_balance_value
           order by ctid
         ) as rn
  from clientbalance
)
delete from clientbalance
where ctid in (select ctid from dups where rn > 1);




