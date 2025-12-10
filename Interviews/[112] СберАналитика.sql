--Задача 1
--
--Какие строки вернет запрос?


SELECT x
FROM some_table
WHERE x NOT IN (1,2);


| x    |
| ---- |
| 1    |
| 2    |
| 3    |
| NULL |


Ответ:
| x    |
| ---- |
| 3    |

в WHERE остаются только TRUE, а сравнение с NULL дают UNKNOWN, а не TRUE.




--Задача 2
--Нужно получить новую таблицу NEW_TABLE с колонкой MERCHANT, в которой каждая строка из MERCHANT_SRC будет очищена и нормализована.
--
-------------
--из чат гпт

create table new_table as
select
    upper(                                   -- всё в ВЕРХНИЙ регистр
        trim(                                -- обрезать пробелы по краям
            regexp_replace(                  -- 2. сжать подряд идущие пробелы в один
                regexp_replace(              -- 1. все НЕ [A-Z a-z 0-9 _] → пробел
                    merchant_src,
                    '[^0-9A-Za-z_]+', ' ', 'g'
                ),
                '\s+', ' ', 'g'
            )
        )
    ) as merchant
from some_table;



--Задача 3

with
month_amount as (
    select date_trunc('month', trans_time) as month_date, client_id,
            sum(amount) as month_amount
    from t
    group by date_trunk('month', trans_time), client_id
),
rn as (
    select month_date, client_id, month_amount,
        row_number() over(partition by month_date order by month_amount desc) as rn
    from month_amount
)

select month_date, client_id, month_amount
from rn
where rn = 5

















--