 Задача 1
Кол-во событий в разрезе рекламных кампаний (campaign_id) и типов событий (event_type).

select campaign_id,  event_type , count(*) as count_events
from ads a
left join events e
    using(ad_id)
group by  campaign_id,  event_type


Задача 2
События могут быть двух типов
event_ type:
'Impression' - показ,
'click' -клик.
Надо рассчитать:
CTR (кол-во кликов / кол-во показов) в разрезе рекламных кампаний (campaign_id).


select campaign_id, round(count_events_click*1.0/ nullif(count_events_impress, 0), 2) as ctr
from (
select campaign_id,
        count(*) filter (where event_type = 'click') as count_events_click,
        count(*) filter (where event_type = 'Impression') as count_events_impress
from ads a
left join events e
    using(ad_id)
group by  campaign_id) as t



--Задача 3
--Есть, таблица competitors:
--member_id (PK) - id участика сорвнования
--points - кол-по очков набранных в ходе соревнования
--Необходимо для каждого участника рассчитать место, которое он занял в соревнованиях

select *,
        row_number() over(order by points desc) as place
from competitors
