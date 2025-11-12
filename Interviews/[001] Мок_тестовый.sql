--### 1) Подписки стримингового сервиса
--- `subscriptions(user_id, plan, started_at, price)`
--- `payments(user_id, paid_at, amount, status)`
--Для каждого пользователя определить последнюю активную подписку на
--момент оплаты: вернуть по одному актуальному эпизоду подписки на
--пользователя вместе с датой начала и ценой. Если в один день у
--пользователя было несколько стартов подписок, оставить запись с более
--дорогим планом.

with
--Последний успешный платёж по каждому юзеру
last_pay as (
  select user_id, paid_at
  from (
    select user_id, paid_at,
           row_number() over (partition by user_id order by paid_at desc) as rn
    from payments
    where status = 'ok'
  ) t
  where rn = 1
),
--Если в один календарный день у юзера несколько стартов — берём самый дорогой
subs_dedup as (
  select distinct on (user_id, date_trunc('day', started_at))
         user_id,
         first_value(plan)  over (partition by user_id, date_trunc('day', started_at)
                                  order by price desc, started_at desc) as plan,
         first_value(price) over (partition by user_id, date_trunc('day', started_at)
                                  order by price desc, started_at desc) as price,
         date_trunc('day', started_at)::timestamp as started_at
  from subscriptions
  order by user_id, date_trunc('day', started_at)
),
--Эпизоды подписок: [started_at, ended_at)
episodes as (
  select
    user_id, plan, price, started_at,
    lead(started_at) over (partition by user_id order by started_at) as ended_at
  from subs_dedup
)

-- Выбираем эпизод, действующий на момент последнего платежа
select
  lp.user_id,
  e.plan,
  e.price,
  e.started_at,
  lp.paid_at
from last_pay lp
join episodes e
  on e.user_id = lp.user_id
 and lp.paid_at >= e.started_at
 and (e.ended_at is null or lp.paid_at < e.ended_at)
order by lp.user_id;




--### 2) Поддержка: инциденты по дням
--`tickets(ticket_id, customer_id, created_at, status, channel)`
--`status ∈ {'opened','resolved','reopened','closed_without_resolution'}`
--
--
--**Задача**
--По каждому дню (по полю `created_at::date`) посчитать:
--- сколько заявок было со статусом `resolved`;
--- долю `resolved` от всех заявок за день;
--- сколько уникальных клиентов в этот день имели заявки, где встречался
--`reopened`, но не встречался `resolved`.
--Вернуть: `day, resolved_cnt, resolved_share, customers_reopened_only_cnt`.\


with
-- A) Помесячная агрегация по тикетам (для resolved_cnt и доли)
day_stats as (
  select
    created_at::date as day,
    count(*)                                         as day_cnt,
    --- сколько заявок было со статусом `resolved`;
    count(*) filter (where status = 'resolved')      as resolved_cnt
  from tickets
  group by created_at::date
),

-- B) Флаги по (день × клиент): был reopened? был resolved?
cust_flags as (
  select
    created_at::date                                  as day,
    customer_id,
    bool_or(status = 'reopened')                      as has_reopened,
    bool_or(status = 'resolved')                      as has_resolved
  from tickets
  group by created_at::date, customer_id
),

-- C) Сколько клиентов в день: есть reopened и нет resolved
reopened_only as (
  select
    day,
    count(*) filter (where has_reopened and not has_resolved)
      as customers_reopened_only_cnt
  from cust_flags
  group by day
)

select
  d.day,
  d.resolved_cnt,
  --- долю `resolved` от всех заявок за день;
  round(d.resolved_cnt::numeric / nullif(d.day_cnt, 0), 4) as resolved_share,
  --- сколько уникальных клиентов в этот день имели заявки, где встречался
  ---`reopened`, но не встречался `resolved`.
  coalesce(r.customers_reopened_only_cnt, 0)               as customers_reopened_only_cnt
from day_stats d
left join reopened_only r using (day)
order by d.day;




--### 3) HR: изменения зарплат
--`salary_events(employee_id, salary, changed_at)` — запись добавляется при каждом изменении оклада.
--Для каждого сотрудника вывести историю изменений с разницей оклада
--относительно предыдущего значения и отметкой случаев, когда оклад
--вырос более чем на 15%. Вернуть:
--`employee_id, changed_at, salary, prev_salary, salary_diff, raise_gt_15pct_flag`.

with
hist as (
  select
    employee_id,
    changed_at,
    salary,
    lag(salary) over (
      partition by employee_id
      order by changed_at
    ) as prev_salary
  from salary_events
)
select
  employee_id,
  changed_at,
  salary,
  prev_salary,
  (salary - prev_salary)                                  as salary_diff,
  case
    when (salary - prev_salary) / nullif(prev_salary, 0.0) > 0.15
      then 1 else 0
  end                                                     as raise_gt_15pct_flag
from hist
order by employee_id, changed_at;



