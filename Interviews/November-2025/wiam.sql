--1
--Найти TOP-5 клиентов по сумме потраченных средств за последние 6 месяцев.
--Нужно вывести:
--customer_id
--полное имя (full_nam
--email
--количество заказов (total_orders)
--общую сумму (total_spent)

with
last_6m as (
    select customer_id, sum(total_amount) as total_spent,
           count(*) as total_orders
    from orders
    where order_date >= date_trunc('month', current_date) - interval '6 month'
        and order_date < date_trunc('month', current_date)
        and status = 'done'
    group by customer_id
    order by total_spent desc
    limit 5
)

select l.customer_id, concat(c.first_name, c.last_name) as full_name,
        c.email, l.total_orders, l.total_spent
from last_6m l
join customers c
    using(customer_id)
order by l.total_spent desc;



--