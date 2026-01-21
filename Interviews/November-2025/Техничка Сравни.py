# with tmp as (
#     select
#         user_id,
#         min(case when event_type = 'registration'    then event_time end) as reg,
#         min(case when event_type = 'first_purchase'  then event_time end) as first,
#         min(case when event_type = 'second_purchase' then event_time end) as second
#     from user_events
#     group by user_id
# ),
# tmp2 as (
#     select
#         user_id,
#         first  - reg   as diff_1,
#         second - first as diff_2
#     from tmp
#     where reg is not null
#       and first is not null
#       and second is not null
#       and reg < first
#       and first < second
# )
# select
#     avg(diff_1) as avg_diff_1,
#     avg(diff_2) as avg_diff_2
# from tmp2;

# user_events: колонки ['user_id','event_type','event_time']


import pandas as pd

df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

reg = df.query(" event_type = 'registration' ").groupby('user_id')['event_time'].min()
reg = reg.rename(columns={'event_time': 'reg'})

first = df.query("event_type = 'first_purchase'").groupby('user_id')['event_time'].min()
first = first.rename(columns={'event_time': 'first'})

second = (df.query("event_type = 'second_purchase'").groupby('user_id')['event_time'].min()
          .rename(columns={'event_time': 'second'}))

tmp = (reg.merge(first, how='inner', on='user_id')
          .merge(second, how='inner', on='user_id'))

tmp2 = tmp.query("reg < first and first < second").assign(
    diff_1=lambda d: d['first'] - d['reg'],
    diff_2=lambda d: d['second'] - d['first']
)

avg_diff_1 = tmp2['diff_1'].mean()
avg_diff_2 = tmp2['diff_2'].mean()

print(f' avg_diff_1: {avg_diff_1}')
print(f' avg_diff_2: {avg_diff_2}')







#