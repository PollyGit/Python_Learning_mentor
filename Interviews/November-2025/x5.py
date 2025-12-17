# 1
# группировка слов по анаграммам.

l = ["eat", "tea", "tan", "ate", "nat", "bat"]

def anagrams(l: list):
    anagram_dict = {}

    for i in l:
        j = sorted(i)
        key = ''.join(j)
        if key not in anagram_dict:
            anagram_dict[key] = [i]
        else:
            anagram_dict[key].append(i)
        l2 = list(anagram_dict.values())
    return l2

print(anagrams(l))





# 2
# 7 парней, 3 девушки
# Найти вероятность того, что случайно выбранные 3 человека будут - П.

ЧИсло Сочетаний без повторений выбора 3 человек из 10 :

С(10 3) = 10! / 3!(10-3)! = 8*9*10 / (2*3) = 120

Число сочетаний  без повторений = сколько способов выбрать 3 П изи 7 П:

С(7 3) = 35

Р = удачные исходы / все исходы  = С(7 3) / С(10 3) = 35/120= 0.29



#
