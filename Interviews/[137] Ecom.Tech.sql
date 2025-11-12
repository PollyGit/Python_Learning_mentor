Задача 1

Есть две таблицы:
orders: customer_id, loyalty_program_id, client_amount.
loyalty: loyalty_program_id, loyalty_name.

Нужно получить список наименований программ лояльности,
сумму продаж по ним и id клиента, принесшего большего всего денег
по этой программе лояльности.
Решить через общее табличное выражение (cte)


with
sum_am as (
    select loyalty_program_id,
           sum(client_amount) as sum_amount
    from orders
    group by loyalty_program_id
),
cust as (
    select loyalty_program_id, customer_id as max_customer_id
    from
    (select loyalty_program_id,
            sum(client_amount) as cust_amount,
           row_nuber() over(partition by loyalty_program_id order by sum(client_amount) desc, , customer_id) as rn
    from orders
    group by loyalty_program_id, customer_id
    ) t1
    where rn = 1
)

select  l.loyalty_name,
        c.max_customer_id,
        c.sum_amount
from sum_am s
join cust c
    using(loyalty_program_id)
join loyalty l
     using(loyalty_program_id)

