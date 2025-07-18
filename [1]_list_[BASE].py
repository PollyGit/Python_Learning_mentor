# 1
# отсортировать список по принципу  RGB

my_list = ['black', 'blue', 'green', 'grey', 'red', 'rose']


def rgb(mu_list):
    r = []
    g = []
    b = []

    for word in my_list:
        if word.startswith('r'):
            r.append(word)
        elif word.startswith('g'):
            g.append(word)
        elif word.startswith('b'):
            b.append(word)

    r = sorted(r)
    g = sorted(g)
    b = sorted(b)

    return r + g + b


print(rgb(my_list))

# 2
# Даны две отсортированных по неубыванию последовательности целых чисел.
# Необходимо вернуть все элементы из первой последовательности, которых нет во второй.


lst1 = [1, 2, 3]
lst2 = [3, 4]

lst3 = []
for i in lst1:
    if i not in lst2:
        lst3.append(i)
print(lst3)
# or
lst3 = [i for i in lst1 if i not in lst2]
print(lst3)


# 3
# Напиши функцию even odd принимащую на вход один параметр limit.
# функция подуце вволить все числа между 0 и limit (вкл) и для каждого числа выводить
# четное оно или не четное

def even_odd(limit):
    for i in range(0, limit + 1):
        #        print(f"{i} {i % 2 == 0}") #0 True 1 False
        if i % 2 == 0:
            print(f"{i} is even")
        else:
            print(f"{i} is odd")


even_odd(3)  # 0 is even 1 is odd 2 is even 3 is odd

# 4
# Какой результат получится в результате выполнения скрипта?
#
# for i in (10):
#     print(i)
# TypeError: 'int' object is not iterable

# цикл должен идти по итерируемому объекту, а число 10 - не итерируемое
# Чтобы проитерировать по кортежу из 1 числа нужно:

for i in (10,):
    print(i)

# 5
# Какой результат получится в результате выполнения скрипта?
l = [1, 2, 3]
l.extend('abc')
# l.extend(range(1,3))
print(l)  # [1, 2, 3, 'a', 'b', 'c']

# 6
# Что выведет код?
a = [1, 2, [3], 4]
b = a[2]
b.append(10)  # [3, 10]

print(a)  # [1, 2, [3, 10], 4]


# a тоже изменяется, тк b ссылается на а, а не копирует его


# 7
# Написать код, который вытащит первый локальный минимум из массива х.
# Если локального минимума нет, то ничего не выводить.


def find_first_local_min(x):
    for i in range(1, len(x) - 1):
        if x[i] < x[i - 1] and x[i] < x[i + 1]:
            return x[i]
    return None


x = [1, 2, 1, 2, 3, 4, 5, 6]
print(find_first_local_min(x))

# 8
a = 2;
b = 6
a, b = b, a
print(a, '-', b)
# ответ:  6 - 2

c = ['1', '2', 3]
d = c
d.append(4)  # ['1', '2', 3, 4]
print(c, d)
# ответ:  ['1', '2', 3, 4],['1', '2', 3, 4]

print(['k' for k in range(9)])
# ответ: ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k']

s = 'y'
t = s;
t += '5'  # t = 'y5'
u = f'{s}' + '{s}'  # y{s}
print(s, t, u)
# ответ: y y5 y{s}


# lst2.intersection()
# print(dir(list))
