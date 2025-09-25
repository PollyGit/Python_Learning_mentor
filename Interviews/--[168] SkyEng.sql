--Задача 1
--Промаркировать каждого сотрудника уровнем его иерархии
--
--не решила

--ответ из интернета:


--Создаётся временная рекурсивная таблица hierarchy, которая будет заполняться в 2 этапа:
--базовый случай (начало рекурсии)
--рекурсивное расширение (саморекурсия)
WITH RECURSIVE hierarchy AS (
    -- базовый случай: сотрудники без начальника
    -- Присваиваем им level = 0
    SELECT
        employee_id,
        employee_name,
        boss_id,
        0 AS level
    FROM employee_data
    WHERE boss_id IS NULL

    UNION ALL  --Объединяет базовый уровень и все последующие уровни иерархии.

    -- рекурсивный случай: находим подчинённых уже найденных сотрудников.
    SELECT
        e.employee_id,
        e.employee_name,
        e.boss_id,
        h.level + 1 AS level
    FROM employee_data e
    JOIN hierarchy h ON e.boss_id = h.employee_id
    -- e.boss_id = h.employee_id  означает:
    -- «начальник текущего сотрудника (e) — это кто-то, кто уже есть в hierarchy»
    -- К их уровню прибавляем +1


    -- На каждой итерации добавляются подчинённые следующего уровня.
)

SELECT *
FROM hierarchy
ORDER BY level, employee_id;





--Задача 2
--К нам приходит приходит продакт и говорит
-- "а почему в некоторых запросах нет utm меток?" Как эту проблему исправить?

-- Протянуть UTM-метки из первого события


SELECT
  user_id,
  event_name,
  event_timestamp,
  --первую непустую метку по пользователю
  COALESCE(utm_source, first_utm_source) AS utm_source,
  COALESCE(utm_medium, first_utm_medium) AS utm_medium,
  COALESCE(utm_campaign, first_utm_campaign) AS utm_campaign
FROM (
  SELECT *,

  -- FIRST_VALUE(... IGNORE NULLS) — оконная функция, возвращающая первое непустое значение utm-метки:
         FIRST_VALUE(utm_source) IGNORE NULLS OVER (PARTITION BY user_id ORDER BY event_timestamp) AS first_utm_source,
         FIRST_VALUE(utm_medium) IGNORE NULLS OVER (PARTITION BY user_id ORDER BY event_timestamp) AS first_utm_medium,
         FIRST_VALUE(utm_campaign) IGNORE NULLS OVER (PARTITION BY user_id ORDER BY event_timestamp) AS first_utm_campaign
  -- or
      MAX(utm_source) FILTER (WHERE utm_source IS NOT NULL)
        OVER (PARTITION BY user_id ORDER BY event_timestamp
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)


  FROM events_data
) t1;


