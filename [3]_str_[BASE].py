# 1 = 4
# Напишите функцию на Python,
# которая принимает на вход строку и возвращает максимальное
# количество подряд идущих одинаковых символов
# в этой строке.

s = 'aacaaffdddfffrrttggggg'

# 2
# алгоритм сжатия данных, заменяющий повторяющиеся символы на
# один символ и число его повторов

s2 = 'aaaabbbbbbbbrrrr'


# мое решение
def count_dubbled_letters(s):
    result = ''
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result += s[i - 1] + str(count)
            count = 1
    result += s[-1] + str(count)
    return result


# решение через список, тк
# При каждом += создаётся новая строка → это неэффективно при больших данных
def count_doubled_letters2(s):
    result = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(s[i - 1])
            result.append(str(count))
            count = 1

    # Добавить последний символ и его количество
    result.append(s[-1])
    result.append(str(count))

    return ''.join(result)


print(count_doubled_letters2("aaabbccccddeee"))  # a3b2c4d2e3


# ответ: решение задачи
def rle_encode(data):
    encoding = ''
    prev_char = ''
    count = 1

    if not data:
        return ''

    for char in data:
        # If the previous and current characters don't match...
        if char != prev_char:
            # ...then add the count and character to our encoding
            if prev_char:
                encoding += prev_char + str(count)
            count = 1
            prev_char = char
        else:
            # Or increment our counter if the characters do match
            count += 1
    else:
        # Finish off the encoding
        encoding += prev_char + str(count)
    return encoding


print(rle_encode(s2))
print(count_dubbled_letters(s2))

# 3
# Написать функцию, которая проверяет строчку на палиндром
# Например, “шалаш“ является палиндромом - читается одинаково с любой стороны

s3 = 'Abnnba'


# мое решение
def is_palindrom(s):
    s1 = s.lower().replace(' ', '')
    return s1 == s1[::-1]


print(is_palindrom(s3))
print(is_palindrom('Шалаш'))


# ответ: решение задачи
def is_palindrome(s: str) -> bool:
    # Убираем пробелы, приводим строку к нижнему регистру
    cleaned = ''.join(c for c in s if c.isalnum()).lower()

    # Проверяем посимвольно
    n = len(cleaned)
    for i in range(n // 2):
        if cleaned[i] != cleaned[n - 1 - i]:
            return False
    return True


# 4
# Напишите код, который выведет максимальную последовательность повторяющихся
# символов в строке (сам символ и кол-во повторений)
# Пример строки s = "aabbbccdddd"
# Рез-т: d 4


s4 = "aabbbccddddddd"


def max_dubbled_symbol(s: str) -> str:
    max_count = 0
    count = 1
    max_char = s[0]
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            if count > max_count:
                max_count = count
                max_char = s[i - 1]
            count = 1

    if count > max_count:
        max_count = count
        max_char = s[-1]

    return max_char + ' ' + str(max_count)


print(max_dubbled_symbol(s4))

# 5
# анаграма

s5 = 'пила'
s55 = 'липа'
s555 = 'плита'


def is_anagram(s1: str, s2: str) -> bool:
    s1 = s1.replace(' ', '').lower()
    s2 = s2.replace(' ', '').lower()
    return sorted(s1) == sorted(s2)


print(is_anagram('пила', 'липа'))


def anagramCheck(s1, s2):
    s1 = s1.replace(' ', '').lower()
    s2 = s2.replace(' ', '').lower()
    list1 = list(s1)
    list2 = list(s2)

    # через подсчет букв
    for i in list2:
        if list1.count(i) < list2.count(i):
            return False

    return True


print(anagramCheck('reddd', 'dred'))
