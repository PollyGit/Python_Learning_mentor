1
написать запрос, который выведет топ страну по количеству фильмов
за 31 декабря 2024 года


select country, count(film_id) as film_count
from boxoffice
where date_trunc('day', dt) = date '2024-12-31'
group by country
order by film_count desc
limit 1


2
Написать запрос, который выведет топ-5 названия фильмов,
у которых были самые высокие продажи за декабрь 2024 года

with
t1 as (
    select film_id, sum(value) as film_sum
    from boxoffice
    where date_trunc('month', dt) = date '2024-12-01'
    group by film_id)

select f.film_name, t1.film_sum
from t1
join films f
    on t1.film_id=f.id
order by t1.film_sum desc, f.film_name
limit 5








