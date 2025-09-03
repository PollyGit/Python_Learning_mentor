# 4
# является ли данная строка палиндромом.

def is_palindrom(s: str) -> bool:
    for i in [' ', ',', '!']:
        s = s.replace(i, '')
    s1 = s.lower()
    print(s1[::-1] == s1)

s = 'A man, a plan, a canal, Panama!'
is_palindrom(s)


# 5
#Представь, что мы работаем в компании которая делает рекламный движок.
# Нужно написать функцию, которая на вход принимает баннеры и веса, а на выходе отдает случайный
#баннер с вероятностью пропорциональной весу.

import random

banners = ['a', 'b', 'c']
weights = [1, 2, 3]


def probobility(b: list, w: list) -> tuple:
    p100 = sum(w)
    p = []
    # список вероятностей
    for i in w:
        p.append(round(i* 100.0 / p100, 2))

    # рандомное число на отрезке весов
    r = random.uniform(0, p100)
    cumulative_sum = 0
    # смотрим, на какой отрезок попало это число
    for i, j, k in zip(b, w, p):
        cumulative_sum += j
        if r <= cumulative_sum:
            return 'banner', i, 'weight', j, 'probobility', k
    # n = random.randint(0, len(b)-1)
    # return (b[n], p[n])

print(probobility(banners, weights))