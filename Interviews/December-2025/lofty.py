# Задача 1. Объединение двух DataFrame
# Имеются два объекта pandas.DataFrame, в обоих содержится общий ключевой столбец user_id. Опишите, как в Pandas можно:
#
# выполнить объединение по ключу (аналог SQL JOIN);
# какие виды соединений поддерживаются (left, right, inner, outer);
# какими методами библиотеки pandas это реализуется.


import  pandas as pd


# 1
out1 = pd.concat([df1, df2], axis=1)

# 2
out2 = df1.merge(df2, how='left', on='user_id')

# 3
out3 = df1.set_index('user_id').join(df2.set_index('user_id'), how='outer').reset_index()

# Задача 2. Фильтрация по дате
# Дан DataFrame df с колонкой event_date в формате даты. Нужно отфильтровать строки только за одну конкретную дату, например '2024-01-01'.
#
# Опишите, как это сделать с помощью булевой индексации и/или методов .loc в Pandas.

# 1
this = pd.Timestamp('2024-01-01')
df = df.query("event_date == @this")


# 2
df = df.loc[df.event_date == '2024-01-01']
# 3
df = df.loc[df['event_date'] == this]




