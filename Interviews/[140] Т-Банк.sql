1
В таблице user_logs определите, есть ли дубли по колонкам
user_id и dttm. Если есть, выведите эти user_id и dttm

select user_id, dttm, count(*) as cnt_str
from user_logs
group by user_id, dttm
having count(*) > 1


--Задача 2
--Для каждого пользователя в таблице user_logs выберите последнюю запись по
--полю dttm
--В таблице 3 столбца: user_id, dttm, action

select user_id, dttm, action
from
(select user_id, dttm, action,
    row_number() over(partition by user_id order by dttm desc) as rn
from user_logs) t
where rn = 1
