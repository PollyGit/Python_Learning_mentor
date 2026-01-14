# 2
# Дан массив nums, содержащий n различных чисел в диапазоне [0, n]. Найдите единственное число из этого диапазона, которое отсутствует в массиве.

nums = [5, 3, 2, 0, 1, 4]

def find_x(l: list):
    n = len(l)
    l.sort()
    for i in range(0, n):
        if i != l[i]:
            return i
    return 'its ok'

print(find_x(nums))


# 3
# Есть df c 2умя полями: id (уникальный номер клиента), volume (сумма сделки).
# Нужно посчитать суммарный volume по каждому клиенту

out1 = df.groupby('id')['volume'].sum().reset_index(name ='amount')

# Нужно посчитать долю количества сделок по каждому клиенту от общего числа.

out2 = df['id'].value_counts(normalize=True).rename('share')
# or
df['deal_share_by_client'] = df.groupby('id')['id'].transform('size') / len(df)
# or






















#