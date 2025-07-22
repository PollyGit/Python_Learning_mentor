# 1. Перевернуть строку
def reverse_string(s):
    return s[::-1]


my_str = 'iuld421'
print(reverse_string(my_str))


# 2. Проверить, является ли строка палиндромом
def is_palindrome(s):
    s = s.replace(' ', '').lower()
    s1 = s[::-1]
    return s1 == s


print(is_palindrome("madam"))  # True


# 3. Подсчитать количество вхождений символа в строку
def count_char(s, char):
    counter = 0
    for i in s:
        if i == char:
            counter += 1
    return counter


# or
def count_char2(s, char):
    return s.count(char)


print(count_char("hello", "l"))  # 2
print(count_char2("hello", "l"))  # 2


# 4. Удалить все гласные из строки
def remove_vowels(s):
    result = ''
    for i in s:
        if i not in 'aeiouyAEIOUY':
            result += i
    return result


# or
def remove_vowels2(s):
    return ''.join(i for i in s if i not in 'aeiouyAEIOUY')


print(remove_vowels("hello"))  # "hll"
print(remove_vowels2("hello"))  # "hll"


# 5. Найти самое длинное слово в строке
def longest_word(s):
    my_list = s.split()
    longest_list = []
    longest = ''
    for i in my_list:
        if len(i) >= len(longest):
            longest_list.append(i)
            longest = i
    return longest_list


def longest_word(s):
    my_list = s.split()
    # длинная запись через цикл
    # m = []
    # for i in my_list:
    #     m.append(len(i))
    # max_length = max(m)

    # сокращенная запись этого цикла
    max_length = max(len(i) for i in my_list)

    # длинная запись через цикл
    my_longest_list = []
    # for i in my_list:
    #     if len(i) == max_length:
    #         my_longest_list.append(i)

    # сокращенная запись этого цикла
    my_longest_list = [i for i in my_list if len(i) == max_length]

    return my_longest_list


print(longest_word("hello world this is a test"))  # ["hello", "world"]


# 6. Заменить все пробелы в строке на подчеркивания
def replace_spaces(s):
    return s.replace(' ', '_')


print(replace_spaces("hello world"))  # "hello_world"


# 7. Удалить все цифры из строки
def remove_digits(s):
    s2 = ''
    for i in s:
        if i not in '1234567890':
            s2 += i
    return s2


# or: решение
def remove_digits2(s):
    return ''.join(i for i in s if i not in '1234567890')


print(remove_digits("hello123"))  # "hello"
print(remove_digits2("hello123"))  # "hello"


# 8. Вернуть первые n символов строки
def first_n_chars(s, n):
    return s[:n]


print(first_n_chars("hello", 3))  # "hel"


# 9. Сделать первую букву строки заглавной
def capitalize_first(s):
    return s[0].upper() + s[1:]


# or: решение
def capitalize_first2(s):
    return s.capitalize()


print(capitalize_first("hello"))  # "Hello"
print(capitalize_first2("hello"))  # "Hello"


# 10. Поменять местами первую и последнюю буквы строки
def swap_first_last(s):
    n = len(s)
    if n <= 1:
        return s
    return s[n - 1] + s[1:n - 1] + s[0]
    # or: решение
    # return s[-1] + s[1:-1] + s[0]


print(swap_first_last("hello"))  # "oellh"


# 11. Найти сумму элементов списка
def sum_list(lst):
    return sum(lst)


print(sum_list([1, 2, 3, 4]))  # 10


# 12. Найти максимальный и минимальный элементы списка
def min_max(lst):
    return max(lst), min(lst)


print(min_max([1, 2, 3, 4]))  # (1, 4)


# 13. Удалить дубликаты из списка
def remove_duplicates(lst):
    return list(set(lst))


print(remove_duplicates([1, 2, 3, 3, 4]))  # [1, 2, 3, 4]


# 14. Отсортировать список по убыванию
def sort_desc(lst):
    lst.sort(reverse=True)
    return lst
    # or: решение
    # return sorted(lst, reverse=True)


print(sort_desc([1, 4, 2, 3]))  # [4, 3, 2, 1]



# 15. Перевернуть список
def reverse_list(lst):
    lst.reverse()
    return lst
    # or: решение
    # return lst[::-1]


print(reverse_list([1, 2, 3, 4]))  # [4, 3, 2, 1]



# 16. Объединить два списка без дубликатов
def merge_lists(lst1, lst2):
    lst1.extend(lst2)
    return list(set(lst1))

# or: решение
def merge_lists2(lst1, lst2):
    return list(set(lst1 + lst2))

print(merge_lists([1, 2], [2, 3]))  # [1, 2, 3]
print(merge_lists2([1, 2], [2, 3]))  # [1, 2, 3]



# 17. Вернуть список только с четными числами
def even_numbers(lst):
    lst2 = []
    for i in lst:
        if i % 2 == 0:
            lst2.append(i)
    return lst2

# or: решение

def even_numbers2(lst):
    return [i for i in lst if i % 2 == 0]


print(even_numbers([1, 2, 3, 4]))  # [2, 4]
print(even_numbers2([1, 2, 3, 4]))  # [2, 4]



# 18. Посчитать количество положительных чисел в списке
def count_positive(lst):
    count = 0
    for i in lst:
        if i > 0:
            count += 1
    return count

# or: решение
def count_positive2(lst):
    return sum(1 for x in lst if x > 0)


print(count_positive([1, -2, 3, 4]))  # 3
print(count_positive2([1, -2, 3, 4]))  # 3

# 19. Создать список квадратов чисел
def square_numbers(lst):
    return [i**2 for i in lst]

print(square_numbers([1, 2, 3]))  # [1, 4, 9]



# 20. Объединить два списка в список кортежей
def pair_lists(lst1, lst2):
    return list(zip(lst1, lst2))

print(pair_lists([1, 2], ["a", "b"]))  # [(1, "a"), (2, "b")]

# 21. Проверить, является ли строка строкой с уникальными символами
def has_unique_chars(s):
    s1 = set(s)
    return len(s) == len(s1)

# or
def has_unique_chars2(s):
    seen = set()
    for c in s:
        if c in seen:
            return False
        seen.add(c)
    return True


print(has_unique_chars("abcdef"))  # True
print(has_unique_chars("aabbcc"))  # False

# 22. Найти индекс первого вхождения символа в строке
def first_occurrence(s, char):
    for i in range(len(s)):
        if s[i] == char:
            return i


# or
def first_occurrence2(s, char):
    return s.find(char)


print(first_occurrence("hello", "l"))  # 2
print(first_occurrence2("hello", "l"))  # 2


# 23. Проверить, является ли число простым
# Проверяем делители от 2 до корня из n — оптимизация
# (если число делится на что-то больше корня, то второй множитель уже меньше корня)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


print(is_prime(7))  # True
print(is_prime(4))  # False

# 24. Найти количество слов в строке
def word_count(s):
    return len(s.split())


print(word_count("hello   world"))  # 2

# 25. Найти наибольшее число из двух
def max_of_two(a, b):
    return max(a, b)

print(max_of_two(3, 5))  # 5


# 26. Найти наименьшее число из двух
def min_of_two(a, b):
    return min(a, b)

print(min_of_two(3,5))  # 3


# 27. Проверить, является ли строка числом
#для целых чисел
def is_number(s):
    return s.isdigit()

#для любых чисел
def is_number2(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


print(is_number("123"))  # True
print(is_number("abc"))  # False
print(is_number2("12.3"))  # True
print(is_number2("abc"))  # False


# 28. Найти длину строки
def string_length(s):
    return len(s)

print(string_length("hello"))  # 5


# 29. Найти индекс последнего вхождения символа в строке
def last_occurrence(s, char):
    s1 = s[::-1]
    return len(s) - 1 - s1.find(char)

# or
def last_occurrence2(s, char):
    for i in range(len(s) - 1, -1, -1):
        if s[i] == char:
            return i
    return -1

# or
def last_occurrence3(s, char):
    return s.rfind(char)


print(last_occurrence("hello", "l"))  # 3
print(last_occurrence2("hello", "l"))  # 3
print(last_occurrence3("hello", "l"))  # 3


# 30. Проверить, является ли строка пустой
def is_empty(s):
    return len(s.replace(' ', '')) == 0

print(is_empty("   "))  # True
print(is_empty("hello"))  # False


# 31. Перевести строку в нижний регистр
def to_lower_case(s):
    return s.lower()

print(to_lower_case("HELLO"))  # "hello"

# 32. Перевести строку в верхний регистр
def to_upper_case(s):
    return s.upper()

print(to_upper_case("hello"))  # "HELLO"

# 33. Найти разницу двух списков
def list_difference(lst1, lst2):
    return list(set(lst1)-set(lst2))

#or
def list_difference2(lst1, lst2):
    return [i for i in lst1 if i not in lst2]


print(list_difference([1, 2, 3], [2, 3, 4]))  # [1]
print(list_difference2([1, 2, 3], [2, 3, 4]))  # [1]


# 34. Найти индекс элемента в списке
def find_index(lst, value):
    return lst.index(value)

print(find_index([1, 2, 2, 3], 2))  # 1


# 35. Проверить, является ли число четным
def is_even(n):
    return n % 2 == 0

print(is_even(4))  # True
print(is_even(5))  # False

# 36. Проверить, является ли число нечетным
def is_odd(n):
    return n % 2 != 0

print(is_odd(5))  # True
print(is_odd(4))  # False


# 37. Найти второе по величине число в списке
def second_largest(lst):
    sorted_lst = sorted(lst, reverse=True)
    return sorted_lst[1]


#Если нужно без дубликатов
def second_largest2(lst):
    unique = list(set(lst))
    unique.sort(reverse=True)
    if len(unique) < 2:
        return None  # или выбросить ошибку
    return unique[1]


print(second_largest([1, 2, 3, 4]))  # 3
print(second_largest([1, 2, 3, 4, 4]))  # 3
print(second_largest([1, 2, 4, 3, 4, 4]))  # 3



# 38. Поменять местами два элемента списка
def swap_elements(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]
    return lst

print(swap_elements([1, 2, 3], 0, 2))  # [3, 2, 1]


# 39. Найти общие элементы двух строк

# если дубликаты нужны
def common_chars(s1, s2):
    return [x for x in s1 if x in s2]

# если дубликаты не нужны
def common_chars2(s1, s2):
    return list(set(s1) & set(s2))

def common_chars3(s1, s2):
    return set(s1).intersection(set(s2))


print(common_chars("abc", "bcd"))  # ['b', 'c']
print(common_chars2("abbbc", "bbbcd"))  # ['b', 'c']
print(common_chars3("abbbc", "bbbcd"))  # ['b', 'c']

# 40. Проверить, является ли число палиндромом
def is_number_palindrome(n):
    n1 = str(n)
    return n1[::-1] == n1

print(is_number_palindrome(121))  # True
print(is_number_palindrome(123))  # False


















