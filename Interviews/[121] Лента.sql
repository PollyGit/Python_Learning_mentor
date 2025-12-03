--stage.lo_events
--
--Лог событий.
--
--Колонки:
--
--- user_id – id пользователя
--- event_name – тип события:
--    - view_item – просмотр товара
--    - add_to_cart – добавление товара в корзину
--- event_datetime – время события
--- product_id – id товара
--- order_type – способ получения заказа: delivery / pickup
--
--Каждая строка = какое-то действие пользователя с товаром в определённое время.
--
--stage.items
--
--Справочник товаров.
--
--Колонки:
--
--- item_id – id товара (соответствует product_id в событиях)
--- item_name – название товара (Яблоко, Банан, …)
--- item_price – цена товара
--
--Задача 1
--
--Найти цену первого добавленного в корзину товара для каждого пользователя

with
first as (
select user_id, event_datetime, product_id
       row_number() over (partition by user_id order by event_datetime) as rn
from stage.lo_events
where event_name= 'add_to_cart'
group by user_id, event_datetime, product_id
)

select f.user_id, f.product_id, s.item_price
from first f
join stage.items s
    on f.product_id = s.item_id
where f.rn = 1;

--
--Задача 2
--
--Вывести список пользователей, которые добавляли в корзину товары с id 101 и 102 (и 101, и 102), но не добавляли товар 104.

select user_id
from stage.lo_events
where event_name = 'add_to_cart'
    and product_id = 101

intersect

select user_id
from stage.lo_events
where event_name = 'add_to_cart'
    and product_id = 102

except

select user_id
from stage.lo_events
where event_name = 'add_to_cart'
    and product_id = 104





----