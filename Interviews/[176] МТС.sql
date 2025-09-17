
CREATE TABLE EmployeeDetails(
	EmpId int,
	FullName varchar (100),
	managerId int,
	HireDate timestamp,
	city varchar (100))

CREATE TABLE Employeesalary (
	EmpId int,
	Project varchar (100),
	Salary int)

INSERT INTO EmployeeDetails VALUES
(121, Олег Иванов, 321, 01.31.2019, Москва) ;
(321, Иван Алексеев, 986, 01.30.2020, Санкт-Петербург);
(421, Оксана Сидорова, 876, 27.11.2021, Берлин) ;
(156, Андрей Орлов, 321, 05.10.2022, Екатеринбург);
(240, юлия Новикова, 976, 25.04.2019, Калуга);

INSERT INTO EmployeeSalary VALUES
(121, P1, 8000);
(156, P1, 7000);
(240, Null, 9000);
(321, P2, 10000);
(421, Null, 12000);


--1. Написать запрос, который выведет ид и имена сотрудников, не участвующих ни в одном проекте

select e.EmpId, d.FullName
from Employeesalary as e
left join EmployeeDetails as d
    using(EmpId)
where Project is null


--2. имена сотрудников с зп [7000, 10000]

select e.EmpId, d.FullName, d.Salary
from Employeesalary as e
left join EmployeeDetails as d
    using(EmpId)
where Salary between 7000 and 10000

--3. проекты, кол-во человека, отсортировать по кол-ву человек

select Project, count(*) as proj_empl
from Employeesalary
group by Project
order by count(*) desc

--4. добавить поле чтобы пронумеровать получившиеся проекты в зависимости от кол-ва человек

select *,
    row_number() over(order by proj_empl desc ) as rn
from (
    select Project, count(*) as proj_empl
    from Employeesalary
    group by Project
    order by count(*) desc
) as t1
order by proj_empl desc


