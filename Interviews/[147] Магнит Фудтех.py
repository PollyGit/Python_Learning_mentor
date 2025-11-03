# Задача 3
#
# Является ли данная строка палиндромом.
# 'A man, a plan, a canal, Panama!'

import string

s = 'A man, a plan, a canal, Panama!'

def is_palindrom(s: str) -> bool:
    s1 = s[::-1].lower().translate(str.maketrans('', '', string.punctuation))
    return s1 == s

print(is_palindrom('sos'))
print(is_palindrom(s))