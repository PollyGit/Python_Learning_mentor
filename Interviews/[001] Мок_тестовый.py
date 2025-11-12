# Задача 4
# Написать функцию, которая проверяет, является ли строка палиндромом
# (палиндром - это строка, которая читается слева направо и справа налево одинаково)

import string

s = 'A man!'

def is_palindrom(s: str) -> bool:
    s1 = s[::-1].lower().translate(str.maketrans('', '', string.punctuation))
    return s1 == s

print(is_palindrom('sos'))  #True
print(is_palindrom(s))  #False

# Задача 5
# **Дан DataFrame**:
df_deliveries('order_id', 'customer_id', 'city', 'created_at', 'status', 'courier_type', 'items_cost', 'delivery_fee', 'promised_at', 'delivered_at')
#
# Выбрать заказы:
# - период: с `2025-08-01` по `2025-09-30` включительно по `created_at`;
# - города: `['Amsterdam','Rotterdam','Utrecht']`;
# - статусы: оставить `delivered` и `returned`;
# - тип курьера: только `bike` и `foot`;
# - суммарная стоимость (`items_cost + delivery_fee`) не менее 20.
#     Вернуть тот же набор колонок.

import pandas as pd

# вариант 1
res1 = df_deliveries.loc[
    pd.to_datetime(df_deliveries["created_at"], errors="coerce").between("2025-08-01", "2025-09-30", inclusive="both")
    & df_deliveries["city"].isin(["Amsterdam", "Rotterdam", "Utrecht"])
    & df_deliveries["status"].isin(["delivered", "returned"])
    & df_deliveries["courier_type"].isin(["bike", "foot"])
    & (df_deliveries["items_cost"] + df_deliveries["delivery_fee"] >= 20)
]

# вариант 2
# created_at приведём к дате отдельным шагом
df_deliveries["created_at"] = pd.to_datetime(df_deliveries["created_at"], errors="coerce")

res2 = df_deliveries.query(
    "created_at >= @pd.Timestamp('2025-08-01') and created_at <= @pd.Timestamp('2025-09-30')"
    " and city in ['Amsterdam','Rotterdam','Utrecht']"
    " and status in ['delivered','returned']"
    " and courier_type in ['bike','foot']"
    " and items_cost + delivery_fee >= 20"
)



# вариант 3

# 1) гарантируем, что created_at — datetime
df_deliveries["created_at"] = pd.to_datetime(df_deliveries["created_at"], errors="coerce")

# 2) соберём булевы маски
m_date = df_deliveries["created_at"].between("2025-08-01", "2025-09-30", inclusive="both")
m_city = df_deliveries["city"].isin(["Amsterdam", "Rotterdam", "Utrecht"])
m_status = df_deliveries["status"].isin(["delivered", "returned"])
m_courier = df_deliveries["courier_type"].isin(["bike", "foot"])
m_amount = (df_deliveries["items_cost"] + df_deliveries["delivery_fee"]) >= 20

# 3) финальный фильтр; возвращаем тот же набор колонок
res = df_deliveries.loc[m_date & m_city & m_status & m_courier & m_amount].copy()

print(res.head())
print("Итоговых заказов:", len(res))



# Задача 6
# - `df_invoices(invoice_id, customer_id, issued_at, currency, amount_currency)`
# — счета клиентам в разных валютах;
# - `df_fx(date, currency, rate_to_eur)` — ежедневные курсы валют к EUR.
#
# Для каждого счета подставить курс соответствующей валюты, действовавший
# на дату `issued_at`, и рассчитать сумму счета в евро. \
#     Вернуть: `(invoice_id, customer_id, issued_at, currency,
#                amount_currency, rate_to_eur, amount_eur)`

import pandas as pd

df_invoices["issued_at"] = pd.to_datetime(df_invoices["issued_at"], errors="coerce")
df_fx["date"] = pd.to_datetime(df_fx["date"], errors="coerce")

out = (df_invoices
       .merge(df_fx, left_on=["currency","issued_at"],
                     right_on=["currency","date"], how="left"))

out["amount_eur"] = out["amount_currency"] * out["rate_to_eur"]
out = out[["invoice_id","customer_id","issued_at","currency",
           "amount_currency","rate_to_eur","amount_eur"]]





# Если курсы валют есть НЕ НА КАЖДЫЙ ДЕНЬ
# 1) Даты в datetime
df_invoices["issued_at"] = pd.to_datetime(df_invoices["issued_at"], errors="coerce")
df_fx["date"] = pd.to_datetime(df_fx["date"], errors="coerce")

# 2) Отсортируем (merge_asof требует сортировки по ключевому времени)
df_invoices = df_invoices.sort_values(["currency", "issued_at"])
df_fx = (df_fx.sort_values(["currency", "date"])
               .drop_duplicates(subset=["currency", "date"], keep="last"))

# 3) Подставим курс на тот же день ИЛИ последний доступный ДО даты счета
#    by="currency" — asof по каждой валюте отдельно
res = pd.merge_asof(
    left=df_invoices,
    right=df_fx,
    left_on="issued_at",
    right_on="date",
    by="currency",
    direction="backward"   # взять ближайшую предыдущую дату курса
)

# 4) Посчитаем сумму в EUR
#    Предположение: rate_to_eur = сколько EUR за 1 единицу currency (умножаем).
#    Если у вас наоборот (EUR за 1 EUR в currency), замените на деление.
res["amount_eur"] = res["amount_currency"] * res["rate_to_eur"]

# 5) Вернём нужные колонки
out = res[[
    "invoice_id", "customer_id", "issued_at", "currency",
    "amount_currency", "rate_to_eur", "amount_eur"
]]

print(out.head())





# Задача 7
# 3) Продукт — события приложения
#
# **Дан DataFrame**:
# `df_events(user_id, event_time, event_name, screen, session_id, revenue)` — `revenue` указано только у событий оплаты.
#
# **Задача**
# Посчитать по каждой паре `(month, screen)`, где `month` — месяц по `event_time`:
#
# - `sessions_cnt` — количество уникальных `session_id`;
# - `users_cnt` — количество уникальных `user_id`;
# - `events_cnt` — общее число событий;
# - `revenue_sum` — сумма `revenue`;
# - `arpu` — `revenue_sum / users_cnt`;
# - `p90_session_events` — 90-й перцентиль количества событий на сессию для данного `(month, screen)`.
# Вернуть плоский DataFrame с колонками:
#  `month, screen, sessions_cnt, users_cnt, events_cnt, revenue_sum, arpu, p90_session_events`.

import pandas as pd
import numpy as np

# 0) Подготовка дат и месяца
df_events["event_time"] = pd.to_datetime(df_events["event_time"], errors="coerce")
df_events["month"] = df_events["event_time"].dt.to_period("M").astype(str)
# astype(str) превращает период в вид 'YYYY-MM'.
# Но можно не приводить (даже лучше не писать это, есл нет необходимости)

# revenue указано только у оплат — остальные NaN трактуем как 0
df_events["revenue"] = df_events["revenue"].fillna(0.0)

# 1) Базовые метрики по (month, screen)
base = (
    df_events.groupby(["month", "screen"])
    .agg(
        sessions_cnt=("session_id", "nunique"),
        users_cnt=("user_id", "nunique"),
        events_cnt=("user_id", "count"),
        revenue_sum=("revenue", "sum"),
    )
    .reset_index()
)

# 2) p90 количества событий на сессию по (month, screen)
#    Сначала посчитаем, сколько событий в каждой сессии внутри (month, screen)
sess_ev_counts = (
    df_events.groupby(["month", "screen", "session_id"])
    .size()  # число событий в этой сессии
    .rename("events_per_session")
)

# p90 по сессионным счетчикам внутри каждой (month, screen)
p90 = (
    sess_ev_counts.groupby(level=["month", "screen"])
    .quantile(0.90)
    .rename("p90_session_events")
    .reset_index()
)


# sess_ev_counts — это Series с MultiIndex: уровни индекса — (month, screen, session_id).
# groupby(level=[...]) говорит «группируй по указанным уровням индекса», а не по столбцам.
# Аналог с явными колонками (если сделать reset_index()):
tmp = sess_ev_counts.reset_index(name="events_per_session")
p90 = (tmp.groupby(["month","screen"])["events_per_session"].quantile(0.9))



# 3) Соединяем и считаем ARPU
out = base.merge(p90, on=["month", "screen"], how="left")

# ARPU = revenue_sum / users_cnt (защита от деления на ноль)
out["arpu"] = out["revenue_sum"].div(out["users_cnt"]).replace([np.inf, -np.inf], np.nan)

# или
out["arpu"] = out["revenue_sum"] / out["users_cnt"]
out.loc[~np.isfinite(out["arpu"]), "arpu"] = np.nan  # заменить inf/-inf

# или
out["arpu"] = np.divide(out["revenue_sum"], out["users_cnt"],
                        out=np.full(len(out), np.nan), where=out["users_cnt"]!=0)


# 4) Порядок колонок как в задании
out = out[
    ["month", "screen", "sessions_cnt", "users_cnt", "events_cnt",
     "revenue_sum", "arpu", "p90_session_events"]
]

print(out.head())


#