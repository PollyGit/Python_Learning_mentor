--Задача1
--Есть две таблицы.
--Рекламные объявления ads:
--ad_id (PK),
--campaign_id (FK),
--status.
--События events:
--event_id (PK),
--ad_id (FK),
--source,
--event_type,
--event_date,
--event_hour.
--Надо рассчитать:
--Кол-во событий в разрезе рекламных кампаний (campaign_id) и типов событий (event_type).


select a.campaign_id, e.event_type, count(*) as event_count
from ads as a
left join events as e
    using(ad_id)
group by a.campaign_id, e.event_type


--Задача2
--Дана таблица logs:
--Платформа platform
--Экран nav_screen
--Время просмотра с экрана total_view_time
--Для каждой платформы посчитать топ-5 экрана по времени

with
screen_time as (
    select platform, nav_screen, sum(total_view_time) as total_view_time
    from logs
    group by platform, nav_screen
)

select *
from (
      select *,
          row_number() over(partition by platform order by total_view_time desc) as rn
      from screen_time) as t1
where rn <6



