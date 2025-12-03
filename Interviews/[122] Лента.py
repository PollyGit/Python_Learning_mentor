# Задача 4
#
# Задание: дан словарь городов с их численностью населения:
# {
# 'Moscow: 10000000,
# 'Spb': 5000000,
# 'Ekb':5000000
# }
#
# Необходимо написать код, возвращающий название города с вероятностью, пропорциональной населению в нем

d = {'Moscow': 10000000, 'Spb': 5000000, 'Ekb':5000000}


import random

def func(d):
    return random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]


def func2(d):
    cities = list(d.keys())
    weights = list(d.values())
    return random.choices(cities, weights, k=1)[0]

d = {'Moscow': 10_000_000, 'Spb': 5_000_000, 'Ekb': 5_000_000}
print(func2(d))





#