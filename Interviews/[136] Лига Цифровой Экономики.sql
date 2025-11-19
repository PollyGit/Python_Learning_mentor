--1
--в таблице Т1 три записи
--В таблице Т2 четыре записи

T1 join T2 on T1.col1 = T2.col1
min: 0
max: 3*4 =12

TI left join T2 on T1.coll = T2.col1
min: 3
max: 3*4 =12

T1 full join T2 on T1.col1 = T2.col1
min: 4
max: 3*4 =12

T1 cross join T2
min: 3*4 =12
max: 3*4 =12


--Задача 2
--
--Дана таблица Т (value), выведите все повторящиеся записи.
--Т - название таблицы, value - название атрибута

T(value)
1 1 1 3 4 5 1 3

-- вывести значения, которые дублируются
select value
from T
group by value
having count(*) > 1;

select value
from (
    select value,
           row_number() over(partition by value)  as rn
    from T) as T2
where rn = 2;


--Задача 3
--вывести сотрудника и департамент, со второй максимальной зарплатой в каждом
--департаменте за апрель 2023

with
t1 as (
    select *,
          dense_rank() over(partition by empl_dep order by amount desc) as dr_salary
    from salary
    where date_part('year', value_day) = 2023
        and date_part('month', value_day) = 4
)

select empl_fio, empl_dep
from t1
where dr = 2



--Задача 4
--Имеется таблица с продажами по регионам. Данные в таблицу вносятся вручную,
--поэтому возможны дефекты написания регионов. Учтите это при выполнении задачи
--- регионы нужно привести к единому виду.

--Структура таблицы sales:
--id - номер чека, value_day - дата продажи, region - регион, total_price - сумма чека)

--Выведите поквартальную статистику продаж в разрезе регионов:
--1. Объем продаж (руб)
--2. Кол-во продаж (шт)
--3. Средний чек (руб)
--4. Максимальный чек (руб)
--5. Медианный чек (руб)
--6. Среднее кол во продаж в день (шт)
--7. максимальный дневной обьем продаж (руб)

with
norm as (
    select id, value_day, total_price,
            case
            when lower(region) like '%москва%' then 'Москва'
            when lower(region) like '%московск%' then 'Московская обл'
            when lower(region) like '%санкт%' then 'Санкт-Петербург'
            when lower(region) like '%тульская%' then 'Тульская обл'
            when lower(region) like '%тверская%' then 'Тверская обл'
            else region
            end as region,
            date_trunc('quarter', value_day)::date as quarter_start
    from sales
),
-- 2) Метрики по чекам (1–5) в разрезе регион×квартал
count1_5 as (
select region,
       quarter_start,
       sum(total_price) as revenue,
       count(*) as count_sales,
       avg(total_price) as avg_check,
       max(total_price) as max_check,
       percentile_cont(0.5) within group (order by total_price) as median_check
from norm
group by region
),
-- 3) Дневная статистика в квартале (для 6 и 7)
daily_stats as (
select region, quarter_start, value_day,
       count(*) as day_sales_cnt,
       sum(total_price) as day_revenue
from norm
group by region, quarter_start, value_day
),
count6_7 as (
    select region, quarter_start,
            avg(day_sales_cnt) as avg_sales_per_day,
            max(day_revenue) as max_day_revenue
    from daily_stats
    group by region, quarter_start
)

select    t1.quarter_start,
          t1.revenue,
          t1.sales_cnt,
          t1.avg_check,
          t1.max_check,
          t1.median_check,
          t2.avg_sales_per_day,
          t2.max_day_revenue
from count1_5 as t1
join count6_7 as t2
    on t1.region = t2.region
    and t1.quarter_start = t2.quarter_start
order by t1.region, t2.quarter_start;







--