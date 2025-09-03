# Задача 2
# перевод кода sql запроса на питон пандас

import pandas as pd

# Предположим, у тебя уже есть DataFrame T
# T содержит колонки: 'id', 'moment', 'status'
# moment — это datetime

# Фильтруем только события 2006 года
T_2006 = T[T['moment'].dt.year == 2006]

# Разделяем на две таблицы по статусу
a_status = T_2006[T_2006['status'] == 'a'][['id', 'moment']].rename(columns={'moment': 'date_a'})
s_status = T_2006[T_2006['status'] == 's'][['id', 'moment']].rename(columns={'moment': 'date_s'})

# Джоиним по id
merged = pd.merge(a_status, s_status, on='id', how='inner')

# Оставляем только те, где s позже, чем a
merged = merged[merged['date_s'] > merged['date_a']]

# Считаем разницу в днях
merged['diff_days'] = (merged['date_s'] - merged['date_a']).dt.days

# Оставляем только задержанные (больше 3 дней)
delayed = merged[merged['diff_days'] > 3]

# Группируем по месяцу и считаем
delayed['month'] = delayed['date_s'].dt.month
result = delayed.groupby('month').size().reset_index(name='delayed_orders')

# Результат:
print(result)
