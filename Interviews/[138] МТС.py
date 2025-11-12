# --Задача
# 4
# --
# --Строка
# называется
# строкой
# гласной, если
# она
# начинается
# с
# гласного
# символа
# --заканчивается
# символом
# гласного
# vowels = ['a', 'e', 'i', 'o', 'u'].
# --Есть
# список
# строк
# words, надо
# вернуть
# количество
# гласных
# строк
# words[i],
# --где
# і
# принадлежит
# к
# инклюзивному
# диапазону[left, right]
# списка
# слов.
# --Input
# words = ["hey", "aeo", ‘ mi’, "000", "artro"], left = 1, right = 4

vowels = ['a', 'e', 'i', 'o', 'u']
words = ["hey", "aeo", 'mi', '000', 'artro']
l = 1
r = 4


def func(words, vowels, l, r):
    words2 = []
    count = 0
    for i in range(l, r + 1):
        words2.append(words[i])
    print(words2)
    for j in words2:
        j = j.strip().lower()
        if j[0] in vowels and j[-1] in vowels:
            count += 1
    return count

print((func(words,vowels,l,r )))


#