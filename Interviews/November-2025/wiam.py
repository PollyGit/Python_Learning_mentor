# 2

def print_n():
    for n in range(1, 101):
        if n == 100:
            print(n)
        elif n % 5 == 0 and n % 3 == 0:
            print('FizzBuzz')
        elif n % 3 == 0:
            print('Fizz')
        elif n % 5 == 0:
            print('Buzz')
        else:
            print(n)


print_n()









#