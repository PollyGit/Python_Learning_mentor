--Задача 1
--Напишите  запрос, который выведет статистику по количеству покупателей,
-- привлеченных каждой маркетинговой акцией, которая есть у Вас в базе.


select ma.name_ma, count(distinct o.client_id) as buyers
from orders as o
join clients as c
    on o.client_id = c.client_id
join ma
    on c.ma_id = ma.ma_id
group by ma.name_ma


--Задача 2
--Напишите  запрос, который выведет помесячную статистику по задержанным заказам за 2006 год.

--Есть таблица Т со следующими полями Id (int) – идентификатор заказа
--Moment (datetime) – временной штамп изменения статуса
--Status (varchar (1)) – (‘a’ или ‘s’) в зависимости от статуса,
--который присвоен заказу в момент, отображенный в поле moment.
--Если этот срок прехода от статуса ‘a’ к статусу ‘s’ был больше 3 дней,
--то заказ считается задержанным. Hint: Функция datediff (dd,date1,date2)
-- возвращает разницу в днях между date1 и date2. Функция month (date1)
--  возвращает номер месяца date1. Напишите запрос, который выведет помесячную
--  статистику по задержанным заказам за 2006 год

with
date_a as (
    select id, moment as date_a
    from T
    where status = 'a' and date_part('year', moment) = 2006
    -- and year(moment) = 2006
),
date_s as (
    select id, moment as date_s
    from T
    where status = 's' and date_part('year', moment) = 2006
)

select month(date_s), count(*) as delayed_orders
from
    (
    select id, date_a, date_s,
            datediff(dd, a.date_a, s.date_s) as diff_days
    from date_a as a
    join date_s as s
        using(id)
    WHERE s.date_s > a.date_a  -- на всякий случай
    ) as T2
where diff_days > 3
group by month(date_s)
order by month(date_s)


--Задача 3
--Допустим, вы решили добавить поле, напрямую указывающее, что заказ был задержан.
--Для этого к таблице Т Вы добавили Атрибут IsDelayed (int) и хотите, чтобы
--он принимал значение 0 или 1 в зависимости от того, был задержан заказ или нет.
--Изначально поле пустое, т.е. =null
--Напишите запрос, который производит update таблицы Т и проставляет нужные значения.

with
date_a as (
    select id, moment as date_a
    from T
    where status = 'a' and date_part('year', moment) = 2006
    -- and year(moment) = 2006
),
date_s as (
    select id, moment as date_s
    from T
    where status = 's' and date_part('year', moment) = 2006
)

update T

set IsDelayed = case
    when id in (
        select a.id
        from date_a as a
        join date_s as s
            on a.id = s.id
        where DATEDIFF(dd, a.date_a, s.date_s) > 3
        )
    then 1
    else 0
    end;













