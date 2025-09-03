--Задача 1
--Вам дана таблица app_events , содержащая события в мобильном приложении.
--Таблица имеет следующие столбцы:
--event_id' (ID события)
--user_id' (ID пользователя)
--event_type (тип события, например 'login', 'transfer', 'payment")
--event_time (время события)
--
--Используя ту же таблицу app events, найдите пользователей,
--которые совершали больше всего logins в течение последнего месяца
--и ранжируйте их по количеству логинов.

with
last_month as (
    select date_trunc('month', max(event_time)) as last_month
    from app_events
),
last_month_logins as (
    select *
    from app_events
    where event_type = 'login' and
          date_trunc('month', event_time) = (select last_month from last_month)
)

select user_id, count(*) as count_user_logins
from last_month_logins
group by user_id
order by count(*) desc;


--Используя таблицу app_events, найдите среднее время между логинами
--для каждого пользователя за последние три месяца и вычислите медиану времени
--между логинами по всем пользователям.


with
last_3_month_logins as (
    select *
    from app_events
    where event_time <= current_date - interval '3 months' and
         event_type = 'login'
),
login_diff as (
    select user_id, event_time,
            lag(event_time) over(partition by user_id order by event_time) as prev_login_time
    from last_3_month_logins
),
login_interval as (
    select user_id, event_time, prev_login_time,
       (event_time - prev_login_time) as login_interval
    from login_diff
    where prev_login_time is not null
)

-- найдите среднее время между логинами
--для каждого пользователя за последние три месяца

select user_id, event_time, prev_login_time,
       avg(event_time - prev_login_time) as avg_login_interval
from login_diff
where prev_login_time is not null
group by user_id;


-- вычислите медиану времени
-- между логинами по всем пользователям.

select percentile_cont(0.5) within group (order by login_interval) as median_time_between_logins
from login_interval
