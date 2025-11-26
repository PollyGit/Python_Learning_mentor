# Посчитать кол-во смен из первой задачи (скл запрос)
#
# with
# prepared as (
#  select
# 		src.*,
# 		row_number () over( partition by service_center order by dt asc)
# 	    - row_number () over ( partition by service_center, emloyee_name
# 	order by dt asc) as rn_diff
# 	from src
# ),
# result as (
# 	select
# 				service_center, emloyee_name,
# 				dt,
# 				row_number () over (
# 				partition by service_center, emloyee_name, r_diff
# 				order by dt asc
# 				) as rn
# 	from prepared
# 	order by dt asc)
#
# select service_center, sum(1) as cnt
# from result
# where rn=1
# group by service_center;

import pandas as pd


df = pd.DataFrame({
    "service_center": ["Южный", "Северный", "Северный", "Северный", "Северный", "Северный"],
    "emloyee_name":   ["Петров", "Иванов",   "Иванов",   "Иванов",   "Сидоров",  "Иванов"],
    "dt":             ["2022-01-01","2022-01-01","2022-01-02","2022-01-03","2022-01-04","2022-01-05"]
})

print(df.head(10))

df['dt'] = pd.to_datetime(df['dt'])
df['service_center'] = df['service_center'].str.strip()
df['emloyee_name'] = df['emloyee_name'].str.strip()


# sort like in SQL (partition/order by)
# Сбросить индекс, но НЕ сохранять его как столбец
df = df.sort_values(["service_center","emloyee_name","dt" ], ascending=[True, True,  True]).reset_index(drop=True)

# row_number() over (partition by service_center order by dt asc)
df['rn_sc'] = df.groupby(['service_center']).cumcount() +1
# row_number() over (partition by service_center, emloyee_name order by dt asc)
df['rn_sc_en'] = df.groupby(['service_center', 'emloyee_name']).cumcount() +1
# r_diff = rn_sc - rn_sc_emp  (same idea as in SQL CTE 'prepared')
df['rn_diff'] = df['rn_sc'] - df['rn_sc_en']

# row_number() over (partition by service_center, emloyee_name, r_diff order by dt asc)
# (we only need to know which rows start a run, i.e., rn == 1)
df['rn'] = df.groupby(['service_center', 'emloyee_name', 'rn_diff']).cumcount() +1

# final: count runs per service_center where rn == 1
out = (
    df.query("rn == 1")  # ==df.loc[df["rn"].eq(1)]
      .groupby("service_center")
      .agg(cnt=("rn", "size"))           # именованная агрегация
      .reset_index()
)

print(out)













#