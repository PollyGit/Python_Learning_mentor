-- 1

--Даны две таблицы Т1 (col1, col2) 3 строки,  и Т2 (со1, col3) 4 строки.
--Оцените какое количество строк вернут операторы:

TI join T2 on TI.coll = T2.coll
min 0
max 12  3x4


TI left join T2 on TI.coll = T2.coll
min 3  считается п Т1
max 12  3x4

TI full join T2 on TI.coll = T2.coll
min 4 считается по мах из Т1 и Т2
max 12  3x4


TI cross join T2
min 12  декартово произведение
max 12  3x4



--2
--Дана таблица T(value), выведите все повторяющиеся записи

select value
from T
group by value
having count(*) > 1;

select value
from (
select value,
    row_number() over(partition by value) as rn
from T) as T2
where rn >1;


--3
--Вывести сотрудника и департамент, со второй максимальной зарплатой в каждом департаменте за апрель 2023


select *
from t2
    (select empl, department,
        dense_rank() over(partition by department order by amount desc) as dr_salary
    from t
    where date_part('year', value_day) = 2023
            and date_part('month', value_day) = 4) as t2
where dr_salary = 2;


