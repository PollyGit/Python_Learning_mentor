--1

with
filtered as (
    select *,
        row_number() over(partition by user_id order by event_time) as rn
    from user_events
    where event_type = 'registration'
        or event_type = 'first_purchase'
        or event_type = 'second_purchase'
),
rn as (
select *,
    case
    when rn = 1 and event_type = 'registration' then 1
    when rn = 2 and event_type = 'first_purchase' then 10
    when rn = 3 and event_type = 'second_purchase' then 100
    end as point
from filtered
),
-- 1) выбор соответствующих пользователей
users as (
    select user_id, sum(point)
    from rn
    group by user_id
    having sum(point) = 111
),

lagtime as (
    select user_id, event_type, event_time, rn,
    lag(event_time, 1, event_time) over(partition by user_id order by event_time) as lag_time
    from filtered
    where user_id in (select user_id from users)

),
diff as (
    select user_id, event_type, event_time, rn,
           extract(epoch from event_time - lag_time) as diff_time_sec
    from lagtime
    where rn = 2
        or rn = 3
)

select rn, avg(diff_time_sec) / 3600.0 as "среднее время между действиями в часах"
from diff
group by rn;


-- or

with tmp as (
    select
        user_id,
        min(case when event_type = 'registration'    then event_time end) as reg,
        min(case when event_type = 'first_purchase'  then event_time end) as first,
        min(case when event_type = 'second_purchase' then event_time end) as second
    from user_events
    group by user_id
),
tmp2 as (
    select
        user_id,
        first  - reg   as diff_1,
        second - first as diff_2
    from tmp
    where reg is not null
      and first is not null
      and second is not null
      and reg < first
      and first < second
)
select
    avg(diff_1) as avg_diff_1,
    avg(diff_2) as avg_diff_2
from tmp2;








--