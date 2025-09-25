--#1
--Даны таблицы
--sales (city, mnth, trx), гд city - город продажи, mnth - месяц продажи, trx - сумма продажи
--Нужно получить таблицу sales_sum (city, mnth, trx, trx_sum),
--где trx_sum - сумма продажи накопительным итогом по месяцам с начала года.


select *,
       sum(trx) over(partition by city
                    order by date_trunc('month', mnth) asc
                    rows between unbounded preceding and current row) as trx_sum
from sales
order by date_trunc('month', mnth)



--2
--Даны таблицы
--cur_tbl (dt, currency, cur_rate) - курсы валют на дату по курсу ЦБ.
--ЦБ публикует курсы только в рабочие дни, в вых и праздники курс равен курсу на последний рабочий день.
--trx_tbl (dt, currency, trx) - сумма транзакций, агрегированная до дня, в разрезе валют.
--Вывести сумму транзакций в рублях по курсу цб на каждый день

with
t1 as (
    select t.dt, t.currency, t.trx, c.dt_cur as , c.cur_rate
    from trx_tbl as t
    left join cur_tbl as c
        on t.currency=c.currency  and c.dt <= t.dt)

select dt, currency, trx,
        last_value(cur_rate) over(partition by dt, currency
                                  order by dt_cur
                                  rows between unbounded preceding and current row) as used_rate,
        trx * last_value(cur_rate) over(partition by dt, currency
                                  order by dt_cur
                                  rows between unbounded preceding and current row) as sum_rub
from t1



--3
--Вывести помесячно среднее, максимальное и минимальное количество и сумму транзакций по всем клиентам

select time_key,
       avg(trans_cnt)  as avg_trans_cnt,
       min(trans_cnt)  as min_trans_cnt,
       max(trans_cnt)  as max_trans_cnt,
       min(trans_amt)  as min_trans__amt,
       max(trans_amt)  as max_trans__amt,
       avg(trans_amt)  as avg_trans__amt,
from HISTORY_CLIENT_TRANS
group by time_key
order by time_key;


--Вывести распределение клиентов в январе 2024 по филиалам и банкам (в %, сумма должна равняться 100%)


with
january as (
    select *
    from HISTORY_CLIENT_TRANS
    where date_part('month', time_key) = 1
),
client_number as (
    select count(client_rk) as client_number
    from january
),
client_count as (
    select bank_id, market_key, count(*) as client_count
    from january
    group by bank_id, market_key
)

select bank_id, market_key, round(client_count * 100.0/n.client_number, 2) as percent_part
from client_count c
cross join client_number n




--Вывести клиентов, которые совершали транзакции в феврале 2024, но не совершали в марте


select client_rk
from HISTORY_CLIENT_TRANS
where date_part('month', time_key) = 2

except

select client_rk
from HISTORY_CLIENT_TRANS
where date_part('month', time_key) = 3

-- or
SELECT client_rk
FROM history_client_trans
WHERE time_key = DATE '2024-02-01'
  AND client_rk NOT IN (
      SELECT client_rk
      FROM history_client_trans
      WHERE time_key = DATE '2024-03-01'
  );