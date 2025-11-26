# Задача 1 (Кейс):
# Упала на графике конверсия в первую покупку за вчера - что будешь делать?



подтвердить факт, исключить ложную тревогу
→ локализовать, определелить сегмент, где не работает:  платформа, гео/язык, канал трафика, лэндинг,На каком шаге рост отвалов?
→ проверить технику/платежи/ассортимент/маркетинг/AB
→ подтвердить гипотезу, что сломалось именно там
→ быстрое исправление
→ мониторинг на будущее.


# # Задача 2
# **есть 2 df:**
#
# 1. **transactions:**
#     1. user_id
#     2. transaction_id
#     3. psp
#     4. amount
#     5. status
#     6. created_at
# 2. **users:**
#     1. user_id
#     2. brand
#     3. country
#     - Написать функцию которая определяет были ли вчера аномалии / поломки в платежной системе
#     - Выводит были ли аномалии в срезе стран / брендов / psp


# решение чат гпт


import pandas as pd
import numpy as np

# подготовка дат
transactions["created_at"] = pd.to_datetime(transactions["created_at"], errors="coerce")
transactions["day"] = transactions["created_at"].dt.date

# присоединим страну и бренд к транзакциям
tx = transactions.merge(users[["user_id", "brand", "country"]], on="user_id", how="left")

# нормализуем статус (подставь свой код "approved" / 1)
is_approved = tx["status"].astype(str).str.lower().isin(["1", "approved", "success"])
tx["approved"] = is_approved.astype(int)


# Дневные метрики по срезам
# Считаем по каждому дню и каждому срезу (включая “в целом”).
# “в целом”
g_all = (tx.groupby(["day"])
           .agg(approved=("approved","sum"), total=("transaction_id","count"))
           .assign(scope="all", key="all"))

# по PSP / бренду / стране
def rollup(col):
    return (tx.groupby(["day", col])
              .agg(approved=("approved","sum"), total=("transaction_id","count"))
              .rename_axis(index={"day":"day", col:"key"})
              .assign(scope=col))

g_psp    = rollup("psp")
g_brand  = rollup("brand")
g_country= rollup("country")

daily = pd.concat([g_all, g_psp, g_brand, g_country], axis=0).reset_index()
daily["apr"] = daily["approved"] / daily["total"].replace(0, np.nan)  # approval rate




# Вчера vs базовая линия (например, пред. 7 дней)
# вычислим вчера и окно базовой линии
yesterday = daily["day"].max()
baseline_start = pd.to_datetime(yesterday) - pd.Timedelta(days=7)
baseline_start = baseline_start.date()

# baseline: 7 дней ДО вчера (не включая вчера)
base = daily[(daily["day"] >= baseline_start) & (daily["day"] < yesterday)]

# агрегируем baseline по каждому (scope,key)
base_stats = (base.groupby(["scope","key"])
                   .agg(base_approved=("approved","mean"),
                        base_total=("total","mean"),
                        base_apr=("apr","mean"),
                        base_apr_std=("apr","std"))
                   .reset_index())

# вчерашние метрики
yest = daily[daily["day"] == yesterday][["scope","key","approved","total","apr"]]
yest = yest.rename(columns={"approved":"y_approved","total":"y_total","apr":"y_apr"})

# джоин вчера с baseline
res = yest.merge(base_stats, on=["scope","key"], how="left")


# падение > 70% по количеству
res["drop_approved"] = (res["base_approved"] - res["y_approved"]) / res["base_approved"].clip(lower=1)
res["rule1"] = res["drop_approved"] > 0.70

# z-score по apr
z = (res["y_apr"] - res["base_apr"]) / res["base_apr_std"].replace(0, np.nan)
res["rule2"] = z < -3

# итоговый флаг аномалии
res["anomaly"] = res[["rule1","rule2"]].any(axis=1)

# отсортируем, выведем только сработавшие
alerts = res.sort_values(["scope","anomaly"], ascending=[True, False])
alerts = alerts[alerts["anomaly"].fillna(False)]










# --