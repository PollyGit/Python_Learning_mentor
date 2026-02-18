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

with
cogort as (
    select user_id,
        min(date_trunc('week', ts)::date) as cohort_week
    from event_log
    where event_name='Install'
    group by user_id
),
cogort_size as (
    select cohort_week,
        count(*) as cohort_size
    from cogort
    group by cohort_week
),
activity as (
    select distinct
        user_id,
        date_trunc('week', ts)::date as activity_week
    from event_log
    where event_name = 'Consultation'
),
cohort_activity as (
    select a.user_id, c.cohort_week, a.activity_week,
        ((a.activity_week - c.cohort_week) / 7)::int as week_index
    from cogort as c
    join activity  as a
    using(user_id)
)

select ca.cohort_week, ca.week_index, cs.cohort_size,
    count(distinct ca.user_id) as active_users,
    count(distinct ca.user_id) * 1.0/ nullif(cs.cohort_size, 0) as retention
from cohort_activity as ca
join cogort_size as cs
on cs.cohort_week = ca.cohort_week
group by  ca.cohort_week, ca.week_index, cs.cohort_size
order by ca.cohort_week, ca.week_index;




















--
