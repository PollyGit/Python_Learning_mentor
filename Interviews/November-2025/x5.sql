--3
--все клиенты с суммарным весом покупок более 2 кг за последний месяц. 1 столбец.

with
last_month as (
    select *
    from fct_sales
    where dttm::date >= current_date - interval '1 month'
        and dttm::date <  current_date
    -- or последний календарный месяц
--    where dttm >= date_trunc('month', current_date) - interval '1 month'
--        and dttm < date_trunc('month', current_date)

),
weight as (
    select l.client_id, (l.sku_cnt * d.weight) as sku_weight
    from last_month as l
    join dim_sku as d
        using(sku_id)
)

select client_id
from weight
group by client_id
having sum(sku_weight) > 2;











--