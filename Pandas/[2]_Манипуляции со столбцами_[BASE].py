import pandas as pd

# [1] Задача
# Создать новый столбец, который будет содержать значение четное
# или нечетное в зависимости от store_id

data = { 'product_id': [101, 102, 101, 103, 102, 101, 103],
         'store_id': [1, 1, 2, 1, 2, 2, 1],
         'sales': [5, 3, 9, 7, 2, 4, 8] }
df = pd.DataFrame(data)

df['even_odd'] = df['store_id'].map(lambda x:'even' if x % 2 == 0 else'odd')


# [2] Задача
# Есть два столбца А и Б в датафрейме - сделать столбец С как среднее значение А и Б

df['C'] = df.apply(lambda x: x[['A','B']].mean(), axis=1)
# or
df['C'] = (df['A'] + df['B']) / 2
# or
df['c'] = df[['a', 'b']].mean(axis=1)


# [3] Задача
# Написать функцию по возведению в степень и применить ее к столбцу
data = {
    'A': [2, 3, 4, 5],
}
df = pd.DataFrame(data)

def power_of_number(x, n):
    result = x ** n
    return result


df['powered'] = power_of_number(df['A'], 2)
# or
df['powered_2'] = df['A'].apply(power_of_number, n=2)
#or
df['A_powered'] = df['A'].apply(lambda x: power_of_number(x, 3))



# [4] Задача
# Что делает df[‘col’] = df[‘col’].apply(lambda x: 1 if x ==’test’ else 0)

#Для каждого элемента из колонки col делает замену на 1 или на 0






