# Задача 4
#
# написать Функцию, которая принимает список списков
# и делает из них одноуровневый список.


l = [[1, 2], [3], [12,87,99], [7]]

def unzip_list(l):
    l2 = []
    for i in l:
        for j in i:
            l2.append(j)
    return l2

l3 = [j for i in l for j in i]
print(l3)

print(unzip_list(l))




# Задача 5:

a = [1,2]
b = a
b[0] = 3
print(a)
# [3, 2]


# Задача 6:

a = [[1,2]]
b = a.copy()
b[0][0] = 3
print(a)
[[3, 2]]


#