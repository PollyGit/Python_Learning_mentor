#  1
# написать функцию, которая бы принимала
# на вход словарь d и выводила данные в таком формате:
# a: 1
# b: 2
# c: 3

d = {}
d['a'] = 1
d['b'] = 2
d['c'] = 3


def dict_view(d: dict) -> str:
    for k, v in d.items():
        print(f'{k}: {v}')


dict_view(d)
