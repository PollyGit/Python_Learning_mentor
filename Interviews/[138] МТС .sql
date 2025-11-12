--Задача 1
--Будут ли отличаться результаты, возвращаемые следующими запросами?
--1) select * from A left join B on [A.id] = [B.id] and B.val = 'A'
--2) select * from A left join B on [A.id] = [B.id] where B.val = 'A'

--Будут, тк во 2) фильтрация происходит после соединения и строки где в А есть null удаляются.



--Задача 2
--У нас есть кластер серверов и надо посчитать суммарное работы время работы
--всех серверов в кластере.
--В табличке server_utilization ( server_id,status_time, session_status)
--у нас для каждого сервера есть даты запуска и остановки.

with
stop_t as (
    select *,
            lead(status_time) over (partition by server_id order by status_time) as stop_time
    from server_utilization
),
diff_t as (
    select *,
        extract(epoch from (stop_time - status_time)))  as seconds_work_intervals
    from stop_t
    where session_status = 'start' and stop_t is not null
)

select sum(seconds_work_intervals) as seconds_work,
       round(sum(seconds_work_intervals) / 3600), 2) as hours_work,
       server_id
from diff_t
group by server_id;


--Если нужно считать «незакрытый» последний старт до «сейчас»,

with
stop_t as (
    select *,
            lead(status_time) over (partition by server_id order by status_time) as stop_time
    from server_utilization
),
diff_t as (
    select *,
        extract(epoch from (coalesce(stop_time, now()) - status_time)))  as seconds_work_intervals
    from stop_t
    where session_status = 'start'
)

select sum(seconds_work_intervals) as seconds_work,
       round(sum(seconds_work_intervals) / 3600), 2) as hours_work,
       server_id
from diff_t
group by server_id;


--Задача 3
--Мы продаем пиццу и компания хочет организовать акцию, продавать
--пиццы с 3 начинками по единой цене. Нам надо рассчитать экономику акции и
--собрать все варианты начинок с ценой.
--В одной пицце не может быть 2 одинаковых начинок и нам не важно,
--в каком порядке будут ингредиенты, нам важна стоимость.
--
--Должна быть хотя бы одна из трех начинок: Chicken, Pepperoni, Sausage

with
combo as (
select t1.topping_name as a,
    t2.topping_name as b,
    t3.topping_name as c,
    t1.ingredient_cost + t2.ingredient_cost + t3.ingredient_cost as total_cost
from pizza_toppings t1
join pizza_toppings t2
    on t1.topping_name < t2.topping_name
join pizza_toppings t3
    on t2.topping_name < t3.topping_name
where t1.topping_name in ('Chicken','Pepperoni','Sausage')
     or t2.topping_name in ('Chicken','Pepperoni','Sausage')
     or t3.topping_name in ('Chicken','Pepperoni','Sausage')
)

select array_to_string (t1.topping_name, t2.topping_name, t3.topping_name, ',') as pizza,
        total_cost
from combo



--Задача 6
--Что выдаст запрос?

SELECT count(*)
FROM one_thousand
INNER JOIN one_thousand ON random() < 0.5;

Ответ из wiki:

`random()` → случайное число, равномерно распределённое между 0 и 1.
`random() < 0.5` → логическое выражение (истинно примерно в половине случаев).

Тут прикол задачи в том, что random() выполняется один раз при запуске запроса, а не для каждой строчки. И выдает true/false. И потом условие ON true или ON false.

Поэтому будет либо 0 либо 1000х1000 = 1 000 000 строчек в результате (это правильный ответ)



--
--Задача 5
--
--Таблица: id, datetime, (lat, lon)
--
--id-шники карт лояльности покупателей и транзакции по ним(дата и время) при покупке памперсов сети 5-ка по Москве за несколько месяцев.
--(lat, lon) - Гео-координаты терминалов в магазинах
--У МТС есть данные по гео абонентов с картой-то точностью: msisdn, datetime, (lat, lon)+-100м
--Хотим провести рекламную кампанию с рекламой акции на памперсы, для чего нужно сматчить id карты лояльности с номером абонента.
--Задача: найти, какие id (карты) и msisdn (номера)
--скорее всего принадлежат одному и тому же человеку.

не решила, взяла из чат гпт решение

-- 1) Преобразуем lat/lon в geography
-- (можно один раз добавить вычисляемые поля или делать на лету)
with t1 as (
  select id, datetime, lat, lon,
         st_setsrid(st_point(lon, lat), 4326)::geography as g1
  from transactions
),
t2 as (
  select msisdn, datetime, lat, lon,
         st_setsrid(st_point(lon, lat), 4326)::geography as g2
  from geodata
)

-- 2) Сопоставление событий по времени и дистанции ≤100 м
, matches as (
  select
    t1.id,
    t2.msisdn,
    t1.datetime as tx_ts,
    t2.datetime as geo_ts,
    st_distance(t1.g1, t2.g2) as dist_m
  from t1
  join t2
    on t2.datetime between t1.datetime - interval '10 minutes'
                      and     t1.datetime + interval '10 minutes'
   and st_dwithin(t1.g1, t2.g2, 100)  -- 100 метров
)

-- 3) Агрегация по паре (id, msisdn) и отсев случайных совпадений
select
  id,
  msisdn,
  count(*)                      as match_cnt,
  round(avg(dist_m)::numeric,2) as avg_dist_m
from matches
group by id, msisdn
having count(*) >= 3           -- порог надёжности (подбери)
order by match_cnt desc, avg_dist_m;


--


create table one_thousand(n int);
insert into one_thousand
select generate_series(1,10);
