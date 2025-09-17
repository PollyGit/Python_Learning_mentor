--Задача 1:
--
--Есть две таблицы.
--Рекламные объявления
--ads: ad_id (PK),
--campaign_id (FK),
--status.
--События
--events: event_id (PK), ad_Id (FK), source, event_type, event_date,
--event_hour.
--Надо рассчитать:
--Кол-во событий в разрезе рекламных кампаний (campaign_id) и типов событий (event_type).

select a.campaign_id, e.event_type, count(*) as count_events
from ads as a
join events as e
    using(ad_id)
group by campaign_id, event_type


--Задача 2:
--Дана таблица всех сотрудников компании
--employees:
--full_name VARCHAR (PK),
--position VARCHAR,
--department VARCHAR.
--Напиши запрос, выводящий все отделы, в которых меньше 5 разработчиков (position = 'Software Developer').

select department , count(*) as n_dev
from employees
where position = 'Software Developer'
group by department
having count(*) < 5









