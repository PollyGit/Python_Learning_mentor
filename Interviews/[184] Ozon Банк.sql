--Задача 1 (SQL):
--Есть кол-во очков (score) каждого атлета
--Нужно вывести места атлетов, но без оконных функций по типу row_number, rank, dense_rank

drop table if exists #Competitions
create table #Competitions (
    Athlete_id INT,
    Score int
)


insert into #Competitions (Athlete_id , Score)
values
(1, 100)
(2, 100),
(3, 100)
(4, 100),
(5, 100),
(6, 0),
(7, 0)

with
n_scores as (
    select distinct Score
    from Competitions),

--для каждого уникального Score (a) считаем,
-- сколько уникальных Score больше, с помощью b.Score > a.Score
rank as (
    select a.Score, count(b.Score) + 1 as rank
    from n_scores  as a
    left join n_scores as b
        on b.Score > a.Score
    group by a.Score
)

select r.rank, c.Athlete_id, c.Score
from Competitions as c
join rank as r
    on r.Score = c.Score
order by r.rank, c.Athlete_id













--Задача 2
count (*) = 7
count (distinct Athlete_id) = 7
avg(score) = 500/7 = 71.43
Count (1) = 7
count ('текст') = 7
Athlete id not between 1 and null = unknown

