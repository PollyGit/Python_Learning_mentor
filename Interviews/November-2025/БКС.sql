--1
--Корабли
--
--Вероятности отразить атаки?
--
--М => P = 1X
--С => P = 2X
--Б => P = 3X
--
--Б или С и М.
--Какую конфигурацию выбрать?

A — С отразил атаку, P(С)=2x.  С не отразил: Р(-С) = 1−2x
B — М отразил атаку, P(М)=x.  М не отразил: Р(-М) = 1−x

Нужно найти P(С∪М):
P(никто не отразил)=(1−2x)(1−x)
P(что хоть кто-то отразил из М и С) = P(С∪М) = 1−(1−2x)(1−x) = 3x−2x^2

P(что  отразил  Б) = P(Б) = 3x

Теперь сравнить:
3x > 3x−2x^2

Всегда выгоднее выбрать один корабль Б ,чем конфигурацию С + М (при любом x>0)



--2
--- Как определить, что монетка честная?


    План эксперимента:

    1. Гипотеза
    H0::p=0.5 — монетка честная
    H1: p≠0.5 — монетка нечестная

    2. Выбираем уровень значимости α=0.05 (мы готовы в 5% случаев ошибочно обвинить честную монету)
    3. Определяем, какую нечестность мы хотим уметь ловить.  Напримр,
    мы хотим уметь отличить честную монету от нечестной монеты с вероятностью, например, p=0.6 или p=0.4.  То есть дельта = 0.1

    4. Задаём β = 0.2,  мощность 1−β=0.8 —> мы хотим в 80% случаев поймать нечестность, если она есть
    5. Считается размер выборки N. Сколько подбрасываний нужно?
    Для ее расчета нужны: α, β, р, р+-дельта

    Решение задачи:
    Мы подбрасываем монетку N=20000 раз.
    Наблюдаем 10 180 орлов.
    Проверяем H0:p=0.5 против H1:p!=0.5 при α=0.05.
    Считаем p-value биномиального теста.
    Если p-value<0.05, отвергаем H0, иначе — нет.



--3

--У нас есть таблички вида:
--Orders
--
--account_id|  order_id                                  | value            | order_dttm
--acc_1        aab662a6-4d72-476a-bf0b-667fd87dbae4        133.18             2004-05-23T14:25:10
--acc_2        17977547-52ef-4ef1-8ace-153a74ffae8a        18238.9            2007-11-12T17:20:15
--
--Где account_id – идентификатор счета, order_id – идентификатор транзакции, value – сумма транзакции,  order_dttm – время транзакции.
--
--Accounts
--
--user_id| account_id| deactivate_dttm
--user_1   acc_1       Null
--user_2   acc_2       2007-11-12T17:20:15
--
--Где user_id – идентификатор клиента, account_id – идентификатор счета,
--deactivate_dttm – время деактивации счета.
--
--Задачи:
--1) Найти долю людей, у которых все счета деактивированы.

with
cnt_all as (
    select count(distinct user_id) as cnt_all_clients
    from accounts
),
user_accs as (
    select user_id,
        count(*) as n_user_accs,
        count(*) filter (where deactivate_dttm is not null) as n_user_accs_deactive,
        count(*) - count(*) filter (where deactivate_dttm is not null) as n_user_diff
    from  accounts
    group by user_id
    having count(*) - count(*) filter (where deactivate_dttm is not null) = 0
),
cnt_deactive_clients as (
    select count(*) as cnt_deactive_clients
    from user_accs
)


select d.cnt_deactive_clients * 1.0 /  nullif(a.cnt_all_clients,0) as share
from cnt_all a
cross join cnt_deactive_clients d;


-- or
with users as (
    select
        user_id,
        bool_and(deactivate_dttm is not null) as all_deactivated
    from accounts
    group by user_id
)
select
    avg(all_deactivated::int)::numeric as share
from users;



--2) Найти долю людей, которые совершают большую часть сделок в "часы пик"


with
user_orders as (
    select a.user_id,
        o.order_id,
        (o.order_dttm::time >= time '18:00'
         and o.order_dttm::time <  time '22:00') as is_peak
    from orders o
    join accounts a
      using(account_id)
),
per_user as (
    select user_id,
        count(*) as total_orders,
        sum(is_peak::int) as peak_orders,
        avg(is_peak::int::numeric) as peak_share
    from user_orders
    group by user_id
)

select
    avg((peak_share > 0.5)::int::numeric) as share_users_majority_peak
from per_user;













--