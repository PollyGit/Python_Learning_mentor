--# 1
--Вывести все случаи, когда в имени или в фамилии две буквы S подряд

select full_name
from full_names
where lower(full_name) like '%ss%'

-- or
select full_name
from full_names
where full_name ~* 'ss'


--# 2
--Дана таблица order, в которой хранятся заказы пользователей. Внутри нее есть поля:
--
--- order id (идентификатор заказа),
--- user id (идентификатор пользователя),
--- order_sum (сумма заказа),
--- order_success (успешность заказа),
--- country_id (идентификатор страны)
--
--Нужно получить таблицу с полями user_id, country_id, вклад пользователя в выручку в каждой стране. В выручку входят только заказы с флагом order_success = 1, каждый пользователь
--(user id) покупает только в одной стране (country_id)


select country_id, user_id,
       round(total_user_revenue* 100.0 / total_country_revenue, 2) as user_for_country_revenue
from
(select country_id, user_id,
       sum(order_sum) over(partition by country_id) as total_country_revenue,
       sum(order_sum) over(partition by user_id) as total_user_revenue
from "order"
where order_success = 1) as t1



