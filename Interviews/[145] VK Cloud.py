# 3
# Есть данные по зарплатам сотрудников в разных департаментах.
# Необходимо вывести айди человека с максимальной зарплатой.

import pandas as pd

max_ids = df.loc[df('salary').idxmax(), 'emp_no']
print(max_ids)


# 4
# Задана строка S из малых латинских букв, требуется узнать
# длину наибольшей подстроки, в которой все буквы одинаковые.
s = 'cffbcccc'

def max_len(s:str):
    n = 1
    nmax = 0
    for i in range(1,len(s)):
        if s[i] == s[i-1]:
            n += 1
        else:
            nmax = max(nmax, n)
            n = 1
    return nmax

print(max_len(s))

# 5
# Задан список элементов. надо вывести первую пару которая
# в сумме выдаст число 7:

my_list = [1,2,3,4,5,7,8,5,10]

def find_couple(l:list, s:int):
    for i in range(0, len(l)):
        for j in range(i+1, len(l)):
            if l[i] + l[j] ==s:
                return (l[1], l[j])

print(find_couple(my_list, 7))


# or

def find_pair_sum(l: list, s: int):
    seen = set()
    for x in l:
        needed = s - x
        if needed in seen:
            return (needed, x)
        seen.add(x)
    return None
