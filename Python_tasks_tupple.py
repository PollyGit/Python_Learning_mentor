# https://pynative.com/python-tuples/

my_tuple = (1, 2, 3, 4, 5)
print(f"My tuple: {my_tuple}")

# 2. Access Elements
third_element = my_tuple[2] # Index 2 corresponds to the third element
print(f"The third element of my_tuple: {third_element}")

# 3. Tuple Length
tuple_length = len(my_tuple)
print(f"The length of my_tuple: {tuple_length}")


# Exercise 2: Tuple Repetition
original_tuple = ('a', 'b')
print(original_tuple * 3)

# Exercise 3: Slicing Tuples
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
sliced_numbers = numbers[3:7]

# Exercise 4: Reverse the tuple
tuple1 = (10, 20, 30, 40, 50)
out = tuple1[::-1]
print(out)


# Exercise 5: Access Nested Tuples
tuple1 = ("Orange", [10, 20, 30], (5, 15, 25))

# understand indexing
# tuple1[0] = 'Orange'
# tuple1[1] = [10, 20, 30]
# list1[1][1] = 20

print(tuple1[1][1])

# Exercise 6: Create a tuple with single item 50
tuple1= (50, )
print(tuple1)
print(type(tuple1))

# Exercise 7: Unpack the tuple into 4 variables
tuple1 = (10, 20, 30, 40)
a, b, c, d = tuple1
print(a)
print(b)
print(c)
print(d)

# Exercise 8: Swap two tuples in Python
tuple1 = (11, 22)
tuple2 = (99, 88)
tuple1, tuple2 = tuple2, tuple1
print(tuple1, tuple2)

# Exercise 9: Copy Specific Elements From Tuple
tuple1 = (11, 22, 33, 44, 55, 66)
tuple2 = tuple1[3:-1]

# Exercise 10: List to Tuple
my_list = [10, 20, 30]

# Use the tuple() constructor to convert the list
converted_tuple = tuple(my_list)


# Exercise 11: Function Returning Tuple
def get_min_max(numbers):
    if not numbers:
        return (None, None)  # Handle empty list case
    min_val = min(numbers)
    max_val = max(numbers)
    return (min_val, max_val)


# Test the function
my_numbers = [10, 5, 20, 2, 15]
min_max_values = get_min_max(my_numbers)
print(f"Original numbers: {my_numbers}")
print(f"Minimum and maximum values: {min_max_values}")


# Exercise 12: Comparing Tuples
t1 = (1, 2, 3)
t2 = (1, 2, 4)
if t1 > t2:
    print(f"{t1} is greater than {t2}")
elif t1 < t2:
    print(f"{t1} is less than {t2}")
else:
    print(f"{t1} is equal to {t2}")


# Exercise 13: Removing Duplicates from Tuple
# create a new tuple with only unique elements.
my_tuple = (1, 2, 2, 3, 4, 4, 5)
print(f"Original tuple with duplicates: {my_tuple}")

# Convert to a set to remove duplicates (order is not preserved)
unique_elements_set = set(my_tuple)

# Convert back to a tuple
unique_tuple = tuple(unique_elements_set)
print(f"Tuple with unique elements: {unique_tuple}")


# Exercise 14: Filter Tuples
students = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
high_achievers_loop = []
for student in students:
  if student[1] >= 90:
    high_achievers_loop.append(student)
print(f"Students with scores 90 or above (loop method): {high_achievers_loop}")

# or
high_achievers = [student for student in students if student[1] >= 90]

# Exercise 15: Map Tuples
# Given a tuple of numbers, create a new tuple where each number is squared.
t = (1, 2, 3, 4)
t2 = tuple(i**2 for i in t)
print(t2)
# or
squared_tuple_map = tuple(map(lambda x: x**2, t))


# Exercise 16: Modify Tuple
tuple1 = (11, [22, 33], 44, 55)
tuple1[1][0] = 222


# Exercise 17: Sort a tuple of tuples by 2nd item
tuple1 = (('a', 23),('b', 37),('c', 11), ('d',29))
my_list = list(tuple1)
sorted_list = sorted(my_list, key=lambda x: x[1])
sorted_tuple = tuple(sorted_list)
print(sorted_tuple)


# Exercise 18: Count Elements
tuple1 = (50, 10, 60, 70, 50)
out = tuple1.count(50)
print(out)


# Exercise 19: Check if all items in the tuple are the same
tuple1 = (45, 45, 45, 45)
def check(t):
    return all(i == t[0] for i in t)

tuple1 = (45, 45, 45, 45)
print(check(tuple1))


nums = (1, 2, 3, 4, 5)
out = nums[::1]
print(out)


t1 = (1, 2, 3)
t2 = (3, 4)
print(t1+t2)


#