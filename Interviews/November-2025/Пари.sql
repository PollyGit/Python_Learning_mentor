----1
--категория А - 80% от общей выручки
--категория В - 15% от общей выручки
--категория С - 5% от общей выручки
--
--вывести ид товаров категории А

with
revenue as (
    select
        sum(qnty * price) as revenue_total
    from orders_art
    where created_date >= current_date - interval '4 weeks'
),
revenue_id as (
    select art_id,
        sum(qnty * price) as revenue_id
    from orders_art
    where created_date >= current_date - interval '4 weeks'
    group by art_id
),
share as(
    select t1.art_id, t1.revenue_id * 100 / nullif(t2.revenue_total, 0) as share,
     t2.revenue_total
    from revenue_id t1
    cross join revenue as t2
),
cumsum as (
    select art_id,
           sum(share) over(order by share desc) as cumsum
    from share
)

select art_id
from cumsum
where cumsum <= 80











--