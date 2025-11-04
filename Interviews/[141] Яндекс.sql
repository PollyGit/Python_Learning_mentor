--Задача 1
--
--Необходимо вывести данные, чтобы нарисовать распределение:
--сколько пользователей проводит на сайте Х часов

with
count_hours as (
    select id, count(*) as count_hours
    from sessions
    group by id
)

select count_hours, count(*) as count_users
from count_hours
group by count_hours
group by count_hours

--Задача 2
--Вывести любых 100 пользователей, впервые зашедших на сайт в 5 часов

with
first_hour as (
  select id, min(time) as first_time
  from sessions
  group by id
)
select id
from first_hour
where first_time = 5
limit 100;



--Задача 3
--
--В какое время наибольшее число пользователей на сайте?
--Если таких вариантов несколько, вывести все

with
per_time as (
  select time, count(*) as users_cnt
  from sessions
  group by time
)

select time
from per_time
where users_cnt = (select max(users_cnt) from per_time)


--Задача 4

select id, time, value,
    lag(value) ignore nulls over(partition by id order by time) as new_value
from sessions
order by id, time;

--or

select
  id, time, value,
  last_value(value) ignore nulls
    over (partition by id order by time) as new_value
from t
order by id, time;

