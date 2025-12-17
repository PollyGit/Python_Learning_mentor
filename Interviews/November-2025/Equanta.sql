1
Найти ошибки в запросе

Select
    gender
    ,ord
    ,count(loan_id) as qnt
(
    select c.gender,
           loan_id,
           row_number() over (partition by c.client_id order by loan_id) as ord
    from LOANS_TABLE l
    join CLIENTS_TABLE c on c.client_id = l.client_id
    where eomonth(loan_date) = '2022-10-31'
) a

Ошибки:
1) нет from во внешнем запросе
2) нет GROUP BY во внешнем запросе
3) не везде проставлены элиасы во внутреннем запросе
4) условие where внутри join'а
5) eamonth - в постгрессе нет такой ф-ции
6) услоие с датой неверное , лучше писать типа where dt = date '2022-10-31'



Исправленный:

SELECT
    a.gender,
    a.ord,
    COUNT(a.loan_id) AS qnt
FROM (
    SELECT
        c.gender,
        l.loan_id,
        ROW_NUMBER() OVER (
            PARTITION BY c.client_id
            ORDER BY l.loan_id
        ) AS ord
    FROM LOANS_TABLE   AS l
    JOIN CLIENTS_TABLE AS c
      ON c.client_id = l.client_id
    WHERE EOMONTH(l.loan_date) = '2022-10-31'
) AS a
GROUP BY
    a.gender,
    a.ord;


--2


with
rn as (
    select l.client_id, c.gender, l.loan_id,
           row_number() over(partition by l.client_id order by l.loan_date) as rn
    from loans_table l
    join clients_table c
        using(client_id)
)


select gender,
        count(*) filter (where rn = 1) as "количество первых договоров 2022",
        count(*) filter (where rn = 2) as "количество вторых договоров 2022",
        count(*) filter (where rn = 3) as "количество третьих договоров 2022",
        count(*) filter (where rn = 4) as "количество четвертых договоров 2022",
from rn
where date_part('year', loan_date) = 2022
    and date_part('month', loan_date) = 10
group by gender;











--