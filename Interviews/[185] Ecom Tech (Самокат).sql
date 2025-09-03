--Задача 0 (На логику):
--8 курьеров за 10 часов = 320 заказов
--сколькао  заказов вывезут 6 курьеров за 8 часов

1 курьер/час = 320/10 / 8 = 4 заказа
6*4*8 = 24*8 = 192 заказа


--Задача 1 (SQL):
--сколько строк вернется?

select *
from table
where column1 = null

Ответ: 0 строк. Тк сравнение = null всегда возвращает UNKNOWN.


--Задача 2 (SQL):
--сколько строк вернется?

select *
from t1
where null = null or
    null <> null or
    123 <> nul or
    null is null

Ответ: все строки. Тк Всё условие = TRUE:
where null = null это UNKNOWN
where    null <> null это UNKNOWN
where   123 <> nul это UNKNOWN
where   null is null это TRUE



--Задача 3 (SQL):
--create table transactions
--(
--customer_id int,
--transaction_id int,
--created_time datetime2,
--amount float
--)
--ТОП 5 кастомеров по каждому месяцу (по суммарному объему транзакций)

with
total_customer_by_month as (
    select customer_id, date_trunc('month', created_time) as month,
            sum(amount) as total_customer_by_month
    from transactions
    group by customer_id, date_trunc('month', created_time)
    )

select customer_id, date_trunc('month', created_time)
from (
    select *,
            row_number() over(partition by month order by total_customer_by_month desc) as rn
    from total_customer_by_month) as t1
where rn <= 5
order by month, rn;
