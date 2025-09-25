# Написать функцию, в которой на вход подается число N,
# и она возвращает все простые числа до N включительно.

def simply_num(n: int):
    l = []
    for i in range(2, n+1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime == True:
            l.append(i)
    return l

print(simply_num(10))