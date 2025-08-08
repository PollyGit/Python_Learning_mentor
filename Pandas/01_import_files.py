# The first step in most data analytics projects is reading the data file
# Here it's example

# import pandas as pd
# pd.set_option('display.max_rows', 5)
# from learntools.core import binder; binder.bind(globals())
# from learntools.pandas.creating_reading_and_writing import *
# print("Setup complete.")


import pandas as pd

# Your code goes here. Create a dataframe matching the above diagram and assign it to the variable fruits.
fruits = pd.DataFrame({'Apples': [30], 'Bananas': [21]})
print(fruits)

fruit_sales = pd.DataFrame({'Apples': [35, 41], 'Bananas': [21, 34]},
                          index=['2017 Sales', '2018 Sales'])
print(fruit_sales)
print('----------\n', fruit_sales.iloc[-1, 0])
#print('----------\n', fruit_sales.loc[0])
print(fruit_sales.Apples == 41)
print(fruit_sales.Apples.isin([41, 35]))
print('----------\n', fruit_sales.Apples.notnull())

fruit_sales['Apples'] = 90
fruit_sales['Apples'] = range(len(fruit_sales), 0,-1)
print(fruit_sales)


ingredients = pd.Series(['4 cups', '1 cup', '2 large', '1 can'],
                       index=['Flour', 'Milk', 'Eggs', 'Spam'],
                       name='Dinner')
print(ingredients)


#reviews = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv',
#                       index_col=0)






