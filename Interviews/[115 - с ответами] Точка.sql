--Задача 1
--
--Какой результат будет?
t
1
2
3
null

select *
from t
where t.id <> 1;

при сравнении null с чем-то , будет  unknown.
1 = 1.
Значит   <> 1 это 2  и 3.
получается:
2
3



--Задача 2

select *
from t
left join t
  on 1 = 1;

ON 1 = 1 — условие всегда TRUE, поэтому каждая строка слева соединится с каждой строкой справа.
Те это CROSS JOIN.

t
1
2
3
null



--Задача 3
--В чем различие запросов? Будут ли разные результаты?

-- Запрос №1
select *
from t1
left join t2
  on t1.DT = t2.DT
where t2.DT >= 10;

-- Запрос №2
select *
from t1
left join t2
  on t1.DT = t2.DT
 and t2.DT >= 10;


-- Запрос №1
Для строк t1, у которых нет совпадения в t2, правая часть будет NULL.
Тогда
where t2.DT >= 10 → NULL не удовлетворет условию и фильтруется → строка удаляется в WHERE.
Строки, где t2_dt равно null (т.е. нет соответствия в t2), будут исключены из результата

-- Запрос №2
JOIN пытается найти строки t2, где t1.DT = t2.DT и t2.DT >= 10.
Если таких строк нет, LEFT JOIN всё равно сохранит строку из t1, но с NULL во всех колонках t2.
Все строки t1 останутся (просто часть из них будет с NULL-ами справа).




--Задача 4
--
--Пока снято не более 100 тысяч рублей, снятие бесплатное При превышении лимита
--в 100 тысяч рублей мы берём 3 процента от суммы, но не менее 100 рублей

with
cum_sum as (
select *,
    sum(amount) over(partition by user_id, date_trunk('month', dt)
                order by dt rows between unbounded presceding and current row) as cum_sum_cash
from t
)

select id, user_id, amount, cum_sum_cash,
        case
        when cum_sum_cash <= 100000 then 0
        when cum_sum_cash - amount >= 100000 then greatest(amount*0.03, 100)
        else greatest((cum_sum_cash - 100000)*0.03, 100)
        end as tax
from cum_sum;




--Задача 5
--сравнить графики (линии) по 2-м метрикам в динамике, где в конце метрики падают
--(подробнее на скриншоте) и назвать причины падения, ок это или не ок


--------------------
--решение из ответа:

WITH cohort_data AS (
    SELECT
        trunc(OPEN_DATE, 'mm') AS cohort_month, -- Месяц когорты (регистрации)
        trunc(BORN_DATE, 'mm') AS born_month,   -- Месяц "рождения"
        months_between(trunc(BORN_DATE, 'mm'), trunc(OPEN_DATE, 'mm')) AS month_offset, -- Сколько месяцев прошло с регистрации до "рождения"
        CLIENT_ID,
        BORN_DATE,
        OPEN_DATE
    FROM client
    WHERE OPEN_DATE IS NOT NULL
),
cohort_metrics AS (
    SELECT
        cohort_month,
        month_offset,
        COUNT(*) AS total_clients_in_cohort, -- Общее число клиентов в когорте
        COUNT(CASE WHEN BORN_DATE IS NOT NULL THEN 1 END) AS born_clients, -- Число "родившихся" клиентов
        AVG(CASE
              WHEN BORN_DATE IS NOT NULL
              THEN BORN_DATE - OPEN_DATE
            END) AS avg_days_to_born -- Среднее количество дней до "рождения"
    FROM cohort_data
    GROUP BY cohort_month, month_offset
)
SELECT
    cohort_month AS "Месяц когорты",
    month_offset AS "Месяц после регистрации",
    total_clients_in_cohort AS "Всего клиентов",
    born_clients AS "Родившихся клиентов",
    (born_clients::float / total_clients_in_cohort * 100) AS "Доля рождаемости, %",
    avg_days_to_born AS "Среднее число дней до рождения"
FROM cohort_metrics
WHERE month_offset IS NOT NULL
ORDER BY cohort_month, month_offset;


---------------------
--решение из чат гпт:

WITH base AS (
  SELECT
    client_id,
    date_trunc('month', open_date)::date AS cohort_month,
    born_date,
    open_date
  FROM client
  WHERE open_date IS NOT NULL
),
cohort_size AS (
  SELECT cohort_month, COUNT(*) AS cohort_n
  FROM base
  GROUP BY 1
),
events AS (
  -- возраст клиента в месяцах до рождения (целое)
  SELECT
    b.cohort_month,
    CASE
      WHEN born_date IS NOT NULL
      THEN (date_part('year', born_date) - date_part('year', open_date)) * 12
         + (date_part('month', born_date) - date_part('month', open_date))
    END::int AS month_offset,
    born_date,
    open_date
  FROM base b
),
conv_by_age AS (
  -- кумулятивная конверсия по возрасту когорты
  SELECT
    e.cohort_month,
    g.m AS month_age,
    SUM(CASE WHEN e.born_date IS NOT NULL
              AND (date_part('year', e.born_date) - date_part('year', e.open_date)) * 12
                + (date_part('month', e.born_date) - date_part('month', e.open_date)) <= g.m
        THEN 1 ELSE 0 END) AS born_leq_m
  FROM events e
  JOIN LATERAL generate_series(0, 12) AS g(m) ON true     -- возраст до 12 мес, например
  GROUP BY 1,2
)
SELECT
  c.cohort_month        AS "Месяц когорты",
  c.month_age           AS "Месяц после регистрации",
  s.cohort_n            AS "Размер когорты",
  c.born_leq_m          AS "Родившихся к возрасту m",
  ROUND(100.0 * c.born_leq_m / s.cohort_n, 1) AS "Кумулятивная доля, %",
  -- среднее число дней до рождения (только по родившимся к возрасту m, для зрелых когорт)
  NULL                  AS "Среднее дней до рождения (см. примеч.)"
FROM conv_by_age c
JOIN cohort_size s USING (cohort_month)
ORDER BY 1,2;


Из чат ГПТ:

Падение доли рождённых в конце календарной шкалы — почти наверняка эффект незрелых когорт (нормально).
Падение средних дней до рождения к концу — следствие того, что в свежих когортах видны только «быстрые» рождения (selection bias).
Чтобы ответить «ок / не ок» по продукту, надо:
сравнить одинаковый возраст когорты (0, 1, 2… месяц) между месяцами открытия,
убедиться, что после контроля зрелости кумулятивная конверсия не падает.




--Задача 6
--Посчитать метрику скорости карт, % выданных карт.
--Когортный анализ - для отслеживания динамики месяц к месяцу.
--
--id - заявки
--DT1 - время создания заявки на карту
--DT2 - время получения карты клиентом, Может быть null


--------------------
--решение из ответа:

WITH base AS (
    SELECT
        id,
        DATE_TRUNC('month', DT1) AS cohort_month,
        DATE_TRUNC('month', COALESCE(DT2, NOW())) AS event_month,
        CASE
            WHEN DT2 IS NULL THEN 0
            ELSE 1
        END AS issued_flag
    FROM applications
),
cohort AS (
    SELECT
        cohort_month,
        EXTRACT(MONTH FROM age(event_month, cohort_month)) AS month_number,
        COUNT(*) AS total_requests,
        SUM(issued_flag) AS issued_cards
    FROM base
    GROUP BY cohort_month, month_number
)
SELECT
    cohort_month,
    month_number,
    total_requests,
    issued_cards,
    ROUND(100.0 * issued_cards / total_requests, 2) AS issued_percent
FROM cohort
ORDER BY cohort_month, month_number;








--