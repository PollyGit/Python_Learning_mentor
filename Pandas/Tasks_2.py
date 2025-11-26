# https://pynative.com/python-pandas-exercise/

import pandas as pd


df = pd.read_csv("cars_sample.csv")
df.head(5)
df.tail(5)

# 2: Clean the dataset and update the CSV file
# Replace all column values which contain ?, n.a, or NaN.
df = pd.read_csv("cars_sample.csv", na_values={
'price':["?","n.a"],
'stroke':["?","n.a"],
'horsepower':["?","n.a"],
'peak-rpm':["?","n.a"],
'average-mileage':["?","n.a"]})
print(df)

# df.to_csv("cars_sample.csv")


# 3: Find the most expensive car company name
# Print most expensive car’s company name and price.

grouped = df.groupby('company')['price'].sum()
company = grouped.idxmax()
price = grouped.max()
print(company, price)

price_max = df['price'].max()
out = df.query("price == @price_max")[['company', 'price']]
print(out)
out2 = df[['company', 'price']].query("price == @price_max")
print(out2)
out3 = df.nlargest(1, "price")[["company", "price"]]
print(out3)

df1 = df[['company','price']][df.price==df['price'].max()]
print(df1)


# 4: Print All Toyota Cars details
out = df.query("company == 'audi'")
print(out)
out2 = df.groupby('company').get_group('audi')
print(out2)


# 5: Count total cars per company
out = df['company'].value_counts()
print(out)

# 6: Find each company’s Higesht price car
grouped = df.groupby('company')['price'].max().reset_index()
out = grouped.set_index("company", drop=False)[['company','price']]
print(out)
#                  company    price
# company
# alfa-romero  alfa-romero  16500.0
# audi                audi  17450.0
# volkswagen    volkswagen   9995.0
# volvo              volvo  13415.0


# 7: Find the average mileage of each car making company
out = df.groupby("company")['average-mileage'].mean()
print(out)


# 8: Sort all cars by Price column
out = df.sort_values(by='price', ascending=False)
print(out)


# 9: Concatenate two data frames using the following conditions
GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925 , 71400]}
japaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '], 'Price': [29995, 23600, 61500 , 58900]}

gcars = pd.DataFrame(GermanCars)
print(gcars)
jcars = pd.DataFrame(japaneseCars)
print(jcars)

out = pd.concat([gcars, jcars], keys=["Germany", "Japan"])
print(out)


# 10: Merge two data frames using the following condition
# Merge two data frames, and append the second data frame as a new column to the first data frame.

Car_Price = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'Price': [23845, 17995, 135925 , 71400]}
car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 'horsepower': [141, 80, 182 , 160]}

dt1 = pd.DataFrame(Car_Price)
dt2 = pd.DataFrame(car_Horsepower)

out = dt1.merge(dt2, on="Company")
print(out)














#