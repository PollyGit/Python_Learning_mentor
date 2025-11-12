--#1
--Задача на порядок выполнения операторов в select запросе

from--join--where--group by--having--select--distinct--order by--offset--limit

--2
--найти ежемесячное процентное изменение MAU: дата | MAU | % изменения m/m


with
mau as (
    select date_trunc('month', df_date) as dt_m, count (distinct user_id) as mau
    from mytest
    group by date_trunc('month', df_date)
),
prev_m as (
    select dt_m, mau,
        lag(mau) over(order by dt_m) as prev_m
    from mau
)

select dt_m, mau,
    round((mau-prev_m) * 100.0 / nullinf(prev_m, 0), 2) as change_mau
from prev_m
order by dt_m



--3
--Как оптимизировать запрос?
--Сначала агрегировать payments, потом присоединять справочники.
--Посмотреть, нужен left join или хватит join
with
pay as (
  select p.user_id, sum(p.sumRub) as sum_rub
  from payments p
  group by p.user_id
)
select
  c.country_name,
  c.city_name,
  u.user_id,
  u.email,
  pay.sum_rub
from pay
join users  u on u.user_id = pay.user_id
join cities c on c.city_id = u.city_id;















--