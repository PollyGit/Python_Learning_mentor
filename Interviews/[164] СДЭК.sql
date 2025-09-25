--1. Оптимизировать запрос
--SELECT p.id AS project_id,
--        p.name AS project_name,
--        i.id As issue_id,
--        i.subject As issue_subject,
--        i.status_name As last_status,
--        h.status AS current_status,
--        h.date_update
--FROM project AS p
--LEFT JOIN issue AS i
--    ON p.id=i.project_id
--LEFT JOIN issue_history AS h
--    ON h.id issue=i.id
--WHERE h.code IN (1,4,6)


with
t1 as (
    select *
    from issue_history
    WHERE code IN (1,4,6)
)


SELECT p.id AS project_id,
        p.name AS project_name,
        i.id As issue_id,
        i.subject As issue_subject,
        i.status_name As last_status,
        h.status AS current_status,
        h.date_update
FROM project AS p
LEFT JOIN issue AS i
    ON p.id=i.project_id
JOIN issue_history AS h
    ON h.id issue=i.id



--
--2. Выведите имена пользователей с 3 по 7 в алфавитном порядке.

select first_name
from
    (select first_name
        row_number() over(order by first_name) as rn
    from users) as t
where rn between 3 and 7
order by rn