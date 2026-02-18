--1
--сколько клиентов видели рекламу не менее 2 раз


select count(*) as clients_2plus_shown
from (
    select
        id,
        count(*) filter (where event = 'shown') as shown_cnt
    from events
    group by id
) t
where shown_cnt >= 2;


--2
--сколько показов и кликов

select
    count(*) filter (where event = 'shown') as total_shown,
    count(*) filter (where event = 'started') as total_started
from events;



--конверсия клики / показы
with
s as (
    select
        count(*) filter (where event = 'shown') as total_shown,
        count(*) filter (where event = 'started') as total_started
    from events
)

select
    total_shown,
    total_started,
    total_started * 1.0 / nullif(total_shown, 0) as ctr
from s;






--сколько продаж в течение 4 дней после клика (last click, одна продажа = один учёт)

with
last_click as (
    select
        s.id,
        s.ts as sale_ts,
        max(e.ts) as last_click_ts
    from sales s
    join events e
      on e.id = s.id
     and e.event = 'started'
     and e.ts <= s.ts
    group by s.id, s.ts
)
select count(*) as attributed_sales
from last_click
where sale_ts <= last_click_ts + interval '4 days';


--