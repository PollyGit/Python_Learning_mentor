--1
select *
from t1
left join t2
  on t1.N = t2.N
where t2.N <> 10;

where удаляет все строки, где:
t2.N = 10 и
t2.N is null
В итоге не все t1.N могут остаться и получится INNER JOIN

--

select *
from t1
left join t2
  on t1.N = t2.N
 and t2.N <> 10;

Остаются все t1.N и в столбце t2.N будут значения != 10 и останутся null значения


--2

select *
from t
left join t
  on 1 + 1 = 2;

1+1=2 — условие всегда TRUE, значит для каждой строки из левой t подойдут все строки из правой t.
это будет кросс-джойн


--3
--Есть две таблицы table1 и table2.
--В каждой по 3 поля:
--Ф — фамилия
--И — имя
--О — отчество
--Нужно либо убедиться, что данные в двух таблицах идентичны, либо вывести ФИО людей, по которым есть расхождения.

--если есть одинаковые строки, то группируем
with t1 as (
    select Ф, И, О, count(*) as cnt
    from table1
    group by Ф, И, О
),
t2 as (
    select Ф, И, О, count(*) as cnt
    from table2
    group by Ф, И, О
)

-- строки, которые есть в table1, но нет в table2
select Ф, И, О
from t1
except
select Ф, И, О
from t2

union

-- строки, которые есть в table2, но нет в table1
select Ф, И, О
from t2
except
select Ф, И, О
from t1;


Если результат пустой → набор ФИО в двух таблицах идентичен.
Если что-то вернулось → это как раз ФИО, которые есть только в одной из таблиц.



--4
--Сгруппировать по временным интервалам - десятилетиям

with
decade as (
    select name, sex,
           (extract(year from birth_date)::int / 10) * 10 as decade_date
    from t
    where sex = 'ж'
),
cnt as (
    select decade_date, name, count(*) as freq_name
    from decade
    group by decade_date, name
),
rn as (
    select decade_date, name, freq_name,
        row_number() over(partition by decade_date order by freq_name desc) as rn
    from cnt
)

select decade_date, name
from rn
where rn = 1
order by decade_date

--5
составила систему уравнений

у + 5х = 1
у = 2х

у = 2/7


--6
--Мы показываем клиенту индивидуальное предложение двумя каналами:
--баннер в ИБ. Вероятность, что он его прочитает, составляет 40%,
--письмо на e-mail. Вероятность его прочтения — 30%.
--Считая события прочтения в двух каналах независимыми,
--с какой вероятностью клиент увидит наше предложение?

Идти от обратного. Посчитать вероятность того, что он и не прочитает в приложении И не прочтает в почте.
Затем вычесть это Р из 1.

Р(А-) = 1 - 0.4 = 0.6
Р(В-) = 1 - 0.3 = 0.7
Р(А- и В-) = 0.6 * 0.7 = 0.42
Р(А и В) = 1 - 0.42 = 0.58

--