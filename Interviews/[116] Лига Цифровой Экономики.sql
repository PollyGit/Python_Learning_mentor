
--Задача 1
--
--Даны две таблицы Т1 (col1, col2) и Т2 (col1, col3) В таблице T1 три записи
--В таблице Т2 четыре записи Оцените какое минимальное и максимальное количество строк вернут разные типы join
--при любом возможном наборе данных в (со1)

T1 join T2 on T1.col1 = T2.col1
min: 0
max: 12

T1 left join T2 on T1.col1 = T2.col1
min: 3
max: 12

T1 full join T2 on T1.col1 = T2.col1
min: 4
max: 12

T1 cross join T2
min: 12
max: 12




--Задача 2
--
--Дана таблица T(value), выведите все повторяющиеся записи

select value, count(*)
from T
group by value
having count(*) >1


Задача 3

Вывести сотрудника и департамент, со второй максимальной зарплатой (зарплата в таблице может повторятся)
в каждом департаменте за любой день апреля 2023

with
t1 as (
select *,
        dense_rank() over(partition by empl_dep order by amount desc) as dr
from salary
where date_part('year', value_day) = 2023
    and date_part('month', value_day) = 4
--    or
--    where extract(year from value_day) = 2023
--        and extract(month from value_day) = 4

)

select empl_fio, empl_dep, amount
from t1
where dr = 2;




--Задача 4
--
--Для сотрудников с минимальной зарплатой (3 минимальных значения 3П) в разрезе всей компании в мае
-- 2023 найти разницу с заплатой в предыдущем месяце. Вывести в результат: фио, разницу 3П.

with
ranked as (
    select *,
            dense_rank() over(order by amount) as rn
    from salary
    where extract(year from value_day) = 2023
        and extract(month from value_day) = 5
),
top3 as (
    select empl_fio, amount
    from ranked
    where rn < 4
),
prev as (
    select empl_fio,
        max(amount) as prev_amount
    from salary
    where value_day >= date '2023-04-01'
      and value_day <  date '2023-05-01'
    group by empl_fio
)

select t.empl_fio, t.amount - coalesce(p.prev_amount, 0) as diff_amount
from top3 t
left join prev p
    on t.empl_fio = p.empl_fio



--