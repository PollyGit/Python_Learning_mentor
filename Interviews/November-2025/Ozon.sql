--1

with
agg as (
select client_id, date_trunc('month', report_date) as report_date,
        sum(txn_amount) filter (where txn_type = 'debit') as debit_amount,
        sum(txn_amount) filter (where txn_type = 'credit') as credit_amount,
        max(report_date) as last_date
from vsp_oper_data
group by client_id, date_trunc('month', report_date)
)

select a.client_id, a.report_date, a.debit_amount, a.credit_amount, max(v.vsp_number) as last_vsp
from agg a
join vsp_oper_data v
    on a.client_id = v.client_id
    and a.last_date = v.report_date
group by a.client_id, a.report_date, a.debit_amount, a.credit_amount


--2

with
client_m as (
    select client_id,
            date_trunc('month', report_date) as report_date,
            sum(txn_amount) filter (where txn_type = 'debit') over(
                partition by client_id, date_trunc('month', report_date)) as client_m_sum
    from vsp_oper_data
),
with_totals as (
    select client_id, report_date, client_m_sum,
        sum(client_m_sum) over (partition by report_date) as total_m_sum
    from client_m
)

select client_id, report_date,
        round( client_m  * 1.0 / nullif(total_m_sum, 0), 2) as ratio
from with_totals
order by report_date, client_id


--3
конверсия = clicks / views можно по событиям или по уник юзерам
показы (impressions) — события view этого виджета на /catalog
клики — события click по этому же виджету

events(
  user_id,
  event_time   -- timestamp
  event_type   -- 'view' / 'click'
  widget_id,
  page_path    -- '/catalog' и т.п.
)

with
widget_events as (
    select event_time::date as report_date,
           event_type
    from events
    where widget_id = 522955
      and page_path = '/catalog'
)

select report_date,
    count(*) filter (where event_type = 'view')  as views,
    count(*) filter (where event_type = 'click') as clicks,
    round(
        100.0 * count(*) filter (where event_type = 'click')
        / nullif(count(*) filter (where event_type = 'view'), 0),
        2
    ) as conversion_pct
from widget_events
group by report_date
order by report_date;



--4
--Найти клиентов, которые покупали билет в театр, но не в кино


select distinct client_id
from t
where event_type = 'театр'

except

select distinct client_id
from t
where event_type = 'кино'



-- or
--select client_id
--from t
--group by client_id
--having
--    sum(case when event_type = 'театр' then 1 else 0 end) > 0   -- был театр
--    and
--    sum(case when event_type = 'кино'  then 1 else 0 end) = 0;  -- не было кино



--Найти клиентов, у которых первый билет куплен в театр, а последний - в кино

with
rn as (
select client_id, event_type,
    row_number() over(partition by client_id order by purchase_date) as rn_first,
    row_number() over(partition by client_id order by purchase_date desc ) as rn_last
from t
)

select client_id
from rn
where rn_first = 1
        and event_type = 'театр'

except

select client_id
from rn
where rn_last = 1
        and event_type = 'театр'


-- or
--intersect
--
--select client_id
--from rn
--where rn_last = 1 and event_type = 'кино';






--