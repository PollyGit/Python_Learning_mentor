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

















