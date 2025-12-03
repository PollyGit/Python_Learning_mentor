# https://www.machinelearningplus.com/python/101-pandas-exercises-python/
import pandas as pd
import numpy as np


# 3. How to convert the index of a series into a column of a dataframe?
# Input
mylist = list('abcedfghijklmnopqrstuvwxyz')
myarr = np.arange(26)
mydict = dict(zip(mylist, myarr))
ser = pd.Series(mydict)
print(ser.head())

# Solution
df = ser.to_frame().reset_index()
print(df.head())


# 4. How to combine many series to form a dataframe?
ser1 = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser2 = pd.Series(np.arange(26))

df = pd.concat([ser1, ser2], axis=1)
print('------------')


# 5. How to assign name to the series’ index?
ser = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser.name = 'alphabets'
print(ser.head())

# 6. How to get the items of series A not present in series B?
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])

print(ser1[~ser1.isin(ser2)])

# 7. How to get the items not common to both series A and series B?
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
# Solution
ser_u = pd.Series(np.union1d(ser1, ser2))  # union
ser_i = pd.Series(np.intersect1d(ser1, ser2))  # intersect
ser_u[~ser_u.isin(ser_i)]


# 8. How to get the minimum, 25th percentile, median, 75th, and max of a numeric series?
ser = pd.Series(np.random.normal(10, 5, 25))
out = ser.describe(())
print(out)
# Solution
out2 = np.percentile(ser, q=[0, 25, 50, 75, 100])
out3 = np.percentile(ser, q=[50])
print(out2, out3)
print('------------')


# 9. How to get frequency counts of unique items of a series?
ser = pd.Series(np.take(list('abcdefgh'), np.random.randint(8, size=30)))
out=ser.nunique()
out2 = ser.value_counts()
print(out, out2)
print('------------')


# 10. How to keep only top 2 most frequent values as it is and replace everything else as ‘Other’?
# np.random.RandomState(100)
# ser = pd.Series(np.random.randint(1, 5, [12]))
# print(f'ser: {ser}')
# # Solution
# print("Top 2 Freq:", ser.value_counts())
# out = ser[~ser.isin(ser.value_counts().index[:2])] = 'Other'
# print(out)


# 11. How to bin a numeric series to 10 groups of equal size?
ser = pd.Series(np.random.random(20))
print(ser)


























#