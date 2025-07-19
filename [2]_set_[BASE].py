# 1
# написать функцию func возврацаицую число пар одинаковых элементов
# на вход подается массив [1,2,1,2,1,1,5] на веходе мы получим 3
# так как возможно составить 3 пары [[1,1],[1,1], [2,2]]

x = [1, 2, 1, 2, 1, 1, 5]


def count_pairs(x):
    count = 0
    used_indexes = set()  # чтобы проверка наличия работала быстрее
    for i in range(len(x)):
        if i in used_indexes:
            continue  # Пропускаем уже использованные элементы
        for j in range(i + 1, len(x)):
            if x[j] == x[i] and j not in used_indexes:
                count += 1
                used_indexes.add(i)
                used_indexes.add(j)
                break  # Нашли пару, переходим к следующему элементу
    return count


print(count_pairs(x))



# 2
# Есть массив целых чисел и число К.
# Найти два таких (не обязательно различных) числа в массиве, сумма которых равна К,
# либо вывести, что таких чисел нет.

y = [2, 3, 3, 10]
k = 6

def find_number(y, k):
    for i in range(len(y)):
        for j in range(i+1, len(y)):
            if y[i] + y[j] == k:
                return y[i], y[j]
    return f'таких чисел нет'

print(find_number(y,k))

# or: решение

def find_number2(y, k):
    my_set = set()
    for i in y:
        number = k - i
        if number in my_set:
            return (number, i)
        my_set.add(number)
    return f'таких чисел нет'


print(find_number2(y,k))



# 3
# Получить пересечение этих двух списков без повторений
list_a = [1, 1, 2, 2, 3, 4, 4, 5]
list_b = [1, 2, 3, 4, 4, 5, 6, 18, 27]

def intersection_sets(a,b):
    a = set(a)
    b = set(b)
    return list(a.intersection(b))


print(intersection_sets(list_a,list_b))


# 4
# Получить уникальные элементы из списка

my_list = [1,2,1,2,3,4]
print(list(set(my_list)))

uniq_list = []
for i in my_list:
    if i not in uniq_list:
        uniq_list.append(i)
print(uniq_list)




