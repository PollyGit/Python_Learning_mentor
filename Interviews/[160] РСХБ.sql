--1
--Таблица заходов в мобильное приложение банка (id и dttm).
--Найти количество пользователей, которые заходили на сайт в месяц.
--Найти долю прироста заходивших на сайт пользователей от месяца к месяцу.


with
monthly_users as (
        select date_trunc('month', dttm) as month_date,
            count(distinct id) over(partition by date_trunc('month', dttm))
                                    order by dttm) as user_count
        from t
),
monthly_lag as (
   select
        month_date,
        user_count,
        lag(user_count) over (order by month_date) as prev_user_count
    from monthly_users
)

select month_date, user_count, prev_user_count
        round((user_count - COALESCE(NULLIF(prev_user_count, 0), user_count)) * 1.0
    / COALESCE(NULLIF(prev_user_count, 0), user_count) ,2) as percent_rate
from monthly_lag
order by month_date


--2
--Дана таблица транзакций (id , amt_pay, dttm)
--Нужно посчитать для каждого id сумму транзакций за последние
--7, 14, и 28 дней от расчетной даты включительно.
--Расчетная дата задана, например dt = '2024-10-20'.

with
d7 as (
    select id, sum(amt_pay) as amt_pay_7d
    from t
    where dttm::date >= date '2024-10-20' - interval '7 days'
    group by id),
d14 as (
    select id, sum(amt_pay) as amt_pay_14d
    from t
    where dttm::date >= date '2024-10-20' - interval '14 days'
    group by id),
d28 as (
    select id, sum(amt_pay) as amt_pay_28d
    from t
    where dttm::date >= date '2024-10-20' - interval '28 days'
    group by id)

select id, amt_pay_7d, amt_pay_14d, amt_pay_28d
from d7
full join d14
    using(id)
full join d28
    using(id)


-- or
SELECT id,
       SUM(amt_pay) FILTER (WHERE dttm::date BETWEEN DATE '2024-10-14' AND DATE '2024-10-20') AS amt_pay_7d,
       SUM(amt_pay) FILTER (WHERE dttm::date BETWEEN DATE '2024-10-07' AND DATE '2024-10-20') AS amt_pay_14d,
       SUM(amt_pay) FILTER (WHERE dttm::date BETWEEN DATE '2024-09-23' AND DATE '2024-10-20') AS amt_pay_28d
FROM t
GROUP BY id;



--3
--Трое аналитиков на экзамене независимо друг от друга решают одну и ту же задачу.
--Вероятности ее решения этими аналитиками равны 0,8, 0,7 и 0,6 соответственно.
--Найдите вероятность того, что хотя бы один аналитик решит задачу.

Р1(никто не решит) = (1-0.8) * (1-0.7) * (1-0.6) = 0.024
Р2(хоть кто-то решит) = 1-Р1 = 1 - 0.024 = 0.976


--4
--В трех углах равностороннего треугольника находится по роботу.
--Каждый из роботов мачинает двигаться в случайно выбранный угол по стороне треугольника
--Какова вероятность того, что ни один из роботов не столкнется с другим роботом?

Р( все роботы поедут направо) = 1/2 * 1/2 * 1/2 = 1/8
Р( все роботы поедут налево) = 1/2 * 1/2 * 1/2 = 1/8
Р = 1/8+1/8 = 1/4



--5
--Устройство, состоящее из пяти независимо работающих элементов,
--включается за время Т. Вероятность отказа каждого из мих за это
--время равна 0,4
--наити вероятность того, что откажут три элемента.

задача на биномиальное распределение:
Р = 0.4^3 * 0.6^2* С(5,3) = 0,2304



















