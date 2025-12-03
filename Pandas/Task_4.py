# https://wiki.yandex.ru/bestiarijj/zadachi-s-sobesedovanijj-v2/pandas/

import pandas as pd
import numpy as np
# 1
# Для каждого магазина найдите сумму, среднее значение и максимальные продаж по каждому продукту.


data = { 'product_id': [101, 102, 101, 103, 102, 101, 103], 'store_id': [1, 1, 2, 1, 2, 2, 1], 'sales': [5, 3, 9, 7, 2, 4, 8] }
df = pd.DataFrame(data)

out = df.groupby(['store_id', 'product_id'])['sales'].agg(['sum', 'mean', 'max']).reset_index()
print(out)


# [2] Задача
# Посчитайте количество сессий и кол-во уник. пользователей для каждого типа устройств в США
# Датафрейм df columns: ‘User_id’ 'Device' 'Region'  'Channel' 'Session Start' 'Session End'

df=df.query("Region == 'USA'")
out = df.groupby(['Device']).agg(
    cnt_session=('Session_Start', 'size'),
    cnt_User_id=('Session_Start', 'nunique'),
).reset_index()


# [3] Задача
# Вам дан датафрейм df со следующими столбцами
# - user_id
# - product_id
# - revenue
# Напишите скрипт, который выдаст сумму по revenue для каждого пользователя

out3 = df.groupby(['user_id'])['revenue'].sum().reset_index()


# [4] Задача
df['change_date'] = pd.to_datetime(df['change_date'])
df_filtered = df[df['change_date']<'2023-08-08']
df.groupby['product_id'].agg(
    change_date=('change_date':'max'),
    cnt_changes=('change_date':'count')
).reset_index()

df_filtered.merge(df, on=['product_id', 'change_date'], how='inner')
df_filtered.loc[df_filtered['cnt_changes'] < 2, 'new_price'] = 10

out4 = df_filtered[['product_id', 'new_price']]


# [5] Задача
gmv_x_users = {1: 100, 2: 100, 3: 300, 4: 400, 5: 700, 6: 600}
test_users = [1, 2, 6]

df = pd.DataFrame(list(gmv_x_users.items()), columns=["users", "gmv"])
df['group'] = df['users'].map(lambda x: 'B' if x in test_users else 'A')
arpu = df.groupby('group')['gmv'].mean().reset_index()
out5 = arpu[['group', 'arpu']]


# [6] Задача

manager_counts = employee.groupby('managerId').size().reset_index(name='direct_reports')
result = manager_counts[manager_counts['direct_reports'] >= 5]
result.merge(employee, left_on='managerId', right_on='id', how='inner')
result = result[['name']]


# [7] Задача

data = {'День': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'Продажи': [200, 158, 400, 300, 250, 500, 600]}
df = pd.DataFrame(data)

# 1. Общая сумма продаж
total_sales = df['Продажи'].sum()

# 2. День с максимальной продажей
max_sales_day = df.loc[df['Продажи'].idxmax(), 'День']
# max_sale_day= df['День'].loc[df['Продажи'].idxmax()]


# 3. Средние продажи за неделю
average_sales = df['Продажи'].mean()

# Вывод результатов
print(f"Общая сумма продаж: {total_sales}")
print(f"День с максимальной продажей: {max_sales_day}")
print(f"Средние продажи за неделю: {average_sales}")



# [1] Задача
data = { 'product_id': [101, 102, 101, 103, 102, 101, 103], 'store_id': [1, 1, 2, 1, 2, 2, 1], 'sales': [5, 3, 9, 7, 2, 4, 8] }
df = pd.DataFrame(data)
# Создать новый столбец, который будет содержать значение четное или нечетное в зависимости от store_id

df['odd'] = df['store_id'].map(lambda x:'четное' if x%2 ==0 else 'нечетное')



# [2] Задача
# Есть два столбца А и Б в датафрейме - сделать столбец С как среднее значение А и Б
df['c'] = df[['a', 'b']].mean(axis=1)




# [3] Задача
# Написать функцию по возведению в степень и применить ее к столбцу
# Пример DataFrame
data = {
    'A': [2, 3, 4, 5],
}

df = pd.DataFrame(data)

# Функция для возведения в степень
def power(x, exponent):
    return x ** exponent

# Применение функции к столбцу с указанием степени (например, 3)
df['A_powered'] = df['A'].apply(lambda x: power(x, 3))

print(df)












#