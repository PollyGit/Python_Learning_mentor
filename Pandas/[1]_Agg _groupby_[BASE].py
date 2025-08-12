import pandas as pd


# [1] Задача
# Для каждого магазина найдите сумму, среднее значение и максимальные продаж по каждому продукту.

data = { 'product_id': [101, 102, 101, 103, 102, 101, 103],
         'store_id': [1, 1, 2, 1, 2, 2, 1],
         'sales': [5, 3, 9, 7, 2, 4, 8]
         }

df = pd.DataFrame(data)
print(df.head())

task1 = df.groupby(['store_id', 'product_id'])['sales'].agg(['sum', 'mean', 'max'])
print(task1)

# or
# Группировка и расчёты
result = df.groupby(['store_id', 'product_id']).agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    max_sales=('sales', 'max')
).reset_index()
print(result)



#[2] Задача
#Посчитайте количество сессий и кол-во уник. пользователей для каждого типа устройств в США
#Датафрейм df columns: ‘User_id’ 'Device' 'Region'  'Channel' 'Session Start' 'Session End'


# Пример DataFrame
data = {
    'User_id': [1, 2, 1, 3, 4, 2, 5],
    'Device': ['Mobile', 'Desktop', 'Mobile', 'Tablet', 'Mobile', 'Desktop', 'Tablet'],
    'Region': ['USA', 'USA', 'Canada', 'USA', 'USA', 'USA', 'Canada'],
    'Channel': ['Email', 'Search', 'Search', 'Email', 'Search', 'Email', 'Email'],
    'Session Start': ['2023-02-01 10:00', '2023-02-01 11:00', '2023-02-02 12:00', '2023-02-01 13:00', '2023-02-01 14:00', '2023-02-02 15:00', '2023-02-01 16:00'],
    'Session End': ['2023-02-01 10:30', '2023-02-01 11:30', '2023-02-02 12:30', '2023-02-01 13:30', '2023-02-01 14:30', '2023-02-02 15:30', '2023-02-01 16:30']
}

df = pd.DataFrame(data)

df_usa = df[df['Region'] == 'USA']
task2 = df_usa.groupby('Device').agg(
    {'User_id': 'nunique',
     'Session Start': 'count'}
).reset_index()

# or
task2_2 = df_usa.groupby('Device').agg(
    unique_users=('User_id', 'nunique'),
    session_count=('Session Start', 'count')
).reset_index()


# [3] Задача
# Вам дан датафрейм df со следующими столбцами
# - user_id
# - product_id
# - revenue (выручка)
# Напишите скрипт, который выдаст сумму по revenue для каждого пользователя

data = {
    'user_id': [1, 1, 2, 2, 3],
    'product_id': [101, 102, 101, 103, 102],
    'revenue': [100, 200, 150, 300, 50]
}
df = pd.DataFrame(data)
task3 = df.groupby('user_id')['revenue'].sum().reset_index()
print(task3)


# [4] Задача
# у нас есть таблица с изменениями цен (product_id, new_price, change_date),
# и нужно определить цены на все продукты на 8 августа 2023 года, при условии,
# что до любых изменений цена равна 10.


def price_at_given_date(products):
    # 1) все изменения до даты '2023-08-09'
    before_target_date = products[products['change_date'] < '2023-08-09']
    # 2) последняя дата изменения на продукт
    df_max = (before_target_date.groupby('product_id')
              .agg(change_date=('change_date', 'max'))
              .reset_index())
    # 3) берём цену именно на последнем изменении
    last_prices = (before_target_date
                   .merge(df_max, on=['product_id', 'change_date'], how='inner')
                   [['product_id', 'new_price']])
    # 4) добавляем продукты, у которых не было изменений до даты ⇒ цена 10
    all_ids = products[['product_id']].drop_duplicates()
    res = all_ids.merge(last_prices, on='product_id', how='left')
    res['price'] = res['new_price'].fillna(10).astype(int)
    return res[['product_id', 'price']]



#[5] Задача
# Нужно посчитать ARPU отдельно по тесту и контролю:
# ARPU = (сумма GMV в группе) / (число пользователей в группе).
gmv_X_users = {1: 100, 2: 100, 3: 300, 4: 400, 5: 700, 6: 0}
test_users  = [1, 2, 6]

# Преобразуем данные в DataFrame
# список кортежей
df = pd.DataFrame(list(gmv_X_users.items()), columns=["user_id", "gmv"])
# Отмечаем, кто в тестовой группе, создаем новый столбец
df['group'] = df["user_id"].apply(lambda x: 'test' if x in test_users else 'control')

# ARPU = (сумма GMV в группе) / (число пользователей в группе).
arpu_df = df.groupby('group').agg(
    total_gmv=('gmv', 'sum'),
    total_users=('user_id', 'count')
).reset_index()

arpu_df["ARPU"] = arpu_df["total_gmv"] / arpu_df["total_users"]
print(arpu_df)



# [6] Задача

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    count_employees = employee.groupby('managerId').size().reset_index('counted_employees')
    managers_with_5 = count_employees['managerId'][count_employees['counted_employees'] >= 5]
    result_df = managers_with_5.merge(employee, how='inner', left_on='managerId', right_on='id')
    return result_df['name']


# [7] Задача
# Найти:
# Общая сумма продаж
# День с максимальной продажей
# Средние продажи за неделю

data = {'День': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'Продажи': [200, 158, 400, 300, 250, 500, 600]}
df = pd.DataFrame(data)

sales_amount = df['Продажи'].sum()
max_sales_day = df.loc[df['Продажи'].idxmax(), 'День']
avr_sales = df['Продажи'].mean()

print("Общая сумма продаж:", sales_amount)
print("День с максимальной продажей:", max_sales_day)
print("Средние продажи за неделю:", avr_sales)






