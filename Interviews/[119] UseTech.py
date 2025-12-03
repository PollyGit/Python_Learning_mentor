# Подключиться к БД - выгрузить в датафрейм -
# отрисовать распределение, посчитать метрики какин-нибудь,
# сохранить в эксель данные


# ответ с чат гпт

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine("postgresql+psycopg2://user:pass@localhost:5432/analytics")

sql = """
SELECT order_id, user_id, amount, created_at, device
FROM public.orders
WHERE created_at >= %(dt)s
"""
df = pd.read_sql(sql, engine, params={"dt": "2024-01-01"}, parse_dates=["created_at"])

df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["month"] = df["created_at"].dt.to_period("M").astype(str)

# график
df["amount"].hist(bins=40); plt.title("Amount distribution"); plt.show()

# метрики
metrics = df["amount"].agg(["count","mean","median","std","min","max"])
by_month = df.groupby("month", as_index=False).agg(revenue=("amount","sum"),
                                                   orders=("order_id","nunique"),
                                                   users=("user_id","nunique"),
                                                   avg_check=("amount","mean"))

with pd.ExcelWriter("report_orders.xlsx", engine="xlsxwriter") as xw:
    metrics.to_frame("value").to_excel(xw, sheet_name="metrics")
    by_month.to_excel(xw, sheet_name="by_month", index=False)
