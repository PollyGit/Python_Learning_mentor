# 3
# построить таблицу ретеншена пользователей по дням с момента установки приложения

import pandas as pd
import  numpy as np

df = df.copy()
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')

installs = (df.query("event_type == 'install'").groupby('user_id')['event_date'].min()
         .rename(columns={'event_date': 'install_date'}))

df = df.merge(installs, on='user_id', how='inner')   # оставим только юзеров с install

# Нормализуем даты (.dt.normalize()), чтобы разница шла по календарным дням, а не по часам.
# 3) когорты = дата установки (день)
df['cohort'] = df['install_date'].dt.normalize()     # YYYY-MM-DD

# 4) считаем day_n: дни от установки до события (тоже по календарным дням)
df['event_day'] = (df['event_date'].dt.normalize() - df['install_date'].dt.normalize()).dt.days

# 5) учитывать активность как «любое событие, кроме install»
# активность считаем по факту сессии в день >= 0
active = df.query("event_type != 'install' and event_day >= 0")

# 6) размер когорты (сколько установок в день)
#  Сделаем колонку cohort = дата установки без времени
installs2 = installs.copy()
installs2["cohort"] = installs2["install_date"].dt.normalize()
# Посчитаем размер каждой когорты (уникальные пользователи)
cohort_size = installs2.groupby('cohort')['user_id'].nunique()


# 7) для каждой (cohort, day_n) считаем долю уникальных активных пользователей
ret = (active.groupby(['cohort', 'event_day'])['user_id'].nunique()  #Считаем, сколько уникальных пользователей активно в (cohort, event_day)
              .div(cohort_size)     # поделили на размер своей когорты
              .rename('retention')  #Оформим как таблицу с колонкой 'retention'
              .reset_index())


# 8) финальный «pivot»-шаг
# 8.1) Делаем «широко»: строки = cohort, колонки = event_day, значения = retention
ret_wide = ret.pivot(index="cohort", columns="event_day", values="retention")

# 8.2) Отсортировать когорты по дате (опционально, но удобно)
ret_wide = ret_wide.sort_index()

# 8.3) Убрать имя оси столбцов (чтобы сверху не висело 'event_day')
ret_wide = ret_wide.rename_axis(index="cohort", columns=None)

# 8.4) Переименовать числовые колонки 0,1,2 → 'day_0','day_1','day_2'
ret_wide.columns = [f"day_{int(c)}" for c in ret_wide.columns]

# 8.5) (необязательно) заполнить пропуски нулями и округлить для печати
ret_pivot = ret_wide.fillna(0).round(4)




#