--1
--
--Гипотезы:
--
--1. Акция увеличила объём заказов и выручку, те пользователи с промокодом тратят больше, чем без промокода


with
promo as (
    select has_promo,
            sum(amount) filter (where has_promo = TRUE) as promo_amount,
            sum(amount) filter (where has_promo = FALSE) as no_promo_amount,
            avg(amount) filter (where has_promo = TRUE) as promo_avg,
            avg(amount) filter (where has_promo = FALSE) as no_promo_avg,
            count(distinct user_id) filter (where has_promo = TRUE) as promo_cnt_users,
            count(distinct user_id) filter (where has_promo = FALSE) as no_promo_cnt_users,
            count(order_id)  filter (where has_promo = TRUE) as promo_cnt_orders,
            count(order_id)  filter (where has_promo = FALSE) as no_promo_cnt_orders
    from orders
    where order_date::date between date '2025-06-01' and date '2025-07-16'
)

select
      round(promo_amount * 100.0 / nullif(no_promo_amount, 0), 2) as is_effect_amount,
      round(promo_avg * 100.0 / nullif(no_promo_avg, 0), 2) as is_effect_avg,
      round(promo_cnt_users * 100.0 / nullif(no_promo_cnt_users, 0), 2) as is_effect_cnt_users,
      round(promo_cnt_orders * 100.0 / nullif(no_promo_cnt_orders, 0), 2) as is_effect_cnt_orders
from promo







--