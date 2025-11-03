--1
--Есть две таблицы
CREATE TABLE country
(
country_name varchar (32),
city varchar(32)
);
CREATE TABLE sales
(
date datetime '2022-10-01 12:30:00',
city varchar(32),
income decimal (18,2)
);
--Вывести разницу income в % по каждой стране YoY, сравнивая октябрь 2022 с октябрь 2023

with
sales_22_23 as (
    select c.country_name, s.city, s.income, s.'date',
        sum(s.income) filter ( where date_part('month', s.'date') = 10 and date_part('year', s.'date') = 2022) as oct_2022,
        sum(s.income) filter ( where date_part('month', s.'date') = 10 and date_part('year', s.'date') = 2023) as oct_2023,
    from sales s
    join country c
        using (city)
    group by c.country_name
)

select country_name, oct_2022, oct_2023,
    ROUND( (oct_2023- oct_2022) * 100.0 / nullif(oct_2022, 0), 2) as diff_income
from sales_22_23


--2
--У первого события в каждой сессии пользователя проставлен уникальный текстовый id сессии.
--Для последующих событий id в сессии присвоен null
--Необходимо вместо null проставить іd сессии, к которой это событие относится.

select
    event_uuid,
    ts,
    user_id,
    event_name,
    last_value(session_id) ignore nulls
        over (partition by user_id order by ts) as session_id_filled
from events
order by user_id, ts;


-- или
-- без ignore nulls
-- посмотрела решение

with marked as (
  select
    event_uuid,
    ts,
    user_id,
    event_name,
    session_id,
    count(session_id) over (
        partition by user_id
        order by ts, event_uuid
        rows between unbounded preceding and current row
    ) as grp
  from events
)
select
    event_uuid,
    ts,
    user_id,
    event_name,
    max(session_id) over (partition by user_id, grp) as session_id_filled
from marked
order by user_id, ts;


--5
Придумали АБ тест: на выдаче в тестовой группе половине врачей повесили шильдик "лучший врач",
чтобы сфокусировать пользователей.
Конверсия в запись на выдаче к любому врачу упала. Предположи, почему.

Предположение: Конверсия упала тк

- сломалось что-то на техническом уровне. Нужно смотреть логи, на каком этапе проблема.
- увеличилось время выбора врача , то есть время до первого клика. Таким образом, часть пользователей так и не выбирает ничего.
- доверие к подбору врачей падает, тк такое кол-во лучших не выглядит нормлой, а выглядит рекламой. Часто навязывающая реклама воспринимается негативно.
- меняет ли шильдик “лучший врач” цену в большую сторону?



