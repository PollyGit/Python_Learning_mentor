--Задача 1
--УБрать дубли

select *
from (
    select *
        row_number() over(partition by emp_id, client_id, value_day, dur) as rn
    from calls) as t
where rn = 1


--Задача 2
--Дана таблица Rates (value_day, code, rate)
--value day - дата начала действия курса
--соdе - код валюты
--rate - курс
--В таблицу вносятся данные только тогда когда курс изменяется.
--Напишите запрос, который обновляет курс валюты usd (code = 'usd’) на заданную дату (15.09.2013) с 90 на 100


update Rates
set rate = 100
where code = 'usd'
    and value_day = date '2013-09-15'
    and rate = 90

-- or

insert into Rates (value_day, code, rate)
values (date '2013-09-15', 'usd', 100)
ON CONFLICT (value_day, code) DO UPDATE
SET rate = EXCLUDED.rate;



--Задача 3
--регионы нужно привести к едному виду.

with
normal as (
    select id, value_day, total_price, region,
            case
                when lower(region) like '%москв%' then 'Москва'
                when lower(region) like '%москв%' and '%обл%' then 'Московская область'
                when lower(region) like '%санкт%' then 'Санкт-Петербург'
                when lower(region) like '%тул%' and '%обл%' then 'Тульская область'
                when lower(region) like '%твер%' and '%обл%' then 'Тверская область'
                else 'another'
            end as normal_reg

    from sales
),
reg_day_sales as (
    select normal_reg, value_day, count(*) as count_sales_day, sum(total_price) as total_sum_day
    from normal
    group by normal_reg, value_day
)


select normal_reg,
    sum(total_price) as total_sum,
    count(*) as count_sales,
    avg(total_price)  as avg_sales,
    max(total_price) as max_sales,
    percentile_cont(0.5) within group (order by c.total_price) as mediana,
    percentile_cont(0.8) within group (order by c.total_price) as 80_sales,
    max(r.total_sum_day) as max_day_sales,
    round(count(*)*1.0 / r.count_sales_day, 2) as avg_day_sales
from normal n
join reg_day_sales r
    on m.normal_reg=r.normal_reg and m.value_day=r.value_day
group by normal_reg





--Задача 5
--Выведите id подразделений в которых число сотрудников не превышает 15

select dep_id, count(distinct emp_id)
from emp
group by dep_id
having count(distinct emp_id) <= 15;


--Выведите id сотрудников с самый высокой заработной платой в своем подразделении

select dep_id, emp_id
from (
select dep_id, emp_id
       row_number() over(partition by dep_id order bu salary desc) as rns
from emp) t
where rns = 1;


--Выведите id подразделений с максимальной суммарной заработной платой "*

select dep_id, total_salary
from
    (select dep_id, sum(salary) as dep_s,
        rank() over(order by sum(salary) desc) as r_salary
    from emp
    group by dep_id) t
where r_salary =1;



