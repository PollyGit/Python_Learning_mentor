import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Генерация случайных данных
np.random.seed(42)
n_rows = 1000

product_names = ["Ноутбук", "Смартфон", "Планшет", "Наушники", "Клавиатура", "Мышь", "Монитор", "Часы", "Колонка", "Флешка"]
categories = ["Электроника", "Аксессуары", "Гаджеты"]
customer_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Васильев", "Морозов", "Павлов", "Фёдоров", "Белов"]

sales_data = {
    "order_id": np.arange(1, n_rows + 1),
    "customer_name": np.random.choice(customer_names, n_rows),
    "product": np.random.choice(product_names, n_rows),
    "category": np.random.choice(categories, n_rows),
    "price": np.random.randint(500, 50000, n_rows),
    "quantity": np.random.randint(1, 5, n_rows),
    "order_date": [datetime.today() - timedelta(days=np.random.randint(1, 365)) for _ in range(n_rows)],
    "rating": np.round(np.random.uniform(1, 5, n_rows), 1),
}

df = pd.DataFrame(sales_data)
print(df.iloc[0:8].head(5))

customers = pd.DataFrame({
    "customer_name": customer_names,
    "city": ["Москва", "СПб", "Новосибирск", "Екатеринбург", "Казань",
             "Челябинск", "Омск", "Самара", "Ростов", "Уфа"]
})


# 1. Вывести 5 первых строк датасета.
print(df.iloc[0:5])

# 2. Определить количество уникальных товаров.
#uniq_products = df.product.nunique()
# df.product может конфликтовать с встроенным методом DataFrame.product()
# — это метод для перемножения значений

uniq_products = df['product'].nunique()
print(uniq_products)

# 3. Подсчитать количество заказов по каждому товару.
n_orders = df['product'].value_counts()
print(n_orders)

# 4. Найти товар с наибольшим количеством заказов.
print('наибольшее количество заказов:  ', n_orders.max())
print('4. товар с наибольшим количеством заказов:  ', n_orders.idxmax())


# 5. Найти среднюю цену каждого товара.
print('5. Найти среднюю цену каждого товара \n' , df.groupby('product')['price'].mean())

# 6. Вывести топ-5 самых дорогих товаров по средней цене.
mean_price = df.groupby('product')['price'].mean()
print('6. Вывести топ-5 самых дорогих товаров по средней цене \n', mean_price.sort_values(ascending=False).head(5))

# or: решение
print(df.groupby("product")["price"].mean().nlargest(5))

# 7. Найти суммарную выручку по каждому товару.
df["total_spent"] = df["price"] * df["quantity"]
print('7. Найти суммарную выручку по каждому товару \n', df.groupby('product')['total_spent'].sum())

# 8. Найти самый прибыльный товар.
print('8. Найти самый прибыльный товар \n', df.groupby('product')['total_spent'].sum().idxmax())

# 9. Определить, сколько заказов сделал каждый клиент.
print('9. Определить, сколько заказов сделал каждый клиент \n', df["customer_name"].value_counts())

# 10. Найти клиента, совершившего больше всего заказов.
print('10. Найти клиента, совершившего больше всего заказов \n', df["customer_name"].value_counts().idxmax())

# 11. Определить, какой клиент потратил больше всего денег.
df["total_spent"] = df["price"] * df["quantity"]
top_customer = df.groupby('customer_name')['total_spent'].sum().idxmax()
print('11. Определить, какой клиент потратил больше всего денег.\n', top_customer)

# 12. Определить средний чек заказа.
print('12. Определить средний чек заказа \n', round(df["total_spent"].mean(), 2))

# 13. Найти общее количество проданных товаров.
print('13. Найти общее количество проданных товаров \n', df['quantity'].sum() )

# 14. Определить товар с наибольшим общим количеством продаж.
print('14. Определить товар с наибольшим общим количеством продаж\n', df.groupby('product')['quantity'].sum().idxmax())

# 15. Найти средний рейтинг товаров.
print('\n',  )
print('15. Найти средний рейтинг товаров\n', df.groupby('product')['rating'].mean())
print('15. Найти средний рейтинг товаров\n', round(df["rating"].mean(), 2))


# 16. Определить, какой товар имеет самый высокий средний рейтинг.
print('16. Определить, какой товар имеет самый высокий средний рейтинг \n', df.groupby('product')['rating'].mean().idxmax())


# 17. Определить, какой товар имеет самый низкий средний рейтинг.
print('17. Определить, какой товар имеет самый низкий средний рейтинг \n', df.groupby('product')['rating'].mean().idxmin())


# 18. Найти процент товаров с рейтингом ниже 3.
avg_rating = df.groupby('product')['rating'].mean()
print('18. Найти процент товаров с рейтингом ниже 3\n', (df[df["rating"] < 3].shape[0] / df.shape[0]) * 100)


# 19. Определить день недели с наибольшим количеством заказов.
# Добавляем столбец с названием дня недели
df["weekday"] = df["order_date"].dt.day_name()
сount_orders = df["weekday"].value_counts()
print('19. Определить день недели с наибольшим количеством заказов \n', сount_orders.idxmax())


# 20. Определить, в каком месяце было больше всего заказов.
df["month"] = df["order_date"].dt.month_name()
print('20. Определить, в каком месяце было больше всего заказов\n', df["month"].value_counts().idxmax() )


# 21. Подсчитать количество заказов по дням недели.
df["weekday"] = df["order_date"].dt.day_name()
print('21. Подсчитать количество заказов по дням недели.\n', df.groupby('weekday').size())
# or
# print(df["weekday"].value_counts())


# 22. Найти количество заказов по месяцам.
print('22. Найти количество заказов по месяцам \n', df['order_date'].dt.month.value_counts() )


# 23. Определить средний рейтинг товаров по категориям.
print('23. Определить средний рейтинг товаров по категориям \n', df.groupby('category')['rating'].mean() )


# 24. Найти топ-3 клиентов с наибольшей суммой заказов.
df['order_sum'] = df['price'] * df['quantity']
print('24. Найти топ-3 клиентов с наибольшей суммой заказов\n', df.groupby('customer_name')['order_sum'].sum().nlargest(3) )
# or
#print(df.groupby("customer_name")["total_spent"].sum().nlargest(3))


# 25. Определить среднее количество товаров в заказе.
print('25. Определить среднее количество товаров в заказе\n', df['quantity'].mean() )


# 26. Найти процент заказов с более чем 3 товарами.
print('26. Найти процент заказов с более чем 3 товарами\n', (df[df['quantity'] > 3].shape[0] / df.shape[0]) * 100.0 )


# 27. Определить, сколько заказов было сделано за последние 30 дней.
past = datetime.now() - timedelta(days=30)  # дата 30 дней назад
print('27. Определить, сколько заказов было сделано за последние 30 дней \n', df[df['order_date'] >= past].shape[0] )


# 28. Найти день с наибольшей выручкой.
df['order_sum'] = df['price'] * df['quantity']
df.groupby(df['order_date'].dt.date)['order_sum'].sum().idxmax()
print('28. Найти день с наибольшей выручкой\n', df.groupby(df['order_date'].dt.date)['order_sum'].sum().idxmax() )


# 29. Определить месяц с наибольшей выручкой.
df['order_sum'] = df['price'] * df['quantity']
df.groupby(df['order_date'].dt.to_period('M'))['order_sum'].sum().idxmax()
print('29. Определить месяц с наибольшей выручкой\n', df.groupby(df['order_date'].dt.to_period('M'))['order_sum'].sum().idxmax() )

# or: решение
df['order_date_month'] = df.order_date.map(lambda x: x.strftime('%Y.%m'))
most_profitable_month = df.groupby('order_date_month').order_sum.sum().idxmax()
print(most_profitable_month)

# 30. Найти самый популярный товар в каждом месяце.
# Группировка по месяцу и товару, суммируем количество
#создаёт объект «год-месяц»
df["order_month"] = df["order_date"].dt.to_period("M")
# считает, сколько раз товар встречался в каждом месяце.
# превращает результат в DataFrame с колонкой order_count
group_by_month_product = df.groupby(["order_month", 'product'])["quantity"].sum().reset_index(name="order_count")
# находит индекс товара с наибольшим числом заказов в каждом месяце.
most_popular_per_month = group_by_month_product.loc[group_by_month_product.groupby("order_month")["order_count"].idxmax()]

print('30. Найти самый популярный товар в каждом месяце\n', most_popular_per_month )

# or: решение
# Добавим столбец с месяцем в формате 'YYYY-MM'
df['month'] = df['order_date'].dt.to_period('M')
# Группировка по месяцу и товару, суммируем количество
monthly_product_sales = df.groupby(['month', 'product'])['quantity'].sum().reset_index()
# Для каждого месяца находим товар с максимальной продажей
most_popular_products = monthly_product_sales.loc[
    monthly_product_sales.groupby('month')['quantity'].idxmax()
].reset_index(drop=True)
print(most_popular_products)


# 31. Добавить таблицу с городами клиентов и объединить её с основным DataFrame по имени клиента.
merged_df_31 = df.merge(customers, on='customer_name', how='left')
print('31. Добавить таблицу с городами клиентов\n', merged_df_31)

# 32. Объединить таблицу со средним рейтингом товара по названию продукта.
avg_rating = df.groupby('product')['rating'].mean().reset_index(name="avg_rating")
merged_df_32 = df.merge(avg_rating, on='product', how='left')
print('32. Объединить таблицу со средним рейтингом товара по названию продукта\n', merged_df_32 )

# 33. Найти клиентов, которые заказывали только один уникальный товар, и
# объединить с основным DataFrame.
n_uniq_products = df.groupby('customer_name')['product'].nunique().reset_index(name="product_count")
customer_with_uniq_prod = n_uniq_products[n_uniq_products['product_count'] == 1]
df_uniq_prod = df.merge(customer_with_uniq_prod['customer_name'], on='customer_name')
print('33. Найти клиентов, которые заказывали только один уникальный товар\n', df_uniq_prod  )

# or: решение
unique_products = df.groupby("customer_name")["product"].nunique().reset_index(name="product_count")
one_product_customers = unique_products[unique_products["product_count"] == 1]
df_one_product = df.merge(one_product_customers[["customer_name"]], on="customer_name")
print(df_one_product)


# 34. Получить описательную статистику по всем числовым столбцам основного DataFrame.
print('34. Получить описательную статистику\n', df.describe() )


# 35. Получить описательную статистику по цене и количеству в разрезе категорий.
print('35. Получить описательную статистику по цене и количеству в разрезе категорий\n', df.groupby('category')[['price', 'quantity']].describe() )


# 36. Найти товары с наибольшим средним чеком (цена × количество).
df["total"] = df["price"] * df["quantity"]
avg_check = df.groupby("product")["total"].mean().sort_values(ascending=False)
print('36. Найти товары с наибольшим средним чеком\n', avg_check)

# 37. Построить корреляционную матрицу для всех числовых столбцов.
corr_matrix = df.corr(numeric_only=True)
print('37. Построить корреляционную матрицу \n', corr_matrix)

# 38. Найти три признака с наибольшей корреляцией по модулю с total (цена × количество).
correlations = df.corr(numeric_only=True)["total"].drop(["total", 'order_sum', 'total_spent']).abs().sort_values(ascending=False)
print('Найти три признака с наибольшей корреляцией по модулю с total\n', correlations.head(3) )


# 39. Вычислить корреляцию между количеством (quantity) и рейтингом (rating).
corr_quantity_rating = df[["quantity", "rating"]].corr().iloc[0, 1]
corr_quantity_rating2 = df["quantity"].corr(df["rating"])
print('39. Вычислить корреляцию между количеством (quantity) и рейтингом (rating) \n', corr_quantity_rating )
print('39. Вычислить корреляцию между количеством (quantity) и рейтингом (rating) \n', corr_quantity_rating2 )


# 40. Визуализировать тепловую карту корреляций с помощью seaborn.
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))  # задаём размер графика
sns.heatmap(df.corr(numeric_only=True).drop(['order_sum', 'total_spent']), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Корреляционная матрица", fontsize=14)
plt.show()
print('\n',  )

# тепловая карта, которая показывает только корреляции с order_sum
# Считаем корреляции с order_sum и превращаем в DataFrame для тепловой карты
target_corr = df.corr(numeric_only=True)[["order_sum"]].drop(['order_sum', 'total_spent']).sort_values(by="order_sum", ascending=False)

# Рисуем тепловую карту
plt.figure(figsize=(4, 6))
sns.heatmap(target_corr, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
plt.title("Корреляции с order_sum", fontsize=14)
plt.show()
