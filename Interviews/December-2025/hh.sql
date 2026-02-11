--1
--Нужно вывести список сотрудников, которые получают максимальную зарплату в своём отделе. Если в отделе несколько сотрудников с одинаковой максимальной зарплатой, вывести всех таких сотрудников.

departments(
    department_id   INT,
    department_name TEXT
)

employees(
    employee_id     INT,
    employee_name   TEXT,
    department_id   INT,
    salary          NUMERIC
)


with
t as (
    select *,
        rank() over(partition by department_id order by salary desc) as r
    from employees
)

select  d.department_name, t.employee_name, t.salary
from t
left join departments d
    on t.department_id = d.department_id
where r = 1
order by d.department_name;



--2
--Нужно вывести всех сотрудников, чья зарплата строго выше зарплаты их непосредственного руководителя.
employees(
    employee_id     INT,
    employee_name   TEXT,
    manager_id      INT,    -- employee_id его непосредственного руководителя, может быть NULL
    salary          NUMERIC
)

select e.employee_name, e.salary as emp_salary, m.employee_name as chief_name, m.salary as chief_salary
from employees e
join employees m
  on m.employee_id = e.manager_id
where e.salary > m.salary;



--3
--Для каждой строки нужно вывести:
--
--исходные поля операции (как минимум operation_id, contract_id, amount)
--долю суммы операции в общей сумме по договору в процентах с точностью до трёх знаков после запятой.
--Нужно аккуратно обработать случаи, когда сумма по договору может быть 0 (например, если данные грязные).

operations(
    operation_id    INT,
    contract_id     INT,
    operation_date  DATE,
    amount          NUMERIC
)

with
t as (
    select *,
        sum(amount) over(partition by contract_id) as contract_sum
    from operations
)

select operation_id, contract_id, amount ,
     round(amount * 100.0/ nullif(contract_sum), 3)
from t;
































--