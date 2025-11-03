--Задача 1

table1 table2
id:    id:
1     1
1     1
2     3
3     3
4     null
null  null

1. SELECT tablel.id, table.id FROM table
LEFT JOIN table2 on table1.id = table2.id

table1 table2
id:    id:
1     1
1     1
1     1
1     1
2     null
3     3
3     3
4     null
null  null


2. SELECT tablel.id, table.id FROM table
INNER JOIN table2 on table1.id = table2.id

table1 table2
id:    id:
1     1
1     1
1     1
1     1
3     3
3     3


3. select id from table1
UNION
select id from table2

table1
id:
1
2
3
4
NULL

4. select id from table1
UNION all
select id from table2

table1
id:
1
1
1
1
2
3
3
3
4
NULL
NULL
NULL

5. А как найти те записи, которые есть в table1, но для них нет аналога в table2

select id from table1
except
select id from table2;

2
4
NULL



SELECT t1.id
FROM table1 t1
WHERE NOT EXISTS (
  SELECT 1 FROM table2 t2
  WHERE t2.id = t1.id
);

2
4
NULL




--Задача 2
--Имеем таблицу TRIP с поездками пользователей на такси:
--trip_id, passenger_id,  tariff, dt, cost
--
--Мы хотим, чтобы пассажиры чаще ездили в тарифе comfort, и решили провести
--промо-рассылку на часть пользователей, которые много ездят в эконом, но
-- мало в comfort.
--
--Напишите запрос, который найдет всех пользователей, кто суммарно потратил
--в тарифе эконом более 5000, но при этом совершил не более одной поездки
--(или ноль поездок) в тарифе comfort.

with
econom_id as (
    select passenger_id, sum(cost) as sum_econom
    from trip
    where tariff = 'econom'
    group by passenger_id
    having sum(cost) > 5000
),
comfort_id_1 as (
    select passenger_id, count(*) as count_comfort
    from trip
    where tariff = 'comfort'
    group by passenger_id
    having count(*) < 2
)

select passenger_id
from econom_id
intersect
select passenger_id
from comfort_id_1


-- or

select passenger_id
from trip
group by passenger_id
having
  sum(case when tariff = 'econom'  then cost else 0 end) > 5000
  and count(*) filter (where tariff = 'comfort') <= 1;


-- or
from trip
group by passenger_id
having
  sum(cost) filter (where tariff = 'econom') > 5000
  and count(*) filter (where tariff = 'comfort') <= 1;


--Интервал активности длины N - это N дней подряд, в
-- каждый из которых пользователь совершил поездку. Написать запрос,
-- который для каждого пользователя найдет максимальную длину интервала активности.
1 1 1 0 0 1 1 0 1 1 1 1
1 0 0 1 1 1 0 1 1 0 0 0 is_break_line
1 2 3 3 3 4 5 5 6 7 8 9 interval_id
1 1 3 1 2 1 1 1 1 count(*) as interval_length

with
no_double_days as (
  select passenger_id, dt as trip_day
  from trip
  group by passenger_id, dt -- убираю дубли по дням, если есть неск поездок в 1 день
),
lag_dt as (
    select passenger_id, trip_day,
    case  -- cмотрю, чтоб разница между текущим и предыдущим днем = 1 day
        when lag(dt) over (partition by passenger_id order by trip_day) = dt - interval '1 day'
            then 0
            else 1  -- 1 - это начало нового интервала
        end as is_break_line
    from no_double_days
),
interval_id as ( -- накопительный счётчик разрывов
    select passenger_id, trip_day,
            sum(is_break_line) over(
                partition by passenger_id order by trip_day
                rows between unbounded preceding and current row
            ) as interval_id  -- все элементы каждого нового интервала
            -- на 1 больше, чем все элементы предыдущего
    from lag_dt
),
interval_length as ( -- длина интервала по каждому пользователю
-- считаем сколько элементов у интервала с цифрами 1, потом с цифрами 2 и тд
    select passenger_id, interval_id, count(*) as interval_length
    from interval_id
    group by passenger_id, interval_id
)

-- Максимальная длина интервала по пользователю
select passenger_id, max(interval_length) as max_length
from interval_length
group by passenger_id
order by passenger_id;





-- or

with days as (  -- 1. Убираем повторы в один день
  select passenger_id, dt::date as trip_day
  from trip
  group by passenger_id, dt::date
),

groups as (  -- 2. Нумеруем дни и вычисляем "сдвиг"
  select
    passenger_id,
    trip_day,
    trip_day - (row_number() over (partition by passenger_id order by trip_day)) * interval '1 day' as grp_key
  from days
),

streaks as (  -- 3. Считаем длину каждого непрерывного интервала
  select
    passenger_id,
    grp_key,
    count(*) as streak_len,
    min(trip_day) as start_day,
    max(trip_day) as end_day
  from groups
  group by passenger_id, grp_key
)

-- 4. Находим максимальную длину интервала по каждому пользователю
select
  passenger_id,
  max(streak_len) as max_active_streak
from streaks
group by passenger_id
order by passenger_id;



