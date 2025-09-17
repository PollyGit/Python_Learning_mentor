import pandas as pd

df = pd.DataFrame([
    ['11', 'genre1, genre2'],
    ['22', 'genre1'],
    ['33', 'genre1, genre2'],
    ['55', 'genre1, genre2'],
], columns=['id', 'genres']
)

print(df)

x = df['genres'].str.contains('genre1', na=False).sum()
y = df['genres'].str.contains('genre2', na=False).sum()
print(f'genre1, {x}')
print(f'genre2, {y}')

df2 = pd.DataFrame([
    ['genre1', x],
    ['genre2', y],
], columns=['genre', 'count_unique_movies'])
print(df2)


#or

# 1. Разделим жанры на списки
df['genres'] = df['genres'].str.split(',')
print(df)

# 2. "Развернём" строки по жанрам (explode)
df_exploded = df.explode('genres')
print(df_exploded)

# 3. Посчитаем уникальные id по каждому жанру
result = df_exploded.groupby('genres')['id'].nunique().reset_index()
print(result)

# 4. Переименуем столбцы
result.columns = ['genre', 'count_unique_movies']

# 5. (по желанию) Отсортируем по убыванию
result = result.sort_values(by='count_unique_movies', ascending=False)

print(result)

