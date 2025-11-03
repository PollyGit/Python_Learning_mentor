--Задача 1 (SQL):
--Что не так с запросом?
SELECT user_name, YEAR(user_birth_date) AS
year_of birth
FROM users
WHERE year_of_birth = 2000

использование алиаса в where



--Задача 2 (SQL):
Есть таблица транзакций пользователей transactions и таблица юзеров
users с указанием тестовых и нетестовых. Необходимо рассчитать Retention
для новых нетестовых пользователей по Дням


with
-- Только нетестовые юзеры  и транзакции
no_test_t as (
    select t.id_transaction, t.transaction_date::date as t_day, u.user_id
    from transactions t
    join users u
        using(user_id)
    where user_group = 'no_test'
),
-- разобьем дни на когорты,
-- где Первый день транзакции пользователя = дата когорты (Day 0)
first_day as (
    select user_id, min(t_day) as cohort_day
    from no_test_t
    group by user_id
),
-- Размер когорт (кол-во новых пользователей в день)
cohort_size as (
    select cohort_day, count(*) as users_in_cohort
    from first_day
    group by cohort_day
),
-- добавляем в основную таблицу столбец с датой первой транзакции для
-- каждого польщователя
-- вычитаем из даты транзакции дату первой транзакции
-- получится кол-во дней, которые прошли после регистрации (первой транзакции).
-- Те посмотрим, через сколько дней каждый аользователь возвращается
-- и это когл-во дней - будет порядковый номер дня возвращения, те следующей когорты:
-- 2, 3 , 5 день - это когорта День2, день3, день5...
activity as (
    select  n.user_id, n.t_day, f.cohort_day,
            (n.tx_day - f.cohort_day) as day_n -- на какой день каждый пользователь возвращается
    from no_test_t n
    join first_day f
        using (user_id)
),
--Считаем, сколько уникальных пользователей из каждой когорты было
--активно в конкретный day_n:
active_by_day as (
  select cohort_day, day_n, count(distinct user_id) as active_users
  from activity
  where day_n >= 0
  group by cohort_day, day_n
)
--Retention по дням
-- берем последнюю табл и добавляем в нее размер когорт и делим:
-- активные пользователи в эту дату из данной когорты делим на общее число
-- юзеров из этой когорты

select a.cohort_day, a.day_n, a.active_users,
        c.users_in_cohort,
        round(a.active_users / c.users_in_cohort * 100.0, 2) as retention_pct
from  active_by_day a
join cohort_size c
    using (cohort_day)
order by cohort_day, day_n;
