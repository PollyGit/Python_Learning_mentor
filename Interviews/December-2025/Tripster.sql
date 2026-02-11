--1
with
rn_inst as (
    select *,
        row_number() over(partition by user_id order by event_time) as rn_install
    from events
    where event_type = 'install'
),
t1 as (
    select user_id, event_time::date as event_date, event_type
    from rn_inst
    where rn_install = 1
),
rn_purch as (
    select *,
        row_number() over(partition by user_id order by event_time) as rn_purchase
    from events
    where event_type = 'purchase'
),
t2 as (
    select user_id, event_time::date as event_date, event_type, revenue
    from rn_purch
    where rn_purchase = 1
)

    select t1.user_id,
            coalesce(t2.revenue, 0) as first_purch_revenue,
        case
        when t2.event_date is not null
        then t2.event_date - t1.event_date
        else null
        end as days_to_pay
    from t1
    left join t2
        using (user_id)


--2




with
users_with_3p as (
    select user_id
    from events
    where event_type = 'purchase'
    group by user_id
    having count(*) >= 3
),
purchases as (
    select user_id, event_time,
        lag(event_time, 1) over(partition by user_id order by event_time) as prev_time
        --extract(epoch from (event_time - lag(event_time, 1) over(partition by user_id order by event_time))) / 3600 / 24 ::integer as days_left
    from events
    where event_type = 'purchase'
        and user_id in (select user_id from users_with_3p)
),
gaps as (
    select user_id,
        ((extract(epoch from (event_time - prev_time)) / 3600 / 24))::int as days_left
    from purchases
    where prev_time is not null
),
out as (
    select user_id,
        max(days_left) as max_gap_days
    from gaps
    group by user_id
)

select user_id, max_gap_days,
    (max_gap_days > 30) as churned
--    case
--    when max_gap_days > 30
--    then TRUE
--    else FALSE
--    end as churned
from out






--