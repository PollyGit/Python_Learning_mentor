# 3

df['col'] = df['col'].map(lambda x: 1 if x=='test' else 0)

Берёт каждое значение в колонке col.Если значение равно "test" → ставит 1, иначе 0.
Результат записывает обратно в df['col'] (колонка станет из 0/1).


df = df.apply(lambda x: 1 if x['col']=='test' else 0, 1)
в конце 1 означает axis=1, то есть по строкам
В каждой строке заменяет значение в колонке col на 0 или 1.
В результате df останется не таблицей, а столбцом с колонкой 'col'


# 4

import pandas as pd
import numpy as np

df = pd.read_csv('table.csv')

df['event_dt'] = pd.to_datetime(df['event_dt'], errors='coerce')
df['revenue'] = df['amount']*df['price']
out = df.groupby('store').agg(
    total_revenue=('revenue', 'sum'),
    uniq = ('item', 'nunique'),
    avg_price=('price', 'mean')
).reset_index()

print(out)

# 5

sorted(
    zip([1230930093, 123630960960, 123960132511],
        ['Maxim A.', 'Alexander P.', 'Ilya R.']),
    key=lambda x: x[1],
    reverse=True
)

массив кортежей
[
 (1230930093, 'Maxim A.'),
 (123630960960, 'Alexander P.'),
 (123960132511, 'Ilya R.')
]
сортируется по алфавиту в обратном порядке  Сортировка идет по второму элементу - по именам



[
 (1230930093, 'Maxim A.'),
 (123960132511, 'Ilya R.'),
 (123630960960, 'Alexander P.')
]



















#