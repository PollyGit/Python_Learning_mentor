----1)Определить, сколько потратил в 2005 году каждый из членов семьи.
--в результирующеи выборке не выводите тех членов семьи, которые ничего не потратили.
--2)Посчитать для каждого члена семьи на каждый день рассчитать затраты.
--3)Найти самый затратный день для каждого члена отдельно

--1
select  f.member_id,
        f.member_name,
        f.status,
        sum(p.amount * p.unit_price) as costs
from FamilyMembers f
join Payments p
    on f.member_id = p.family_member
where date_part('year',p.date) = 2005
group by f.member_id, f.member_name, f.status
order by f.member_name;

--2
select  f.member_id,
        f.member_name,
        f.status,
        p."date"::date as day,
        sum(p.amount * p.unit_price) as day_cost
from FamilyMembers f
join Payments p
    on f.member_id = p.family_member
group by f.member_id, f.member_name, f.status, p."date"::date
order by f.member_name, day;


--3
with
day_payment as (
select  member_id,
        member_name,
        status,
        "date"::date as day,
        sum(amount * unit_price) as day_cost
from FamilyMembers f
join Payments p
    on f.member_id = p.family_member
group by f.member_id, f.member_name, f.status, p."date"::date
order by f.member_name, day
)

select member_id,
       member_name,
       status,
       day as max_payment_day,
       day_cost as max_day_cost
from (
    select member_id,
           member_name,
           status,
           day,
           row_number() over(partition by member_id order by day_cost desc) as rn
    from day_payment) t1
    where rn = 1

--