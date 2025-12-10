Задача 2 (SQL):

Есть таблица table со схемой user_id, campaign, datetime,
datetime - это дата и время визита пользователя,
user_id - идентификатор пользователя,
campaign - канал привлечения.
Нужно написать запрос , чтобы построить 3 графика:
1) Когорты пользователей по дате привлечения (кол-во новых пользователей по дням).
2) Ретеншена первой недели по когортам,
те доля пользователей, которые впервые пришли в день Х, а потом повторно зашли в течение 7 дней.
3)Ретеншена первых 7 дней по каналам привлечения.


1)

with
first_day as (
    select user_id, datetime::date as dt, campaign,
           row_number() over(partition by user_id order by datetime::date) as rn
    from table
)

select dt, count(*) as user_day_cogort
from first_day
where rn = 1
group by dt
order by dt



2)

with
first_day as (
    select user_id, datetime::date as dt, campaign,
           row_number() over(partition by user_id order by datetime::date) as rn,
           first_value(datetime::date) over(partition by user_id order by datetime::date) as first_day
    from table
),
d7_retention as (
    select user_id, dt, campaign, first_day,
            dt - first_day as n_day_retention,
            case
            when dt - first_day <= 7 then 1
            else 0
            end as 7d_retention
    from first_day
    where rn = 2
),
d7_retention_count as (
    select first_day,
            sum(d7_retention) as n_user_7d_retention
    from 7d_retention
    group by first_day
),
n_user_first_day as (
    select dt, count(*) as n_user_first_day
    from first_day
    where rn = 1
    group by dt
    order by dt
)

select f.dt,
        coalesce(n_user_7d_retention* 100.0 /n_user_first_day  , 0) as retention_7d_pct
from n_user_first_day  f
left join d7_retention_count r
    on f.dt = r.first_day
group by f.dt



3)

with
-- 1. Визиты с порядковым номером и датой первого визита
visits as (
    select user_id, campaign, datetime::date as dt,
        row_number() over (partition by user_id order by datetime) as rn,
        first_value(datetime::date) over (partition by user_id order by datetime) as first_day
    from events
),
-- 2. Берём только одну строку на пользователя: его первый визит и канал привлечения
first_visit as (
    select user_id, first_day, campaign       -- канал первого визита
    from visits
    where rn = 1
),
-- 3. Считаем флаг 7-дневного ретеншена для каждого пользователя
retention_7d as (
    select f.user_id, f.campaign, f.first_day,
        case
            when exists (
                select 1
                from events e2
                where e2.user_id = f.user_id
                  and e2.datetime::date >  f.first_day
                  and e2.datetime::date <= f.first_day + interval '7 day'
            )
            then 1
            else 0
        end as retained_7d
    from first_visit f
),
-- 4. Агрегация по каналам привлечения
agg as (
    select campaign,
        count(*)                    as users_total,         -- все юзеры этого канала
        sum(retained_7d)            as users_retained_7d    -- вернувшиеся за 7 дней
    from retention_7d
    group by campaign
)

select campaign, users_total, users_retained_7d,
    round(100.0 * users_retained_7d::numeric / users_total, 2) as retention_7d_pct
from agg
order by retention_7d_pct desc;

















--