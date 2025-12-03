import pandas as pd

data = {
    "date": pd.to_datetime(["2025-07-01","2025-07-01","2025-07-02","2025-07-02","2025-07-02"]),
    "store": ["A","A","B","A","B"],
    "item":  ["Phone","Case","Phone","Laptop","Case"],
    "qty":   [1, 3, 2, 1, 5],
    "price": [700, 20, 680, 1200, 18],
    "customer": ["u1","u2","u1","u3","u4"],
}
df = pd.DataFrame(data)
df["revenue"] = df["qty"] * df["price"]




# --------
# A. Основа
# Показать размер, типы и первые 3 строки.
print(df.dtypes)
print(df.head(3))
print(df.shape)


# Сколько уникальных item и store
print(df['item'].nunique())
print(df['store'].nunique())

# Отсортируй по revenue по убыванию и выведи топ-3.
df.sort_values(['revenue'], ascending=[False])
# or
top3 = df.nlargest(3, "revenue")
print(top3)

# Оставь только строки, где price >= 100
df_filtered = df.query("price >= 100").copy()
print(df_filtered)

# Добавь столбец is_phone = 1, если item == "Phone", иначе 0 (без apply).
df["is_phone"] = (df["item"] == "Phone").astype(int)
print(df[["item", "is_phone"]].head())

# -------
# B. Группировки (20–25 мин)
# По каждому store: orders (кол-во строк), units (сумма qty), revenue (сумма).

result = (
    df.groupby("store").agg(
        orders=("date", "count"),
        units=("qty", "sum"),
        revenue=("revenue", "sum"),   # без пробела в "sum"
    )
    .reset_index()
)
print(result)

# Доля выручки каждого item внутри своего store
# (столбец на уровень строки, через transform).
total_by_store = df.groupby('store')['revenue'].transform('sum')
df['share'] = df['revenue']/total_by_store
print(df['share'])


# Для каждого customer посчитай средний чек (среднее revenue) и выведи топ-2.
avg_check = df.groupby('customer')['revenue'].mean().rename("avg_check").nlargest(2)


# Для каждого store посчитай взвешенную цену: sum(revenue)/sum(qty).
wavg = df.groupby("store").agg(rev=("revenue","sum"), qty=("qty","sum"))
wavg["weighted_avg_price"] = wavg["rev"] / wavg["qty"]
wavg = wavg.reset_index()[["store", "weighted_avg_price"]]
print(wavg)

# -------
# D. Даты (10–15 мин)
# Сгруппируй дневную выручку: по date суммарный revenue.
day_rev = df.set_index('date').resample('D')['revenue'].sum().reset_index(name="daily_revenue")


# Добавь month = date.dt.to_period("M") и посчитай выручку по месяцам.
month_rev = df.set_index('month').resample('M')['revenue'].sum().reset_index(name="monthly_revenue")

# or
df["month"] = df["date"].dt.to_period("M")
monthly = (df.groupby("month")["revenue"].sum()
             .reset_index(name="monthly_revenue"))


# Топ-день по выручке для каждого store

g = df.groupby(['store', 'date'])['revenue'].sum()
idx = g.groupby(level=0).idxmax() # максимум по каждой store
top_day_per_store = g.loc[idx].reset_index(name="top_day_revenue")

# or
top_day_per_store2 = (
    df.groupby(["store", "date"])["revenue"].sum().reset_index()
      .sort_values(["store", "revenue"], ascending=[True, False])
      .groupby("store", as_index=False).head(1)
      .rename(columns={"revenue": "top_day_revenue"})
)










# v