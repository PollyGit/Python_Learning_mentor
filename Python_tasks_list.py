my_list = [10, 20, 30, 40, 50]

print(my_list[2])
print(len(my_list))
print('list is not empty') if len(my_list) > 0 else print('list is empty')

my_list[1] = 200
print(my_list)
my_list.append(600)
print(my_list)
my_list.insert(2, 300)
print(my_list)
my_list.remove(600)
print(my_list)
del my_list[0]
print(my_list)


my_list1 = [10, 20, 30, 40, 50]
print(sum(my_list1))
print(sum(my_list1)/len(my_list1))


list1 = [100, 200, 300, 400, 500]
l = list1[::-1]
print(l)
list1.reverse()
print(list1)


num = [1, 2, 3, 4, 5, 6, 7]
num2 = [i**2 for i in num]
print(num2)
print(max(num2), min(num2))


num3 = [5, 2, 8, 1, 9]
num5 = num3[:]
num3.sort()
print(num3)
print(sorted(num3, reverse=True))


num4= num3.copy()
print(num4, num3, num5)
num4.append(3)
print(num4, num3, num5)


list_a = [1, 2]
list_b = [3, 4]
list_d = list_a + list_b
print(list_d)
list_a.extend(list_b)
print(list_a)


# Remove empty strings from the list of strings
list1 = ["Mike", "", "Emma", "Kelly", "", "Brad"]
res = list(filter(None, list1))
print(res)

list1 = [i for i in list1 if i != ""]
print(list1)


# Remove Duplicates from list
list_with_duplicates = [1, 2, 2, 3, 1, 4, 5, 4]
print(list(set(list_with_duplicates)))
print(list(dict.fromkeys(list_with_duplicates)))


# Remove all occurrences of a specific item from a list
list1 = [5, 20, 15, 20, 25, 50, 20]
def remove_value(sample_list, val):
    return [i for i in sample_list if i != val]

res = remove_value(list1, 20)
print(res)


list1 = [5, 20, 15, 20, 25, 50, 20]
while 20 in list1:
    list1.remove(20)
print(list1)


# List Comprehension for Numbers
# create a new list containing only the numbers
my_list = [1, 2, 3, 'Jessa', 4, 5, 'Kelly', 'Jhon', 6]
l1 = [i for i in my_list if isinstance(i, (int, float))]
print(l1)


# Access Nested Lists
# Given a nested list, print the element '55'
nested_list = [[10, 20, 30], [44, 55, 66], [77, 87, 99]]
element_55 = nested_list[1][1]
print(f"The element '55' is: {element_55}")

# Flatten Nested List
# Write a function to flatten a list of lists into a single, non-nested list.
l = [[1, 2], 8, [3, 4], [5, 6, 7]]
def unlist(l: list):
    l2 = []
    for i in l:
        if isinstance(i, list):
            for _ in i:
                l2.append(_)
        else:
            l2.append(i)
    return l2


def flatten_list_comprehension(nested_list):
  return [item for sublist in nested_list for item in sublist]

print(unlist(l))

# Concatenate two lists index-wise
list1 = ["M", "na", "i", "Ke"]
list2 = ["y", "me", "s", "lly"]

list3 = []

for i in range(len(list1)):
    list3.append(list1[i] + list2[i])
print(list3)

list4 = [i + j for i, j in zip(list1, list2)]
print(list4)


# 18: Concatenate two lists in the following order
# ['Hello Dear', 'Hello Sir', 'take Dear', 'take Sir']
list1 = ["Hello ", "take "]
list2 = ["Dear", "Sir"]

list3 = [x+y for x in list1 for y in list2]
print(list3)


# Iterate both lists simultaneously
list1 = [10, 20, 30, 40]
list2 = [100, 200, 300, 400]

for x , y in zip(list1, reversed(list2)):
# for x, y in zip(list1, list2[::-1]):
    print(x, y)


# Add new item to list after a specified item
# Write a program to add item 7000 after 6000 in the following Python List
list1 = [10, 20, [300, 400, [5000, 6000], 500], 30, 40]
list1[2][2].append(7000)
print(list1)


# 22: Extend nested list by adding the sublist
list1 = ["a", "b", ["c", ["d", "e", ["f", "g"], "k"], "l"], "m", "n"]

# sub list to add
sub_list = ["h", "i", "j"]
list1[2][1][2].extend(sub_list)
print(list1)


# 23: Replace list’s item with new value if found
# You have given a Python list. Write a program to find value 20 in the list, and if it is present, replace it with 200. Only update the first occurrence of an item.
list1 = [5, 10, 15, 20, 25, 50, 20]

k = list1.index(20)
list1[k] = 200
print(list1)



#