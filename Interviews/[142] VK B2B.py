# 4

lst = [1, 1, 2, 3, 5, 8, 13]
print(lst[lst[4]])
# 8
#
# [lst[4]] -- 5 - элемент из списка с индексом 4
# [lst[5]] -- 8 - элемент из списка с индексом 5


# Задача 5
# Напишите программу, которая выводит все позиции списка Ist,
# на которых встречается число b.
# Номера позиций должны быть выведены одной строкой через пробел

l = [5, 8,2,7,8,8,2,4]
b = 8

def position_n(l:list, b):
    s = ''
    for i in range(len(l)):
        if l[i] == b:
            s += str(i) + ' '
    return s

print(position_n(l,b))



#6
# Посчитать сумму покупок и средний чек в каждой категории

import pandas as pd


df = pd.DataFrame({'category': ['A' , 'B' , 'B', 'A', 'A', 'B'],
                   'amount': [380., 370., 24., 26., 100., 45.17]})


a = df.groupby('category').agg(sum_amount=('amount','sum'), avg=('amount','mean')).reset_index()
print(a)

#