--1
--Объяснить, что делает SQL запрос
with
prepared as (
 select
		src.*,
		row_number () over( partition by service_center order by dt asc)
	    - row_number () over ( partition by service_center, emloyee_name
	order by dt asc) as rn diff
	from src
),
result as (
	select
				service_center, emloyee_name,
				dt,
				row_number () over (
				partition by service_center, emloyee_name, r_diff
				order by dt asc
				) as rn
	from prepared
	order by dt asc)

select service_center, sum(1) as cnt
from result
where rn=1
group by service_center;

`prepared` : Здесь идет 1) ранжирование строк по датам внутри сервисного центра и
2) ранжирование строк по датам внутри сервисного центра и каждого сотрудника.
3) Разность 1 и 2 = `rn_diff`. Разность этих двух нумераций  = const для подряд
идущих строк, где сотрудник один и тот же. То есть один и тот же сотрудник пользовался
 сервис центром несколько дней подряд.

`result`: Здесь идет ранжирование строк по датам внутри сервисного центра и каждого
 сотрудника и `rn_diff`. Тем самым ранжируется количество дней в каждом интервале
 отдельно, когда сотрудник пользовался сервисным центром = `as rn`.
 Теперь каждый интервал подряд идущих дней одного сотрудника имеет свои строки с rn = 1,2,3,….

Финальный запрос: фильтрация по `where rn=1`. То есть берется только первый день каждого
интервала по каждому сотруднику. `sum(1)` - считается количество интервалов/смен
сотрудников по каждому сервисному центру.



--2
--Будет ли вывод отличаться?
select service_center,
sum (1) as cnt_1 ,sum(rn) as cnt_2, count(* ) as cnt 3
from result
where rn=1
group by service_center;


нет, по факту везд считается колво строк



--