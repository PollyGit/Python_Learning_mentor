# Задача 4
#
# Дан неотсортированный массив.
# Удалить дубли не нарушив порядок сортировки

n = [1, 5, 2, 1, 5, 7, 1]


def del_dubbles(n: list):
    m = []
    for i in n:
        if i not in m:
            m.append(i)
    return m


print(del_dubbles(n))

# Задача 5
# Нужно найти максимальную прибыль, купив акцию в один день и продав в какой-то последующий день.
#

price = [6, 3, 2, 3, 1, 4, 5]


def profit(price: list):
    buy = price.index(min(price))
    sell = price.index(max(price))
    if buy < sell:
        return max(price) - min(price)
    else:
        return 0


print(profit(price))


# or

def profit2(price: list):
    min_price = price[0]
    max_profit = 0
    for p in price:
        if p < min_price:
            min_price = p
        else:
            max_profit = max(max_profit, p - min_price)
    return max_profit


print(profit2(price))
