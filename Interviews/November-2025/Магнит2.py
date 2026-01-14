# 4
# определить, простое ли число

num = 5

def is_prime_number(num: int) -> bool:
    if isinstance(num, int) and num < 2:
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    else:
        return False


print(is_prime_number(num))


# 5

s = 'ssaaaafkaaaaaaa'

def func(s):
    n = 1
    x = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            n += 1
        else:
            x = max(n, x)
            n = 1
    return max(n, x)

print(func(s))



# 6
# 100 монет, 1 фальшивая с двумя орлами. Достали 1 монету, сверху орел. Какова вероятность, что это фальшивая монета?
#
# всего орлов 99 + 2 = 101 орел.
#
# Значит, верхняя сторона - одна из этих 101.
#
# Р = число орлов от фальшивой монеты / общее число орлов = 2/ 101 = 1.98%

for i in range(9, 10):
    if i % 2:
        print(i)
    else:
        break


#


