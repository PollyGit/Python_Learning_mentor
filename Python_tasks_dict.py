# https://pynative.com/python-dictionary-exercise-with-solutions/

# Exercise 1: Perform basic dictionary operations
my_dict = {'name': 'Alice', 'age': 35, 'city': 'New York'}

my_dict['profession'] = 'Doctor'
my_dict['age'] = 40
# print key
print('City:', my_dict['city'])

# Exercise 2: Perform dictionary operations
# Remove Key-Value Pair
del my_dict['profession']
print(my_dict)
# Print all key - value pairs
print(my_dict.items())
for key, value in my_dict.items():
  print(f"{key}: {value}")
# Check if Key Exists in the dictionary
print(my_dict.get('name'))


# Exercise 3: Dictionary from Lists
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]
dict1 = dict(zip(keys, values))
print(dict1)
# or
# empty dictionary
res_dict = dict()

for i in range(len(keys)):
    res_dict.update({keys[i]: values[i]})
print(res_dict)


# Exercise 4: Clear Dictionary
my_dict = {'name': 'Alice', 'age': 35, 'city': 'New York'}
my_dict.clear()
print(my_dict)


# Exercise 5: Merge two Python dictionaries into one
dict1 = {'Ten': 10, 'Twenty': 20, 'Thirty': 30}
dict2 = {'Thirty': 30, 'Fourty': 40, 'Fifty': 50}

dict3 = dict1 | dict2
print(dict3)

# or
dict4 = {**dict1, **dict2}
print(dict4)
# or
dict5 = dict1.copy()
dict5.update(dict2)
print(dict5)


# Exercise 6: Count Character Frequencies
# Given a string, create a dictionary where keys are characters and values are their frequencies in the string.

str1 = 'Jessa'
k = []
w = []
for i in str1:
    if i not in k:
        k.append(i)
        c = str1.count(i)
        w.append(c)
dict1 = dict(zip(k,w))
print(dict1)


# or
def count_char_frequencies(str):
  frequency_dict = {}
  for i in str:
    # Use get() method: if char is in dict, get its value; otherwise, default to 0
    frequency_dict[i] = frequency_dict.get(i, 0) + 1
  return frequency_dict

print(f"Frequencies for '{str1}': {count_char_frequencies(str1)}")


# Exercise 7: Access Nested Dictionary
data = {'person': {'name': 'Alice', 'age': 30}}

alices_age = data['person']['age']
print(f"Alice's age is: {alices_age}")


# Exercise 8: Print the value of key ‘history’ from nested dict
sampleDict = {
    "class": {
        "student": {
            "name": "Mike",
            "marks": {
                "physics": 70,
                "history": 80
            }
        }
    }
}
print(sampleDict['class']['student']['marks']['history'])


# Exercise 9: Modify Nested Dictionary
sampleDict['class']['student']['name'] = 'Jessa'
print(sampleDict)


# Exercise 10: Initialize dictionary with default values
employees = ['Kelly', 'Emma']
defaults = {"designation": 'Developer', "salary": 8000}

res = dict.fromkeys(employees, defaults)
print(res)
print(res["Kelly"])


# Exercise 11: Create a dictionary by extracting the keys from a given dictionary
sample_dict = {
    "name": "Kelly",
    "age": 25,
    "salary": 8000,
    "city": "New york"}

# Keys to extract
keys = ["name", "salary"]
dict1 = {k: sample_dict[k] for k in keys}
print(dict1)

#or
# Фильтруем только нужные пары (ключ, значение)
new_dict = {k: v for k, v in sample_dict.items() if k in keys}
print(new_dict)



# Exercise 12: Delete a list of keys from a dictionary
sample_dict = {
    "name": "Kelly",
    "age": 25,
    "salary": 8000,
    "city": "New york"
}

# Keys to remove
keys = ["name", "salary"]
for k in keys:
    sample_dict.pop(k)
print(sample_dict)


# Exercise 13: Check if a value exists in a dictionary
sample_dict = {'a': 100, 'b': 200, 'c': 300}
if 200 in sample_dict.values():
    print(f'200 is exist')



# Exercise 14: Rename key of a dictionary
# rename a key city to a location
sample_dict = {
  "name": "Kelly",
  "age":25,
  "salary": 8000,
  "city": "New york"
}
sample_dict['location'] = sample_dict.pop('city')
print(sample_dict)


# Exercise 15: Get the key of a minimum value
sample_dict = {
  'Physics': 82,
  'Math': 65,
  'history': 75
}

d = min(sample_dict, key=sample_dict.get)
print(d)


# Exercise 16: Change value of a key in a nested dictionary
# change Brad’s salary to 8500
sample_dict = {
    'emp1': {'name': 'Jhon', 'salary': 7500},
    'emp2': {'name': 'Emma', 'salary': 8000},
    'emp3': {'name': 'Brad', 'salary': 500}
}

sample_dict['emp3']['salary'] = 8500
print(sample_dict)
sample_dict.update({'emp3': {'name': 'Bradddy', 'salary': 8500}})
print(sample_dict)


# Exercise 17: Invert Dictionary
original_dict1 = {'a': 1, 'b': 2, 'c': 3}
inverted_dict1 = {}
for k,v in original_dict1.items():
    inverted_dict1[v] = k
print(inverted_dict1)


# Exercise 18: Sort Dictionary by Keys
# Sort a dictionary by its keys and print the sorted dictionary (as an OrderedDict or by converting to a list of tuples).
my_dict = {'apple': 3, 'zebra': 1, 'banana': 2, 'cat': 4}

dict1 = sorted(my_dict.items())
print(dict1)
#[('apple', 3), ('banana', 2), ('cat', 4), ('zebra', 1)]



# Exercise 19: Sort Dictionary by Values
my_dict = {'Jessa': 3, 'Kelly': 1, 'Jon': 2, 'Kerry': 4, 'Joy': 1}
dict1 = sorted(my_dict.values())
print(dict1)    #[1, 1, 2, 3, 4]


# Exercise 20: Check if All Values are Unique
# Write a function that takes a dictionary and returns True if all values in the dictionary are unique, False otherwise.

dict1 = {'a': 1, 'b': 2, 'c': 3}             # All values unique
dict2 = {'x': 10, 'y': 20, 'z': 10}          # Value 10 is duplicated
dict3 = {} # Empty dictionary (all values are vacuously unique)

def is_uniq_values(d:dict):
    return len(d.values()) == len(set(d.values()))

print(is_uniq_values(dict1))
print(is_uniq_values(dict2))
print(is_uniq_values(dict3))













#