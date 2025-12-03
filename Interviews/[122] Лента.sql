--# 1)Выведите количество активных подписок для каждого приложения. Приложения должны иметь ID и наименование,
--# а также ID и описание категории (заполненные).
--#

with
subs_active as (
    select product_id, status
    from subscriptions
    where status = 'active'
)

select a.product_id, a.name, ac.description, ac.id, count(s.subscription_id) as cnt_active_subscriptions
from app a
join app_category ac
    on ac.id = a.category_id
left join subs_active sa
    using(product_id)
group by a.product_id, a.name, ac.description, ac.id
order by a.product_id



--# 2)в разрезе тарифных планов среди отмененных подписок, выведите кол-во пользователей, а также кол-во и сумму платежей

with
subs_cancel as (
    select product_id, status, subscription_id, user_id, plan_id
    from subscriptions
    where status = 'cancel'
),
pay_done as (
    select *
    from payments
    where payment_status = 'done'
)

select sc.plan_id , count(distinct sc.user_id) as cnt_users, sum(pd.amount) as sum_canceled_payments,
        count(pd.payment_id) as cnt_canceled_payments
from subs_cancel sc
inner join pay_done pd  -- хотела inner, но вдруг есть отмененные подписки без платежей, тогда надо left
    using(subscription_id)
group by sc.plan_id
order by sc.plan_id








--# 3)Выведите top-3 приложений в каждой категории по убыванию оборота по приложению.

with
app_revenue as (
    select a.product_id, a.name as app_name, a.category_id,
        sum(p.amount) as revenue
    from app a
    join subscriptions s
        on s.product_id = a.product_id
    join payments p
        on p.subscription_id = s.subscription_id
       and p.payment_status = 'done'
    group by a.product_id, a.name, a.category_id
),
rn as (
    select *,
        row_number() over(partition by category_id order by revenue_per_app desc) as rn
    from app_revenue
)

select r.category_id, ac.name as category_name, r.product_id, r.app_name, r.revenue
from rn r
join app_category ac
    on t.category_id = ac.id
where r.rn <= 3
order by r.category_id, r.revenue desc




--