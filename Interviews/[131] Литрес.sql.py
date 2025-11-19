# --1
# --1)Найти топ-15 жанров по суммарной выручке за 2024 год.
# --Вывести жанр, общее количество покупок и суммарную выручку
#
#
# select  genre,
#         sum(amount) as total_sum,
#         count(*) as cnt_orders
# from sales s
# join books b
#     on s.art_id = b.art_id
# where date_part('year', sale_dt) = 2024
# group by genre
# order by total_sum desc
# limit 15;


import pandas as pd

# 1. Фильтр по 2024 году (предполагаем, что sale_dt уже datetime)
sales['sale_dt'] = pd.to_datetime(sales['sale_dt'])
sales_2024 = sales['sale_dt'].query('sale_dt.dt.year == 2024')

# 2. Джойн с books
sales_books = sales_2024.merge(
    books[['art_id', 'genre']],
    on='art_id',
    how='left'
)

# 3. Группировка
genre_stats = sales_books.groupby('genre').agg(
    total_sum=('amount', 'sum'),
    cnt_orders=('amount', 'size')
)

# 4. Сортировка — топ-15
top15_genres = (
    genre_stats
    .sort_values('total_sum', ascending=False)
    .head(15)
)

print(top15_genres)

#