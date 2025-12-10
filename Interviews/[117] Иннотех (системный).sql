--Задача 1

select report_dt, count(*)
from dscal_in_r_tech_sbicl_contact
group by 1

union

select report_dt, count(*)
from dscal_in_r_tech_sbicl_segment
group by 1

union

select report_dt, count(*)
from dscal_in_r_tech_sbicl_making
group by 1;


--Почему вывод в запросе именно такой?

все результаты запросов имеют одинаковые даты, и при этом
разное значение счетчиков лишь у 2х запросов. Поэтому в результате 2 строки.