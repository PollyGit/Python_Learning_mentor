# Задача 1
# Выбрать уникальные элементы из списка;

l = [1, 5, 5, 8, 1]

# 1
l1 = list(set(l))
print(l1)

# 2
import numpy

l2 = numpy.unique(l)
print(l2)

# 3
l3 = []
for i in l:
    if i not in l3:
        l3.append(i)
print(l3)

# 4
l4 = list(dict.fromkeys(l))
print(l4)

# 5
# from toolz import unique
#
# l5 = unique(l)
# print(l5)


# Задача 2
# Что выведет? True
print(set('milannn') == set('nilam'))

# Задача 3
# Есть список из ключей к = [101, 102, 103,...]
# и значений v = [а, b, с, ...]. Нужно создать словарь

k = [101, 102, 103]
v = ['a', 'b', 'c']

d = dict(zip(k, v))
print(d)

# Задача 4
# Что выведет следующий код?
# список от 1 до 6: [1, 2, 3, 4, 5, 6]

example = [i + 1 for i in range(6)]
print(example)

# [0, 4, 3, 16, 5, 6]
# для каждого элемента списка выведет х, если он делится без остатка на 3 или 5,
# выведет х в квадрате, если четный, иначе выведет 0
x = 2
print(list(map(lambda x: x if ((x % 3 == 0) | (x % 5 == 0)) else x * x if x % 2 == 0 else 0, example)))

# Задача 5
# Будет ли разница в скорости выполнения кода?

# Долго. Создаёт новый список каждый раз. Это работает за O(n²) по времени
a = []
for i in range(10000):
    a = a + [i]

# Просто добавляет элемент в конец списка
a = []
for i in range(10000):
    a.append(i)


# Задача 6
# Что выведет следующий код?

def test(list_example):
    list_example.append(3)
    print(list_example)


var = [1, 2]

print(var)  # [1, 2]
test(var)  # [1, 2, 3]
print(var)  # [1, 2, 3]


# тк список - изменяемый тип


def test(text):
    text = '2'
    print(text)


var = '1'

print(var)  # 1
test(var)  # 2
print(var)  # 1

# тк строка - неизменяемый тип
