# Задача 4
# Дана строка Str, посчитайте поличество вхождений символа j в строке без использования
# регулярных выражений.


s ='asvavnaiuvashvbsuvaojjevnasyvjhvb'
symbol = 'j'

def count_char(s: str, symbol: str):
    count_c = 0
    for i in s:
        if i == symbol:
            count_c += 1
    return count_c

print(count_char(s,symbol))










