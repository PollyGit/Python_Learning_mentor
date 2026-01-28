--1
-- Таблица reports_stg.watch_content (таблица с просмотрами видео):
user_id    video_id    date
=================================
1          1           2021-01-01
1          2           2021-01-01
1          3           2021-02-15
2          1           2019-12-31
2          2           2020-07-01
3          4           2022-12-10
4          1           2022-12-11
5          1           2021-01-01
5          3           2021-02-15
               ...
-- Поля:
-- user_id - идентификатор пользователя
-- video_id - идентификатор просмотренного видео
-- date - дата просмотра видео
-- Примечание: 1 строка в таблице - 1 просмотр видео

-- ## ЗАДАЧА:
-- Вывести список пользователей, смотревших video_id 1 и 3 (посмотрел и видео 1, и видео 3), но не смотревших 2

(
    select distinct user_id
    from reports_stg.watch_content
    where video_id = 1
)
intersect
(
    select distinct user_id
    from reports_stg.watch_content
    where video_id = 3
)
except
(
    select distinct user_id
    from reports_stg.watch_content
    where video_id = 2
);


-- or

select user_id
from reports_stg.watch_content
group by user_id
having sum(case
           when video_id = 1 then 1 else 0 end) >= 1
       and sum(case
           when video_id = 3 then 1 else 0 end) >= 1
       and sum(case
           when video_id = 2 then 1 else 0 end) = 0


-- or

with
watched as (
    select user_id,
        max(case when video_id = 1 then 1 else 0 end) as watched_1,
        max(case when video_id = 3 then 1 else 0 end) as watched_3,
        max(case when video_id = 2 then 1 else 0 end) as watched_2
    from reports_stg.watch_content
    group by user_id
)

select user_id
from watched
where watched_1 = 1
  and watched_3 = 1
  and watched_2 = 0;


--2

-- Таблица raw.orders (таблица с покупками товаров по датам):
user_id         transaction_datetime        item_id     order_id
============================================================================
6500013827      01.03.2021 10-45-59         9224        561321
6500013827      10.04.2021 12-36-45         4504        465456
6500013827      16.04.2021 11-47-41         5794        654567
1813578445      16.04.2021 09-42-41         8174        621563
1813578445      25.03.2021 20-11-21         8152        452135
1813578445      25.03.2021 20-11-21         3516        452135
1813578445      25.03.2021 20-11-21         5429        452135
2923870261      03.06.2021 10-29-56         5407        784521
2923870261      03.06.2021 10-29-56         6100        784521
2923870261      25.08.2021 12-20-07         2791        425987
8592660637      26.10.2021 15-01-44         6468        126549
2917355039      06.01.2022 21-02-37         3931        148635
5343310807      19.03.2021 18-10-18         5638        578913
5343310807      06.04.2021 17-01-42         4439        685547
                                ...
-- Поля:
-- user_id - идентификатор пользователя
-- transaction_datetime - дата и время покупки (для одного пользователя не может быть два заказа в одно и тоже время)
-- item_id - id товара
-- order_id - id покупки

-- Таблица dicts.items (словарь соответствия id товара и наименование бренда, наименования товара):
item_id     brand     name                  price
==================================================
8509        apple     macbook pro 16        350100
1873        apple     macbook pro air       237000
3092        samsung   Galaxy Watch          44990
8460        sony      Sony Bravia           207000
4051        dyson     Dyson Airwrap         89999
                ...

-- ## ЗАДАЧА
-- Для каждого пользователя вывести наименование и цену самого дорогого товара в его первой транзакции.
-- Поля в аутпут-таблице:
-- - user_id
-- - name
-- - price

with
rn as (
    select user_id, item_id,  transaction_datetime,
    rank() over(partition by user_id order by transaction_datetime) as rn
    from raw.orders
),
filtered as (
    select *
    from rn
    where rn = 1
),
prices as (
    select f.user_id, d.price, d.name,
    row_number() over (partition by f.user_id order by d.price desc) as price_rn
    from filtered f
    join dicts.items d
        using(item_id)
)

select user_id, name, price
from priced
where price_rn = 1;



-- или

with
tmp as (
    select r.user_id,
        i.name,
        i.price,
        row_number() over (partition by user_id order by transaction_datetime asc, price desc) as rn
    from raw.orders r
    join dicts.items i
    on r.item_id = i.item_id
)
select user_id, name, price
from tmp
where rn = 1



--3
-- Таблица raw.orders (таблица с покупками товаров по датам):
user_id         transaction_datetime        item_id     order_id
============================================================================
6500013827      01.03.2021 10-45-59         9224        561321
6500013827      10.04.2021 12-36-45         4504        465456
6500013827      16.04.2021 11-47-41         5794        654567
1813578445      16.04.2021 09-42-41         8174        621563
1813578445      25.03.2021 20-11-21         8152        452135
1813578445      25.03.2021 20-11-21         3516        452135
1813578445      25.03.2021 20-11-21         5429        452135
2923870261      03.06.2021 10-29-56         5407        784521
2923870261      03.06.2021 10-29-56         6100        784521
2923870261      25.08.2021 12-20-07         2791        425987
8592660637      26.10.2021 15-01-44         6468        126549
2917355039      06.01.2022 21-02-37         3931        148635
5343310807      19.03.2021 18-10-18         5638        578913
5343310807      06.04.2021 17-01-42         4439        685547
                                ...
-- Поля:
-- user_id - идентификатор пользователя
-- transaction_datetime - дата и время покупки (для одного пользователя не может быть два заказа в одно и тоже время)
-- item_id - id товара
-- order_id - id покупки
-- ЗАДАЧА:
-- На основе данных о покупках вывести:
--  1 - размерт когорт по месяцам
--  2 - ретеншен 2-го месяца
-- Когорта - это множество пользователей, объединенных первой датой покупки.



with
--первый месяц покупки пользователя
tmp_first AS (
    select
        user_id,
        min(transaction_datetime) as first_dt,              -- первая покупка
        date_trunc('month', min(transaction_datetime))::date as cohort_month
    from raw.orders
    group by user_id
),
--размерт когорты по первому месяцу покупки
tmp_cohort_size AS (
    select
        cohort_month,
        count(*) as cohort_size           -- сколько юзеров в этой когорте
    from tmp_first
    group by cohort_month
),
--таблицa «юзер + месяц, в который он что-то покупал»
tmp_activity AS (
    select distinct
        user_id,
        date_trunc('month', transaction_datetime)::date as activity_month
    from raw.orders
),
--для каждой когорты посчитаем, сколько её пользователей покупали в следующем месяце.
--Берём юзера с его cohort_month, смотрим, есть ли у него активность в месяце cohort_month + 1 month
tmp_ret2 AS (
    select
        f.cohort_month,
        count(distinct f.user_id) as returned_2m  --считаем таких юзеров по когорте.
    from tmp_first f
    join tmp_activity a
      on a.user_id = f.user_id
     and a.activity_month = f.cohort_month + interval '1 month'   -- следующий месяц после когорты
    group by f.cohort_month
)

--размер когорты + ретеншен
select
    c.cohort_month,
    c.cohort_size,
    coalesce(r.returned_2m, 0) as returned_2m,
    coalesce(r.returned_2m, 0)::numeric / c.cohort_size as retention_2m
from tmp_cohort_size c
left join tmp_ret2 r
  on r.cohort_month = c.cohort_month
order by c.cohort_month;












--