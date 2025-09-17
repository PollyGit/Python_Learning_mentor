--таблица WORKFLOWS:
--id - id маршрутного листа (int)
--status - статус маршрутного листа: completed/canceled (string)
--performer_uuid - уникальный uuid исполнителя (string)
--created_at - дата-время создания маршрутного листа (timestamp)
--updated_at - дата-время последнего обовления маршрутного листа (timestamp)
--
--таблица SEGMENTS
--id - id сегмента (int)
--created_at - дата-время создания сегмента (timestamp)
--updated_at - дата-время последнего обновления сегмента (timestamp)
--workflow_id  - id маршрутного листа, к которому принадлежит сегмент (int)
--segment_type - тип сегмента: подлет/сборка/доставка/передача клиенту (string)
--order_n - порядок сегмента (int)
--plan_started_at - плановое время начала выполнения сегмента (timestamp)
--plan_ended_at - плановое время конца выполнения сегмента (timestamp)
--fact_started_at - фактическое время начала выполнения сегмента (timestamp)
--fact_ended_at фактическое время конца выполнения сегмента (timestamp)

--Посчитать насколько мы в среднем хорошо предсказываем плановую длительность сборки
--(segment type ='assembly') по сравнению с фактической по выполненным маршрутным листам
-- за последнюю неделю"

with
completed_id as (
    select id
    from workflows
    where status = 'completed' and
          created_at >= now() - interval '7 days'),
time_diff as (
    select s.workflow_id,s.segment_type, s.plan_ended_at - s.plan_started_at as plan_due,
            s.fact_ended_at - s.fact_started_at as fact_due
    from completed_id  as c
    join segments as s
        on c.id = s.workflow_id
    where segment_type ='assembly'
    order by c.id)

select id, segment_type, avg(fact_due-plan_due) as avg_diff
from time_diff