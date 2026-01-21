--1
--необходимо для каждого пользователя рассчитать следующие метрики:
--
--recency – кол-во дней от последней транзакции (не важно успешной или нет)
--frequency – кол-во дней, в течение которых пользователь был “активным”
--(“активный” = минимум 1 успешная транзакция в этот день)
--monetary – общая сумма успешных транзакций
--success rate – доля успешных транзакций
--
--Структура данных transactions:
--
--user_id – идентификатор пользователя.
--txn_id – идентификатор транзакции.
--amount – сумма транзакции.
--operation_time – дата и время транзакции.
--status – статус транзакции ('OK' или 'Cancelled').

with
last_tr  as (
    select user_id,
    max(operation_time::date) as last_tr,
    (current_date - max(operation_time::date)) as recency,
    count(*) as cnt_tr
    from transactions
    group by user_id
),
ok_txn as (
    select
        user_id,
        operation_time::date as op_date,
        amount
    from transactions
    where status = 'OK'
),
frequency as (
    select user_id,
        count(distinct op_date) as frequency,
        sum(amount) as monetary,
        max(rn) as successful_tr
    from ok_txn
    group by user_id
)

select a1.user_id, a1.recency,
    a2.frequency, a2.monetary,
    a2.successful_tr * 1.0 / nullif(a1.cnt_tr, 0) as success_rate
from last_tr a1
left join frequency as a2
    using(user_id)



















--