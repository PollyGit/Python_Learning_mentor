import pandas as pd
import datetime as dt

# [1] Задача
# Отформатировать датафрейм таким образом, чтобы в результате
# получилось 4 столбца:
# sategory, subcateranx, stock 2022, stock 2023

data = {
    'category': ['Цифровая техника', 'Цифровая техника', 'Цифровая техника', 'Цифровая техника',
                 'Бытовая техника', 'Бытовая техника', 'Бытовая техника', 'Бытовая техника'],
    'subcategory': ['Мобильные телефоны', 'Мобильные телефоны', 'Пылесосы', 'Пылесосы',
                    'Мобильные телефоны', 'Мобильные телефоны', 'Пылесосы', 'Пылесосы'],
    'stock': [1000, 1100, 2400, 2650, 1500, 1100, 900, 920],
    'year': [2022, 2023, 2022, 2023, 2022, 2023, 2022, 2023]
}

df = pd.DataFrame(data)

pivot_df = df.pivot_table(index=['category','subcategory' ],
                    columns='year',
                    values='stock',
                    aggfunc='sum').reset_index()
print(pivot_df)
pivot_df.columns = ['category','subcategory','stock_2022', 'stock_2023']
print(pivot_df)

pivot_df['diff_stock_%'] = round(((pivot_df['stock_2023'] - pivot_df['stock_2022']) / pivot_df['stock_2022']) * 100, 2)
print(pivot_df)



# [2] Задача


data_2 = {
    'order_date': ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15', '2023-03-01', '2023-03-15'],
    'city': ['Moscow', 'Moscow', 'Moscow', 'St. Petersburg', 'St. Petersburg', 'St. Petersburg'],
    'order_id': [1, 2, 3, 4, 5, 6]
}

df_2 = pd.DataFrame(data_2)
df_2['order_date'] = pd.to_datetime(df_2['order_date'])
df_2['month'] = df_2["order_date"].dt.month_name()
print(df_2)

pivot_df_2 = df_2.pivot_table(index='city',
                              columns='month',
                              values='order_id',
                              aggfunc="count",
                              fill_value=0)
print(pivot_df_2)
pivot_df_2['sum_orders'] = pivot_df_2.sum(axis=1)
print(pivot_df_2)
pivot_df_2_div = pivot_df_2.div(pivot_df_2['sum_orders'], axis=0)
print(pivot_df_2_div)

