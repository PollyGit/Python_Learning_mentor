--1

select a.campaign_id,
    e.event_type,
    count(e.event_id) as events_cnt
from ads a
left join events e
  on e.ad_id = a.ad_id
where e.event_id is not null
group by a.campaign_id, e.event_type
order by a.campaign_id, e.event_type;


--2


select c.member_id, c.points,
        count(distinct o.points) + 1 as place
from competitors c
left join competitors o
    on c.member_id = o.member_id
        and c.points < o.points
group by c.member_id, c.points
order by place

-- or
select member_id,
  points,
  dense_rank() over(order by points desc) as place
from competitors
order by place, member_id;















--