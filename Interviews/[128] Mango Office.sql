--1
--Скока строк может быть в виде результата?

если результат rank() = 1,1,3,4,5 , то 0,
а может и = 1, 2,2,2,2,2,….18


--Задача 2
--Написать запрос который для каждого ficust_id выберет сумму
--и дату последнего платежа.
-- table t: ficust_id, fxestimated_revenue, fddate

select ficust_id, fxestimated revenue, fddate
from (
    select ficust_id, fxestimated_revenue, fddate,
           row_number() over(partition by ficust_id order by fddate desc, id desc) as rn
    from t) as t1
where rn = 1;


-- если надо найти последнюю дату и сумму за этот день:

select ficust_id, day_sum, fddate as last_day
from
    (select *,
        sum(fxestimated_revenue) over(partition by ficust_id, fddate) as day_sum,
        row_number() over(partition by ficust_id order by fddate desc) as rn
    from t) as t1
where rn = 1;

-- or
with last_day as (
    select
        ficust_id,
        max(fddate) as last_day
    from t
    group by ficust_id
)
select
    t.ficust_id,
    sum(t.fxestimated_revenue) as day_sum,
    ld.last_day
from t
join last_day ld
    on ld.ficust_id = t.ficust_id
   and ld.last_day = t.fddate
group by t.ficust_id, ld.last_day;



--