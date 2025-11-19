# Задача
# написать ф-цию расчета факториала

x = 5


def factorial(x: int):
    if x < 0:
        raise ValueError('x < 0')
    if 0 <= x <= 1:
        return 1
    res = 1
    for i in range(2, x + 1):
        res *= i
    return res


print(factorial(x))




# Проверить список на палиндром

import math

l = [1,2,3,2,1]

def palindrom_l(l: list):
    l2 = list(reversed(l))
    return l == l2

print(palindrom_l(l))
print(l)




#
