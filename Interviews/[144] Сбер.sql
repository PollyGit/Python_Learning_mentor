
--Задача 1
left join t2 on t1.nun1=t2. nun2

1 1
2 2
2 2
2 2
2 2
3 3
3 3
4 null
null null
null null

--Задача 2
--
--Есть табличка в которой в колонке хранятся четные и нечетные числа.
--Необходимо написать запрос, который выведет в одной колонки четные
--в другой нечетные в порядке их возрастания. Количество записей в
--выборке определяется максимальным количеством либо четных либо нечетных
-- чисел в таблице. Запрос необходимо написать для общего случая (для
-- любых вариантов чисел в таблице)

with
t1 as (
select
    case
    when num % 2 = 0 then row_number() over(num) end as rn_even
    case
    when num % 2 = 1 then row_number() over(num) end as rn_odd
from t
)

select
        max(nun) filter (where rn_odd is not null)  as odd,
        max(nun) filter (where rn_even is not null) as even
from t1
group by coalesce(rn_odd, rn_even)
order by coalesce(rn_odd, rn_even)


-- or

with odds as (
  select num as odd, row_number() over (order by num) as rn
  from t
  where n % 2 = 1
),
evens as (
  select num as even, row_number() over (order by num) as rn
  from t
  where n % 2 = 0
)
select o.odd, e.even
from odds o
full join evens e
    using (rn)
order by coalesce(o.rn, e.rn);



--Задача 3
--
--У нас есть кластер серверов и данные о запуске и остановке сервера.
--Надо посчитать активное время работы всех серверов в кластере.
--В табличке server_utilization у нас для каждого сервера есть даты запуска и остановки.
--Таблица содержит следующий набор атрибутов: server_id, status_ time, session_status
--Ответ должен быть в целых днях.


--Берём для каждой строки её «следующее» время и
--оставляем только промежутки, где текущий статус — start.

with e as (  -- в строку старта сервера добавим время выключения сервера
  select
    server_id,
    status_time,
    session_status,
    lead(status_time)  over (partition by server_id order by status_time) as next_time,
    lead(session_status) over (partition by server_id order by status_time) as next_status
  from server_utilization
),
--посчитаем интрвалы между стопом и стартом,
--отфильтруем сначала таблицу:
intervals as (
  select
    server_id,
    status_time as t_start,
    next_time   as t_end
  from e
  where session_status = 'start'
    and next_time is not null
    and next_status = 'end'

select server_id,
   floor(sum(date_part('epoch', (t_end - t_start)))/ 86400)::int as full_active_days
from intervals
group by server_id
order by server_id;



----Задача 4
--Кубик кидается 6 раз подряд.
--Какова вероятность, что за эти 6 раз буду выкинуты все 6 значений?”


--6 бросков по 6 вероятных исходов. Значит, всего исходов: 6^6=46,656.
--
--Благоприятные исходы - это Чтобы выпали все 6 разных чисел ровно по 1 разу.
--Количество способов расставить 6 разных значений по 6 позициям без повторений: 6!=720
--
--Р = благоприятные исходы / общее кол-во исходов = 6! / 6^6 = 0.015 = 1.5%


--Задача 5
--Среднее кол-во волос на голове человека 100 тыс.
--Какова вероятность, что в Москве живут 2 человека с одинаковым кол-вом
--
--По Принципу Дирихле :
--Если M>N, то хотя бы два объекта будут иметь одинаковое значение признака.
--Пусть число жителей Москвы 13,000,000, число волос от 0 до 200,000.
--Здесь 13,000,000>200,000, значит, вероятность совпадения = 1 (то есть 100 %)



