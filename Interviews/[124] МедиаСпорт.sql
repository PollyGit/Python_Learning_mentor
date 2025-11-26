--Для каждой строки посчитайте и подтяние новой колонкой скользящее среднемесячное дохода с окном в 3 предыдущих месяца
--без учета текущего (если вы в сентябре, то среднее от тоталов по трем летним месяцам).



with
month_transactions as (
    select date_trunc('month', date) as m_date, sum(income) as m_sum
    from transactions
    group by date_trunc('month', date)
),
avg_inc as (
select m_date,
        avg(m_sum)  over(order by m_date rows between 3 preceding and 1 preceding) as avg_income
from month_transactions
)

select t.id, t.date, t.income, a.avg_income
from transactions t
left join avg_inc a
on date_trunc('month', t.date) = a.m_date




















--