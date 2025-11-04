--Задача 1

1. Как можно выбрать уникальные значения из таблицы

Через Distinct, group by, union таблицы к самой себе,
вывести его через row_number: сделать оконную ф-цию с нумерацией и группировкой и вывести только при row_number=1

2. Как проверить наличие дублей по атрибуту в таблице?

Через group by + having count(*) > 1,
через count(*)-count(distinct col),
найти точные строки-дубликаты с ROW_NUMBER()

3. Что такое первичный ключ? Это всегда один атрибут(столбец)?

- Это уникальный ключ:
- 1 столбец или составной (несколько колонок, напр  primary key (a, b))
- может быть только один ПК
- гарантирует уникальность своих значений
- запрещает NULL
- может быть суррогатный (технич. идентификатор) или естественный (набор бизнес-полей : (country_code, phone))

4. Как можно заменять null на 0 при обращении к таблице запросом

coalesce(amount, 0)



--Задача 2
--- Необходимо посчитать оборот продаж за последнюю неделю.
--- Какую долю занимают продажи этой недели в общем обороте за месяц (30 дней)?

Витрина 1 - v_orders
day_id - дата покупки
order_id - id чека
product id - id товара
quantity - продажа товара в штуках

Витрина 2 - v_price
product_id - id товара
price -цена товара
day_start - дата начала действия цены
day_end - дата окончания действия цены

with
order_price as (
    select o.*, p.price
    from v_orders o
    join v_price p
        on o.product_id = p.product_id
        and o.day_id >= p.day_start
        and (o.day_id <= p.day_end or p.day_end is null)
)
revenue_week as (
    select
            round(sum(price * quantity) filter (
            where day_id >= current_date - interval '7 days'
                and day_id <  current_date
            )::numeric, 2) as revenue_week
    from order_price
),
revenue_30 as (
    select
            round(sum(price * quantity) filter (
            where day_id >= current_date - interval '30 days'
                and day_id <  current_date
            )::numeric, 2) as revenue_30
    from order_price
)

select t2.revenue_week as revenue_week,
       t1.revenue_30 as revenue_30,
       round((t2.revenue_week * 100.0 / nullif(t1.revenue_30, 0)),2)  as part
from revenue_30 t1
cross join revenue_week t2
