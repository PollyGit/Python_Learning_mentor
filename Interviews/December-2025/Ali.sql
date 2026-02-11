--1
--Найти сотрудников, которые получают больше своих же менеджеров

select e2.fullname as manager_name, e2.salary as manager_salary, e1.fullnamw as empl_name, e1.salary as empl_salary
from employees e1
join employees e2
    on e1.manager_id = e2.id
where e1.salary > e2.salary



--2
--Для каждого юзера найти день, в который суммарные траты за год превысили 10000

with
t as (
    select *,
        sum(gmv) over(partition by date_trunc('year', order_dt), user_id order by order_dt
                        rows between unbounded preceding and current row) as sum_gmv
    from orders
),
t2 as (
    select *,
        (sum_gmv > 10000)::int as flag
    from t
)

select user_id,
    min(order_dt) filter (where flag = 1) as limit_day
from t2
group by user_id;



--3
--топ 5% пользователей по кол-ву заказов


with
t1 as (
    select user_id,
        count(*) filter (where status = 'successful') as cnt_orders
    from orders
    group by user_id
),
t2 as (
    select user_id, cnt_orders,
        ceil(count(user_id) over() * 0.05) as top_n,
        row_number() over(order by cnt_orders desc) as rn
    from t1
)

select u.name
from t2
join users u
    using(user_id)
where rn <= top_n








--