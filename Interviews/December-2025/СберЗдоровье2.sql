--1


with
t1 as (
    select s.city, c.country_name, s."date"::date as dt, s.income
    from sales as s
    join country as c
    using(city)
),
t2 as (
    select country_name,
        sum(income) filter (where date_trunc('month',dt) = date '2022-10-01') as inc_2022,
        sum(income) filter (where date_trunc('month',dt) = date '2021-10-01') as inc_2021,
    from t1
    group by country_name
)

select country_name,
        (inc_2022 - inc_2021) *  100.0 / nullif(inc_2021, 0) as yoy_pct
from t2
order by country_name;


--2
--если в один день у пользователя было несколько like, без distinct ты получатся “дубликаты дней”,
--а нужны уникальные дни

with
days as (
    select distinct  --оставь только уникальные комбинации (user_id, log_type, d)
        user_id,
        log_type,
        ts::date as d
    from events
),
marked as (
    select user_id,
        log_type,
        d,
        case
            when d = lag(d) over (partition by user_id, log_type order by d) + 1 then 0
            else 1
        end as is_new_block
    from days
),
-- ранжирование по группам
grp as (
    select user_id,
        log_type,
        d,
        sum(is_new_block) over (
            partition by user_id, log_type
            order by d
            rows between unbounded preceding and current row
        ) as block_id
    from marked
)

select user_id,
    log_type,
    min(d) as start_date,
    max(d) as end_date,
    (max(d) - min(d) + 1) as length
from grp
group by user_id, log_type, block_id
having (max(d) - min(d) + 1) >= 3
order by user_id, log_type, start_date;



--3

with
t1 as (
    select store,
    sum(amount*price) as total_sum,
    sum(price * amount) / nullif(sum(amount), 0) as avg_price_weighted,
    --avg(price) as avg_price,
    count(distinct item) as cnt_uniq_items
    from t
    group by store
)

select *
from t1
order by store;


--4
--маркетолог запустил новый платный канал и через месяц спрашивает «оставляем или нет»


Канал оставляем, если он даёт положительную инкрементальную прибыль:
LTV > CAC  , где

CAC = расходы канала / число привлечённых.
LTV по когортам этого канала (хотя бы 30/60 дней + прогноз хвоста).














--