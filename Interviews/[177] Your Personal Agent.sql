# Таблица bet_log - логирование каждой ставки, совершенной пользователем.
create table bet_log
(
    "userId"            integer           not null,
    "createdAt"         timestamp         not null,
    amount              bigint            not null,
    currency            text              not null,
    "gameId"            integer           not null,
    "usdCurrencyRate"   double precision  not null
    );

# Таблица win_log - логирование каждого выигрыша, полученного пользователем
create table win_log
(
    "userId"            integer           not null,
    "createdAt"         timestamp         not null,
    amount              bigint            not null,
    currency            text              not null,
    "gameId"            integer           not null,
    "usdCurrencyRate"   double precision  not null
    );
# Таблица tranzes_logs - логирование депозитов и выводов средств с лицевого счета
# пользователя, поле type принимает одно из двух значений(депозит/вывод)
create table tranzes_logs
(
    "userId"            integer     not null,
    "createdAt"         timestamp   not null,
    amount              bigint      not null,
    "isError"           boolean     not null,
    type                text        not null
);


--Задача 1
--# Написать скрипт SQL, позволяющий вычислить среднюю дельту по пользователям
--# между первым и вторым депозитом для пользователей, кто совершил минимум 2 депозита.

with
users as (
    select userId, count(*) as n_deposin
    from tranzes_logs
    where type = 'депозит' and isError = false
    group by userId
    having count(*) >= 2
),
rn as (
    select userId, amount, createdAt,
            row_number() over(partition by userId order by createdAt) as user_dep_rn
    from tranzes_logs tl
    join users u
        on tl.userId = u.userId
    where tl.type = 'депозит'
),
t1 as (
    select userId, amount, user_dep_rn as user_dep_rn_1
    from rn
    where user_dep_rn = 1
),
t2 as (
    select userId, amount, user_dep_rn as user_dep_rn_2
    from rn
    where user_dep_rn = 2
)

select userId, avg(t2.amount - t1.amount) as avg_diff_dep
from t1
join t2
    using(userId)




--Задача 2
--# Написать скрипт SQL, вычисляющий  долю средств,
--# которые пользователи проиграли от совершенных депозитов за последние 12 часов.

with
sum_dep_last_12h as (
    select sum(amount) as sum_dep
    from tranzes_logs
    where createdAt >= now() - interval '12 hours'
            and type = 'депозит'
            and isError = false
),
-- посчитатать: ставки − выигрыши
sum_bet_last_12h as (
    select sum(amount * usdCurrencyRate) as sum_bet
    from bet_log  --логирование каждой ставки
    where createdAt >= now() - interval '12 hours'
),
sum_win_last_12h as (
    select sum(amount * usdCurrencyRate) as sum_win
    from win_log  --логирование каждого выигрыша
    where createdAt >= now() - interval '12 hours'
)

select round(
        case
        when sum_dep= 0 then 0
        else (sum_bet-sum_win)/sum_dep
        end, 2
        ) as loss_ratio
from sum_dep_last_12h, sum_bet_last_12h, sum_win_last_12h