# https://pynative.com/python-set-exercise-with-solutions/

fruits = {'apple', 'orange', 'mango', 'banana'}
fruits.add('grape')
fruits.remove('banana')
fruits.discard('mango')
print(fruits)

# Exercise 2: Union of Sets
set1 = {10, 20, 30, 40, 50}
set2 = {30, 40, 50, 60, 70}
out= set1.union(set2)
print(out)
# {70, 40, 10, 50, 20, 60, 30}

# Exercise 3: Intersection of Sets
out= set1.intersection(set2)
print(out)
# {40, 50, 30}

# Exercise 4: Difference of Sets
out= set1.difference(set2)
print(out)
# {10, 20}

# Exercise 5: Symmetric Difference
out = set1.symmetric_difference(set2)
print(out)
# {20, 70, 10, 60}

# Exercise 6: Add a list of Elements to a Set
sample_set = {"Yellow", "Orange", "Black"}
sample_list = ["Blue", "Green", "Red"]
sample_set.update(sample_list)
print(sample_set)

# Exercise 7: Set Difference Update
set1 = {10, 20, 30}
set2 = {20, 40, 50}
set1.difference_update(set2)
print(set1)


# Exercise 8: Remove Items From Set Simultaneously
set1 = {10, 20, 30, 40, 50}
set2 = {10, 20, 30}
set1.difference_update(set2)

# Exercise 9: Check Subset
subset_set = {10, 20}
main_set = {10, 20, 30, 40}

print(subset_set.issubset(main_set))

# Exercise 10: Check Superset
set1 = {10, 20}
set2 = {10, 20, 30, 40}
print(set2.issuperset(set1))

# Exercise 11: Set Intersection Check
set1 = {10, 20, 30, 40, 50}
set2 = {60, 70, 80, 90, 10}

print(set1.isdisjoint(set2))

# Exercise 12: Set Symmetric Difference Update
# update set1 by adding items from set2 that are not common to both sets.
set1 = {10, 20, 30, 40, 50}
set2 = {30, 40, 50, 60, 70}
set1.symmetric_difference_update(set2)
print(set1)
# {20, 70, 10, 60}


# Exercise 13: Set Intersection Update
# remove items from set1 that are not present in set2
set1 = {10, 20, 30, 40, 50}
set2 = {30, 40, 50, 60, 70}
set1.intersection_update(set2)
print(set1)
# {40, 50, 30}


# Exercise 14: Find Common Elements in Two Lists
list1 = [10, 20, 30, 40]
list2 = [30, 40, 50, 60]
out = set(list1).intersection(set(list2))
print(out)
# {40, 30}

# Exercise 15: Frozen Set
# Create a frozen set from a list.
my_list = [10, 20, 30]
frozen_set = frozenset(my_list)
print(frozen_set)


# Exercise 16: Count Unique Words
sentence = "dog is a simple animal dogs is selfless animal"
words = sentence.lower().split()
unique_words = set(words)
unique_word_count = len(unique_words)

#