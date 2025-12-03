# Задача 5
# **Дан DataFrame**:
# df_deliveries('order_id', 'customer_id', 'city', 'created_at', 'status', 'courier_type', 'items_cost', 'delivery_fee', 'promised_at', 'delivered_at')
#
# Выбрать заказы:
# - период: с `2025-08-01` по `2025-09-30` включительно по `created_at`;
# - города: `['Amsterdam','Rotterdam','Utrecht']`;
# - статусы: оставить `delivered` и `returned`;
# - тип курьера: только `bike` и `foot`;
# - суммарная стоимость (`items_cost + delivery_fee`) не менее 20.
#     Вернуть тот же набор колонок.
import numpy as np
import pandas as pd

df_deliveries['created_at']=pd.to_datetime(df_deliveries['created_at'], erors='coerse')

df_deliveries = df_deliveries.query(
    "created_at >= @pd.Timestamp('2025-08-01') and  created_at <= @pd.Timestamp('2025-09-30')"
    "and city in ['Amsterdam','Rotterdam','Utrecht']"
    "and status in ['delivered', 'return']"
    "and courier_type in ['bike', 'foot']"
    "items_cost + delivery_fee >= 20"

)



# Задача 6
# - `df_invoices(invoice_id, customer_id, issued_at, currency, amount_currency)`
# — счета клиентам в разных валютах;
# - `df_fx(date, currency, rate_to_eur)` — ежедневные курсы валют к EUR.
#
# Для каждого счета подставить курс соответствующей валюты, действовавший
# на дату `issued_at`, и рассчитать сумму счета в евро. \
#     Вернуть: `(invoice_id, customer_id, issued_at, currency,
#                amount_currency, rate_to_eur, amount_eur)`

df_invoices['issued_at'] = pd.to_datetime(df_invoices['issued_at'], error='coerce')
df_fx['date'] = pd.to_datetime(df_fx['date'], error='coerce')

out = df_invoices.merge(df_fx, how='left', df_invoices_on=['issued_at', 'currency'], df_fx_on=['date','currency'])
out['amount_eur']=out['amount_currency']*out['rate_to_eur']
print(out[["invoice_id","customer_id","issued_at","currency",
           "amount_currency","rate_to_eur","amount_eur"]])




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

import numpy as np

df_events['event_time'] = pd.to_datetime(df_events['event_time'], errors='coerce')
df_events['month'] = df_events['event_time'].dt.to_period('M')
df_events['revenue'] = df_events['revenue'].fillna(0.0)

# df_events['sessions_cnt'] = df_events.groupby([['month', 'screen']])['session_id'].nunique()
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
base['arpu'] = (base['revenue_sum'] / base['users_cnt']).replace([np.inf, -np.inf], np.nan)

df_events_per_session = df_events.groupby(["month", "screen", 'session_id'])['user_id'].size().rename('events_per_session')
df_events_per_session['p90_session_events'] = np.percentile(df_events_per_session['events_per_session'], q=90)

out = base.merge(df_events_per_session, how='left', base_on=["month", "screen"], df_events_per_session_on=["month", "screen"])
print(out[["month", "screen", 'sessions_cnt', 'users_cnt', 'events_cnt', 'revenue_sum', 'arpu', 'p90_session_events' ]])















#