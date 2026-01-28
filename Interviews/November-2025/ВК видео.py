# --3

l1 = [1,5,1,4,5,9,3]

def  del_dubbles(l1):
    l2 = []
    for i in l1:
        if i not in l2:
            l2.append(i)
    return l2


print(del_dubbles(l1))


l3 = list(dict.fromkeys(l1))
print(l3)


# 4

# select a.campaign_id,
#     e.event_type,
#     count(e.event_id) as events_cnt
# from ads a
# left join events e
#   on e.ad_id = a.ad_id
# where e.event_id is not null
# group by a.campaign_id, e.event_type
# order by a.campaign_id, e.event_type;

merged = ads.merge(events, on='ad_id', how='inner')
out = (
    merged.groupby(['campaign_id', 'event_type'], as_index=False)
          .agg(events_cnt=('event_id', 'count'))
          .sort_values(['campaign_id', 'event_type'])
)







#