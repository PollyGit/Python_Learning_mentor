--Таблица пользователей:
CREATE TABLE users [
user_id INT PRIMARY KEY,
created_at DATE,
country TEXT
);
-- события в приложении
CREATE TABLE events (
user_ id INT,
event_ date DATE,
event_name TEXT,   -- "app_open', 'view_product', ...
revenue NUMERIC   -- NULL, кроме события 'purchase'
);
-- заказы
CREATE TABLE orders (
order_id INT PRIMARY KEY,
user id INT,
created_at DATE,
amount NUMERIC
);

--7-дневная ретеншн. Для пользователей, зарегистрированных в апреле 2025, посчитайте процент тех,
--кто вернулся в приложение ровно на 7-й календарный день после регистрации (по любому событию в events).

with
april as (
    select user_id, created_at
    from users
    where date_trunc('month', created_at) = '2025-04-01'
),
april_users as (
    select count(user_id) as april_users
    from april
),
event_7d as (
    select count(distinct e.user_id) as user_7d_retention
    from events e
    join april a
        ON e.user_id = a.user_id
    WHERE e.event_date = a.created_at + INTERVAL '7 days'
)

select round(user_7d_retention * 100 /april_users, 2 ) as retention_7d
from event_7d
cross join april_users