import pandas as pd

df = pd.read_csv("lenta_data_2.csv", sep=";")
df["order_dates"] = pd.to_datetime(df["order_dates"], errors="coerce")

start = "2019-01-01"
end = "2020-01-01"
df_2019 = df.query("@start <= order_dates < @end").copy()
# df_2019 = df[df["order_dates"].dt.year == 2019].copy()

df_2019["month"] = df_2019["order_dates"].dt.to_period("M").astype(str)

avg_check_by_month = (
    df_2019.groupby("month", as_index=False)
           .agg(avg_check=("order_values1", "mean"),
                orders_cnt=("order_values1", "size"))   # по желанию: число заказов
           .sort_values("month")
)

print(avg_check_by_month)
