# https://pynative.com/python-functions-exercise-with-solutions/

# Exercise 2: Create a function with variable length of arguments
def func1(*args):
  for arg in args:
    print(arg)

# Example calls to the function with different numbers of arguments
func1(10, 20)
func1("hello", 3.14, True)
func1(1, 2, 3, 4, 5)
func1() # Calling with no arguments


# Exercise 3: Return multiple values from a function
def calculation(a, b):
    addition = a + b
    subtraction = a - b
    # return multiple values separated by comma
    return addition, subtraction

# get result in tuple format
res = calculation(40, 10)
print(res)


# Exercise 4: Create a function with a default argument
# Write a program to create a function show_employee() with the following specifications:
# It should accept the employee’s name and salary.
# It should display both the name and salary.
# If the salary is not provided in the function call, it should default to 9000.


def show_employee(name, salary=9000):
    print("Name:", name, "salary:", salary)


show_employee("Ben", 12000)
show_employee("Jessa")


# Exercise 5: Create an inner function
# Create a program with nested functions to perform an addition calculation as follows:
#
# Define an outer function that accepts two parameters, a and b.
# Inside this outer function, define an inner function that calculates the sum of a and b.
# The outer function should then add 5 to this sum.
# Finally, the outer function should return the resulting value.”
# outer function
def outer_fun(a, b):
    square = a ** 2

    # inner function
    def addition(a, b):
        return a + b

    # call inner function from outer function
    add = addition(a, b)
    # add 5 to the result
    return add + 5

result = outer_fun(2, 5)
print(result)


# Exercise 6: Create a recursive function
def addition(num):
    if num:
        # call same function by reducing number by 1
        return num + addition(num - 1)
    else:
        return 0

res = addition(3)
print(res)


# Exercise 7: Assign a different name to function and call it through the new name
# Below is the function display_student(name, age). Assign a new name show_student(name, age) to it and call it using the new name.

def display_student(name, age):
    print(name, age)

display_student("Emma", 26)

# assign new name
showStudent = display_student
# call using new name
showStudent("Emma", 26)


# Exercise 8: Generate a Python list of all the even numbers between 4 to 30
print(list(range(4, 30, 2)))


# Exercise 10: Call Function using both positional and keyword arguments
def describe_pet(animal_type, pet_name):
  print(f"\nI have a {animal_type} named {pet_name}.")

# Calling the function using positional arguments
describe_pet('hamster', 'Harry')
describe_pet('dog', 'Lucy')

# Calling the function using keyword arguments
describe_pet(animal_type='cat', pet_name='Whiskers')
describe_pet(pet_name='Buddy', animal_type='goldfish')


# Exercise 11: Create a function with keyword arguments
def print_info(**kwargs):
    if kwargs:  # Check if any keyword arguments were passed
        print("\n--- Information ---")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    else:
        print("\nNo information provided.")

# Example calls to the function
print_info(name="Alice", age=30, city="New York")
print_info(job="Engineer", salary=75000)
print_info(country="USA", state="California", zip_code="90210")
print_info()  # Call with no arguments



# Exercise 12: Modifies global variable
global_var = 10
def modify_global_var():
    global global_var
    global_var = 20
    print("Inside function:", global_var)

modify_global_var()
print("Outside function:", global_var)


# Exercise 13: Write a recursive function to calculate the factorial
def factorial_recursive(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0:
        return 1  # Base case: factorial of 0 is 1
    else:
        return n * factorial_recursive(n - 1)  # Recursive step

# Example usage:
number = 5
result = factorial_recursive(number)
print(f"The factorial of {number} is {result}")
# Output: The factorial of 5 is 120



# Exercise 14: Create a lambda function that squares a given number
square = lambda x: x**2
# Example usage:
number = 5
squared_number = square(number)
print(f"The square of {number} is {squared_number}")


# Exercise 15: Use a lambda with the filter() function to get all even numbers from a list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"The even numbers in the list are: {even_numbers}")


# Exercise 16: Use a lambda with the map() function to double each element in a list
numbers = [1, 2, 3, 4, 5]
doubled_numbers = list(map(lambda x: x * 2, numbers))
print(f"The doubled numbers are: {doubled_numbers}")


# Exercise 17: Use a lambda with the sorted() function to sort a list of tuples based on the second element
data = [('apple', 5), ('banana', 2), ('cherry', 8), ('date', 1)]
sorted_data = sorted(data, key=lambda item: item[1])
print(f"The sorted list of tuples based on the second element is: {sorted_data}")


# Exercise 18: Create Higher-Order Function
# Write a function apply_operation(func, x, y) that takes a function func and two numbers
# x and y as arguments, and returns the result of calling func(x, y). Demonstrate its
# use with different functions (e.g., addition, subtraction).
def apply_operation(func, x, y):
  """
  Applies a given function to two numbers.

  Args:
    func: The function to apply (should take two arguments).
    x: The first number.
    y: The second number.

  Returns:
    The result of calling func(x, y).
  """
  return func(x, y)

# Demonstrate with addition using a regular function
def add(a, b):
  return a + b

result_add = apply_operation(add, 5, 3)
print(f"Result of addition: {result_add}")

# Demonstrate with subtraction using a lambda function
subtract = lambda a, b: a - b
result_subtract = apply_operation(subtract, 10, 4)
print(f"Result of subtraction: {result_subtract}")

# Demonstrate with multiplication using another lambda function
multiply = lambda a, b: a * b
result_multiply = apply_operation(multiply, 2, 6)
print(f"Result of multiplication: {result_multiply}")




#