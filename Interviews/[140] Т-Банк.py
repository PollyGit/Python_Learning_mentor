# Задача 3
# Дана строка, состоящая из чисел, разделённых пробелом.
# Напишите функцию calc_even_numbers чтобы считать сумму
# всех чётных чисел

s = '2 10 3 15'
def calc_even_numbers(s:str):
    n = 0
    l = list(map(int, s.split()))
    for i in range(len(l)):
        if l[i] % 2 == 0:
            n += l[i]
    return n

def calc_even_numbers2(s: str):
    return sum(int(x) for x in s.split() if int(x) % 2 == 0)


print(calc_even_numbers(s))
print(calc_even_numbers2(s))


# Задача 5
# Напишите функцию is_prime, принимающую 1 аргумент - целое
# число от 1 до 1000, и возвращающую True, если оно простое, и
# False - иначе

def is_prime(n: int) -> bool:
    if not (1 <= n <= 1000):
        raise ValueError("Число должно быть от 1 до 1000")

    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


print(is_prime(3))



# Задача 4
# Дан csv файл с действиями клиентов Т-банка
# "дата | клиент | сумма покупки" ="date | user | amount"
# За последний день посчитайте:
# 1. Самого часто встречающегося покупателя
# 2. Среднее значение и стандартное отклонение продаж для каждого клиента


import pandas as pd


df = pd.read_csv('tbank.csv')
df.columns = df.columns.str.strip()
# делает очистку имён колонок: у каждого названия убираются пробелы с начала и конца.

df['date'] = pd.to_datetime(df['date'], errors='coerce')


# 2) Находим последний календарный день в данных
last_day = df['date'].dt.date.max()  #день без времени


# 3) Фильтруем строки только этого дня
df_last = df[df["date"].dt.date == last_day].copy()
# or
#df_last = df.query("date.dt.date == @last_day")


# 4) (1) Самый частый покупатель
most_freq_user = df_last['user'].value_counts().nlargest(1).index[0]
print(most_freq_user)


# 5) (2) Среднее и стандартное отклонение суммы покупок по каждому клиенту
stats = (
    df_last.groupby("user")["amount"]
           .agg(mean_amount="mean", std_amount="std")
           .reset_index()
           .sort_values("mean_amount", ascending=False) #можно без sort_values
)
print(stats)



