
--Есть 2 таблицы.
--1) сколько учеников всего и есть ли полные тезки в таблице?
select
    count(*) as students_cnt,
    case
    when count(distinct name) < count(*) then 'есть тезки'
    else 'нет тезок'
    end as similar
from students


--2) Когда ученик, который имеет хотя бы одну 5, в последний раз получал не 5?

with
t as (
    select s.id, s.name, l.date, l.mark
    from students s
    join lessons l
        on s.id = l.student_id
),
fine_students as (
    select id
    from t
    where mark = 5
)

select id, name,
    max(date) as date_less_5
from t
where id in (select id from fine_students)
    and mark != 5
group by id, name




--3) сколько оценок у каждого учениеа?

with
t as (
    select s.id, s.name, l.date, l.mark
    from students s
    left join lessons l
        on s.id = l.student_id
)

select id, name, count(mark) as mark_cnt
from t
group by id, name










--
Что выведет этот код?



for i in range(10):
    if i % 2:
        print(i)
    else:
        break

Ничего не выведет, тк 0 при делении на 2 дает 0, поэтому будет  break

--