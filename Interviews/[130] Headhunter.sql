--Задача 1
--Есть 2 таблицы:
--employer: employer_id bigint, name varchar
--vacancy: vacancy_id bigint, active boolean, employer_id bigint.
--
--Найти работодателей, у которых не более 5 активных вакансий

select e.employer_id, e.name
from employer e
left join vacancy v
    using(employer_id)
group by e.employer_id, e.name
having count(*) filter (where v.active = true) <= 5;


--Задача 2
--
--Таблица поиска пользователей
--
--search: user_id, search_number int (номер поиска, порядковая нумерация в рамках каждого пользователя), vacancy_id, vacancy_position int (позиция вакансии на выдаче).
--Таблица кликов пользователей clicks: ts timestamp (время клика), user_id , search_number int (номер поиска, порядковая нумерация в рамках каждого пользователя),vacancy_id.
--
--Написать запрос, который подсчитает среднюю позицию первых трех кликов пользователей (нужны первые 3 клика из каждого пользователя). Если на поисковой выдаче пользователь вообще не делает кликов или сделал меньше 3 кликов, то такого пользователя не учитывать.


with
-- 1. Пользователи, у которых хотя бы 3 клика всего
users_with_3_clicks as (
  select user_id
  from clicks
  group by user_id
  having count(*) >= 3
),
-- 2. Все клики этих пользователей с позициями вакансии
user_clicks as (
  select
    c.user_id,
    c.ts,
    c.search_number,
    c.vacancy_id,
    s.vacancy_position,
    row_number() over (
      partition by c.user_id
      order by c.ts
    ) as rn
  from clicks c
  join search s
    on  s.user_id       = c.user_id
    and s.search_number = c.search_number
    and s.vacancy_id    = c.vacancy_id
  where c.user_id in (select user_id from users_with_3_clicks)
),
-- 3. Берём только первые 3 клика каждого пользователя
first3 as (
  select *
  from user_clicks
  where rn <= 3
)

select
  avg(vacancy_position) filter (where rn = 1) as avg_position_1,
  avg(vacancy_position) filter (where rn = 2) as avg_position_2,
  avg(vacancy_position) filter (where rn = 3) as avg_position_3
from first3;







--