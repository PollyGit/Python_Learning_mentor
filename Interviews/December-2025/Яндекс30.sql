--1
--Нахождение даты флага

with
changes as (
    select is_active,
        msk_date,
        case
            when is_active = lag(is_active) over (order by msk_date) then 0
            else 1
        end as is_new_block
    from t
)

select is_active,
    msk_date
    from changes
where is_new_block = 1
order by msk_date;






--2
--Найти дату реактивации клиента


with
l as (
    select *,
        lag(is_active) over (order by msk_date) as prev_is_active
    from t
)

select msk_date as reactivated_date
from l
where is_active = 1
  and rev_is_active = 0
order by reactivated_date;


--3
--топ10 покупателей в 2023г у кого тотал больше 1000р и их сумму покупок

select customer_id, sum(purchase_amount) as total_2023
from t
where date_part('year', msk_date) = 2023
--where msk_date >= date '2023-01-01'
--  and msk_date <  date '2024-01-01'
group by customer_id
having sum(purchase_amount) > 1000
order by sum(purchase_amount) desc
limit 10



--4
--на каждый день итоговую сумму покупок каждого покупателя с начала каждого года

select customer_id, msk_date, date_part('year', msk_date) as d_year,
    sum(purchase_amount) over(partition by date_part('year', msk_date), customer_id order by msk_date
                                rows between unbounded preceding and current row) as cum_sum_year
from t
order by d_year, customer_id, msk_date;


--5
-- макс сумму покупки в каждом году каждым пользователем

with
t1 as (
select customer_id, msk_date, purchase_amount,  date_part('year', msk_date) as d_year,
    sum(purchase_amount) over(partition by date_part('year', msk_date), customer_id order by msk_date
                                rows between unbounded preceding and current row) as cum_sum_year
from t
order by d_year, customer_id, msk_date;
)

select d_year, customer_id, max(purchase_amount) as max_sum
from t1
group by d_year, customer_id
order by d_year, customer_id


--6
-- процент прироста  value от 2022 года к 2021 по каждому name

with
t1 as (
    select name,
        sum(value) filter (where date_part('year', date) = 2022) as total_2022,
        sum(value) filter (where date_part('year', date) = 2021) as total_2021
    from t
    where date >= date '2021-01-01'
        and date <= date '2022-12-31'
    group by name
)

select d_year, name,
    (total_2022 - total_2021) * 100.0 / nullif(total_2021) as share
from t1



--7
--найти кол-во новых пользователей, зарегистрированных в каждом месяце


select date_trunc('month', reg_date) as m_reg,
    count(*) as cnt_new_users
from table_1
group by date_trunc('month', reg_date)
order by date_trunc('month', reg_date)


-- посчитать кол-во пользователей из когорты, которые сделалаи хотя бы один зазказ в первые 30 д после регистрации

with
t2 as (
    select user_id, min(msk_date) as first_p
    from table_2
    group by user_id
)


select count(t1.user_id) as users_with_first_30d_p
from t2
join table_1 as t1
    on t1.user_id = t2.user_id
where t2.first_p >= t1.reg_date
    and t2.first_p - t1.reg_date <= interval '30 days'

















--