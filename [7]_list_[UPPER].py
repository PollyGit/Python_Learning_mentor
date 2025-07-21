# 1
# Написать программу для определения правильности скобочной последовательности

s = '{ss[skks]d}'

# s1 = '{}[]()'
# s3 = ''
#
# for i in s:
#     if i in s1:
#         s3 += i
# s4 = ''.join(i for i in s if i in s1)
#
# print(s3)
# print(s4)

def is_valid_sequence(s):
    s1 = ''.join(i for i in s if i in '{}[]()')
    stack = []
    brackets = {')': '(', '}': '{', ']': '['}

    for i in s1:
        if i in brackets.values():  # Открывающие скобки
            stack.append(i)
        elif i in brackets.keys():  # Закрывающие скобки
            if stack and stack[-1] == brackets[i]:
                stack.pop()  # удалить открывающуюся скобку
            else:
                return False
    return not stack    # True если стек пуст, иначе False

print(is_valid_sequence(s))


# 2
# Написать функцию, которая преобразует список чисел так,
# чтобы на месте каждого элемента стояло произведение всех чисел, кроме него самого.

l = [7, 2, 3, 4, 5]

def product_except_self(l):
    # Создаем список для хранения результата
    result = [1] * len(l)

    # Вычисляем произведение всех элементов слева от текущего
    left_multiply = 1
    for i in range(0, len(l)):
         result[i] = left_multiply
         left_multiply *= l[i]

    # Вычисляем произведение всех элементов справа от текущего
    right_multiply = 1
    for i in range(len(l)-1, -1, -1):
        result[i] *= right_multiply
        right_multiply *= l[i]

    return result

print(product_except_self(l))



# 3
# Есть две roc кривые, которые заданы списком координат:
# Требуется написать скрипт, который считает площади под кривыми и выводит их разницу.
# Координаты упорядочены
# A = ((x_11, y_11), (x_12, y_12), …, (x_1n, y_1n))
# B = ((x_21, y_21), (x_22, y_22), …, (x_2m, y_2m))


A = [(0, 0), (0.1, 0.3), (0.2, 0.5), (0.3, 0.7), (1, 1)]
B = [(0, 0), (0.1, 0.2), (0.2, 0.4), (0.3, 0.6), (1, 0.9)]

# расчет площади по методу трапеций
def calculate_area(lst):
    S = 0
    for i in range(0, len(lst)-1):
        x1, y1 = lst[i]
        x2, y2 = lst[i+1]
        S += 0.5 * (x2 - x1) * (y2 + y1)
    return S

print('разность площадей кривых:  ', abs(calculate_area(A) - calculate_area(B)))





